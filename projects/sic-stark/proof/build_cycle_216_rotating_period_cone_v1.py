#!/usr/bin/env python3
"""Seal Cycle 216/B053's rotating-period continuation obstruction."""
from __future__ import annotations

from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_216_rotating_period_cone import run as cone_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-216-b053-rotating-period-cone-v1.json"
INPUTS = {
    "prior_direct_e_obstruction": (ROOT / "artifacts/cycle-215-b052-equation66-e-transport-v1.json", "900f167c92c68c292d846694f5f2afa280b26c30ea5e27cfd732f271e8f1efbe"),
    "preregistration": (ROOT / "docs/cycle-216-b053-rotating-period-cone-preregistration-v1.md", "6a8b17ec198a7b56ddb7200bc83e59d6df38c516617fea1e4af24273eb172a94"),
    "replay": (ROOT / "proof/verify_cycle_216_rotating_period_cone.py", "e5d386db16d3e2c17675bcd7c35e12b02760a2a357aac24d583f2914cfe39b76"),
    "regression_test": (ROOT / "tests/test_cycle_216_rotating_period_cone.py", "8a276c3c6ebbb7b2a06e6fae1100ec41ecb4a8ab798a873df7802bfba8e45535"),
    "prototype": (ROOT / "discovery/cycle-216-b053-rotating-period-cone-prototype-v1.json", "a3f65f26d1ff3a97b89b3c44a32b928aebbc8b2d14c402c1b94301afd194bc89"),
    "equation66_audit": (ROOT / "scripts/dimension_six_ss_evaluation_audit.py", "24c9258e46a1233c552017f3b58de0d45acd0197c8c807579f090ca1332f626f"),
    "prior_reflection_audit": (ROOT / "proof/verify_cycle_190_balanced_helical_reflection.py", "69da849d11c00ec30a5bca1a1220e1616d3d31beb75c8b906e8a67a9b0c98469"),
    "source_paper": (ROOT / "paper/sic-stark-dimension-six-boundary-fusion.tex", "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 216 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = cone_run()
    cone = result["rotating_cone_audit"]
    matrices = result["one_step_source_matrix_audit"]
    density = result["endpoint_density_audit"]
    packet = result["packet_boundary_audit"]
    require(cone["all_divisors_covered_symbolically"], "divisor-family scope drift")
    require(not cone["interior_pole_crossing"], "interior contour drift")
    require(cone["endpoint_u_one_corridor_width"] == "0 (one-sided limit)", "endpoint-width drift")
    require(density["limiting_m_zero_pole_trajectories_dense_on_real_contour"], "endpoint-density drift")
    require(not matrices["one_step_factorization_reaches_M_E"], "source-matrix census drift")
    require(packet["all_label_t_defects"] == list(range(2, 13)), "packet-defect drift")
    return {
        "artifact_id": "cycle-216-b053-rotating-period-cone-v1",
        "cycle": 216,
        "budget_ordinal": "B053",
        "epistemic_status": "PROVED",
        "status": "SEALED_ROTATING_PERIOD_CONE_LITERAL_ENDPOINT_OBSTRUCTION",
        "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "The frozen upper-path moving contour controls all interior divisor families, but its literal endpoint collapses onto dense limiting pole trajectories; the audited one-step source transformations do not supply M_E or its cocycle."},
        "rotating_cone_audit": cone,
        "one_step_source_matrix_audit": matrices,
        "endpoint_density_audit": density,
        "packet_boundary_audit": packet,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "C216 proves full symbolic pole-cone separation on the frozen upper semicircle, collapse at u=1, density of an admissible m=0 limiting true-pole subfamily on the limiting real contour, and failure of the audited one-step S--S identities to reach M_E.",
            "recommendation": "Seal C216 as a scoped obstruction to this literal endpoint path and one-step transformation family, then open a new cycle; a different completion or multistep identity is a distinct method.",
            "known_flaw": "The result excludes neither another contour/distributional completion nor a multistep or new Gamma_M transformation carrying M to M_E with additional cocycle factors.",
            "falsifier": "Any full-divisor cone inequality, endpoint parametrization, true-pole admissibility, irrational-density argument, source-matrix census, branch convention, or replay discrepancy invalidates the seal.",
            "next_action": "Open a transformation-groupoid cycle: generate the full exact orbit of M under the cited S--S factorization/reflection/shift operations with cocycles tracked; either derive a word reaching M_E and test all 36 defects, or prove an invariant separating the complete generated orbit.",
            "adopted": True,
            "reason": "The specified path and one-step source family are now exactly contained, while the proposed groupoid state space is a distinct method rather than a post hoc contour alteration."
        },
        "preregistration_preflight": {"cycle": 216, "manifest_sha256": sha256(ROOT / "docs/cycle-216-b053-rotating-period-cone-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-216-b053-rotating-period-cone-preregistration-v1.md --expected-cycle 216 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_216_rotating_period_cone.py --output discovery/cycle-216-b053-rotating-period-cone-prototype-v1.json", "test_command": "python3 -m unittest tests/test_cycle_216_rotating_period_cone.py", "write_command": "python3 proof/build_cycle_216_rotating_period_cone_v1.py --write", "check_command": "python3 proof/build_cycle_216_rotating_period_cone_v1.py --check"},
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_216_rotating_period_cone_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
