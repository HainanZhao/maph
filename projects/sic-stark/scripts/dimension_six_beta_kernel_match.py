#!/usr/bin/env python3
"""Exact match of the primitive d=6 quotient with the beta kernel.

For the canonical stabilizer the general modular gamma parameters are

    (p,k,r,s)=(-115,24,5,24),  pr+ks=1.

Writing Gamma_M for the normalized rarefied hyperbolic gamma and Z(m)
for its normalization multiplier, the primitive AFK quotient is

    gamma_M(mu,h) / gamma_M(mu,h+4)
      = Z(h+4)/Z(h) * Gamma_M(mu,h) Gamma_M(Q-mu,-h).

The last product is exactly the two-gamma convolution kernel in
Sarkissian--Spiridonov's degenerate beta integral, specialized to
g=Q and l=0.  The normalization quotient is not mysterious:

    Z(h+4)/Z(h) = tau_6^h,
    tau_6=-exp(pi*i/6).

This script certifies the integer and root-of-unity bookkeeping.  The
remaining theorem is a finite Zak descent of the published
continuous-discrete beta convolution to the affine 36-point grid.
"""

from __future__ import annotations

import json


P_PARAMETER = -115
K_PARAMETER = 24
R_PARAMETER = 5
S_PARAMETER = 24
DIMENSION = 6
ZETA_12_ORDER = 12
TAU_6_EXPONENT_MOD_12 = 7


def z_quadratic_exponent_numerator(discrete: int) -> int:
    """Numerator over 2k in the m-dependent exponential of Z(m)."""

    coefficient = (
        (1 - S_PARAMETER) * K_PARAMETER - P_PARAMETER
    )
    return coefficient * discrete * (discrete - R_PARAMETER + 1)


def z_ratio_exponent_mod_12(discrete: int) -> int:
    """Exponent e with Z(h+4)/Z(h)=zeta_12^e."""

    numerator_difference = (
        z_quadratic_exponent_numerator(discrete + 4)
        - z_quadratic_exponent_numerator(discrete)
    )
    # exp(pi*i*numerator/(2k)); with 2k=48 this is zeta_96^n.
    # The difference is divisible by 8, hence equals zeta_12^(n/8).
    assert numerator_difference % 8 == 0
    return (numerator_difference // 8) % ZETA_12_ORDER


def normalized_quasiperiod_sign(discrete: int) -> int:
    """Sign in Gamma(mu,m+24)=sign*Gamma(mu,m)."""

    coefficient = (
        (1 - S_PARAMETER) * K_PARAMETER - P_PARAMETER
    )
    exponent = (
        coefficient
        * (K_PARAMETER + 2 * discrete - R_PARAMETER + 1)
        // 2
    )
    return -1 if exponent % 2 else 1


def main() -> None:
    assert (
        P_PARAMETER * R_PARAMETER
        + K_PARAMETER * S_PARAMETER
        == 1
    )
    coefficient = (
        (1 - S_PARAMETER) * K_PARAMETER - P_PARAMETER
    )
    assert coefficient == -437

    ratio_records = []
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            h = (second - 4 * first - 1) % K_PARAMETER
            exponent = z_ratio_exponent_mod_12(h)
            expected = (TAU_6_EXPONENT_MOD_12 * h) % ZETA_12_ORDER
            assert exponent == expected
            ratio_records.append(
                {
                    "characteristic": [first, second],
                    "h": h,
                    "Z_ratio_exponent_mod_12": exponent,
                    "tau6_to_h_exponent_mod_12": expected,
                }
            )

    # Each normalized factor is only quasiperiodic in m, but the two
    # factors of K_Q(mu,m)=Gamma(mu,m)Gamma(Q-mu,-m) have the same sign.
    # Their product is therefore genuinely 24-periodic.
    periodicity_records = []
    for discrete in range(K_PARAMETER):
        first_sign = normalized_quasiperiod_sign(discrete)
        # Moving -m backward by 24 has the same sign as moving it forward;
        # signs are self-inverse.
        reflected_sign = normalized_quasiperiod_sign(-discrete - 24)
        assert first_sign == (-1 if discrete % 2 else 1)
        assert reflected_sign == first_sign
        assert first_sign * reflected_sign == 1
        periodicity_records.append(
            {
                "h": discrete,
                "first_factor_quasiperiod_sign": first_sign,
                "reflected_factor_quasiperiod_sign": reflected_sign,
                "kernel_period_sign": 1,
            }
        )

    result = {
        "schema": "sic-stark-dimension-six-beta-kernel-match-v1",
        "general_modular_parameters": {
            "p": P_PARAMETER,
            "k": K_PARAMETER,
            "r": R_PARAMETER,
            "s": S_PARAMETER,
            "bezout_identity": "p*r+k*s=1",
        },
        "primitive_quotient": (
            "gamma_M(mu,h)/gamma_M(mu,h+4)"
        ),
        "normalized_kernel_identity": (
            "gamma_M(mu,h)/gamma_M(mu,h+4)="
            "tau_6^h*Gamma_M(mu,h)*Gamma_M(Q-mu,-h)"
        ),
        "beta_kernel_specialization": {
            "published_kernel": (
                "Gamma_M(y,m)*Gamma_M(-y+g,l-m)"
            ),
            "specialization": "y=mu,m=h,g=Q,l=0",
            "exact_match": True,
        },
        "normalization_ratio_records": ratio_records,
        "kernel_periodicity_records": periodicity_records,
        "kernel_is_periodic_mod_24": True,
        "published_beta_identity_is_continuous_discrete": True,
        "finite_Zak_descent_proved": False,
        "remaining_lemma": (
            "Periodize the g=Q,l=0 beta convolution over the discrete "
            "helical period (omega_1-omega_2,6), take its six-by-six "
            "Zak transform, and prove that the resulting alias sum is "
            "AFK equation (1.49)."
        ),
        "conclusion": (
            "The coefficient-dependent amplitude is already the exact "
            "kernel of a published general-modular beta convolution; "
            "only its finite Zak descent remains.  Together with the "
            "certified AFK/Ishibashi chirp match, this reduces the "
            "dimension-six proof to one explicit harmonic-analysis "
            "lemma rather than a new Stark algebraicity theorem."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
