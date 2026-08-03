#!/usr/bin/env python3
"""Seal Cycle 191's central-character beta-Fourier restriction result."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-191-central-character-fourier-v1.json"
INPUTS = {
    "instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "prior_recurrence_obstruction": (ROOT / "artifacts/cycle-190-balanced-helical-reflection-v1.json", "42c9194365693832b96d7586b4df2eed3c9deefc52deb9dba5c80dec08ff1f2f"),
    "preregistration": (ROOT / "docs/cycle-191-central-character-fourier-preregistration-v1.md", "e283098f91440b83984bd2fbcb9cce9e2b8f4be6cf56e60eb56f9f403356d130"),
    "replay": (ROOT / "proof/verify_cycle_191_central_character_fourier.py", "6159406c96c2218060292492255193ee4f4631a7f7e44377772604ede2fcaefe"),
    "prototype": (ROOT / "discovery/cycle-191-central-character-fourier-prototype-v1.json", "92bc904105ebf170ef95ebf4b12adf4990695223f1330d255ccfa91829982b40"),
    "beta_fourier": (ROOT / "scripts/dimension_six_beta_fourier.py", "d47242027af1851ea29b60b8e8c362f42fa5a1634fd0b375e39233b4d87f7a6e"),
    "beta_kernel_match": (ROOT / "scripts/dimension_six_beta_kernel_match.py", "6210819200882c83ebaed4fc74c9cce220a0d09748a8343a8b02a609d1289e27"),
    "helical_zak": (ROOT / "scripts/dimension_six_helical_zak.py", "185f79ae0c3e5b560939a81551877cf0d14401100466793cc2d7fa4973061bf0"),
    "heisenberg_descent": (ROOT / "scripts/dimension_six_heisenberg_descent.py", "ccc19fd158cc4714c2d5fcbecbb5c8091c2bdbd748561aed6736482bb2dbe11f"),
    "inversion_phase": (ROOT / "scripts/dimension_six_inversion_phase.py", "30234d2e0e87b03ca7109781b193c23751e9c30de9b498972ac2c551b64282be"),
    "d6_paper": (ROOT / "paper/sic-stark-dimension-six-boundary-fusion.tex", "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 191 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads((ROOT / "discovery/cycle-191-central-character-fourier-prototype-v1.json").read_text())
    selection = result["all_alias_selection"]
    holonomy = result["alias_holonomy"]
    normalization = result["afk_normalization_control"]
    require(selection["rows_checked"] == 900 and selection["selection_is_outcome_blind"], "selection census drift")
    require(holonomy["one_alias_step_operator_on_selected_block"] == "diag_j((-1)^j)", "one-step holonomy drift")
    require(holonomy["three_alias_step_operator_on_selected_block"] == "diag_j((-1)^j)", "three-step holonomy drift")
    require(not holonomy["operator_is_scalar"], "scalar obstruction drift")
    require(normalization["rows_checked"] == 36, "AFK normalization census drift")
    return {
        "artifact_id": "cycle-191-central-character-fourier-v1",
        "cycle": 191,
        "budget_ordinal": "B028",
        "epistemic_status": "PROVED",
        "status": "SEALED_ALL36_CENTRAL_CHARACTER_SELECTION_AND_SCALAR_COMPLETION_OBSTRUCTION",
        "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "The d=6 specialization of the published beta Fourier character selects, outcome-blindly, the unique central-character block epsilon=a mod 2 for every one of the 36 characteristics and 25 checked aliases each. Its alias holonomy is the non-scalar operator diag_j((-1)^j); the retained Gamma_M/AFK normalization is block-scalar and cannot cancel it. Thus a scalar block completion is excluded, but a Z2-graded non-scalar completion remains open."},
        "source_transform": result["source_transform"],
        "central_character_blocks": result["central_character_blocks"],
        "all_alias_selection": selection,
        "alias_holonomy": holonomy,
        "afk_normalization_control": normalization,
        "gate_outcome": {"d6_interface": "ALL36_BETA_FOURIER_BLOCK_SELECTION_PROVED_SCALAR_COMPLETION_OBSTRUCTED_Z2_GRADED_OPERATOR_REQUIRED", "remaining_bottleneck": "Define a source-derived Z2-graded non-scalar block representation, prove that the continuous beta transform preserves it, and test its exact matrix-valued AFK intertwiner before any boundary evaluation.", "disallowed_pseudo_progress": ["calling discrete selection continuous block preservation", "replacing diag_j((-1)^j) by a scalar phase", "adding a fitted block or coefficient", "discarding Gamma_M normalization or AFK wrap signs", "claiming source-to-AFK amplitudes, RM boundary, fusion, Stark, or TCC from the finite restriction"]},
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "A source-derived Z2-graded non-scalar completion of the beta Fourier transform may preserve the selected level-six blocks and admit an exact matrix-valued AFK intertwiner; otherwise a clearly declared graded-operator class may be scopedly obstructed."},
        "companion_decision": {"identity": "/root/decision_companion_2", "evidence_scope_review": "The beta-character convention, parity descent, 900-row census, alias spectrum, and block-scalarity control are exact and cover the declared discrete restriction.", "recommendation": "Seal Cycle 191 as PROVED only for the bounded discrete beta-Fourier restriction and scalar-completion obstruction; a non-scalar completion requires a distinct cycle.", "known_flaw": "The result establishes neither continuous-transform block preservation nor amplitude, AFK-value, boundary, or TCC compatibility.", "falsifier": "Any beta-character convention, parity descent, 900-row census, alias-spectrum, block-scalarity, or replay discrepancy.", "next_action": "Preregister a source-derived Z2-graded non-scalar block representation, prove continuous block preservation, and test an exact matrix-valued AFK intertwiner before any boundary evaluation.", "adopted": True, "reason": "The frozen two-block scalar-completion class is fully classified, while a graded non-scalar operator adds a different state representation and proof obligation."},
        "preregistration_preflight": {"cycle": 191, "manifest_sha256": sha256(ROOT / "docs/cycle-191-central-character-fourier-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-191-central-character-fourier-preregistration-v1.md --expected-cycle 191 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_191_central_character_fourier.py --output discovery/cycle-191-central-character-fourier-prototype-v1.json", "write_command": "python3 proof/build_cycle_191_central_character_fourier_v1.py --write", "check_command": "python3 proof/build_cycle_191_central_character_fourier_v1.py --check"},
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_191_central_character_fourier_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
