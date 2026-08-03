#!/usr/bin/env python3
"""Seal Cycle 215/B052's direct-E equation-(66) obstruction."""
from __future__ import annotations

from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_215_equation66_e_transport import run as transport_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-215-b052-equation66-e-transport-v1.json"
INPUTS = {
    "prior_formal_pairing_obstruction": (ROOT / "artifacts/cycle-213-b050-two-ended-completion-v1.json", "4ee1cbeea41b05f9ea402d57e25a85765a8d2cb4f1690a9c5c4273a980c3743b"),
    "prior_source_automorphy": (ROOT / "artifacts/cycle-214-b051-source-automorphy-end-exchange-v1.json", "4b0a693759824bd19d3b9f8e6c07343c1a442c43470fc2d7e698228265900563"),
    "preregistration": (ROOT / "docs/cycle-215-b052-equation66-e-transport-preregistration-v1.md", "0bbe01eefddb999e93f0884d292eade02c40fcb4dd1c5fea9a2312d538a04dd6"),
    "replay": (ROOT / "proof/verify_cycle_215_equation66_e_transport.py", "5507554d51c0b8edf77982d00eb0a4cc283f25b3f10d59904392be875a043ed0"),
    "regression_test": (ROOT / "tests/test_cycle_215_equation66_e_transport.py", "1bb381fe01d95a354f45abc23c9a9bc8b6cedd4c974e6bf5eb3aba41c32cd7d4"),
    "prototype": (ROOT / "discovery/cycle-215-b052-equation66-e-transport-prototype-v1.json", "b4dae7a5bfc1fb8622d690d52d9592820ed90722fe8959db3335f74d3207ccd3"),
    "cycle214_replay": (ROOT / "proof/verify_cycle_214_source_automorphy_end_exchange.py", "a22c53d5e7939687105ac0b5d4a4149a247a7b2769a77d69c888816f9edf2023"),
    "equation66_audit": (ROOT / "scripts/dimension_six_ss_evaluation_audit.py", "24c9258e46a1233c552017f3b58de0d45acd0197c8c807579f090ca1332f626f"),
    "source_packet": (ROOT / "proof/verify_cycle_206_projective_line_interface.py", "8e7769231af66c146f3e5b187bea6b4fe23f9c00c3359f2a606110e98019145a"),
    "prior_reflection_audit": (ROOT / "proof/verify_cycle_190_balanced_helical_reflection.py", "69da849d11c00ec30a5bca1a1220e1616d3d31beb75c8b906e8a67a9b0c98469"),
    "source_paper": (ROOT / "paper/sic-stark-dimension-six-boundary-fusion.tex", "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 215 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = transport_run()
    parameters = result["direct_parameter_audit"]
    packet = result["bare_packet_inversion_audit"]
    require(parameters["transformed_lens_parameters_p_k_r_s"] == [-5, 24, 115, 24], "lens-data drift")
    require(parameters["transformed_phase_coefficient"] == 547, "phase drift")
    require(not parameters["frozen_positive_period_hypothesis_for_E"], "positive-period scope drift")
    require(not packet["label_independent_kappa_h_possible"], "global-scalar obstruction drift")
    return {
        "artifact_id": "cycle-215-b052-equation66-e-transport-v1",
        "cycle": 215,
        "budget_ordinal": "B052",
        "epistemic_status": "PROVED",
        "status": "SEALED_DIRECT_E_EQUATION66_POSITIVE_PERIOD_AND_GLOBAL_SCALAR_OBSTRUCTION",
        "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "Direct E transport changes the frozen equation-(66) lens data and flips omega1's sign; the bare all-label t-inversion ansatz has no channel-global scalar cocycle."},
        "direct_parameter_audit": parameters,
        "bare_packet_inversion_audit": packet,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "C215 establishes failure of the frozen positive-period equation-(66) specialization and the bare channel-global conjugate-dual ansatz under E.",
            "recommendation": "Seal C215/B052 as PROVED only for failure of the frozen positive-period equation-(66) specialization and the bare channel-global conjugate-dual ansatz under E.",
            "known_flaw": "The obstruction excludes neither analytic continuation across omega1->-omega1 nor a source-derived label-dependent Gamma_M cocycle or changed-parameter transformation.",
            "falsifier": "Any canonicalization, Bezout/S--S parameter, phase-547, period-sign, packet-exponent, all-label census, kappa_h independence, or replay discrepancy invalidates the seal.",
            "next_action": "Open a new cycle freezing a path in period space from omega1 to -omega1, with divisor crossings and branch rules fixed, then derive the Gamma_M continuation cocycle and test whether it cancels the exact 12-a-b exponent defect without fitted label factors.",
            "adopted": True,
            "reason": "Both frozen direct constructions fail exactly, while the untested continuation mechanism has a different state space and theorem requirement."
        },
        "preregistration_preflight": {"cycle": 215, "manifest_sha256": sha256(ROOT / "docs/cycle-215-b052-equation66-e-transport-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-215-b052-equation66-e-transport-preregistration-v1.md --expected-cycle 215 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_215_equation66_e_transport.py --output discovery/cycle-215-b052-equation66-e-transport-prototype-v1.json", "test_command": "python3 -m unittest tests/test_cycle_215_equation66_e_transport.py", "write_command": "python3 proof/build_cycle_215_equation66_e_transport_v1.py --write", "check_command": "python3 proof/build_cycle_215_equation66_e_transport_v1.py --check"},
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_215_equation66_e_transport_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
