#!/usr/bin/env python3
"""Seal Cycle 194's source-forced interior meromorphic anti-channel."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-194-b031-meromorphic-anti-channel-v1.json"
INPUTS = {
    "prior_theta_result": (
        ROOT / "artifacts/cycle-193-b030-helical-theta-amplitude-v1.json",
        "21cc93f3c924ecfe01abfd90b5da0371fab8d7923ee3da65a8fc3e844f4d8cca",
    ),
    "preregistration": (
        ROOT / "docs/cycle-194-b031-meromorphic-anti-channel-preregistration-v1.md",
        "4249b01c5142ead9d676afca2f1c84f3b7c29689cbd56f7554278e4f6b272269",
    ),
    "cycle_192_replay": (
        ROOT / "proof/verify_cycle_192_graded_fourier_polarization.py",
        "fa8b7e3a49a442b46be740aa58cf3ee49cc08f5f83fa76f75449f95ca712077b",
    ),
    "cycle_193_replay": (
        ROOT / "proof/verify_cycle_193_helical_theta_amplitude.py",
        "26078ea8dc7a4b0a2735643fcd6e7e534281f7400d2de515d1da7df226a7d9aa",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_194_meromorphic_anti_channel.py",
        "f743900a9bcbb83158e1244e1f6838888c2ea5c9a56e84c72f79dc09b7282f83",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_194_meromorphic_anti_channel.py",
        "701eb3ab018532e92b1e02286534c42f3851aa67fc7e936defef02c8e8c1c23a",
    ),
    "prototype": (
        ROOT / "discovery/cycle-194-b031-meromorphic-anti-channel-prototype-v1.json",
        "14d8a0f8fde92e0ed9ab051cfd83725648f4716814e4fe49a3af9f2ee2cf176c",
    ),
    "beta_fourier": (
        ROOT / "scripts/dimension_six_beta_fourier.py",
        "d47242027af1851ea29b60b8e8c362f42fa5a1634fd0b375e39233b4d87f7a6e",
    ),
    "beta_kernel_match": (
        ROOT / "scripts/dimension_six_beta_kernel_match.py",
        "6210819200882c83ebaed4fc74c9cce220a0d09748a8343a8b02a609d1289e27",
    ),
    "helical_zak": (
        ROOT / "scripts/dimension_six_helical_zak.py",
        "185f79ae0c3e5b560939a81551877cf0d14401100466793cc2d7fa4973061bf0",
    ),
    "interior_factorization": (
        ROOT / "scripts/dimension_six_interior_factorization_audit.py",
        "245a400d830560d981f7b19f8953a0241ac4402bbfbcb8289a5478feb2076964",
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
    runtime = check_runtime("Cycle 194 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads(
        (ROOT / "discovery/cycle-194-b031-meromorphic-anti-channel-prototype-v1.json").read_text()
    )
    forced = result["forced_anti_fibre"]
    retention = result["spectral_anti_retention"]
    collisions = result["primary_pole_collision_lattice"]
    recurrence = result["residue_orbit_recurrence"]
    tail = recurrence["tail_asymptotics"]
    interior = result["interior_periodization"]

    require(forced["dimension"] == 6, "anti-fibre dimension drift")
    require(forced["all_six_anti_coordinates_source_forced"], "source forcing drift")
    require(forced["F24_preserves_A"], "A Fourier preservation drift")
    require(retention["all_six_odd_raw_differences_retained"], "raw anti retention drift")
    require(collisions["finite_witness_count"] > 0, "collision witness drift")
    require(not interior["termwise_principal_parts_permitted_in_interior"], "termwise-residue boundary drift")
    require(interior["coincident_pole_residue_orbit_required"], "residue orbit requirement drift")
    require(interior["residue_ratio_status"].startswith("PROVED"), "residue ratio status drift")
    require(tail["residue_orbit_absolute_convergence"], "residue convergence drift")
    require("23/24" in tail["strict_chamber_log_certificate"], "strict chamber certificate drift")
    require(not tail["all_points_nonvanishing_claimed"], "nonvanishing scope drift")
    require("not identically zero" in tail["nonzero_interior_asymptotic_sector"], "sectorial nonzero drift")
    require(not interior["boundary_continuation_taken"], "endpoint boundary drift")

    return {
        "artifact_id": "cycle-194-b031-meromorphic-anti-channel-v1",
        "cycle": 194,
        "budget_ordinal": "B031",
        "epistemic_status": "PROVED",
        "status": "SEALED_SOURCE_FORCED_ANTI_FIBRE_AND_INTERIOR_RESIDUE_ORBIT",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": "The actual d=6 two-gamma beta kernel has a nonzero simple odd-antisymmetric principal part in each of the six canonical (N,N+12) pairs, forcing the Cycle-192 Fourier-stable A=B_(1,-) complement. The beta spectral projection retains all six R_N-R_(N+12) differences. Helical aliases have a coincident-pole orbit, so termwise residues are invalid; their exact H_+ recurrence instead has root decay |q|*|q_tilde|^(-1/24)<1 in the strict interior chamber |q|<|q_tilde|<1. The residue orbit converges absolutely and is not identically zero in an interior asymptotic sector.",
        },
        "forced_anti_fibre": forced,
        "spectral_anti_retention": retention,
        "primary_pole_collision_lattice": collisions,
        "residue_orbit_recurrence": recurrence,
        "interior_periodization": interior,
        "gate_outcome": {
            "d6_interface": "SOURCE_FORCED_24D_MEROMORPHIC_ANTI_CHANNEL_PROVED_STRICT_INTERIOR_RESIDUE_ORBIT_CONVERGENT_ENDPOINT_DISTRIBUTIONAL_OR_CONTOUR_CONTINUATION_REQUIRED",
            "resolved_class": "the source two-gamma kernel's B_(1,-) principal-part complement and its exact strict-interior helical residue-orbit periodization",
            "remaining_bottleneck": "Define a source-derived distributional or contour continuation of the completed 24D meromorphic channel to the real-multiplication endpoint, with frozen pole-crossing and residue-jump rules, then test preservation of the anti-channel before any AFK identification.",
            "disallowed_pseudo_progress": [
                "calling sectorial interior nonvanishing all-point nonvanishing",
                "calling strict-interior residue convergence endpoint continuation",
                "identifying a raw or periodized channel with an AFK cocycle or completed alias value",
                "fitting a residue, transfer entry, or boundary counterterm",
                "discarding capital Gamma_M normalization or AFK phase",
                "claiming a ray map, RM boundary, fusion, Stark, or TCC consequence",
            ],
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "The completed source-forced 24D meromorphic carrier may possess a distributional or contour-controlled continuation to the real-multiplication endpoint that preserves the anti-channel; no endpoint, AFK, ray, fusion, Stark, or TCC theorem is proved here.",
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "The reconciled replay verifies all six physical principal parts, A preservation, six spectral differences, the exact collision lattice, H_+ recurrence, strict-chamber logarithmic root decay, and sectorial non-cancellation boundary.",
            "recommendation": "Seal B031 as PROVED only for the source-forced anti-channel, exact interior residue-orbit convergence, and non-identically-zero interior asymptotic sector.",
            "known_flaw": "Sectorial interior nonvanishing gives neither all-point nonvanishing nor real-multiplication endpoint continuation, AFK identification, ray data, fusion, or TCC.",
            "falsifier": "Any divisor, F_24 projection, collision lattice, H_+ recurrence, logarithmic root-decay, sectorial no-cancellation, manifest-input, or deterministic replay discrepancy.",
            "next_action": "Preregister a distributional/contour continuation of the completed 24D meromorphic channel to the real-multiplication boundary, including pole-crossing and residue-jump rules before execution.",
            "adopted": True,
            "reason": "The exact construction resolves a source-forced interior channel while preserving the endpoint and AFK claim boundaries explicitly.",
            "manifest_amendment": "Added the exact source two-base alias-ratio executable and transitive Cycle-192 replay before the final preflight; no sealed artifact existed at the time.",
        },
        "preregistration_preflight": {
            "cycle": 194,
            "manifest_sha256": sha256(ROOT / "docs/cycle-194-b031-meromorphic-anti-channel-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-194-b031-meromorphic-anti-channel-preregistration-v1.md --expected-cycle 194 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_194_meromorphic_anti_channel.py --output discovery/cycle-194-b031-meromorphic-anti-channel-prototype-v1.json",
            "test_command": "python3 -m unittest tests/test_cycle_194_meromorphic_anti_channel.py tests/test_cycle_193_helical_theta_amplitude.py tests/test_dimension_six_beta_fourier.py tests/test_dimension_six_beta_kernel_match.py tests/test_dimension_six_helical_zak.py tests/test_cycle_192_graded_fourier_polarization.py",
            "write_command": "python3 proof/build_cycle_194_meromorphic_anti_channel_v1.py --write",
            "check_command": "python3 proof/build_cycle_194_meromorphic_anti_channel_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {
            "path": "proof/build_cycle_194_meromorphic_anti_channel_v1.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
