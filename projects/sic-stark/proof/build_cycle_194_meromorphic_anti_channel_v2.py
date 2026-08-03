#!/usr/bin/env python3
"""Seal the immutable correction to Cycle 194/B031's residue-orbit claim."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-194-b031-meromorphic-anti-channel-v2.json"
INPUTS = {
    "superseded_v1_artifact": (
        ROOT / "artifacts/cycle-194-b031-meromorphic-anti-channel-v1.json",
        "1e9919680100963b23613e510abc99baf139bec626fce79ead572bc731dd3cb6",
    ),
    "original_preregistration": (
        ROOT / "docs/cycle-194-b031-meromorphic-anti-channel-preregistration-v1.md",
        "4249b01c5142ead9d676afca2f1c84f3b7c29689cbd56f7554278e4f6b272269",
    ),
    "correction_record": (
        ROOT / "docs/cycle-194-b031-meromorphic-anti-channel-correction-v2.md",
        "18bfc2bd5e4fe32dc6c202157695d818b3e835515240ecbb6bb7c87b3d09b837",
    ),
    "correction_replay": (
        ROOT / "proof/verify_cycle_194_meromorphic_anti_channel_v2.py",
        "35cec8cb8d888377b86836fa371d3a9dfae413db670291dd227c8586f14db8cf",
    ),
    "correction_test": (
        ROOT / "tests/test_cycle_194_meromorphic_anti_channel_v2.py",
        "ad34d48bdf43493f3f72cfc82a73194a145d3382e7a52519d626f131ebe2b560",
    ),
    "correction_prototype": (
        ROOT / "discovery/cycle-194-b031-meromorphic-anti-channel-correction-v2-prototype.json",
        "50ed5ab4da587fb7186cfe9893f389d9efe33a1088f343ed563ecdc7bbc4eada",
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
    runtime = check_runtime("Cycle 194 v2 correction seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads(
        (ROOT / "discovery/cycle-194-b031-meromorphic-anti-channel-correction-v2-prototype.json").read_text()
    )
    retained = result["retained_v1_results"]
    census = result["corrected_true_pole_census"]

    require(retained["forced_anti_fibre"]["all_six_anti_coordinates_source_forced"], "local anti fibre drift")
    require(retained["forced_anti_fibre"]["F24_preserves_A"], "anti Fourier stability drift")
    require(retained["spectral_anti_retention"]["all_six_odd_raw_differences_retained"], "spectral retention drift")
    require(census["orbit_cardinalities"] == [2, 4, 6, 8, 10, 12], "finite orbit census drift")
    require(census["total_true_pole_summands"] == 42, "true pole count drift")
    require(all(not record["infinite_true_pole_tail_exists"] for record in census["records"]), "infinite tail was not removed")
    require("OPEN" in census["combined_residue_status"], "combined-residue scope drift")

    return {
        "artifact_id": "cycle-194-b031-meromorphic-anti-channel-v2",
        "cycle": 194,
        "budget_ordinal": "B031",
        "epistemic_status": "CORRECTION",
        "status": "SEALED_CORRECTION_TRUE_POLE_ORBITS_FINITE",
        "claim_boundary": result["claim_boundary"],
        "supersedes": {
            "artifact": "cycle-194-b031-meromorphic-anti-channel-v1.json",
            "affected_claims": result["withdrawn_v1_claims"],
            "cause": "The v1 affine collision/recurrent-tail audit omitted the Sarkissian--Spiridonov true-pole inequality 24*n+5*j+m>=0.",
            "unaffected_claims": [
                "six source-forced local B_(1,-) anti-principal parts",
                "F_24 preservation of B_(1,-)",
                "retention of the six odd raw spectral differences",
            ],
        },
        "retained_results": retained,
        "corrected_true_pole_census": census,
        "gate_outcome": {
            "d6_interface": "SOURCE_FORCED_24D_ANTI_FIBRE_PROVED_FINITE_TRUE_POLE_COLLISION_SUM_REQUIRES_EXACT_COMBINATION",
            "resolved_class": "the local source two-gamma kernel's B_(1,-) principal-part complement and finite true-pole collision census",
            "remaining_bottleneck": "Derive an exact source-defined rule for the finite combined residues before testing any distributional or contour continuation to the real-multiplication endpoint.",
            "disallowed_pseudo_progress": [
                "calling affine divisor equality an infinite true-pole orbit",
                "calling the withdrawn tail estimate an endpoint continuation",
                "claiming finite combined-residue noncancellation without an exact sum",
                "identifying a raw or periodized channel with an AFK cocycle or completed alias value",
                "fitting a residue, transfer entry, or boundary counterterm",
                "using selected exponents, s, d, or ray labels",
                "claiming an RM boundary, fusion, Stark, or TCC consequence",
            ],
        },
        "next_target": result["next_unresolved_boundary"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "recommendation": "Issue an immutable Cycle 194 v2 correction immediately, superseding only the false infinite-tail/convergence/nonzero-sector claims while preserving the independently verified six local anti-principal parts and F_24 anti-fibre result; contain Cycle 195 meanwhile.",
            "known_flaw": "The recurrence tracked algebraic divisor collisions but omitted the source true-pole inequality; after substitution it permits only k<=N, so the asserted infinite residue tail does not exist.",
            "falsifier": "Any error in the source inequality, substitutions m=N-6z and (z,j,n)=(-3k,k,-k), or an exact surviving infinite admissible pole sequence.",
            "next_action": "Rebuild the collision verifier with every divisor inequality enforced, classify the resulting finite pole orbits, compute possible finite residue cancellation exactly, seal C194 v2, then re-preregister Cycle 195 from the corrected boundary.",
            "adopted": True,
            "reason": "The correction preserves the valid source-local result while withdrawing the exact unsupported infinite-tail promotion before any endpoint work proceeds.",
        },
        "frozen_hashes": frozen,
        "replay": {
            "prototype_command": "python3 proof/verify_cycle_194_meromorphic_anti_channel_v2.py --output discovery/cycle-194-b031-meromorphic-anti-channel-correction-v2-prototype.json",
            "test_command": "python3 -m unittest tests/test_cycle_194_meromorphic_anti_channel_v2.py tests/test_cycle_194_meromorphic_anti_channel.py",
            "write_command": "python3 proof/build_cycle_194_meromorphic_anti_channel_v2.py --write",
            "check_command": "python3 proof/build_cycle_194_meromorphic_anti_channel_v2.py --check",
        },
        "runtime": runtime,
        "sealer": {
            "path": "proof/build_cycle_194_meromorphic_anti_channel_v2.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
