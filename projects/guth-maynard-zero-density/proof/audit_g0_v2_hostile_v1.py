#!/usr/bin/env python3
"""Bounded hostile audit of the corrected G0 v2 package.

This is deliberately not an authoritative G0 reconciliation.  It records one
invocation-mode defect in v2: its asserted interpreter pin is bypassed by
CPython's ``-O`` flag.  The normal, frozen ``python3`` command is checked
separately and passes.  A successor replay harness must reject optimized mode
before it delegates to v2.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from decimal import Decimal
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/g0-v2-hostile-audit-v1.json"
FROZEN: dict[str, tuple[str, str]] = {
    "reconciliation_script": ("proof/reconcile_g0_full_v2.py", "763f32a703abdf5ce19bc9dcfff4f169f4c5a63c9a611f0d775d7c10f62f4125"),
    "reconciliation_artifact": ("artifacts/g0-full-reconstruction-v2.json", "b6c9a8dbe3cff834f42dfa3afaed7650610211360a921a7731e894592cb1306f"),
    "runtime_v1": ("conventions/proof_runtime_v1.py", "83e486ad6252435745d8465f143a25d0a16e78bd82076ad5965368065deb645b"),
    "published_source_checker_v5": ("proof/check_explicit_formula_published_source_v5.py", "acd16b2f4c1f083fe62c4316eae61cd488f8f0230d46d26dcdb8082f136fd3d3"),
    "published_source_v5": ("artifacts/cycle-2-stream-c-explicit-formula-published-source-v5.json", "04c40acc2ac5a0ac6b1bf4f2380b16c4b9cc95e24dac97ed326b06bb24ee024f"),
    "six_route_harness": ("proof/run_g0_resource_gate_v2.py", "a42a7af6053c6042d243bd0aa17fe5ca86cfe714880d5e6db0336a60ccf24897"),
    "six_route_config": ("artifacts/g0-six-route-resource-gate-config-v2.json", "f8b2b3c32591f5714efe98d1ac95e63c7b49dec093ab0c97ed0f94ce6301a3f8"),
    "six_route_performance": ("artifacts/g0-six-route-resource-gate-performance-v2.json", "fdd32be5b0129dbaa38439517fd07d03a2d3834a98f4eee4b8ee4324164cd8d2"),
}
EXPECTED_ROUTE_IDS = (
    "cycle1-route-a-readonly-v1",
    "cycle1-route-b-readonly-v1",
    "stream-b-route-a-v3",
    "stream-b-route-b-v1",
    "stream-c-route-a-v5",
    "stream-c-route-b-v5",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def frozen_hashes() -> dict[str, str]:
    actual: dict[str, str] = {}
    for label, (relative, expected) in FROZEN.items():
        observed = digest(ROOT / relative)
        require(observed == expected, f"frozen hash mismatch: {relative}")
        actual[label] = observed
    return actual


def run_checked(*command: str) -> None:
    completed = subprocess.run((sys.executable, *command), cwd=ROOT,
                               capture_output=True, text=True)
    require(completed.returncode == 0,
            "normal replay failed: " + json.dumps({"command": list(command), "stdout": completed.stdout, "stderr": completed.stderr}, sort_keys=True))


def certificate() -> dict[str, Any]:
    hashes = frozen_hashes()
    run_checked("proof/reconcile_g0_full_v2.py", "--check")
    run_checked("proof/check_explicit_formula_published_source_v5.py", "--check")
    run_checked("proof/run_g0_resource_gate_v2.py", "--check-config", "artifacts/g0-six-route-resource-gate-config-v2.json")

    reconciliation = json.loads((ROOT / FROZEN["reconciliation_artifact"][0]).read_text())
    source = json.loads((ROOT / FROZEN["published_source_v5"][0]).read_text())
    config = json.loads((ROOT / FROZEN["six_route_config"][0]).read_text())
    performance = json.loads((ROOT / FROZEN["six_route_performance"][0]).read_text())
    runtime_text = (ROOT / FROZEN["runtime_v1"][0]).read_text()

    require(reconciliation["decision"] == {
        "gate": "G0", "status": "PASS", "open_blockers": [],
        "authorized_next_path": "P1 after G1 preregistration is sealed",
        "epistemic_status": "PROVED corrected exact gate adjudication",
    }, "unexpected v2 G0 decision")
    require(source["epistemic_status"] == "PROVED", "published-source v5 is not PROVED")
    require(source["published_item"]["dspace_entity_type"] == "Publication", "v5 lacks MIT Publication classification")
    require(source["published_theorem"]["status"] == "PROVED", "v5 theorem status is not PROVED")
    route_ids = tuple(row["id"] for row in config["routes"])
    require(route_ids == EXPECTED_ROUTE_IDS, f"unexpected six-route order: {route_ids}")
    require(len(set(route_ids)) == 6, "duplicate resource route")
    require(config["limits"] == {
        "wall_seconds_strictly_less_than": 60,
        "max_rss_kib_strictly_less_than": 262144,
    }, "resource ceilings changed")
    require(performance["config_sha256"] == hashes["six_route_config"], "performance does not pin the checked configuration")
    require(tuple(row["id"] for row in performance["route_results"]) == route_ids, "performance/config route order differs")
    for row in performance["route_results"]:
        require(row["epistemic_status"] == "OBSERVED", f"resource row lacks OBSERVED tag: {row['id']}")
        require(row["gate_status"] == "PASS", f"resource row not PASS: {row['id']}")
        require(row["subprocess_returncode"] == row["time_exit_status"] == 0, f"resource exit failure: {row['id']}")
        require(row["parse_error"] is None, f"resource parse error: {row['id']}")
        require(Decimal(row["wall_seconds"]) < Decimal(60), f"resource wall ceiling: {row['id']}")
        require(row["max_rss_kib"] < 262144, f"resource RSS ceiling: {row['id']}")
    require("assert platform.python_implementation()" in runtime_text and "assert actual == VERSION" in runtime_text,
            "runtime-v1 no longer has the audited assert-only enforcement")

    optimized = subprocess.run((sys.executable, "-O", "proof/reconcile_g0_full_v2.py", "--check"), cwd=ROOT,
                                capture_output=True, text=True)
    require(optimized.returncode == 0,
            "the known v2 optimized-mode containment changed; do not silently rewrite this audit")
    return {
        "artifact_id": "g0-v2-hostile-audit-v1",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "OBSERVED bounded hostile audit of the corrected G0 v2 package. It validates normal frozen-command replay, v5 source classification, and six-route resource semantics; it records rather than repairs v2's standalone optimization-mode bypass. It proves no zero-density or prime-interval theorem and is not a G0 decision.",
        "frozen_hashes": hashes,
        "normal_frozen_command": {
            "command": [sys.executable, "proof/reconcile_g0_full_v2.py", "--check"],
            "status": "PASS",
            "epistemic_status": "OBSERVED",
            "scope": "The exact normal CPython invocation used by the package replay.",
        },
        "published_source_classification": {
            "status": "PASS",
            "epistemic_status": "PROVED",
            "evidence": "v5 pins an MIT DSpace Publication item and the selected official theorem/proof; it makes no journal-peer-review claim.",
        },
        "six_route_resource_semantics": {
            "status": "PASS",
            "epistemic_status": "OBSERVED",
            "route_ids": list(route_ids),
            "strict_limits": config["limits"],
            "performance_scope": "Pinned host-specific measurements only; not a proof-grade mathematical claim.",
        },
        "optimization_mode_probe": {
            "command": [sys.executable, "-O", "proof/reconcile_g0_full_v2.py", "--check"],
            "status": "CONTAINED_OPTIMIZATION_BYPASS_OBSERVED",
            "epistemic_status": "OBSERVED",
            "result": "exit status 0",
            "cause": "v2 delegates its runtime checks to bare Python assert statements, which CPython -O removes.",
            "containment": "The v2 standalone runtime pin is not optimization-robust. A successor runner must use explicit failures and reject sys.flags.optimize != 0 before calling v2; no optimized invocation is an authorized proof replay.",
        },
        "recommendation": {
            "status": "CONTAINED",
            "epistemic_status": "OBSERVED",
            "normal_replay_permitted": True,
            "standalone_optimization_robustness": False,
            "required_successor_boundary": "Explicitly require CPython 3.12.3 and sys.flags.optimize == 0 without bare assert enforcement.",
        },
        "falsifier": "A normal replay failure, changed v5 Publication/theorem status, missing or non-PASS six-route row, altered strict ceiling, or a changed optimized probe invalidates this bounded audit and requires a new versioned record.",
        "replay": {
            "script_sha256": digest(Path(__file__)),
            "write_command": "python3 projects/guth-maynard-zero-density/proof/audit_g0_v2_hostile_v1.py --write",
            "check_command": "python3 projects/guth-maynard-zero-density/proof/audit_g0_v2_hostile_v1.py --check",
        },
    }


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = render(certificate())
    if args.write:
        OUTPUT.write_text(payload)
    elif not OUTPUT.is_file() or OUTPUT.read_text() != payload:
        raise SystemExit("G0 v2 hostile-audit mismatch")
    else:
        print(json.dumps({"artifact": OUTPUT.name, "status": "CONTAINED", "verified": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
