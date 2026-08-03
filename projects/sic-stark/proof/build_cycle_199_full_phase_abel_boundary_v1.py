#!/usr/bin/env python3
"""Seal Cycle 199/B036's full-phase symmetric Abel-boundary obstruction."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_199_abel_character_comb import run as character_comb_run
from verify_cycle_199_abel_pole_geometry import run as pole_geometry_run
from verify_cycle_199_full_phase_abel_boundary import run as boundary_run
from verify_cycle_199_full_theta_carrier import run as carrier_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-199-b036-full-phase-abel-boundary-v1.json"
INPUTS = {
    "prior_endpoint_functional": (
        ROOT / "artifacts/cycle-198-b035-analytic-frequency-endpoint-v1.json",
        "78328f0e8df4ea566fea804cef79217ad1201ca028004d911b7f43871e8f9a3f",
    ),
    "prior_gaussian_falsifier": (
        ROOT / "artifacts/cycle-197-b034-gaussian-abel-tail-v1.json",
        "f18e2fdfad7f98551171cd9dc7b1d06dd0d4e76e13ee158a25e8009ab0ad198f",
    ),
    "prior_finite_anti_residue_sum": (
        ROOT / "artifacts/cycle-195-b032-finite-anti-residue-sum-v1.json",
        "7e4d7615414dbf49627c9ea9cfa2b5e0191502cd6a6915fa93d13085cd50ae8d",
    ),
    "prior_meromorphic_anti_channel": (
        ROOT / "artifacts/cycle-194-b031-meromorphic-anti-channel-v2.json",
        "c8eb1e91d496019ed52c8a9b2c48949a5b87a7e88b84857259f34b9a8d43d52d",
    ),
    "prior_helical_theta_amplitude": (
        ROOT / "artifacts/cycle-193-b030-helical-theta-amplitude-v1.json",
        "21cc93f3c924ecfe01abfd90b5da0371fab8d7923ee3da65a8fc3e844f4d8cca",
    ),
    "preregistration": (
        ROOT / "docs/cycle-199-b036-full-carrier-endpoint-descent-preregistration-v1.md",
        "046f9df355adb8deae5f0dd5cef3461da102a6c3431b6a1499d060161a025e1c",
    ),
    "full_theta_carrier_replay": (
        ROOT / "proof/verify_cycle_199_full_theta_carrier.py",
        "da80042d716df205b45f7b082d276da25f18508c92142a836b3fc7bfe552375f",
    ),
    "abel_character_comb_replay": (
        ROOT / "proof/verify_cycle_199_abel_character_comb.py",
        "b06e6493dac1ac4b3de5c7f5af9d19f0367947025c7774b6f049a8a6839ee07b",
    ),
    "abel_pole_geometry_replay": (
        ROOT / "proof/verify_cycle_199_abel_pole_geometry.py",
        "b92e7d3512b289fb411ecbd4ff65d5ed0c5af9c242f5223f44bd08c947555e3d",
    ),
    "full_phase_boundary_replay": (
        ROOT / "proof/verify_cycle_199_full_phase_abel_boundary.py",
        "2ee95df4cf6b418ac2ad8736c6171ddc983412c7dd82567b56526aa88f585f0d",
    ),
    "full_theta_carrier_test": (
        ROOT / "tests/test_cycle_199_full_theta_carrier.py",
        "1f0a7083cd603146267b7af82186c9a46c007b307f92e738ab9215d7cdd575cc",
    ),
    "abel_character_comb_test": (
        ROOT / "tests/test_cycle_199_abel_character_comb.py",
        "eaacb3b574bbeb36fc0d873513aea1b532f93cf5637e6dcfe9ef45db548eb1e3",
    ),
    "abel_pole_geometry_test": (
        ROOT / "tests/test_cycle_199_abel_pole_geometry.py",
        "ef92e5ed79ce30e350949c938c369b6bb1257df26886e445f5eebdb6296cc79d",
    ),
    "full_phase_boundary_test": (
        ROOT / "tests/test_cycle_199_full_phase_abel_boundary.py",
        "317d63e014a60496d7def05fd6a4481df508af1fb980a459417ba995f6a60e9b",
    ),
    "full_theta_carrier_prototype": (
        ROOT / "discovery/cycle-199-b036-full-theta-carrier-prototype-v1.json",
        "39847736d6440cf505dfbd9ece78ec07d11a6971f4608f4668d869a67b6740c2",
    ),
    "abel_character_comb_prototype": (
        ROOT / "discovery/cycle-199-b036-abel-character-comb-prototype-v1.json",
        "ddc7ab879f0bf13b4aaa8a0508daa0fd2bfc1c93044ee3fbedf59ec4b42b8b92",
    ),
    "abel_pole_geometry_prototype": (
        ROOT / "discovery/cycle-199-b036-abel-pole-geometry-prototype-v1.json",
        "abe651f635b0541f18acc704aceab8eca2612b55551f0ef87f753b36adb74bcc",
    ),
    "full_phase_boundary_prototype": (
        ROOT / "discovery/cycle-199-b036-full-phase-abel-boundary-prototype-v1.json",
        "7e79f2bd1604460e32a47641ea8d204e235ab1af6c9de3ab9d79cf8b4b2ca17d",
    ),
    "helical_zak": (
        ROOT / "scripts/dimension_six_helical_zak.py",
        "185f79ae0c3e5b560939a81551877cf0d14401100466793cc2d7fa4973061bf0",
    ),
    "alias_normalization": (
        ROOT / "scripts/dimension_six_alias_normalization.py",
        "b80fe677250136f1465679859f513bad7bccd49c8b72cc6e517a4fea300fe971",
    ),
    "two_base_lens": (
        ROOT / "scripts/dimension_six_two_base_lens.py",
        "72a4e0d9b577f661c89a84132f450c209f1f57a6131ba175b2a238f5bb197f79",
    ),
    "cycle157_fourier_audit": (
        ROOT / "scripts/dimension_six_cycle157_fourier_normalization_audit.py",
        "cd8387fcfc2de0c08fbd0a832f57343f2a4c204e838c265cf846b03919194deb",
    ),
    "cycle198_replay": (
        ROOT / "proof/verify_cycle_198_analytic_frequency_endpoint.py",
        "fd659f66af2d31dbe1e94d6956a22be211ce279cfb93253ee91e0fb2bebb169d",
    ),
    "d6_paper": (
        ROOT / "paper/sic-stark-dimension-six-boundary-fusion.tex",
        "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7",
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
    runtime = check_runtime("Cycle 199 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    carrier = carrier_run()
    comb = character_comb_run()
    poles = pole_geometry_run()
    boundary = boundary_run()

    require(carrier["full_block_action"]["dimension"] == 24, "carrier dimension drift")
    require(carrier["source_label_coverage"]["all_24_source_labels_covered"], "label coverage drift")
    require(carrier["anti_channel_retention"]["all_six_source_forced_coordinates_retained"], "anti retention drift")
    require(comb["endpoint_strip_and_poles"]["six_meromorphic_contour_pole_channels"] == [0, 4, 8, 12, 16, 20], "pole-channel drift")
    require(poles["abel_pole_pairs"]["pinching_channels"] == [0, 4, 8, 12, 16, 20], "geodesic pole drift")
    require(poles["nonpinching_channels"]["only_six_channels_pinch"], "nonpinching-channel drift")
    no_map = boundary["no_linear_all36_intertwiner"]
    require(no_map["impossible"], "all-36 obstruction drift")
    require(no_map["full_phase_abel_boundary_input_rank_at_most"] == 6, "boundary rank drift")
    require(no_map["C198_target_basis_dimension"] == 36, "C198 dimension drift")

    return {
        "artifact_id": "cycle-199-b036-full-phase-abel-boundary-v1",
        "cycle": 199,
        "budget_ordinal": "B036",
        "epistemic_status": "PROVED",
        "status": "SEALED_FULL_PHASE_SYMMETRIC_GEODESIC_ABEL_BOUNDARY_ALL36_INTERTWINER_FALSIFIED",
        "claim_boundary": boundary["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": (
                "For the declared full equation-(66)-phase, symmetric "
                "three-class Abel character comb with the A_6-geodesically "
                "fixed paired i0 boundary prescription, the six pinching "
                "channels give a delta-supported input of rank at most six. "
                "It cannot admit a linear all-36 intertwiner to C198's "
                "distinct T_6 basis."
            ),
        },
        "full_theta_carrier": carrier,
        "abel_character_comb": comb,
        "abel_pole_geometry": poles,
        "full_phase_boundary": boundary,
        "gate_outcome": {
            "full_phase_symmetric_geodesic_abel_comb": "FALSIFIED_FOR_ALL36_LINEAR_T6_INTERTWINER",
            "active_D6_interface": "SOURCE_ANALYTIC_FREQUENCY_ENDPOINT_FUNCTIONAL_ON_T6_SEALED_PERIODIZED_AMPLITUDE_OPEN",
            "remaining_design_problem": (
                "A different source-derived endpoint object must retain "
                "b-dependent off-support, derivative, or explicitly combined-"
                "residue data before any C198 comparison."
            ),
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "recommendation": (
                "Seal C199 as a scoped Abel-boundary obstruction; a "
                "derivative-jet regular-plus-residue construction is a distinct "
                "frozen method family and therefore a new cycle."
            ),
            "known_flaw": (
                "The completed boundary discards off-support regular terms and "
                "higher jets; the delta support and Abel orientation conventions "
                "must remain explicit."
            ),
            "falsifier": (
                "Any discrepancy in the pole pair, i0 orientation, residue, "
                "delta coefficient, b-independence, rank, C198 target census, "
                "or deterministic replay."
            ),
            "next_action": (
                "Preregister a source Laurent/Taylor regular-plus-residue jet, "
                "testing delta through delta^5 as the minimal rank-capable "
                "candidate and admitting channels only when forced by source "
                "expansion or covariance, without fitted coefficients."
            ),
            "adopted": True,
            "reason": (
                "The exact full-carrier, phase, pole, and distributional checks "
                "settle the declared Abel prescription while explicitly leaving "
                "the distinct regular-plus-residue design problem open."
            ),
        },
        "preregistration_preflight": {
            "cycle": 199,
            "manifest_sha256": sha256(ROOT / "docs/cycle-199-b036-full-carrier-endpoint-descent-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": (
                "research prereg check docs/cycle-199-b036-full-carrier-endpoint-descent-preregistration-v1.md "
                "--expected-cycle 199 --allow-head-drift"
            ),
            "prototype_commands": [
                "python3 proof/verify_cycle_199_full_theta_carrier.py --output discovery/cycle-199-b036-full-theta-carrier-prototype-v1.json",
                "python3 proof/verify_cycle_199_abel_character_comb.py --output discovery/cycle-199-b036-abel-character-comb-prototype-v1.json",
                "python3 proof/verify_cycle_199_abel_pole_geometry.py --output discovery/cycle-199-b036-abel-pole-geometry-prototype-v1.json",
                "python3 proof/verify_cycle_199_full_phase_abel_boundary.py --output discovery/cycle-199-b036-full-phase-abel-boundary-prototype-v1.json",
            ],
            "test_command": (
                "python3 -m unittest tests/test_cycle_199_full_theta_carrier.py "
                "tests/test_cycle_199_abel_character_comb.py "
                "tests/test_cycle_199_abel_pole_geometry.py "
                "tests/test_cycle_199_full_phase_abel_boundary.py"
            ),
            "write_command": "python3 proof/build_cycle_199_full_phase_abel_boundary_v1.py --write",
            "check_command": "python3 proof/build_cycle_199_full_phase_abel_boundary_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {
            "path": "proof/build_cycle_199_full_phase_abel_boundary_v1.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
