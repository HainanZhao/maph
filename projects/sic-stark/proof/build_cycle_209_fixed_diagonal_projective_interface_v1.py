#!/usr/bin/env python3
"""Seal Cycle 209/B046's fixed-diagonal all-fibre interface no-go."""
from __future__ import annotations

from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_209_fixed_diagonal_projective_interface import run as interface_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-209-b046-fixed-diagonal-projective-interface-v1.json"
INPUTS = {
    "prior_diagonal_pullback_criterion": (
        ROOT / "artifacts/cycle-208-b045-polarized-minor-pairing-v1.json",
        "933fbf0b09a0d66953193590fbf800c704de2e67ba9960f1ad0e185f00734230",
    ),
    "prior_projective_packet": (
        ROOT / "artifacts/cycle-206-b043-projective-line-interface-v1.json",
        "a1ce1e2a0e0d9b42032dd984d9f7f7161f90e080bdf22d38650c097adfa90c8d",
    ),
    "prior_endpoint_functional": (
        ROOT / "artifacts/cycle-198-b035-analytic-frequency-endpoint-v1.json",
        "78328f0e8df4ea566fea804cef79217ad1201ca028004d911b7f43871e8f9a3f",
    ),
    "preregistration": (
        ROOT / "docs/cycle-209-b046-fixed-diagonal-projective-interface-preregistration-v1.md",
        "15bf453a72315917a9000d12cf3b44be002865d605b613357823ada10b819e17",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_209_fixed_diagonal_projective_interface.py",
        "9d9b7da35c04d010665701a98da4f8e554af3c410c24044cbb5971fd75d7e8cf",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_209_fixed_diagonal_projective_interface.py",
        "9c0c290664aa0795094578063da4c835c8c91eb44ec8ff0022453bccaa027654",
    ),
    "prototype": (
        ROOT / "discovery/cycle-209-b046-fixed-diagonal-projective-interface-prototype-v1.json",
        "0c9e656823c3a1ad5d9ac2145315c11e018fc3d828b1cfb84e04683c5a6c6b04",
    ),
    "cycle206_replay": (
        ROOT / "proof/verify_cycle_206_projective_line_interface.py",
        "8e7769231af66c146f3e5b187bea6b4fe23f9c00c3359f2a606110e98019145a",
    ),
    "cycle198_replay": (
        ROOT / "proof/verify_cycle_198_analytic_frequency_endpoint.py",
        "fd659f66af2d31dbe1e94d6956a22be211ce279cfb93253ee91e0fb2bebb169d",
    ),
    "preregistration_validator": (
        ROOT / "../../tools/preregistration_check.py",
        "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
    ),
    "scaffold": (
        ROOT / "proof/cycle_seal_v1.py",
        "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1",
    ),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 209 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = interface_run()
    source = result["source_ratio_audit"]
    target = result["target_nonvanishing_audit"]
    contradiction = result["fixed_diagonal_contradiction"]

    require(len(source["records"]) == 6, "source h-channel census drift")
    require(source["all_h_ratio"] == "t^4", "source ratio drift")
    require(source["unselected_source_domain"] == "h in Z/6Z and t>0 with t!=1", "source domain drift")
    require(target["target_coordinate_count"] == 36, "target coordinate census drift")
    require(target["all_target_coordinates_finite_nonzero"], "target nonvanishing drift")
    require(target["target_ratio_value"] == "NOT_EVALUATED", "target ratio scope drift")
    require(contradiction["contradiction"], "fixed-diagonal contradiction drift")
    require(
        contradiction["witnesses"] == [{"t": "2", "t_to_fourth": "16"}, {"t": "3", "t_to_fourth": "81"}],
        "admissible witness drift",
    )
    require(
        result["gate_outcome"]["fixed_diagonal_all_source_family_interface"] == "FALSIFIED",
        "gate outcome drift",
    )

    return {
        "artifact_id": "cycle-209-b046-fixed-diagonal-projective-interface-v1",
        "cycle": 209,
        "budget_ordinal": "B046",
        "epistemic_status": "PROVED",
        "status": "SEALED_FIXED_DIAGONAL_ALL_FIBRE_PROJECTIVE_INTERFACE_FALSIFIED",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": (
                "No fixed nonzero label-preserving diagonal map sends every "
                "admissible source packet fibre to the one fixed finite-nonzero "
                "C198 projective point. The contradiction is t^4=16=81 at the "
                "two admissible witnesses t=2,3."
            ),
        },
        "source_ratio_audit": source,
        "target_nonvanishing_audit": target,
        "fixed_diagonal_contradiction": contradiction,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": (
                "Corrected C209 proves nonconstant source projective variation "
                "on the admissible locus: P_(0,1)/P_(0,0)=t^4 gives 16 and 81 "
                "at t=2,3, incompatible with one fixed diagonal map to a fixed "
                "finite nonzero C198 projective point."
            ),
            "recommendation": "Seal the corrected fixed-diagonal/all-fibre no-go and open a new cycle; a t-dependent intertwiner is a distinct method family.",
            "known_flaw": "Uniform equality for every admissible t may be stronger than the bridge requires, and no target ratio or minor has been evaluated.",
            "falsifier": "Any admissible-domain, packet-ratio, h-independence, target nonvanishing, fixed-c, projective-ratio, t=2,3, preflight, or replay discrepancy invalidates the seal.",
            "next_action": "Derive the logarithmic projective connection forced by the packet exponents and test whether its canonical parallel transport is A6/multiplier-compatible and reaches the C198 target without selecting or fitting t.",
            "adopted": True,
            "reason": "The corrected witnesses are in the frozen source domain and give an exact contradiction while leaving every broader interface family outside the claim boundary.",
        },
        "preregistration_preflight": {
            "cycle": 209,
            "manifest_sha256": sha256(ROOT / "docs/cycle-209-b046-fixed-diagonal-projective-interface-preregistration-v1.md"),
            "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"},
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-209-b046-fixed-diagonal-projective-interface-preregistration-v1.md --expected-cycle 209 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_209_fixed_diagonal_projective_interface.py --output discovery/cycle-209-b046-fixed-diagonal-projective-interface-prototype-v1.json",
            "test_command": "python3 -m unittest tests/test_cycle_209_fixed_diagonal_projective_interface.py",
            "write_command": "python3 proof/build_cycle_209_fixed_diagonal_projective_interface_v1.py --write",
            "check_command": "python3 proof/build_cycle_209_fixed_diagonal_projective_interface_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_209_fixed_diagonal_projective_interface_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
