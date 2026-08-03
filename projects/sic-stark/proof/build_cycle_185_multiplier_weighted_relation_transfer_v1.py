#!/usr/bin/env python3
"""Seal Cycle 185's multiplier-weighted relation transfer."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-185-multiplier-weighted-relation-transfer-v1.json"
INPUTS = {
    "instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "multiplier": (ROOT / "artifacts/cycle-166-fibre-torsor-v1.json", "cd0cf07f8ded432a7f53c18126d26b5054b3fddadb530375483c7adbc753991e"),
    "transport": (ROOT / "artifacts/cycle-181-shintani-local-action-v1.json", "539e7179b060c471603154331327843b909487125b80278c2d76d346a3d930e4"),
    "correspondence": (ROOT / "artifacts/cycle-184-multiplier-refined-correspondence-v1.json", "869771fb3299b129c65f7579b15fc5829baf3801b39d7da72566e9fcd7bcb7e2"),
    "transport_rows": (ROOT / "discovery/cycle-181-shintani-local-action-prototype-v1.json", "beed812494154f058b970791112cf76d29ffe6960c32b3736e9e871f1d99f95f"),
    "correspondence_rows": (ROOT / "discovery/cycle-184-multiplier-refined-correspondence-prototype-v1.json", "6c01d20f2c99d0619abe2fe38257c478a5dbba2235471bc15f56319c66ee9d76"),
    "prereg": (ROOT / "docs/cycle-185-multiplier-weighted-relation-transfer-preregistration-v1.md", "9e191233cd25f9ccd07ffab54460e727cdcaaba37091c7c0795eb9007bb48ffb"),
    "replay": (ROOT / "proof/verify_cycle_185_multiplier_weighted_relation_transfer.py", "ffc4546224b5717e7999c0eea66b14f28e502a1bcb7b6f747a5ab7b04c370fb5"),
    "output": (ROOT / "discovery/cycle-185-multiplier-weighted-relation-transfer-prototype-v1.json", "eba8d3e44e935eba20f674dd8a49dc0bac98374f89b5af783fdbd0a4c436b662"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 185 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads((ROOT / "discovery/cycle-185-multiplier-weighted-relation-transfer-prototype-v1.json").read_text())
    summary = result["summary"]
    require((summary["rows_checked"], summary["relation_label_count"], summary["phase_integrality_checks"], summary["direct_relation_agreements"], summary["triple_products_checked"]) == (36, 11, 36, 36, 36), "transfer census drift")
    require(summary["strict_label_compression"] and summary["all_triple_products_equal_independent_kernels"], "transfer law drift")
    require(summary["anchors"]["3,5"][3] == ["1", "0"] and summary["anchors"]["3,4"][3] == ["-1", "0"], "orientation anchor drift")
    return {
        "artifact_id": "cycle-185-multiplier-weighted-relation-transfer-v1", "cycle": 185, "budget_ordinal": "B023", "epistemic_status": "PROVED", "status": "SEALED_MULTIPLIER_WEIGHTED_RELATION_TRANSFER_COMPOSITION_VALIDATED",
        "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "The complete 36-row multiplier-refined correspondence linearizes to 11 normalized relation labels in Q(zeta_6)[C6]; all exact triple convolutions equal the independently retained Cycle-181 kernels and the two anchors have opposite signs."},
        "conventions": result["conventions"], "exact_prototype": {"source_output": "discovery/cycle-185-multiplier-weighted-relation-transfer-prototype-v1.json", "summary": summary},
        "gate_outcome": {"d6_interface": "MULTIPLIER_WEIGHTED_RELATION_TRANSFER_VALIDATED_FORMAL_AFK_PACKET_REPRESENTATION_REQUIRED", "remaining_bottleneck": "Derive a formal AFK coefficient-packet representation source-side, then compare its exact A6 character decomposition with this transfer algebra without calling multiplier weights spectral coefficients.", "disallowed_pseudo_progress": ["calling normalized relation measures AFK spectral coefficients", "inferring a coefficient-to-ray, Stark, fusion, or TCC interface", "fitting a character or ray labels", "selecting exponents or deleting conflicting fibres"]},
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "A formal source-side AFK coefficient-packet representation may have an exact A6-character decomposition that either matches or discriminates against the 11-label multiplier-weighted transfer algebra."},
        "companion_decision": {"identity": "/root/decision_companion_2", "recommendation": "Seal the finite transfer and open a new cycle for a source-side formal AFK coefficient-packet representation and character-decomposition comparison.", "adopted": True, "reason": "The multiplication test is complete, but its coset averages and multiplier phases contain no spectral coefficient data."},
        "preregistration_preflight": {"cycle": 185, "manifest_sha256": sha256(ROOT / "docs/cycle-185-multiplier-weighted-relation-transfer-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-185-multiplier-weighted-relation-transfer-preregistration-v1.md --expected-cycle 185 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_185_multiplier_weighted_relation_transfer.py --output discovery/cycle-185-multiplier-weighted-relation-transfer-prototype-v1.json", "write_command": "python3 proof/build_cycle_185_multiplier_weighted_relation_transfer_v1.py --write", "check_command": "python3 proof/build_cycle_185_multiplier_weighted_relation_transfer_v1.py --check"},
        "runtime": runtime, "sealer": {"path": "proof/build_cycle_185_multiplier_weighted_relation_transfer_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
