#!/usr/bin/env python3
"""Cycle 149: exact d=6 stabilizer and multiplier ledger.

The calculation is finite rational arithmetic.  It checks all 36
characteristics, including the exceptional zero characteristic, but does
not claim that the open analytic fusion-continuity lemma has been proved.
"""

from __future__ import annotations

from fractions import Fraction
import json


DIMENSION = 6
A6 = ((115, -24), (24, -5))
RADEMACHER = 6


def mod_one(value: Fraction) -> Fraction:
    return value - value.numerator // value.denominator


def theta_exponent(first: int, second: int) -> Fraction:
    """Exponent mod 1 of Kopp's characteristic theta multiplier."""

    a, b = A6[0]
    c, d = A6[1]
    r1 = Fraction(first, DIMENSION)
    r2 = Fraction(second, DIMENSION)
    value = Fraction(1, 2) * (
        (c - d + 1) * r1
        + (-a + b + 1) * r2
        - c * d * r1 * r1
        + 2 * (a - 1) * d * r1 * r2
        - (a - 2) * b * r2 * r2
    )
    return mod_one(value)


def form_value(first: int, second: int) -> int:
    return first * first - 5 * first * second + second * second


def afk_phase_exponent_mod_48(first: int, second: int) -> int:
    parity = DIMENSION + 7 * (1 + first) * (1 + second)
    # exp(-pi*i*Psi/12) contributes -2*Psi to the zeta_48
    # exponent; tau_6=zeta_48^28.
    return (
        24 * parity
        - 2 * RADEMACHER
        - 28 * form_value(first, second)
    ) % 48


def main() -> None:
    assert A6[0][0] * A6[1][1] - A6[0][1] * A6[1][0] == 1
    assert all(
        A6[row][column] % DIMENSION
        == (1 if row == column else 0)
        for row in range(2)
        for column in range(2)
    )

    # psi^2(A)=exp(pi*i*Psi(A)/6), hence psi^2(A6)=-1.
    psi_squared_exponent = mod_one(Fraction(RADEMACHER, 12))
    assert psi_squared_exponent == Fraction(1, 2)

    records = []
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            theta = theta_exponent(first, second)
            # psi^{-2} has the same exponent 1/2 because -1 is its own
            # inverse; chi_r^{-1} contributes -theta.
            kopp = mod_one(Fraction(1, 2) - theta)
            afk_square = mod_one(
                Fraction(
                    afk_phase_exponent_mod_48(first, second),
                    24,
                )
            )
            assert kopp == afk_square
            records.append(
                {
                    "characteristic": [first, second],
                    "A6_characteristic_mod_6": [first, second],
                    "theta_exponent_mod_1": str(theta),
                    "kopp_exponent_mod_1": str(kopp),
                    "afk_phase_square_exponent_mod_1": str(afk_square),
                    "match": True,
                }
            )

    result = {
        "schema": "sic-stark-dimension-six-stabilizer-ledger-v1",
        "A6": [list(row) for row in A6],
        "A6_mod_6": [[1, 0], [0, 1]],
        "all_36_characteristics_fixed": True,
        "rademacher_invariant": RADEMACHER,
        "psi_squared_A6": "-1",
        "psi_squared_exponent_mod_1": str(psi_squared_exponent),
        "records": records,
        "record_count": len(records),
        "all_multiplier_comparisons_match": all(
            record["match"] for record in records
        ),
        "two_representations": {
            "analytic": (
                "two-base S--S spectral packet with bases "
                "(exp(2*pi*i*tau), exp(2*pi*i*A6*tau))"
            ),
            "boundary": (
                "AFK/Kopp reciprocal-double-sine cocycle packet"
            ),
            "common_fixed_point": (
                "tau=beta6, A6*beta6=beta6, "
                "beta6+beta6^(-1)=5"
            ),
        },
        "conditional_closure": {
            "hypothesis": (
                "arithmetic fusion-continuity lemma of Cycle 148'"
            ),
            "finite_inputs": [
                "all 36 characteristic labels",
                "all 36 multiplier identities",
                "both formal TCC frequency bijections",
                "225 exact rank-two minor reductions",
                "trace normalization and endpoint -4*sqrt(7)",
            ],
            "conclusion": (
                "both 0 and 1 are shifts for the canonical d=6 tuple; "
                "GL2(Z) covariance transports them to every admissible "
                "dimension-six tuple"
            ),
            "status": "CONDITIONAL",
        },
        "circularity_audit": {
            "earlier_target": (
                "L'_S(0,chi_1)=r_0+zeta_6*r_1+zeta_6^2*r_2"
            ),
            "fusion_implies_earlier_target": True,
            "earlier_target_implies_pointwise_boundary_packet": True,
            "earlier_target_implies_full_flow_continuity": False,
            "reason": (
                "the oriented regulator equality, its conjugate, the "
                "proved quadratic component, C6 Fourier inversion, "
                "standard functional relations, and the multiplier "
                "ledger recover the complete endpoint packet; they do "
                "not prove existence or flow-invariant regularity of "
                "the two-base limit"
            ),
            "verdict": (
                "Grade-2 equivalent at the endpoint; Grade-3 family "
                "formulation has a strictly richer analytic attack "
                "surface"
            ),
        },
    }
    assert len(records) == 36
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
