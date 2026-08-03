#!/usr/bin/env python3
"""Seal Cycle 189's regularized sign-reflected Jacobi--lens interface."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-189-regularized-jacobi-lens-interface-v1.json"
INPUTS = {
    "instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "prior_stabilizer_cycle": (ROOT / "artifacts/cycle-188-stabilizer-covariance-v1.json", "5129382929e50457355c727d13d1f5ccded7f47774895b4893931d7eaead1973"),
    "preregistration": (ROOT / "docs/cycle-189-jacobi-lens-interface-preregistration-v1.md", "d96e1d60a338669e3b2be48599798431c321e4579bbb59f0cb882a73d34c9ba7"),
    "replay": (ROOT / "proof/verify_cycle_189_regularized_jacobi_lens_interface.py", "471a687512c0a0bb0560965e9526405778a0b9075ab825eda42ae379837a401e"),
    "prototype": (ROOT / "discovery/cycle-189-regularized-jacobi-lens-interface-prototype-v1.json", "253196aff1bb11eb524d29dd9c32fe022b08ed6e571af480b9ad6270833f1b18"),
    "alias_packet": (ROOT / "scripts/dimension_six_alias_hypergeometric.py", "a687acc414379289f64d8320f1e0ce4de34f57845e6f5b536681f2b06d11f7b2"),
    "legacy_continuation_reference": (ROOT / "scripts/dimension_six_slater_reduction.py", "b7098424d8293c370ec178e32ab6aae6d5b281501d34d098c236f76d1f2dc1ff"),
    "lens_audit": (ROOT / "scripts/dimension_six_ss_evaluation_audit.py", "24c9258e46a1233c552017f3b58de0d45acd0197c8c807579f090ca1332f626f"),
    "two_base_lens": (ROOT / "scripts/dimension_six_two_base_lens.py", "72a4e0d9b577f661c89a84132f450c209f1f57a6131ba175b2a238f5bb197f79"),
    "d6_paper": (ROOT / "paper/sic-stark-dimension-six-boundary-fusion.tex", "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 189 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads(
        (ROOT / "discovery/cycle-189-regularized-jacobi-lens-interface-prototype-v1.json").read_text()
    )
    continuation = result["continuation"]
    finite_part = result["r_one_finite_part"]
    t_limit = result["t_one_regularization"]
    afk_map = result["source_defined_afk_map"]
    raw_alignment = result["raw_helical_factor_alignment"]
    require(continuation["raw_direct_CCG_hypothesis"] == "FAILED: |bq/d|=1", "raw continuation boundary drift")
    require(finite_part["finite_part_formula"] == "F(1)=-G'(1)/(q;q)_infty", "finite-part formula drift")
    require(afk_map["rows_checked"] == 36 and afk_map["all_gamma_to_shin_matches"], "all-characteristic source map drift")
    require(raw_alignment["frequency_characteristic_pairs_checked"] == 1296, "raw alignment census drift")
    require(raw_alignment["direct_discrete_residue_mod_4"] == [2], "direct obstruction drift")
    require(raw_alignment["reflected_discrete_residue_mod_4"] == [2], "reflected obstruction drift")
    return {
        "artifact_id": "cycle-189-regularized-jacobi-lens-interface-v1",
        "cycle": 189,
        "budget_ordinal": "B026",
        "epistemic_status": "PROVED",
        "status": "SEALED_INTERIOR_REGULARIZATION_ALL36_JACOBI_LENS_MAP_AND_FACTORWISE_OBSTRUCTION",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": "The sign-reflected packet has a checked Chen--Chen--Gu interior regularization, an exact removable r=1 finite-part formula, and a t->1^- unilateral continuation. Independently, lower-case lens gamma maps to the unphased AFK Shintani cocycle on all 36 source-defined characteristic lines. No raw kernel factor, after the only coefficient-compatible constant omega_2 shift, reaches any such line: all 1,296 frequency/characteristic pairs leave the exact residue 2 modulo 4.",
        },
        "continuation": {
            "source": "Chen--Chen--Gu, Theorem 2.1 / equation (2.1)",
            "source_tex_sha256": "3d902b7d9c0beb6cd6f36e0c66c0213b1cc76ad9302e7311b9f4e3525e3df9a6",
            "audit": continuation,
            "r_one_cancellation": result["r_one_cancellation"],
            "finite_part": finite_part,
            "t_one_regularization": t_limit,
        },
        "jacobi_lens": {
            "kopp_source": "Kopp arXiv:2411.06763v3",
            "kopp_source_tex_sha256": "4f3d0b359502e575e28c6be8259ed0ac45422f94ff91a9f6f3caf7a4f1504bcc",
            "sarkissian_spiridonov_source": "Sarkissian--Spiridonov arXiv:1910.11747v4",
            "sarkissian_spiridonov_source_tex_sha256": "69a140cfd4af010a7ffcf0643e1df211f4675a88c2480e1b868c77bca4520941",
            "lower_gamma_identity": result["jacobi_lens_identity"],
            "source_defined_afk_map": afk_map,
            "capital_normalization": "Retained explicitly; it is not absorbed into the unphased lower-gamma source map or AFK phase.",
        },
        "scoped_controls_and_obstruction": {
            "untranslated_one_factor": result["direct_one_factor_test"],
            "raw_helical_factor_alignment": raw_alignment,
        },
        "gate_outcome": {
            "d6_interface": "INTERIOR_PACKET_AND_ALL36_GAMMA_TO_SHIN_LINES_PROVED_NONFACTORWISE_PERIODIZATION_REQUIRED",
            "remaining_bottleneck": "Construct and verify an outcome-blind nonfactorwise periodization from the three-dimensional regularized derivative-core state to the source-defined mu_p(tau) Jacobi lines, retaining the capital Gamma_M normalization and separate AFK phase before any real-multiplication boundary argument.",
            "disallowed_pseudo_progress": [
                "calling the raw CCG boundary condition an interior use of its theorem",
                "equating a raw gamma factor with a full periodization",
                "discarding the capital Gamma_M normalization or AFK phase",
                "using multiplier weights, ray labels, selected exponents, or fitted characters as the map",
                "claiming a real-multiplication, fusion, Stark, or TCC consequence from this interior result",
            ],
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "An explicit outcome-blind nonfactorwise helical periodization of the regularized three-core derivative state may match the all-36 AFK Jacobi lines with exact covariance; otherwise an exact obstruction for a clearly delimited periodization class may identify the next completion mechanism.",
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "The normalized Kopp-to-AFK Shintani source map is checked on all 36 characteristics, and the exact 1,296-case raw-factor census excludes every single raw helical Gamma factor with a constant omega_2 shift in either orientation.",
            "recommendation": "Seal Cycle 189; the factorwise route is exhausted and nonfactorwise periodization is a distinct engine.",
            "known_flaw": "Only one-factor constant shifts are excluded; finite sums, derivative-core constructions, nonconstant periodizations, and the real-multiplication boundary remain open.",
            "falsifier": "A gamma/AFK normalization or phase error, a tau-coefficient reduction error, a missed shift/orientation/census row, or a replay discrepancy.",
            "next_action": "Open a cycle with a frozen at-most-three-dimensional derivative-core state and outcome-blind nonfactorwise periodization; seek exact AFK covariance/matching or a scoped obstruction before the unit-circle step.",
            "adopted": True,
            "reason": "The current replay has completed the frozen continuation and smallest factorwise construction, while its remaining construction has a different state space and failure class.",
        },
        "preregistration_preflight": {
            "cycle": 189,
            "manifest_sha256": sha256(ROOT / "docs/cycle-189-jacobi-lens-interface-preregistration-v1.md"),
            "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"},
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-189-jacobi-lens-interface-preregistration-v1.md --expected-cycle 189 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_189_regularized_jacobi_lens_interface.py --output discovery/cycle-189-regularized-jacobi-lens-interface-prototype-v1.json",
            "write_command": "python3 proof/build_cycle_189_regularized_jacobi_lens_interface_v1.py --write",
            "check_command": "python3 proof/build_cycle_189_regularized_jacobi_lens_interface_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_189_regularized_jacobi_lens_interface_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
