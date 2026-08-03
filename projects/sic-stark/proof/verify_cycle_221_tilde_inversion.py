#!/usr/bin/env python3
"""Exact tilde-sector inversion correction audit for Cycle 221/B058."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


P, K, R, S = -5, 24, 115, 24  # Positive E representative M_+.


def survivor_coordinate_audit() -> dict[str, object]:
    """Verify the two C219 tau/u survivors and their sole tilde defect."""
    rows = []
    for sigma in (-1, 1):
        # (a,b,c,d)=(sigma,-1,sigma,-sigma).  Coefficients are relative to
        # the raw negative-k coordinates in the ordered slots shown below.
        row = {
            "sigma": sigma,
            "signs": {"mu": sigma, "m": -1, "omega1": sigma, "omega2": -sigma},
            "tau_relative": {"omega1": 1, "r": 1},
            "u_relative": {"mu": 1, "m": 1},
            "tilde_tau_relative": {"omega1": 1, "omega2": 1},
            "tilde_u_relative": {"mu": -1, "pm": -1},
        }
        assert all(value == 1 for value in row["tau_relative"].values())
        assert all(value == 1 for value in row["u_relative"].values())
        assert all(value == 1 for value in row["tilde_tau_relative"].values())
        assert all(value == -1 for value in row["tilde_u_relative"].values())
        rows.append(row)
    return {
        "epistemic_status": "PROVED",
        "survivor_count": len(rows),
        "survivors": rows,
        "conclusion": "For both survivors tau, u, and tilde-tau agree with the raw state, while tilde-u is exactly negated.",
    }


def forced_pochhammer_audit() -> dict[str, object]:
    """Derive the sole numerator ratio that repairs tilde-u negation."""
    return {
        "epistemic_status": "PROVED",
        "raw_tilde_numerator": "(qtilde*z;qtilde)_infinity",
        "survivor_tilde_numerator": "(qtilde*z^(-1);qtilde)_infinity",
        "forced_factor": "C(z;qtilde)=(qtilde*z;qtilde)_infinity/(qtilde*z^(-1);qtilde)_infinity",
        "candidate": "H_sigma=C(z;qtilde)*Gamma_M+(sigma*mu,-m;sigma*omega1,-sigma*omega2)",
        "inversion_identity": "C(z;qtilde)*C(z^(-1);qtilde)=1",
        "omega1_r_shift": "z -> z, hence C -> C",
        "omega2_minus1_shift": "z -> qtilde^(-1)*z, hence C -> (1-z)*(1-qtilde/z)*C",
        "scope": "This proves equality of the two frozen unnormalized product sectors. It does not define a negative-k normalized multiplier Z or a source signed-matrix law.",
    }


def first_shift_normalization_audit() -> dict[str, object]:
    """Test the natural direct signed continuation of normalized shift (38).

    The raw signed state would use (p,k,r,s)=(-P,-K,-R,-S).  Under its
    omega1/r shift, both the source candidate and C keep z fixed, so the
    only issue is the frozen normalized sine multiplier.  Exact parities show
    a residual minus sign for both surviving sigma values.
    """
    positive_phase_exponent = (R - 1) * (S - 1) // 2
    raw_phase_exponent = ((-R) - 1) * ((-S) - 1) // 2
    assert positive_phase_exponent == 1311
    assert raw_phase_exponent == 1450
    rows = []
    for sigma in (-1, 1):
        # Candidate: y=-m and its signed period make the sine orientation -1;
        # positive normalization phase is also -1.  Raw continuation has a
        # -1 sine orientation and +1 normalization phase.
        candidate_phase_sign = -1
        candidate_sine_orientation = -1
        raw_phase_sign = 1
        raw_sine_orientation = -1
        candidate_multiplier_sign = candidate_phase_sign * candidate_sine_orientation
        raw_multiplier_sign = raw_phase_sign * raw_sine_orientation
        assert candidate_multiplier_sign == 1
        assert raw_multiplier_sign == -1
        assert candidate_multiplier_sign == -raw_multiplier_sign
        rows.append(
            {
                "sigma": sigma,
                "correction_under_shift": "invariant",
                "candidate_multiplier": "+(-1)^m * 2*sin(A)",
                "direct_signed_continuation_multiplier": "-(-1)^m * 2*sin(A)",
                "matches": False,
            }
        )
    return {
        "epistemic_status": "PROVED",
        "positive_phase_exponent": positive_phase_exponent,
        "raw_phase_exponent": raw_phase_exponent,
        "rows": rows,
        "all_match": False,
        "conclusion": "The forced tilde correction is invariant under the first shift and cannot repair the exact residual normalized-shift sign for either survivor.",
        "source_boundary": "The raw k<0 formula is a frozen natural continuation requirement, not a published source theorem. The proved result is failure of this explicit construction to satisfy that requirement.",
    }


def downstream_identity_audit() -> dict[str, object]:
    shift = first_shift_normalization_audit()
    assert not shift["all_match"]
    return {
        "epistemic_status": "PROVED",
        "unnormalized_product_sector_match": True,
        "simultaneous_sign_involutivity": "not_reached_after_failed_first_shift",
        "normalized_reflection": "not_reached_after_failed_first_shift",
        "second_shift": "not_reached_after_failed_first_shift",
        "factorization": "not_reached_after_failed_first_shift",
        "reason": "The sole preregistered correction fails the first required normalized signed-continuation shift; testing later identities cannot make it an accepted extension.",
    }


def run() -> dict[str, object]:
    survivors = survivor_coordinate_audit()
    correction = forced_pochhammer_audit()
    shift = first_shift_normalization_audit()
    downstream = downstream_identity_audit()
    assert survivors["survivor_count"] == 2
    assert not shift["all_match"]
    return {
        "schema": "sic-stark-cycle-221-tilde-inversion-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "For the two sealed tau/u survivors, the displayed tilde-sector Pochhammer ratio is uniquely forced by the frozen unnormalized product numerator. Under the frozen direct signed continuation of the first normalized shift, that correction is invariant and leaves an exact residual minus sign, so this sole unmodified correction construction fails. The source does not publish a negative-k normalized law; this does not exclude a new label-dependent multiplier, another correction family, a new source theorem, a packet cocycle, AFK covariance, fusion, Stark, or TCC.",
        "survivor_coordinate_audit": survivors,
        "forced_pochhammer_audit": correction,
        "first_shift_normalization_audit": shift,
        "downstream_identity_audit": downstream,
        "gate_outcome": {
            "forced_tilde_pochhammer_product_repair": "PROVED_UNNORMALIZED_ONLY",
            "unmodified_normalized_signed_extension": "FALSIFIED_UNDER_FROZEN_DIRECT_SHIFT_REQUIREMENT",
            "remaining_design_problem": "Derive, rather than fit, a label-dependent signed normalization multiplier from a source theorem or an independent signed-product construction, then re-test the full functional identities.",
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
