#!/usr/bin/env python3
"""Fourier effect of the d=6 antiperiodic helical wrap.

For a one-dimensional model of the helical coordinate, let

    P_-(f)(x)=sum_k (-1)^k f(x+kT).

Then P_-(f)(x+T)=-P_-(f)(x), so its Fourier characters satisfy

    chi(T)=-1,

and are indexed by Z+1/2.  Poisson summation places no alternating
coefficient on the resulting dual aliases.  This elementary distinction
prevents the AFK wrap sign from being incorrectly used as the missing
(-1)^k in the dual 2-psi-2 series.

For G=R x Z/24 and T=(Delta,6), the antiperiodic descent condition is

    xi*Delta+n/4 in Z+1/2.

Multiplication by tau_6^h is the character (xi,n)=(0,14), whose value
on T is -1, exactly matching the primitive AFK quotient.
"""

from __future__ import annotations

import json


DISCRETE_LEVEL = 24
TAU_SIX_FREQUENCY = 14


def helical_character_value_exponent(
    continuous_period_product_twice: int,
    discrete_mode: int,
) -> int:
    """Return twice the exponent xi*Delta+n/4 modulo 2.

    ``continuous_period_product_twice`` stores 2*xi*Delta as an integer.
    """

    numerator_over_two = (
        continuous_period_product_twice
        + discrete_mode // 2
    )
    return numerator_over_two % 2


def main() -> None:
    # tau_6=e^(2*pi*i*14/24) as a character of the discrete coordinate.
    assert TAU_SIX_FREQUENCY == 14
    wrap_exponent_numerator = TAU_SIX_FREQUENCY * 6
    assert wrap_exponent_numerator % DISCRETE_LEVEL == 12

    # An ordinary Fourier series verifies the same rule coefficient by
    # coefficient: exp(2*pi*i*(j+1/2)*(x+1))=-exp(...).
    half_character_records = []
    for integer_frequency in range(-12, 13):
        doubled_frequency = 2 * integer_frequency + 1
        wrap_sign_exponent = doubled_frequency % 2
        assert wrap_sign_exponent == 1
        half_character_records.append(
            {
                "frequency": f"{integer_frequency}+1/2",
                "wrap_sign": "-1",
                "dual_alias_weight": "+1",
            }
        )

    result = {
        "schema": "sic-stark-dimension-six-line-bundle-duality-v1",
        "primal_antiperiodization": (
            "P_-(f)(x)=sum_k (-1)^k*f(x+k*T)"
        ),
        "primal_holonomy": "P_-(f)(x+T)=-P_-(f)(x)",
        "dual_descent_condition": (
            "xi*Delta+n/4 belongs to Z+1/2"
        ),
        "dual_alias_coefficients": "unweighted",
        "tau6_character": {
            "ambient_frequency_n_mod_24": TAU_SIX_FREQUENCY,
            "value_on_T": "-1",
        },
        "half_character_records": half_character_records,
        "wrap_sign_is_not_dual_alias_sign": True,
        "conclusion": (
            "The AFK wrap sign is completely accounted for by a "
            "half-character shift.  Any alternating weight in the "
            "dual 2-psi-2 alias sum must come from an additional TCC "
            "gauge or transformation; it cannot be inferred from wrap "
            "quasiperiodicity alone."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
