#!/usr/bin/env python3
"""Seal Cycle 167's exact bilinear torsor-convolution falsifier."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "cycle-167-bilinear-convolution-v1.json"
FROZEN_INPUTS = {
    "project_instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "cycle_166_torsor": (ROOT / "artifacts/cycle-166-fibre-torsor-v1.json", "cd0cf07f8ded432a7f53c18126d26b5054b3fddadb530375483c7adbc753991e"),
    "preregistration": (ROOT / "docs/cycle-167-bilinear-convolution-preregistration-v1.md", "6cbd1c131dcb883a5b4b2ce1cdd304f9de4aa7a2bb20894075f6536ca03c057f"),
    "census_replay": (ROOT / "proof/verify_cycle_167_bilinear_convolution.py", "e38dd4011edb87a8c8bd4e5a449b35ce2b873a2d5f798f3f1e5f528c8127b48e"),
    "census_output": (ROOT / "discovery/cycle-167-bilinear-convolution-prototype-v1.json", "fa8115bca61b5cf18d01d37bef2f2ba3cebfbd846b7994d18dbd0a64702ca69f"),
    "test": (ROOT / "tests/test_cycle_167_bilinear_convolution.py", "4af470dc81cd3b39d819953b9de51d792b6f6e0ec1c67cd095e7a35fc3ebb3a5"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 167 bilinear-convolution seal")
    frozen_hashes = freeze_inputs(ROOT, FROZEN_INPUTS)
    prototype = json.loads((ROOT / "discovery/cycle-167-bilinear-convolution-prototype-v1.json").read_text())
    summary = prototype["summary"]
    require(summary["matrices_checked"] == 1296, "incomplete matrix census")
    require(summary["basis_pairs_per_matrix"] == 1296, "incomplete pair domain")
    require(summary["graph_identity_checks"] == 1679616, "incomplete graph census")
    require(summary["transport_identity_checks"] == 1679616, "incomplete transport census")
    require(summary["graph_passing_matrix_count"] == 0, "unexpected graph product")
    require(summary["transport_passing_matrix_count"] == 0, "unexpected transport product")
    require(summary["compatible_matrix_count"] == 0, "unexpected compatible product")
    require(summary["bilinear_convolution_exists"] is False, "unexpected bilinear convolution")
    require(prototype["first_graph_failure"] == {"matrix": [0, 0, 0, 0], "left": [0, 1], "right": [0, 3], "expected_graph_label": 1, "actual_product_label": 0}, "graph witness drift")
    require(prototype["first_transport_failure"] == {"matrix": [0, 0, 0, 0], "left": [0, 1], "right": [1, 0], "expected_transported_product_label": 4, "actual_product_of_transports_label": 2}, "transport witness drift")
    return {
        "artifact_id": "cycle-167-bilinear-convolution-v1",
        "cycle": 167,
        "budget_ordinal": "B005",
        "epistemic_status": "PROVED",
        "status": "SEALED_BILINEAR_TWISTED_CONVOLUTION_FALSIFIED",
        "claim_boundary": "This exact finite result falsifies only translation-invariant bilinear C6-twisted convolutions on the sealed Cycle-166 torsor. It does not rule out nonlinear, non-translation-invariant, higher-fibre, or analytic coefficient operations.",
        "outcome": {"epistemic_status": "PROVED", "statement": "No one of the 1,296 bilinear C6 twists makes the frozen torsor graph multiplicative or its Shintani transport an algebra automorphism; hence none meets both conditions."},
        "exact_prototype": {**summary, "first_graph_failure": prototype["first_graph_failure"], "first_transport_failure": prototype["first_transport_failure"], "source_output": "discovery/cycle-167-bilinear-convolution-prototype-v1.json"},
        "gate_outcome": {"d6_interface": "BILINEAR_TWISTED_CONVOLUTION_FALSIFIED_NONLINEAR_ENGINE_REQUIRED", "falsified_operation_class": "translation-invariant bilinear C6-twisted convolutions on the sealed torsor", "remaining_bottleneck": "A genuinely new, outcome-blind nonlinear or other non-bilinear finite operation must be independently specified before it can be tested.", "disallowed_pseudo_progress": ["choosing the graph coboundary after inspecting its defect", "calling this scoped falsifier an AFK or TCC no-go", "repeating the same bilinear census under changed notation"]},
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "Cycle 168/B006: preregister an independent constrained nonlinear 2-cocycle or another genuinely new outcome-blind finite operation family, with an exact multiplicativity-or-falsifier test."},
        "preregistration_preflight": {"cycle": 167, "manifest_sha256": sha256(ROOT / "docs/cycle-167-bilinear-convolution-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen_hashes,
        "replay": {"preflight_command": "research prereg check docs/cycle-167-bilinear-convolution-preregistration-v1.md --expected-cycle 167 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_167_bilinear_convolution.py --output discovery/cycle-167-bilinear-convolution-prototype-v1.json", "test_command": "python3 -m unittest tests.test_cycle_167_bilinear_convolution -v", "write_command": "python3 proof/build_cycle_167_bilinear_convolution_v1.py --write", "check_command": "python3 proof/build_cycle_167_bilinear_convolution_v1.py --check"},
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_167_bilinear_convolution_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
