#!/usr/bin/env python3
"""Read-only replay and observed performance record for G1 sensitivity v1."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/g1-envelope-sensitivity-replay-v1-performance.json"
RECONCILIATION = ROOT / "artifacts/g1-envelope-sensitivity-reconciliation-v1.json"
SCRIPTS = (
    ROOT / "proof/derive_g1_envelope_sensitivity_route_a_v1.py",
    ROOT / "proof/derive_g1_envelope_sensitivity_route_b_v1.py",
    ROOT / "proof/reconcile_g1_envelope_sensitivity_v1.py",
)
RECONCILIATION_SHA256 = "850b825698722d628340b762867c98774dae53443aecde581138c6830993b60e"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record() -> dict[str, Any]:
    require(sys.flags.optimize == 0, "G1 sensitivity performance replay forbids -O/-OO")
    require(platform.python_implementation() == "CPython" and platform.python_version() == "3.12.3", "G1 sensitivity performance replay requires CPython 3.12.3")
    require(digest(RECONCILIATION) == RECONCILIATION_SHA256, "unexpected reconciliation byte identity")
    rows = []
    for script in SCRIPTS:
        started = time.perf_counter()
        completed = subprocess.run([sys.executable, str(script), "--check"], cwd=ROOT, capture_output=True, text=True)
        finished = time.perf_counter()
        require(completed.returncode == 0, script.name + " failed: " + completed.stdout + completed.stderr)
        usage = resource.getrusage(resource.RUSAGE_CHILDREN)
        rows.append({
            "script": str(script.relative_to(ROOT)),
            "script_sha256": digest(script),
            "wall_seconds": finished-started,
            "child_ru_maxrss": usage.ru_maxrss,
            "child_ru_maxrss_unit": "KiB on Linux; cumulative maximum over completed child replays",
        })
    return {
        "artifact_id": "g1-envelope-sensitivity-replay-v1-performance",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "OBSERVED single-host timing and cumulative-child peak-RSS measurement of read-only replay commands. It is not a mathematical certificate or a finite-probe resource result.",
        "reconciliation": {"path": str(RECONCILIATION.relative_to(ROOT)), "sha256": digest(RECONCILIATION)},
        "runtime": {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization": sys.flags.optimize, "platform": platform.platform()},
        "replays": rows,
        "command": "python3 projects/guth-maynard-zero-density/proof/run_g1_envelope_sensitivity_v1.py --write-performance",
    }


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-performance", action="store_true")
    mode.add_argument("--check-performance", action="store_true")
    args = parser.parse_args()
    if args.write_performance:
        OUTPUT.write_text(render(record()))
    else:
        require(OUTPUT.is_file(), "missing observed performance record")
        value = json.loads(OUTPUT.read_text())
        require(value["epistemic_status"] == "OBSERVED", "wrong performance status")
        require(value["reconciliation"] == {"path": str(RECONCILIATION.relative_to(ROOT)), "sha256": RECONCILIATION_SHA256}, "performance record points to wrong reconciliation")
        require(len(value["replays"]) == 3, "performance record has wrong replay count")
        print(json.dumps({"artifact": OUTPUT.name, "verified": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)

