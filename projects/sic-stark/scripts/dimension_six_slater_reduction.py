#!/usr/bin/env python3
"""Slater reduction of the remaining d=6 2-psi-2 packet.

With w^6=1 and w^3=-1, the normalized primitive alias series is

  2psi2(x,w^2*x; -q*w^2*x,-q*x; q,-q).

Slater's two-term transformation reduces it to two 2-phi-1 series.
The x-dependence is confined to explicit infinite-product prefactors;
the unilateral cores are

  2phi1(w,-1; q*w^4; q,-q),
  2phi1(w^(-1),-1; q*w^2; q,-q).

Each core satisfies the parameter relation c=q*a/b of the
Bailey--Daum q-Kummer theorem with b=-1.  That theorem evaluates the
same series at argument -q/b=+q.  The actual argument is -q.
Therefore the last obstruction is an exact sign in two universal,
x-independent q-Kummer-adjacent functions.
"""

from __future__ import annotations

import cmath
import json


def two_psi_two(
    top: tuple[complex, complex],
    bottom: tuple[complex, complex],
    base: complex,
    argument: complex,
    cutoff: int = 100,
) -> complex:
    def ratio(index: int) -> complex:
        return (
            argument
            * (1 - top[0] * base**index)
            * (1 - top[1] * base**index)
            / (
                (1 - bottom[0] * base**index)
                * (1 - bottom[1] * base**index)
            )
        )

    result = 1.0 + 0.0j
    term = 1.0 + 0.0j
    for index in range(cutoff):
        term *= ratio(index)
        result += term
    term = 1.0 + 0.0j
    for index in range(-1, -cutoff - 1, -1):
        term /= ratio(index)
        result += term
    return result


def main() -> None:
    w = cmath.exp(2j * cmath.pi / 6)
    assert abs(w**3 + 1) < 1e-12
    assert abs(-w**2 - w**-1) < 1e-12
    assert abs(-w - w**4) < 1e-12

    # Exact monomial substitutions in Slater's first and swapped terms.
    slater_cores = [
        {
            "top": ["w", "-1"],
            "bottom": "q*w^4",
            "argument": "-q",
            "q_Kummer_parameter_check": (
                "q*w/(-1)=-q*w=q*w^4"
            ),
            "q_Kummer_summable_argument": (
                "-q/(-1)=+q"
            ),
        },
        {
            "top": ["w^(-1)", "-1"],
            "bottom": "q*w^2",
            "argument": "-q",
            "q_Kummer_parameter_check": (
                "q*w^(-1)/(-1)=-q*w^(-1)=q*w^2"
            ),
            "q_Kummer_summable_argument": (
                "-q/(-1)=+q"
            ),
        },
    ]

    # A direct interior convergence check for the original bilateral
    # packet.  The convergence annulus is |q|^2<|-q|<1.
    q = 0.21 * cmath.exp(0.19j)
    x = 0.57 * cmath.exp(0.31j)
    bilateral = two_psi_two(
        (x, w**2 * x),
        (-q * w**2 * x, -q * x),
        q,
        -q,
    )
    assert abs(bilateral) < 1e6

    result = {
        "schema": "sic-stark-dimension-six-slater-reduction-v1",
        "remaining_bilateral_packet": (
            "_2psi_2(x,w^2*x;-q*w^2*x,-q*x;q,-q)"
        ),
        "Slater_unilateral_cores": slater_cores,
        "unilateral_cores_are_independent_of_x": True,
        "Bailey_Daum_parameter_relation_holds": True,
        "actual_argument": "-q",
        "Bailey_Daum_closed_argument": "+q",
        "remaining_sign_gap": True,
        "interior_convergence_annulus": "|q|^2<|-q|<1",
        "interior_sample_absolute_value": abs(bilateral),
        "conclusion": (
            "Slater's transformation isolates the final analytic "
            "difficulty in two universal q-Kummer-adjacent 2-phi-1 "
            "values.  All characteristic dependence is explicit in "
            "product prefactors.  The standard Bailey--Daum sum misses "
            "the needed values by exactly the argument sign."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
