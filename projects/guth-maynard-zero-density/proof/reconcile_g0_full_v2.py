#!/usr/bin/env python3
"""Corrected authoritative G0 reconciliation with six routes and runtime pin."""
from __future__ import annotations

import argparse
from decimal import Decimal
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/g0-full-reconstruction-v2.json"
FROZEN = {
    "v1_artifact": ("artifacts/g0-full-reconstruction-v1.json", "6d12eb62c516198d7292a29fe6dd6e6a1dbdc9957f992564cce6e51e12ea692d"),
    "v1_replay": ("proof/reconcile_g0_full_v1.py", "4a58d005a1ef4af8524187001e5a041660857b987fd459313b459d73fcac1fe3"),
    "runtime": ("conventions/proof_runtime_v1.py", "83e486ad6252435745d8465f143a25d0a16e78bd82076ad5965368065deb645b"),
    "cycle1_route_a": ("proof/replay_cycle1_route_a_readonly_v1.py", "1ea5ab6b3d32007ea5315c446244f71f111a26fb4f43bd8ddd9c9ac229c01625"),
    "cycle1_route_b": ("proof/replay_cycle1_route_b_readonly_v1.py", "fcee4e94fba909ea9fa449ddf344c53c634b870e5181a2d0fe5f4b254976bdcd"),
    "resource_replay": ("proof/run_g0_resource_gate_v2.py", "a42a7af6053c6042d243bd0aa17fe5ca86cfe714880d5e6db0336a60ccf24897"),
    "resource_config": ("artifacts/g0-six-route-resource-gate-config-v2.json", "f8b2b3c32591f5714efe98d1ac95e63c7b49dec093ab0c97ed0f94ce6301a3f8"),
    "resource_performance": ("artifacts/g0-six-route-resource-gate-performance-v2.json", "fdd32be5b0129dbaa38439517fd07d03a2d3834a98f4eee4b8ee4324164cd8d2"),
    "published_formula_replay": ("proof/check_explicit_formula_published_source_v5.py", "acd16b2f4c1f083fe62c4316eae61cd488f8f0230d46d26dcdb8082f136fd3d3"),
    "published_formula": ("artifacts/cycle-2-stream-c-explicit-formula-published-source-v5.json", "04c40acc2ac5a0ac6b1bf4f2380b16c4b9cc95e24dac97ed326b06bb24ee024f"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(key: str) -> dict[str, Any]:
    return json.loads((ROOT / FROZEN[key][0]).read_text())


def module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    assert spec and spec.loader
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def certificate() -> dict[str, Any]:
    hashes = {}
    for key, (relative, expected) in FROZEN.items():
        actual = sha256(ROOT / relative)
        assert actual == expected, f"corrected G0 input changed: {relative}"
        hashes[key] = actual

    runtime = module("g0_proof_runtime_v1", FROZEN["runtime"][0]).assert_pinned_runtime()
    commands = (
        ("proof/reconcile_g0_full_v1.py", "--check"),
        ("proof/check_explicit_formula_published_source_v5.py", "--check"),
        ("proof/replay_cycle1_route_a_readonly_v1.py",),
        ("proof/replay_cycle1_route_b_readonly_v1.py",),
        ("proof/run_g0_resource_gate_v2.py", "--check-config", "artifacts/g0-six-route-resource-gate-config-v2.json"),
    )
    for command in commands:
        subprocess.run((sys.executable, *command), cwd=ROOT, check=True,
                       capture_output=True, text=True)

    prior = load("v1_artifact")
    assert prior["decision"]["status"] == "PASS"
    assert prior["counts"]["resource_routes"] == 4
    formula = load("published_formula")
    assert formula["epistemic_status"] == "PROVED"
    assert formula["published_item"]["dspace_entity_type"] == "Publication"
    assert formula["published_theorem"]["status"] == "PROVED"

    config = load("resource_config")
    performance = load("resource_performance")
    route_ids = [row["id"] for row in config["routes"]]
    rows = performance["route_results"]
    assert route_ids == [row["id"] for row in rows]
    assert route_ids[:2] == ["cycle1-route-a-readonly-v1", "cycle1-route-b-readonly-v1"]
    assert len(rows) == 6 and performance["resource_gate"]["gate_status"] == "PASS"
    for row in rows:
        assert row["gate_status"] == "PASS"
        assert row["subprocess_returncode"] == row["time_exit_status"] == 0
        assert row["parse_error"] is None
        assert Decimal(row["wall_seconds"]) < Decimal(60)
        assert row["max_rss_kib"] < 262144

    retained = [row for row in prior["gate_rows"] if row["id"] not in {"G0-SOURCE-CONVENTIONS", "G0-RESOURCES"}]
    corrected_rows = retained + [
        {
            "id": "G0-SOURCE-CONVENTIONS",
            "requirement": "source hashes, locators, conventions, transformations, and strict PROVED source authority reconcile",
            "evidence": "v4 official bytes/transfer plus v5 authoritative MIT Publication metadata and checked Theorem 1/proof",
            "status": "PASS",
            "epistemic_status": "PROVED",
        },
        {
            "id": "G0-RESOURCES",
            "requirement": "every independent Cycle-1 and Cycle-2 route exits zero in strictly under 60 seconds and 256 MiB",
            "evidence": [
                {"id": row["id"], "wall_seconds": row["wall_seconds"], "max_rss_kib": row["max_rss_kib"], "status": row["gate_status"], "epistemic_status": "OBSERVED"}
                for row in rows
            ],
            "status": "PASS",
            "epistemic_status": "OBSERVED host-specific measurements",
        },
        {
            "id": "G0-RUNTIME-PIN",
            "requirement": "proof-grade one-command replay is version-pinned",
            "evidence": runtime,
            "status": "PASS",
            "epistemic_status": "PROVED exact environment assertion",
        },
    ]
    assert all(row["status"] == "PASS" for row in corrected_rows)

    counts = dict(prior["counts"])
    counts["resource_routes"] = 6
    return {
        "artifact_id": "g0-full-reconstruction-v2",
        "certificate_version": 2,
        "supersedes": "g0-full-reconstruction-v1 as the authoritative G0 decision; v1 is preserved as a premature under-scoped decision",
        "epistemic_status": "PROVED",
        "claim_boundary": "PROVED corrected adjudication that frozen G0 passes, conditional on the cited published analytic theorems whose selected hypotheses were checked. It is a reconstruction of published Guth--Maynard consequences, not a new zero-density or prime-interval theorem.",
        "correction": {
            "status": "OBSERVED CORRECTION",
            "v1_defects": [
                "Resource v1 timed four Cycle-2 routes but omitted the two independent Cycle-1 routes required by the Cycle-1 preregistration.",
                "The official formula theorem was checked in a course item, but v1 did not explicitly establish that DSpace classifies the exact item as a Publication under the repository's strict PROVED rule.",
                "The proof replay recorded CPython 3.12.3 only in OBSERVED performance data rather than asserting a frozen proof-runtime convention.",
            ],
            "containment": "V1 remains immutable but must not be cited as the final G0 authority. V2 adds two read-only Cycle-1 routes, six-route measurements, published-item v5 classification, and an exact CPython 3.12.3 runtime assertion.",
            "regression_correction": "The legacy dynamic-matrix-v2 test now derives its expected first unclassified artifact from the current delta instead of hard-coding a later filename; v2 itself remains fail-closed and unchanged.",
        },
        "decision": {
            "gate": "G0", "status": "PASS", "open_blockers": [],
            "authorized_next_path": "P1 after G1 preregistration is sealed",
            "epistemic_status": "PROVED corrected exact gate adjudication",
        },
        "runtime": runtime,
        "frozen_dependencies": hashes,
        "gate_rows": corrected_rows,
        "inherited_dependency_nodes": prior["inherited_dependency_nodes"],
        "counts": counts,
        "prior_corrections_preserved": prior["corrections_preserved"],
        "non_promotions": prior["non_promotions"],
        "falsifier": "A failed pinned runtime/hash/check, any non-PASS route, an at-or-over-ceiling resource row, loss of published-item/theorem status, or any reopened inherited node invalidates v2 and reopens G0.",
        "replay": {
            "script_sha256": sha256(Path(__file__)),
            "write_command": "python3 projects/guth-maynard-zero-density/proof/reconcile_g0_full_v2.py --write",
            "check_command": "python3 projects/guth-maynard-zero-density/proof/reconcile_g0_full_v2.py --check",
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
        raise SystemExit("corrected G0 v2 mismatch")
    else:
        print(json.dumps({"artifact": OUTPUT.name, "gate": "G0", "status": "PASS", "verified": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
