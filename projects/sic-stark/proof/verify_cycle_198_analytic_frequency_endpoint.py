#!/usr/bin/env python3
"""Exact Cycle 198 audit of the source analytic-frequency endpoint rule.

The published two-gamma transform is used only as a meromorphic identity.
This replay freezes its 36 endpoint characters, proves that they are distinct,
and checks that every prescribed right-hand-side Gamma_M factor avoids the
published true pole and zero divisors.  It never assigns the divergent raw
vertical integral an ordinary improper-integral value.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path


DIMENSION = 6
LEVEL = 24
P = -115
R = 5
SOURCE_PHASE = 437


def centered_mod_six(value: int) -> int:
    residue = value % DIMENSION
    return residue if residue <= 2 else residue - DIMENSION


def is_nonnegative_integer(value: Fraction) -> bool:
    return value.denominator == 1 and value >= 0


def true_divisor_audit(
    omega_coefficient: Fraction,
    constant_coefficient: Fraction,
    discrete: int,
) -> dict[str, object]:
    """Test mu=A*omega+B against the published true Gamma_M divisors."""

    m = discrete % LEVEL

    # A true pole has mu=-j*omega-L, with j,L nonnegative integers and
    # L=24*n+5*j+m.  The congruence is the surviving source condition.
    pole_j = -omega_coefficient
    pole_l = -constant_coefficient
    pole = False
    if is_nonnegative_integer(pole_j) and is_nonnegative_integer(pole_l):
        j = int(pole_j)
        ell = int(pole_l)
        pole = (ell - R * j - m) % LEVEL == 0

    # A true zero has mu=C*omega+(j+1), where C is a positive integer and
    # C=-115*(m+j+1)+24*n.
    zero_j = constant_coefficient - 1
    zero_c = omega_coefficient
    zero = False
    if is_nonnegative_integer(zero_j) and zero_c.denominator == 1 and zero_c > 0:
        j = int(zero_j)
        coefficient = int(zero_c)
        zero = (coefficient - P * (m + j + 1)) % LEVEL == 0

    return {
        "argument_in_Q_omega_basis": {
            "omega_coefficient": str(omega_coefficient),
            "constant_coefficient": str(constant_coefficient),
        },
        "m_mod_24": m,
        "true_pole": pole,
        "true_zero": zero,
        "finite_nonzero": not pole and not zero,
    }


def fixed_scalar_audit() -> dict[str, object]:
    result = true_divisor_audit(Fraction(1), Fraction(1), 0)
    assert result["finite_nonzero"]
    return {
        **result,
        "argument": "Q=omega+1",
        "source_zero_congruence": "1=-115+24*n has no integer solution",
    }


def characteristic_record(first: int, second: int) -> dict[str, object]:
    raw = 4 * second - 5 * first
    sigma = centered_mod_six(raw)
    assert (sigma - raw) % DIMENSION == 0
    helical_shift = (sigma - raw) // DIMENSION
    discrete = first + 2 - DIMENSION * helical_shift
    helical_integer = second - DIMENSION * helical_shift
    raw_beta_mode = 5 * (discrete - 2)
    assert raw + DIMENSION * helical_shift == sigma
    assert 4 * helical_integer - raw_beta_mode == sigma
    assert (-raw_beta_mode) % DIMENSION == first
    assert helical_integer % DIMENSION == second

    # D=(omega-1)/6 and alpha=D*sigma/3.
    alpha_omega = Fraction(sigma, 18)
    alpha_constant = -alpha_omega
    first_factor = true_divisor_audit(alpha_omega, alpha_constant, discrete)
    second_factor = true_divisor_audit(
        -alpha_omega,
        -alpha_constant,
        4 - discrete,
    )
    discrete_frequency = (SOURCE_PHASE * (discrete - 2)) % LEVEL
    assert discrete_frequency == (5 * (discrete - 2)) % LEVEL

    return {
        "characteristic": [first, second],
        "raw_frequency": raw,
        "centered_frequency_sigma": sigma,
        "helical_shift_z": helical_shift,
        "helical_integer_ell": helical_integer,
        "N": discrete,
        "N_mod_24": discrete % LEVEL,
        "raw_beta_discrete_mode": raw_beta_mode,
        "alpha": f"D*({sigma})/3" if sigma else "0",
        "alpha_in_Q_omega_basis": {
            "omega_coefficient": str(alpha_omega),
            "constant_coefficient": str(alpha_constant),
        },
        "discrete_character_frequency_mod_24": discrete_frequency,
        "finite_frequency_recovered": [
            (-raw_beta_mode) % DIMENSION,
            helical_integer % DIMENSION,
        ],
        "first_frequency_factor": first_factor,
        "second_frequency_factor": second_factor,
        "endpoint_value": (
            f"24*Gamma_M(Q,0)*Gamma_M(D*({sigma})/3,{discrete})*"
            f"Gamma_M(-D*({sigma})/3,{4-discrete})"
        ),
        "endpoint_value_finite_nonzero": (
            first_factor["finite_nonzero"] and second_factor["finite_nonzero"]
        ),
    }


def characteristic_ledger() -> dict[str, object]:
    records = [
        characteristic_record(first, second)
        for first in range(DIMENSION)
        for second in range(DIMENSION)
    ]
    labels = {
        (row["centered_frequency_sigma"], row["N_mod_24"])
        for row in records
    }
    character_labels = {
        (
            row["centered_frequency_sigma"],
            row["discrete_character_frequency_mod_24"],
        )
        for row in records
    }
    zero_rows = [row for row in records if row["centered_frequency_sigma"] == 0]
    assert len(records) == 36
    assert len(labels) == len(records)
    assert len(character_labels) == len(records)
    assert len(zero_rows) == 6
    assert all(row["endpoint_value_finite_nonzero"] for row in records)
    assert {
        row["N_mod_24"] for row in zero_rows
    } == {2, 6, 10, 14, 18, 22}
    return {
        "epistemic_status": "PROVED",
        "records": records,
        "row_count": len(records),
        "distinct_continuous_discrete_character_count": len(character_labels),
        "zero_frequency_count": len(zero_rows),
        "zero_frequency_N_mod_24": sorted(row["N_mod_24"] for row in zero_rows),
        "all_36_endpoint_values_finite_nonzero": True,
        "test_space_dimension": 36,
        "linear_independence_reason": (
            "Distinct sigma give distinct real exponential rates in lambda; "
            "at fixed sigma the six distinct Z/24 Fourier characters are "
            "linearly independent."
        ),
    }


def source_continuation() -> dict[str, object]:
    assert P * R + LEVEL * LEVEL == 1
    assert SOURCE_PHASE == P - LEVEL * (1 - LEVEL)
    return {
        "epistemic_status": "PROVED",
        "source": (
            "Sarkissian--Spiridonov, General modular quantum dilogarithm "
            "and beta integrals, arXiv:1910.11747v4, equation (66)"
        ),
        "checked_parameters": {
            "p": P,
            "k": LEVEL,
            "r": R,
            "s": LEVEL,
            "p_times_r_plus_k_times_s": P * R + LEVEL * LEVEL,
            "phase_coefficient": SOURCE_PHASE,
            "periods": "omega=55+12*sqrt(21)>0 and omega_2=1; ratio irrational",
            "specialization": "g=Q=omega+1, l=0",
        },
        "initial_definition": (
            "the equation-(66) transform in its published nonempty "
            "convergence chamber"
        ),
        "continuation": (
            "the same equation-(66) meromorphic identity in the source "
            "parameters, specialized only after continuation"
        ),
        "uniqueness": (
            "Two meromorphic continuations agreeing with the source transform "
            "on a nonempty open subset of the same connected parameter domain "
            "agree identically."
        ),
        "added_entire_or_distributional_term_allowed": False,
        "raw_endpoint_improper_integral_claimed": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    ledger = characteristic_ledger()
    scalar = fixed_scalar_audit()
    result = {
        "schema": "sic-stark-cycle-198-analytic-frequency-endpoint-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "The published equation-(66) meromorphic continuation defines a "
            "unique source-derived linear endpoint transform on the frozen "
            "36-dimensional exponential-character space T_6. Every prescribed "
            "Gamma_M factor is finite and nonzero. This is not the divergent "
            "raw endpoint integral, a general hyperfunction construction, an "
            "AFK amplitude identity, a helical periodization, a ray map, fusion, "
            "Stark algebraicity, or TCC."
        ),
        "endpoint_parameters": {
            "beta": "(5+sqrt(21))/2",
            "omega": "55+12*sqrt(21)",
            "Q": "56+12*sqrt(21)",
            "D": "9+2*sqrt(21)",
            "central_contour_coordinate": "c=Q/2",
        },
        "source_continuation": source_continuation(),
        "fixed_Gamma_M_Q_0": scalar,
        "characteristic_ledger": ledger,
        "endpoint_functional": {
            "epistemic_status": "PROVED",
            "space": (
                "T_6=span_C{chi_ab:(a,b) in (Z/6Z)^2}, with coefficient "
                "l1 norm and the frozen continuous-discrete characters"
            ),
            "dimension": 36,
            "definition": (
                "L_src(chi_ab)=24*Gamma_M(Q,0)*Gamma_M(alpha_ab,N_ab)*"
                "Gamma_M(-alpha_ab,4-N_ab), extended linearly"
            ),
            "all_basis_values_finite_nonzero": True,
            "unique_under_frozen_source_rule": True,
            "ordinary_raw_contour_value": False,
        },
        "gate_outcome": {
            "analytic_frequency_endpoint": (
                "CLOSED_ON_FROZEN_T6_BY_SOURCE_MEROMORPHIC_CONTINUATION"
            ),
            "remaining_bottleneck": (
                "Prove that the source-derived endpoint functional survives "
                "the required helical/Zak periodization and matches the full "
                "capital-Gamma_M amplitude with the separately pinned AFK phase."
            ),
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
