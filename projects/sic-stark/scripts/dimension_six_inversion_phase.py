#!/usr/bin/env python3
"""Exact AFK/Ishibashi inversion-phase match in dimension six.

Ishibashi's even-level cyclic quantum dilogarithm at N=24 has inversion
Gaussian

    gamma_24(h) = zeta_48^(h(h-24)).

The AFK phase for the canonical d=6 form Q(a,b)=a^2-5ab+b^2 is also a
48th root of unity.  With h=b-4a-1, their quotient is exactly a
nondegenerate level-six chirp:

    Phi_AFK(a,b) / gamma_24(h)
      = zeta_48^c_b * zeta_12^(a^2+kappa_b*a),

    kappa_b = b+4+6*(b mod 2)  (mod 12).

For odd b the chirp is antiperiodic on representatives a=0,...,5.
The AFK even-dimensional wrap is therefore not optional: it selects the
half-shifted Fourier sector.  In that sector every six-point Gauss
transform has squared modulus six, exactly.
"""

from __future__ import annotations

from collections import Counter
import json


DIMENSION = 6
LEVEL = 24
ROOT_ORDER = 48
CHIRP_ROOT_ORDER = 12
RADEMACHER = 6


def form_value(first: int, second: int) -> int:
    return first * first - 5 * first * second + second * second


def afk_phase_exponent(first: int, second: int) -> int:
    """Return e mod 48 with Phi_AFK=zeta_48^e."""

    parity_exponent = (
        DIMENSION
        + (1 + DIMENSION) * (1 + first) * (1 + second)
    )
    # exp(-pi*i*R/12)=zeta_48^(-2R), while
    # tau_6=-exp(pi*i/6)=zeta_48^28.
    return (
        24 * parity_exponent
        - 2 * RADEMACHER
        - 28 * form_value(first, second)
    ) % ROOT_ORDER


def characteristic_h(first: int, second: int) -> int:
    return (second - 4 * first - 1) % LEVEL


def inversion_gaussian_exponent(first: int, second: int) -> int:
    h = characteristic_h(first, second)
    return h * (h - LEVEL) % ROOT_ORDER


def chirp_linear_coefficient(second: int) -> int:
    return (
        second + 4 + 6 * (second % 2)
    ) % CHIRP_ROOT_ORDER


def polynomial_remainder_phi_12(coefficients: list[int]) -> list[int]:
    """Reduce an integer polynomial modulo Phi_12=x^4-x^2+1."""

    result = coefficients[:]
    for degree in range(len(result) - 1, 3, -1):
        coefficient = result[degree]
        if coefficient == 0:
            continue
        result[degree] -= coefficient
        result[degree - 2] += coefficient
        result[degree - 4] -= coefficient
    return result[:4]


def gauss_norm_certificate(second: int, frequency: int) -> dict[str, object]:
    """Certify |sum zeta_12^(a^2+kappa*a-(2k+eps)a)|^2=6."""

    kappa = chirp_linear_coefficient(second)
    parity_shift = second % 2
    exponents = [
        (
            first * first
            + kappa * first
            - (2 * frequency + parity_shift) * first
        )
        % CHIRP_ROOT_ORDER
        for first in range(DIMENSION)
    ]
    norm_counts = Counter(
        (left - right) % CHIRP_ROOT_ORDER
        for left in exponents
        for right in exponents
    )
    coefficients = [
        norm_counts[exponent] - (6 if exponent == 0 else 0)
        for exponent in range(CHIRP_ROOT_ORDER)
    ]
    remainder = polynomial_remainder_phi_12(coefficients)
    assert remainder == [0, 0, 0, 0]
    return {
        "frequency": frequency,
        "fourier_shift": (
            "integer" if parity_shift == 0 else "half_integer"
        ),
        "summand_exponents_mod_12": exponents,
        "norm_minus_six_phi12_remainder": remainder,
        "squared_modulus": 6,
    }


def main() -> None:
    columns = {}
    for second in range(DIMENSION):
        constant = (
            afk_phase_exponent(0, second)
            - inversion_gaussian_exponent(0, second)
        ) % ROOT_ORDER
        kappa = chirp_linear_coefficient(second)
        records = []
        for first in range(DIMENSION):
            phase = afk_phase_exponent(first, second)
            inversion = inversion_gaussian_exponent(first, second)
            predicted = (
                constant
                + 4 * (first * first + kappa * first)
            ) % ROOT_ORDER
            assert (phase - inversion) % ROOT_ORDER == predicted
            records.append(
                {
                    "a": first,
                    "h": characteristic_h(first, second),
                    "afk_phase_exponent_mod_48": phase,
                    "inversion_gaussian_exponent_mod_48": inversion,
                    "residual_exponent_mod_48": predicted,
                }
            )

        # Translation a -> a+6 changes the chirp by (-1)^kappa.
        # Since kappa has the parity of b, odd columns are precisely the
        # antiperiodic sector.
        wrap_sign = -1 if kappa % 2 else 1
        assert wrap_sign == (-1 if second % 2 else 1)

        gauss_records = [
            gauss_norm_certificate(second, frequency)
            for frequency in range(DIMENSION)
        ]
        assert {
            record["squared_modulus"]
            for record in gauss_records
        } == {DIMENSION}

        columns[str(second)] = {
            "constant_exponent_c_b_mod_48": constant,
            "kappa_b_mod_12": kappa,
            "wrap_sign": wrap_sign,
            "required_fourier_sector": (
                "integer" if second % 2 == 0 else "half_integer"
            ),
            "phase_records": records,
            "gauss_transform_records": gauss_records,
        }

    result = {
        "schema": "sic-stark-dimension-six-inversion-phase-v1",
        "root_convention": "zeta_48=exp(pi*i/24)",
        "afk_phase_formula": (
            "Phi_AFK=(-1)^(6+7(1+a)(1+b))*"
            "exp(-pi*i*6/12)*tau_6^(-Q(a,b))"
        ),
        "ishibashi_even_inversion_formula": (
            "gamma_24(h)=zeta_48^(h(h-24))"
        ),
        "characteristic_embedding": "h=b-4a-1 mod 24",
        "exact_quotient_formula": (
            "Phi_AFK/gamma_24="
            "zeta_48^c_b*zeta_12^(a^2+kappa_b*a)"
        ),
        "kappa_formula": "kappa_b=b+4+6*(b mod 2) mod 12",
        "columns": columns,
        "all_gauss_transforms_have_squared_modulus_six": True,
        "even_wrap_sign_is_the_fourier_sector_correction": True,
        "conclusion": (
            "The AFK phase supplies exactly the nondegenerate "
            "level-six quadratic chirp missing from the restriction of "
            "Ishibashi's level-24 inversion Gaussian.  Odd b is "
            "antiperiodic and is repaired by the half-shifted Fourier "
            "sector dictated by the even-dimensional wrap.  Thus the "
            "phase conventions are compatible with a unitary six-point "
            "metaplectic kernel; the remaining problem is the "
            "coefficient-dependent amplitude/operator identity."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
