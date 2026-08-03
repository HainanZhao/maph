#!/usr/bin/env python3
"""Seal Cycle 190's balanced helical reflection lattice obstruction."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-190-balanced-helical-reflection-v1.json"
INPUTS = {
    "instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "prior_jacobi_lens_cycle": (ROOT / "artifacts/cycle-189-regularized-jacobi-lens-interface-v1.json", "f46b6bedbef2ac8fbdf63da7864879086ce72dba8becb534f0bc9c20d9725da7"),
    "preregistration": (ROOT / "docs/cycle-190-balanced-helical-reflection-preregistration-v1.md", "a5c0571d31aca9c49c19e9f890b4360215804387aab0b78b02f34fa1374dd3e4"),
    "replay": (ROOT / "proof/verify_cycle_190_balanced_helical_reflection.py", "69da849d11c00ec30a5bca1a1220e1616d3d31beb75c8b906e8a67a9b0c98469"),
    "prototype": (ROOT / "discovery/cycle-190-balanced-helical-reflection-prototype-v1.json", "43c58866528c4f4c3b42614d0b4acb9c52cc40dab52d10725ba6ff7ed1147eff"),
    "ss_audit": (ROOT / "scripts/dimension_six_ss_evaluation_audit.py", "24c9258e46a1233c552017f3b58de0d45acd0197c8c807579f090ca1332f626f"),
    "interior_factorization": (ROOT / "scripts/dimension_six_interior_factorization_audit.py", "245a400d830560d981f7b19f8953a0241ac4402bbfbcb8289a5478feb2076964"),
    "d6_paper": (ROOT / "paper/sic-stark-dimension-six-boundary-fusion.tex", "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 190 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads((ROOT / "discovery/cycle-190-balanced-helical-reflection-prototype-v1.json").read_text())
    lattice = result["lattice"]
    census = result["bounded_census"]
    grid = result["full_grid_control"]
    require(lattice["helical_relation"] == "H=T1-T2 exactly, including the discrete label", "helical relation drift")
    require(lattice["q_shift_discrete_change"] == "5(1-c)-(1+c)+6c=4", "Q shift defect drift")
    require(census["words_checked"] == 117649 and census["continuous_Q_zero_label_words"] == 0, "word census drift")
    require(census["continuous_zero_nonzero_label_words"] == 0, "vertical lattice drift")
    require(grid["frequency_characteristic_residue_rows"] == 3888 and not grid["characteristic_dependent_escape"], "grid control drift")
    return {
        "artifact_id": "cycle-190-balanced-helical-reflection-v1",
        "cycle": 190,
        "budget_ordinal": "B027",
        "epistemic_status": "PROVED",
        "status": "SEALED_RECURRENCE_ONLY_BALANCED_HELICAL_REFLECTION_OBSTRUCTION",
        "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "For the d=6 normalized lens gamma, the helical generator is exactly T1-T2. Every integer word with the continuous Q shift needed to convert the raw reflected factor to its normalized-reflection partner has discrete shift +4, never 0; every continuous-zero word has zero discrete shift. Thus recurrence, normalized reflection, and helical reindexing cannot repair the raw pair's residual label defect."},
        "normalized_reflection": result["normalized_reflection"],
        "raw_pair": result["raw_pair"],
        "reflection_partner": result["reflection_partner"],
        "required_translation": result["required_translation"],
        "exact_lattice": lattice,
        "bounded_census": census,
        "full_grid_control": grid,
        "gate_outcome": {"d6_interface": "RECURRENCE_ONLY_BALANCED_HELICAL_PERIODIZATION_OBSTRUCTED_NEW_DERIVATIVE_OR_CONTOUR_IDENTITY_REQUIRED", "remaining_bottleneck": "A genuine derivative-core or contour-integral transform must supply information beyond the T1,T2,H recurrence/reflection lattice, then be matched exactly to the all-36 source-defined AFK lines before any real-multiplication boundary argument.", "disallowed_pseudo_progress": ["reindexing the old helical quotient as a new transform", "using lower-case periodicity in place of capital Gamma_M quasiperiodicity", "dropping Z(m), Bernoulli normalization, or AFK representative signs", "claiming the reflection norm identity is an oriented cocycle evaluation", "using ray labels, selected exponents, fitted characters, or unit-circle continuation"]},
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "One source-derived derivative or contour-integral identity on the at-most-three-dimensional regularized core state may supply a non-recurrence periodization with exact all-36 AFK matching; otherwise its declared transform class may be scopedly obstructed."},
        "companion_decision": {"identity": "/root/decision_companion_2", "evidence_scope_review": "The classified word family exactly exhausts the declared normalized recurrence/reflection/helical-reindexing engine: T1,T2,H, the Q defect, bounded census, and all-row control agree.", "recommendation": "Seal Cycle 190 as PROVED only for this recurrence/reflection/reindexing lattice obstruction.", "known_flaw": "No identity using differentiation, contour/integral transforms, residues, or genuinely new analytic continuation is excluded.", "falsifier": "Any shift normalization, word classification, label homomorphism, kernel-label, row-control, or replay discrepancy.", "next_action": "Open a new cycle preregistering one source-derived derivative or contour-integral identity on the at-most-three-core state space, with exact AFK matching and boundary criteria frozen before execution.", "adopted": True, "reason": "The exact lattice proof exhausts the declared engine, while the remaining methods require an additional identity not present in its generator set."},
        "preregistration_preflight": {"cycle": 190, "manifest_sha256": sha256(ROOT / "docs/cycle-190-balanced-helical-reflection-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-190-balanced-helical-reflection-preregistration-v1.md --expected-cycle 190 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_190_balanced_helical_reflection.py --output discovery/cycle-190-balanced-helical-reflection-prototype-v1.json", "write_command": "python3 proof/build_cycle_190_balanced_helical_reflection_v1.py --write", "check_command": "python3 proof/build_cycle_190_balanced_helical_reflection_v1.py --check"},
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_190_balanced_helical_reflection_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
