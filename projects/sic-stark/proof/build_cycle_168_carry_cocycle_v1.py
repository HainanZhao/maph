#!/usr/bin/env python3
"""Seal Cycle 168's canonical carry-cocycle falsifier."""
from __future__ import annotations
import json
from pathlib import Path
from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-168-carry-cocycle-v1.json"
FROZEN_INPUTS = {
    "project_instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "cycle_167_falsifier": (ROOT / "artifacts/cycle-167-bilinear-convolution-v1.json", "0bd6aa9149e9e027ee74d3edff7ce98c45dde4e7e05044500f852c26ce03018a"),
    "preregistration": (ROOT / "docs/cycle-168-carry-cocycle-preregistration-v1.md", "9cd5d722748cd68568c8a20b6ecc554cf11798ed629f3cd6dc29fce9e1ff4e5b"),
    "census_replay": (ROOT / "proof/verify_cycle_168_carry_cocycle.py", "15550b55af55776fcd0cd5b1f5aabfa7c32132b027bb77772883e30abf92307a"),
    "census_output": (ROOT / "discovery/cycle-168-carry-cocycle-prototype-v1.json", "07901fa8003c69efdebf099f9e619d18f8a8a92fbc6bdf2b54255cfb99fd0367"),
    "test": (ROOT / "tests/test_cycle_168_carry_cocycle.py", "d088be6e67d983433a09c09b654110e332dc7d503f1d570a19b803ff4a3178f8"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}

def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 168 carry-cocycle seal")
    frozen_hashes = freeze_inputs(ROOT, FROZEN_INPUTS)
    prototype = json.loads((ROOT / "discovery/cycle-168-carry-cocycle-prototype-v1.json").read_text())
    summary = prototype["summary"]
    require(summary["cocycle_candidates_checked"] == 46656, "incomplete candidate census")
    require(summary["basis_cocycle_associativity_checks"] == 279936, "associativity basis census failed")
    require(summary["probe_survivor_count"] == 1, "identifying probes no longer unique")
    require(summary["graph_passing_parameter_count"] == 0 and summary["transport_passing_parameter_count"] == 0 and summary["compatible_parameter_count"] == 0, "unexpected cocycle completion")
    require(prototype["probe_survivors"] == [[0, 5, 5, 0, 3, 3]], "probe reconstruction drift")
    return {
        "artifact_id": "cycle-168-carry-cocycle-v1", "cycle": 168, "budget_ordinal": "B006", "epistemic_status": "PROVED", "status": "SEALED_CANONICAL_CARRY_COCOCYCLE_FALSIFIED",
        "claim_boundary": "This exact finite result falsifies only canonical normalized bilinear-plus-coordinate-carry C6 cocycles on the sealed torsor. It does not rule out general state-dependent, nonlocal, higher-fibre, characteristic-dependent, or analytic coefficient operations.",
        "outcome": {"epistemic_status": "PROVED", "statement": "All 46,656 canonical carry-cocycle representatives are associative, but their sole probe-compatible member [0,5,5,0,3,3] fails both full graph and transport identities."},
        "exact_prototype": {**summary, "probe_survivors": prototype["probe_survivors"], "first_graph_failure": prototype["first_graph_failure"], "first_transport_failure": prototype["first_transport_failure"], "source_output": "discovery/cycle-168-carry-cocycle-prototype-v1.json"},
        "gate_outcome": {"d6_interface": "CANONICAL_COCOCYCLE_FAMILY_FALSIFIED_COHOMOLOGICAL_OBSTRUCTION_REQUIRED", "falsified_operation_class": "canonical bilinear-plus-coordinate-carry normalized C6 cocycle representatives", "remaining_bottleneck": "Determine the full action-groupoid defect cohomology class without fitting a graph coboundary.", "disallowed_pseudo_progress": ["enlarging another parameter family without a cohomological invariant", "taking the graph defect as the operation", "calling this scoped result an AFK or TCC no-go"]},
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "Cycle 169/B007: preregister a full action-groupoid defect cohomology construction and test exactly whether its transport-compatible class is a coboundary under independent normalization constraints."},
        "preregistration_preflight": {"cycle": 168, "manifest_sha256": sha256(ROOT / "docs/cycle-168-carry-cocycle-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen_hashes,
        "replay": {"preflight_command": "research prereg check docs/cycle-168-carry-cocycle-preregistration-v1.md --expected-cycle 168 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_168_carry_cocycle.py --output discovery/cycle-168-carry-cocycle-prototype-v1.json", "test_command": "python3 -m unittest tests.test_cycle_168_carry_cocycle -v", "write_command": "python3 proof/build_cycle_168_carry_cocycle_v1.py --write", "check_command": "python3 proof/build_cycle_168_carry_cocycle_v1.py --check"},
        "runtime": runtime, "sealer": {"path": "proof/build_cycle_168_carry_cocycle_v1.py", "sha256": sha256(Path(__file__))},
    }

if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
