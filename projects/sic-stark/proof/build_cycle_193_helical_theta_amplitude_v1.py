#!/usr/bin/env python3
"""Seal Cycle 193's continuous graded theta transport and scoped obstruction."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-193-b030-helical-theta-amplitude-v1.json"
INPUTS = {
    "prior_graded_closure": (
        ROOT / "artifacts/cycle-192-graded-fourier-polarization-v1.json",
        "467c81b4f6be30963ed252661218bab28376e5538b78d618bab68e12ee428573",
    ),
    "preregistration": (
        ROOT / "docs/cycle-193-b030-helical-theta-amplitude-preregistration-v1.md",
        "e8a992203440cf220bb26265d1500c01e3ac1ca71940770eccbe00af83a0b587",
    ),
    "replay": (
        ROOT / "proof/verify_cycle_193_helical_theta_amplitude.py",
        "26078ea8dc7a4b0a2735643fcd6e7e534281f7400d2de515d1da7df226a7d9aa",
    ),
    "regression_test": (
        ROOT / "tests/test_cycle_193_helical_theta_amplitude.py",
        "fc4f57b428dbd1e9ca69f6305c060dc0bb8dfde8ea6bef06a559899e61351787",
    ),
    "prototype": (
        ROOT / "discovery/cycle-193-b030-helical-theta-amplitude-prototype-v1.json",
        "d4d6d35c9470f155bef9b83297f1918b4c9907b9269fc37cdfde34a9e9915056",
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
    "line_bundle_duality": (
        ROOT / "scripts/dimension_six_line_bundle_duality.py",
        "c019c02b71de1ad12882b3f2683e9117085a8ea6c7bb0d8ca46a8a1fa9fbdb2c",
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
    runtime = check_runtime("Cycle 193 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads(
        (ROOT / "discovery/cycle-193-b030-helical-theta-amplitude-prototype-v1.json").read_text()
    )
    theta = result["continuous_theta_preservation"]
    projection = result["fibre_projection"]
    divisors = result["beta_divisor_separation"]
    coverage = result["all36_coverage"]
    obstruction = result["scoped_amplitude_obstruction"]

    require(theta["finite_fibre_dimension"] == 18, "theta fibre dimension drift")
    require(theta["F24_preserves_finite_fibre"], "F24 theta-fibre preservation drift")
    require(theta["continuous_discrete_transform_preserves_seed_fibre"], "continuous seed transport drift")
    require(theta["p1_boundary_twisted_three_shift_retained"], "p=1 twist drift")
    require("OPEN" in theta["kernel_domain_status"], "kernel-domain boundary drift")
    require(projection["odd_pair_count"] == 6, "odd pair count drift")
    require(
        projection["Pi_V_loses_odd_antisymmetric_subspace_dimension"] == 6,
        "odd polarization dimension drift",
    )
    require(divisors["all_twelve_N_vs_N_plus_12_pairs_distinct"], "divisor separation drift")
    require(len(divisors["pair_divisor_records"]) == 12, "divisor pair census drift")
    require(coverage["odd_characteristic_count"] == 18, "odd characteristic count drift")
    require(coverage["all_12_odd_labels_appear"], "odd label coverage drift")
    require(obstruction["affected_characteristics"] == 18, "obstruction coverage drift")

    return {
        "artifact_id": "cycle-193-b030-helical-theta-amplitude-v1",
        "cycle": 193,
        "budget_ordinal": "B030",
        "epistemic_status": "PROVED",
        "status": "SEALED_CONTINUOUS_GRADED_THETA_TRANSPORT_AND_IOTA_EQUIVARIANT_ODD_AMPLITUDE_OBSTRUCTION",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": "For Schwartz seeds in the source-derived 18-dimensional Z2-graded helical theta fibre, the full continuous-discrete Fourier transform has an exact Poincare/Poisson transport to dual theta distributions and preserves the sealed finite fibre without scalarizing the p=1 twist. Its V projection identifies six odd (N,N+12) pairs. The published beta amplitudes R_N and R_(N+12) have distinct divisors for every canonical pair, so no fixed fibrewise complex-linear iota-equivariant operation on that V-projected theta fibre can recover the individual odd raw beta amplitudes; this affects 18 of 36 characteristics.",
        },
        "continuous_theta_preservation": theta,
        "fibre_projection": projection,
        "beta_divisor_separation": divisors,
        "all36_coverage": coverage,
        "scoped_amplitude_obstruction": obstruction,
        "gate_outcome": {
            "d6_interface": "CONTINUOUS_SCHWARTZ_THETA_TRANSPORT_PROVED_V_FIBREWISE_IOTA_EQUIVARIANT_ODD_RAW_AMPLITUDE_RECOVERY_OBSTRUCTED_MEROMORPHIC_PERIODIZATION_OR_LARGER_FIBRE_REQUIRED",
            "resolved_class": "source-derived Schwartz-seed Poincare/Zak theta sections with the sealed V fibre and fixed fibrewise complex-linear iota-equivariant individual-raw-amplitude operations",
            "remaining_bottleneck": "Construct a source-defined renormalized meromorphic or distributional Poincare periodization of the beta kernel, including principal-part and residue channels, and test whether it restores the lost odd antisymmetric amplitudes without a fitted AFK map.",
            "disallowed_pseudo_progress": [
                "calling Schwartz-seed theta transport a meromorphic beta-kernel periodization",
                "calling raw R_N values AFK cocycle values or completed aliases",
                "adding B_(1,-) without a source-derived continuous construction",
                "breaking iota symmetry through fitted entries or row dependence",
                "discarding capital Gamma_M normalization or the AFK phase",
                "claiming an RM boundary, fusion, Stark, or TCC consequence",
            ],
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "A renormalized meromorphic/distributional helical Poincare periodization with explicitly frozen principal-part and residue channels may recover the odd antisymmetric raw beta amplitudes and supply a genuine source-to-AFK amplitude candidate; no such kernel-domain theorem or AFK identity is proved here.",
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "The replay establishes the exact Poincare/Poisson convention, F_24-invariant 18D fibre, six odd projection pairs, all twelve divisor separations, and all-36 parity coverage.",
            "recommendation": "Seal Cycle 193/B030 as PROVED for Schwartz-seed theta transport and the fixed fibrewise complex-linear iota-equivariant odd-amplitude obstruction.",
            "known_flaw": "The meromorphic beta kernel is outside the proved Schwartz domain; no convergent or distributionally continued Poincare sum, AFK amplitude theorem, alias identity, or boundary theorem is established.",
            "falsifier": "Any Poincare/Poisson convention error, F_24 invariance failure, incorrect odd-pair projection, missed pole-zero cancellation, divisor mismatch, coverage error, or replay discrepancy.",
            "next_action": "Preregister a renormalized meromorphic/distributional Poincare periodization with frozen principal-part and residue channels, then test whether those channels recover the lost odd antisymmetric amplitudes.",
            "adopted": True,
            "reason": "The result closes a substantive, source-derived continuous class while preserving its kernel-domain and AFK-boundary limitations explicitly.",
        },
        "preregistration_preflight": {
            "cycle": 193,
            "manifest_sha256": sha256(ROOT / "docs/cycle-193-b030-helical-theta-amplitude-preregistration-v1.md"),
            "validator": {
                "path": "../../tools/preregistration_check.py",
                "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359",
            },
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-193-b030-helical-theta-amplitude-preregistration-v1.md --expected-cycle 193 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_193_helical_theta_amplitude.py --output discovery/cycle-193-b030-helical-theta-amplitude-prototype-v1.json",
            "test_command": "python3 -m unittest tests/test_cycle_193_helical_theta_amplitude.py tests/test_dimension_six_beta_fourier.py tests/test_dimension_six_beta_kernel_match.py tests/test_dimension_six_helical_zak.py tests/test_dimension_six_line_bundle_duality.py tests/test_cycle_192_graded_fourier_polarization.py",
            "write_command": "python3 proof/build_cycle_193_helical_theta_amplitude_v1.py --write",
            "check_command": "python3 proof/build_cycle_193_helical_theta_amplitude_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {
            "path": "proof/build_cycle_193_helical_theta_amplitude_v1.py",
            "sha256": sha256(Path(__file__)),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
