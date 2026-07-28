#!/usr/bin/env python3
"""Fourier form of the specialized general-modular beta identity.

Specializing Sarkissian--Spiridonov's two-gamma identity to

    (p,k,r,s)=(-115,24,5,24),  g=Q, l=0

turns its left-hand side into the full Fourier transform on
R x Z/24 of

    K_Q(y,m)=Gamma_M(y,m) Gamma_M(Q-y,-m).

After extracting the y-independent phase, the characters are

    exp(2*pi*i*alpha*y/(24*omega1*omega2))
    * omega_24^(5*m*(N-2)).

Since multiplication by five is invertible modulo 24, N traverses every
discrete Fourier frequency.  The identity therefore supplies more than
one special integral: it supplies the complete continuous-discrete
Fourier transform of the exact primitive AFK kernel.

The formula is initially proved in a convergence chamber and reaches
g=Q and positive incommensurate periods by meromorphic continuation.
This script checks the arithmetic and the absence of a pole or zero in
the fixed scalar Gamma_M(Q,0).  It does not prove the finite Zak descent.
"""

from __future__ import annotations

import json
import math


P_PARAMETER = -115
K_PARAMETER = 24
R_PARAMETER = 5
S_PARAMETER = 24
DISCRETE_FREQUENCY_MULTIPLIER = 5


def discrete_frequency(dual_discrete: int) -> int:
    return (
        DISCRETE_FREQUENCY_MULTIPLIER
        * (dual_discrete - 2)
    ) % K_PARAMETER


def inverse_dual_label(frequency: int) -> int:
    inverse = pow(DISCRETE_FREQUENCY_MULTIPLIER, -1, K_PARAMETER)
    return (inverse * frequency + 2) % K_PARAMETER


def gamma_q_zero_divisor_audit() -> dict[str, object]:
    """Audit Gamma_M(Q,0) against the explicit pole and zero lattices."""

    # A pole would express positive Q=omega1+omega2 as a negative
    # combination from the pole lattice, which is impossible.
    pole_possible = False

    # A zero requires j+1=1 in the omega2 coefficient, hence j=0,
    # followed by p*(m+j+1)+k*n=1 in the omega1 coefficient.
    # At m=0 this is -115+24*n=1, with no integral solution.
    zero_numerator = 1 - P_PARAMETER
    zero_possible = zero_numerator % K_PARAMETER == 0
    assert zero_numerator == 116
    assert not zero_possible
    return {
        "pole_possible": pole_possible,
        "zero_equation": "-115+24*n=1",
        "zero_possible": zero_possible,
        "Gamma_M_Q_0_is_finite_nonzero": True,
    }


def main() -> None:
    bezout = (
        P_PARAMETER * R_PARAMETER
        + K_PARAMETER * S_PARAMETER
    )
    assert bezout == 1
    phase_coefficient = (
        P_PARAMETER - K_PARAMETER * (1 - S_PARAMETER)
    )
    assert phase_coefficient == 437
    assert phase_coefficient % K_PARAMETER == 5
    assert math.gcd(5, K_PARAMETER) == 1
    assert pow(5, -1, K_PARAMETER) == 5

    frequency_records = [
        {
            "N_mod_24": dual_discrete,
            "frequency_mod_24": discrete_frequency(dual_discrete),
        }
        for dual_discrete in range(K_PARAMETER)
    ]
    assert {
        record["frequency_mod_24"]
        for record in frequency_records
    } == set(range(K_PARAMETER))
    assert all(
        inverse_dual_label(discrete_frequency(dual_discrete))
        == dual_discrete
        for dual_discrete in range(K_PARAMETER)
    )

    result = {
        "schema": "sic-stark-dimension-six-beta-fourier-v1",
        "parameters": {
            "p": P_PARAMETER,
            "k": K_PARAMETER,
            "r": R_PARAMETER,
            "s": S_PARAMETER,
            "p_minus_k_times_one_minus_s": phase_coefficient,
        },
        "kernel": "K_Q(y,m)=Gamma_M(y,m)*Gamma_M(Q-y,-m)",
        "specialization": "g=Q,l=0",
        "fourier_character": (
            "exp(2*pi*i*alpha*y/(24*omega1*omega2))*"
            "omega_24^(5*m*(N-2))"
        ),
        "continuous_frequency": "alpha/(24*omega1*omega2)",
        "extracted_constant_phase": (
            "exp(-pi*i*alpha*Q/(24*omega1*omega2))"
        ),
        "transformed_value": (
            "24*Gamma_M(Q,0)*Gamma_M(alpha,N)*"
            "Gamma_M(-alpha,4-N)"
        ),
        "frequency_records": frequency_records,
        "all_discrete_frequencies_occur": True,
        "frequency_inverse": "N=5*frequency+2 mod 24",
        "fixed_scalar_divisor_audit": gamma_q_zero_divisor_audit(),
        "direct_convergence_at_g_equals_Q_claimed": False,
        "meromorphic_continuation_required": True,
        "finite_Zak_descent_proved": False,
        "conclusion": (
            "The published beta identity gives the complete Fourier "
            "transform of the exact d=6 primitive kernel on "
            "R x Z/24.  The remaining work is to apply a rigorously "
            "normalized Weil--Brezin/Zak periodization to the affine "
            "(Z/6)^2 sample lattice, including its endpoint correction."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
