#!/usr/bin/env python3
"""Seal Cycle 184's multiplier-refined ray correspondence."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-184-multiplier-refined-correspondence-v1.json"
INPUTS = {
    "instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "multiplier": (ROOT / "artifacts/cycle-166-fibre-torsor-v1.json", "cd0cf07f8ded432a7f53c18126d26b5054b3fddadb530375483c7adbc753991e"),
    "assembly": (ROOT / "artifacts/cycle-180-local-global-artin-assembly-v1.json", "00ed9e7d014d1e53e828390f589ed5b97ceacb8fba2ddf502b8f318707b7817f"),
    "transport": (ROOT / "artifacts/cycle-181-shintani-local-action-v1.json", "539e7179b060c471603154331327843b909487125b80278c2d76d346a3d930e4"),
    "prior": (ROOT / "artifacts/cycle-183-conductor-graded-target-v1.json", "117ab48b1b6a61aa826e39c5ad18527fa930b43b87d1eb927a82d7c839af7654"),
    "prereg": (ROOT / "docs/cycle-184-multiplier-refined-correspondence-preregistration-v1.md", "f3a359c8c92d8dc95718851a55b465e099dfccd790e3fc013ed316f14a06f25d"),
    "replay": (ROOT / "proof/verify_cycle_184_multiplier_refined_correspondence.py", "46e94f28841a029ed5f740bfe5c697d71a9bb4b55781ec23ce9e6c99b359bfdb"),
    "output": (ROOT / "discovery/cycle-184-multiplier-refined-correspondence-prototype-v1.json", "6c01d20f2c99d0619abe2fe38257c478a5dbba2235471bc15f56319c66ee9d76"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 184 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads((ROOT / "discovery/cycle-184-multiplier-refined-correspondence-prototype-v1.json").read_text())
    summary = result["summary"]
    require((summary["rows_checked"], summary["compressed_state_count"], summary["phase_value_count"], summary["direct_ray_difference_validations"], summary["edge_compositions_checked"], summary["third_compositions_checked"], summary["deterministic_successor_conflict_count"]) == (36, 17, 6, 36, 36, 36, 10), "correspondence census drift")
    require(summary["strict_compression"] and summary["all_direct_relations_equal_independent_ray_differences"], "compression or ray validation drift")
    require(len(result["states"]) == 17 and len(result["conflicts"]) == 10, "state/conflict witness drift")
    require(summary["anchors"] == {"3,5": [[1, 2], [1], 32], "3,4": [[1, 2], [2], 8]}, "anchor drift")
    return {
        "artifact_id": "cycle-184-multiplier-refined-correspondence-v1", "cycle": 184, "budget_ordinal": "B022", "epistemic_status": "PROVED", "status": "SEALED_MULTIPLIER_REFINED_CORRESPONDENCE_COMPOSITION_VALIDATED",
        "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "The 17-state multiplier-refined local ray correspondence has exact independent ray validation and a source-defined set-plus-phase composition law, but ten successor conflicts prevent it from being a deterministic state action."},
        "conventions": {"characteristic_action": "T(a,b)=(5a+b,-a) mod 6", "phase": "p(a,b)=24*(6+7*(1+a)*(1+b))-12-28*(a^2-5*a*b+b^2) mod 48", "state": "(lowered conductor grade, assembled C6 exponent coset, p)", "composition": "(D,delta)+(D',delta')=(D+D',delta+delta') in set-valued C6 x Z/48"},
        "exact_prototype": {"source_output": "discovery/cycle-184-multiplier-refined-correspondence-prototype-v1.json", "summary": summary},
        "gate_outcome": {"d6_interface": "MULTIPLIER_REFINED_CORRESPONDENCE_COMPOSITION_VALIDATED_AFK_WEIGHTED_TRANSFER_REQUIRED", "remaining_bottleneck": "Define source-side AFK coefficient weights on the preserved correspondence fibres, then test an unfitted weighted transfer operation before any analytic promotion.", "disallowed_pseudo_progress": ["calling the 17-state correspondence a deterministic action", "selecting ray exponents or fitting labels", "re-encoding 36 rows as states", "claiming an AFK coefficient identification, Stark equality, fusion theorem, or TCC identity"]},
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "A source-defined AFK-coefficient-weighted transfer operator on the multiplier-refined correspondence may yield a genuinely additive operation while retaining its intrinsic fibre ambiguity."},
        "companion_decision": {"identity": "/root/decision_companion_2", "recommendation": "Seal the finite correspondence and start a new cycle for a source-defined AFK-coefficient-weighted transfer operator.", "adopted": True, "reason": "The exact compression/composition result is material, while the remaining ten conflicts require retaining correspondence fibres rather than fitting an action."},
        "preregistration_preflight": {"cycle": 184, "manifest_sha256": sha256(ROOT / "docs/cycle-184-multiplier-refined-correspondence-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-184-multiplier-refined-correspondence-preregistration-v1.md --expected-cycle 184 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_184_multiplier_refined_correspondence.py --output discovery/cycle-184-multiplier-refined-correspondence-prototype-v1.json", "write_command": "python3 proof/build_cycle_184_multiplier_refined_correspondence_v1.py --write", "check_command": "python3 proof/build_cycle_184_multiplier_refined_correspondence_v1.py --check"},
        "runtime": runtime, "sealer": {"path": "proof/build_cycle_184_multiplier_refined_correspondence_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
