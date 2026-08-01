#!/usr/bin/env python3
"""Six-route G0 resource gate correcting the under-scoped Cycle-2 v1 gate."""
from __future__ import annotations

import argparse
from decimal import Decimal
import hashlib
import json
import platform
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "artifacts/g0-six-route-resource-gate-config-v2.json"
TIME = Path("/usr/bin/time")
MAX_SECONDS = Decimal(60)
MAX_RSS_KIB = 262144


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def config() -> dict[str, Any]:
    routes = [
        {"id": "cycle1-route-a-readonly-v1", "command": ["python3", "proof/replay_cycle1_route_a_readonly_v1.py"], "scope": "Cycle-1 independent Route A baseline, bottleneck, and complete case split."},
        {"id": "cycle1-route-b-readonly-v1", "command": ["python3", "proof/replay_cycle1_route_b_readonly_v1.py"], "scope": "Cycle-1 independent Route B baseline, bottleneck, and complete case split."},
        {"id": "stream-b-route-a-v3", "command": ["python3", "proof/audit_cycle2_stream_b_route_a_v3.py", "--check", "artifacts/cycle-2-stream-b-route-a-v3.json"], "scope": "Cycle-2 Stream-B Route A."},
        {"id": "stream-b-route-b-v1", "command": ["python3", "proof/replay_cycle2_stream_b_route_b.py", "--check", "artifacts/cycle-2-stream-b-route-b-v1.json"], "scope": "Cycle-2 Stream-B Route B."},
        {"id": "stream-c-route-a-v5", "command": ["python3", "proof/replay_cycle2_stream_c_route_a_v5.py", "--check", "artifacts/cycle-2-stream-c-route-a-v5.json"], "scope": "Cycle-2 Stream-C Route A."},
        {"id": "stream-c-route-b-v5", "command": ["python3", "proof/replay_short_intervals_stream_c_route_b_v5.py", "--check"], "scope": "Cycle-2 Stream-C Route B."},
    ]
    return {
        "artifact_id": "g0-six-route-resource-gate-config-v2",
        "supersedes": "cycle-2-g0-per-route-resource-gate-config-v1 for complete G0 coverage; v1 is preserved",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Deterministic six-route resource configuration. It corrects v1's omission of the two independent Cycle-1 routes and does not itself adjudicate G0.",
        "limits": {"wall_seconds_strictly_less_than": 60, "max_rss_kib_strictly_less_than": MAX_RSS_KIB},
        "routes": routes,
        "required_outcome": "Every listed route exits zero and is measured strictly below both ceilings; any missing/unparseable/at-ceiling row fails closed.",
    }


def render_config() -> str:
    return json.dumps(config(), sort_keys=True, indent=2) + "\n"


def elapsed_seconds(text: str) -> Decimal:
    fields = text.strip().split(":")
    assert 1 <= len(fields) <= 3
    seconds = Decimal(fields[-1])
    if len(fields) >= 2:
        seconds += Decimal(60) * int(fields[-2])
    if len(fields) == 3:
        seconds += Decimal(3600) * int(fields[0])
    return seconds


def parse_report(text: str) -> tuple[Decimal, int, int]:
    wall = re.search(r"^\s*Elapsed \(wall clock\) time \(h:mm:ss or m:ss\):\s*(.+)$", text, re.MULTILINE)
    rss = re.search(r"^\s*Maximum resident set size \(kbytes\):\s*(\d+)\s*$", text, re.MULTILINE)
    status = re.search(r"^\s*Exit status:\s*(\d+)\s*$", text, re.MULTILINE)
    assert wall and rss and status
    return elapsed_seconds(wall.group(1)), int(rss.group(1)), int(status.group(1))


def measure(row: dict[str, Any]) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="g0-six-route-") as temporary:
        report_path = Path(temporary) / "time.txt"
        completed = subprocess.run([str(TIME), "-v", "-o", str(report_path), *row["command"]], cwd=ROOT, capture_output=True, text=True)
        report = report_path.read_text() if report_path.exists() else ""
    try:
        wall, rss, timed_status = parse_report(report)
        error = None
    except (AssertionError, ValueError) as exception:
        wall, rss, timed_status, error = None, None, None, str(exception)
    passed = error is None and completed.returncode == timed_status == 0 and wall is not None and rss is not None and wall < MAX_SECONDS and rss < MAX_RSS_KIB
    return {
        "id": row["id"], "command": row["command"], "scope": row["scope"],
        "epistemic_status": "OBSERVED", "gate_status": "PASS" if passed else "FAIL",
        "wall_seconds": None if wall is None else str(wall), "max_rss_kib": rss,
        "subprocess_returncode": completed.returncode, "time_exit_status": timed_status,
        "parse_error": error, "stdout": completed.stdout, "stderr": completed.stderr,
    }


def performance() -> dict[str, Any]:
    assert CONFIG.read_text() == render_config()
    rows = [measure(row) for row in config()["routes"]]
    return {
        "artifact_id": "g0-six-route-resource-gate-performance-v2",
        "supersedes": "cycle-2-g0-per-route-resource-gate-performance-v1 for complete G0 coverage; v1 is preserved",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Host-specific measurements of all six independent G0 routes; operational evidence only.",
        "config_sha256": sha256(CONFIG), "harness_sha256": sha256(Path(__file__)),
        "environment": {"implementation": platform.python_implementation(), "python": platform.python_version(), "python_executable": shutil.which("python3")},
        "route_results": rows,
        "resource_gate": {"gate_status": "PASS" if all(row["gate_status"] == "PASS" for row in rows) else "FAIL"},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write-config", type=Path)
    mode.add_argument("--check-config", type=Path)
    mode.add_argument("--write-performance", type=Path)
    args = parser.parse_args()
    if args.write_config:
        args.write_config.write_text(render_config())
        return 0
    if args.check_config:
        if args.check_config.read_text() != render_config():
            raise SystemExit("six-route resource config mismatch")
        return 0
    result = performance()
    args.write_performance.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
    if result["resource_gate"]["gate_status"] != "PASS":
        raise SystemExit("six-route resource gate failed closed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
