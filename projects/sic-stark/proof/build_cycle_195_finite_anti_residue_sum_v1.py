#!/usr/bin/env python3
"""Seal Cycle 195/B032's finite source anti-residue combination."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-195-b032-finite-anti-residue-sum-v1.json"
INPUTS = {
    "corrected_prior_artifact": (
        ROOT / "artifacts/cycle-194-b031-meromorphic-anti-channel-v2.json",
        "c8eb1e91d496019ed52c8a9b2c48949a5b87a7e88b84857259f34b9a8d43d52d",
    ),
    "preregistration": (
        ROOT / "docs/cycle-195-b032-finite-anti-residue-sum-preregistration-v1.md",
        "21c81f97950ede971ff9d7bf434951053abb11c506bb04408f279a1afa6d3c10",
    ),
    "corrected_prior_replay": (
        ROOT / "proof/verify_cycle_194_meromorphic_anti_channel_v2.py",
        "35cec8cb8d888377b86836fa371d3a9dfae413db670291dd227c8586f14db8cf",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_195_finite_anti_residue_sum.py",
        "df7ccb34c408ce29d453373ed8811c7fcca435e101827d660db534030ef36d2b",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_195_finite_anti_residue_sum.py",
        "9b6b6aae61a9fee98ee8686b561223c981f49b660877ffe545da345b8ecc0fb4",
    ),
    "prototype": (
        ROOT / "discovery/cycle-195-b032-finite-anti-residue-sum-prototype-v1.json",
        "d45f779bc6519b649ea5aab85415ef647280513f72b162bbab9ee463d2abb206",
    ),
    "beta_fourier": (
        ROOT / "scripts/dimension_six_beta_fourier.py",
        "d47242027af1851ea29b60b8e8c362f42fa5a1634fd0b375e39233b4d87f7a6e",
    ),
    "beta_kernel_match": (
        ROOT / "scripts/dimension_six_beta_kernel_match.py",
        "6210819200882c83ebaed4fc74c9cce220a0d09748a8343a8b02a609d1289e27",
    ),
    "two_base_ratio": (
        ROOT / "scripts/dimension_six_two_base_lens.py",
        "72a4e0d9b577f661c89a84132f450c209f1f57a6131ba175b2a238f5bb197f79",
    ),
    "d6_paper": (
        ROOT / "paper/sic-stark-dimension-six-boundary-fusion.tex",
        "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7",
    ),
    "scaffold": (
        ROOT / "proof/cycle_seal_v1.py",
        "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1",
    ),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 195 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads(
        (ROOT / "discovery/cycle-195-b032-finite-anti-residue-sum-prototype-v1.json").read_text()
    )
    corrected = result["corrected_input"]
    combined = result["finite_combined_residues"]

    require(corrected["orbit_cardinalities"] == [2, 4, 6, 8, 10, 12], "true-orbit census drift")
    require(corrected["total_true_pole_summands"] == 42, "true-pole total drift")
    require(combined["all_six_finite_combined_residues_meromorphically_nonzero"], "combined-residue result drift")
    require(combined["constant_coefficient_vector"] == [1] * 6, "constant coefficient drift")
    require(combined["maximum_q_adic_order"] == 66, "q-adic degree drift")
    require(all(not row["all_point_nonvanishing_claimed"] for row in combined["records"]), "all-point scope drift")
    require(all(not row["endpoint_continuation_claimed"] for row in combined["records"]), "endpoint scope drift")

    return {
        "artifact_id": "cycle-195-b032-finite-anti-residue-sum-v1",
        "cycle": 195,
        "budget_ordinal": "B032",
        "epistemic_status": "PROVED",
        "status": "SEALED_FINITE_ANTI_RESIDUE_SUMS_MEROMORPHICALLY_NONZERO",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": "For the corrected true-pole orbits at N=1,3,5,7,9,11, the published helical Gamma_M functional equations give source-normalized finite sums C_N. Every normalized non-base summand has q-adic order k(k+1)/2>0, so C_N/c_(N,0) has exact constant coefficient one. All six finite combined anti residues are therefore nonzero meromorphic germs away from their explicitly retained source divisor loci.",
        },
        "corrected_true_pole_input": corrected,
        "finite_combined_residues": combined,
        "gate_outcome": {
            "d6_interface": "SOURCE_FORCED_24D_FINITE_ANTI_RESIDUE_GERMS_PROVED_ENDPOINT_REGULAR_PART_CONTINUATION_REQUIRED",
            "resolved_class": "finite source true-pole collision sums under the corrected C194 range and published helical multiplier",
            "remaining_bottleneck": "Fix a source-derived contour or distributional path to the RM endpoint, decompose the periodized kernel into a controlled regular part plus these finite residue jumps, and prove endpoint preservation before any AFK identification.",
            "disallowed_pseudo_progress": [
                "calling formal meromorphic nonidentity pointwise nonvanishing",
                "calling finite source residue sums an infinite periodization or endpoint continuation",
                "using a fitted residue, counterterm, AFK map, selected exponent, s, d, or ray label",
                "identifying q and q_tilde off the real-multiplication boundary",
                "claiming an AFK identity, boundary value, fusion, Stark, or TCC consequence",
            ],
        },
        "next_target": result["next_unresolved_boundary"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "recommendation": "Seal B032/C195 as PROVED only for the six finite true-pole residue combinations and their nonzero meromorphic germs.",
            "known_flaw": "Formal q-adic constant term 1 proves non-identical vanishing only; it gives no pointwise nonvanishing, infinite periodization, endpoint continuation, or AFK/ray/fusion/TCC consequence.",
            "falsifier": "Any true-pole range, recurrence multiplier, q-adic increment, base-residue, 42-summand census, coefficient-ring, or deterministic replay discrepancy.",
            "next_action": "Open a new cycle freezing a contour path to the RM endpoint and decomposing the periodized kernel into a distributionally controlled regular part plus these finite residue jumps, with every pole crossing fixed in advance.",
            "adopted": True,
            "reason": "The replay meets the preregistered all-six finite-germ criterion while explicitly withholding every endpoint and AFK consequence.",
        },
        "preregistration_preflight": {
            "cycle": 195,
            "manifest_sha256": sha256(ROOT / "docs/cycle-195-b032-finite-anti-residue-sum-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-195-b032-finite-anti-residue-sum-preregistration-v1.md --expected-cycle 195 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_195_finite_anti_residue_sum.py --output discovery/cycle-195-b032-finite-anti-residue-sum-prototype-v1.json",
            "test_command": "python3 -m unittest tests/test_cycle_195_finite_anti_residue_sum.py tests/test_cycle_194_meromorphic_anti_channel_v2.py tests/test_cycle_194_meromorphic_anti_channel.py",
            "write_command": "python3 proof/build_cycle_195_finite_anti_residue_sum_v1.py --write",
            "check_command": "python3 proof/build_cycle_195_finite_anti_residue_sum_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {
            "path": "proof/build_cycle_195_finite_anti_residue_sum_v1.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
