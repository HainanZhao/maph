#!/usr/bin/env python3
"""Bailey product for the d=6 primitive helical alias packet.

At the real-multiplication fixed point,

    q=exp(2*pi*i*beta),  w=exp(2*pi*i/6),
    x=exp(2*pi*i*(alpha+N)/24).

The modularly transformed q-product argument differs from x by

    exp(2*pi*i*(19N-s)/4)=-1,

so

    Gamma_M(alpha,N)=(-q*x;q)_infinity/(x;q)_infinity.

The reflected factor has x_2=w/x.  Hence the k=0 alias term is

    T(x)=(-q*x,-q*w/x;q)_infinity/(x,w/x;q)_infinity.

If an additional *dual alias* weight (-1)^k were present, Bailey's
2-psi-2 summation would give an explicit product.  Multiplying by T(x)
would cancel four factors and leave the theta quotient recorded below.
AFK wrap holonomy does not provide this dual weight: it shifts the dual
lattice instead.  The computation is therefore a comparison formula
and a diagnostic for the one remaining sign, not a proof of the alias
sum.

The script also numerically checks the identity at a generic point
inside |q|<1.  The remaining proof gate is the modular boundary
evaluation of the simplified theta quotient at the quadratic fixed
point, not the bilateral summation itself.
"""

from __future__ import annotations

import cmath
import json


def q_pochhammer_infinite(
    parameter: complex,
    base: complex,
    terms: int = 300,
) -> complex:
    result = 1.0 + 0.0j
    power = 1.0 + 0.0j
    for _ in range(terms):
        result *= 1.0 - parameter * power
        power *= base
    return result


def bilateral_ratio(
    index: int,
    top: tuple[complex, complex],
    bottom: tuple[complex, complex],
    base: complex,
    argument: complex,
) -> complex:
    """Return t_(index+1)/t_index without forming large q^-n products."""

    return (
        argument
        * (1 - top[0] * base**index)
        * (1 - top[1] * base**index)
        / (
            (1 - bottom[0] * base**index)
            * (1 - bottom[1] * base**index)
        )
    )


def numerical_bailey_check() -> dict[str, float]:
    q = 0.17 * cmath.exp(0.37j)
    w = cmath.exp(2j * cmath.pi / 6)
    x = 0.61 * cmath.exp(0.23j)
    bailey_a = w**-1 * x**2
    top = (x, -w**-1 * x)
    bottom = (q * w**-1 * x, -q * x)
    argument = q

    bilateral = 1.0 + 0.0j
    term = 1.0 + 0.0j
    for index in range(0, 120):
        term *= bilateral_ratio(index, top, bottom, q, argument)
        bilateral += term
    term = 1.0 + 0.0j
    for index in range(-1, -121, -1):
        term /= bilateral_ratio(index, top, bottom, q, argument)
        bilateral += term
    numerator = q_pochhammer_infinite(
        bailey_a * q / (top[0] * top[1]),
        q,
    )
    for parameter in (
        bailey_a * q**2 / top[0] ** 2,
        bailey_a * q**2 / top[1] ** 2,
        q**2,
        bailey_a * q,
        q / bailey_a,
    ):
        numerator *= q_pochhammer_infinite(parameter, q**2)
    denominator = 1.0 + 0.0j
    for parameter in (
        bailey_a * q / top[0],
        bailey_a * q / top[1],
        q / top[0],
        q / top[1],
        -bailey_a * q / (top[0] * top[1]),
    ):
        denominator *= q_pochhammer_infinite(parameter, q)
    product = numerator / denominator
    return {
        "absolute_error": abs(bilateral - product),
        "relative_error": abs(bilateral - product) / abs(product),
    }


def main() -> None:
    # Work in Q(beta), beta^2=5 beta-1.  omega1=24 beta-5 and
    # omega1^{-1}=115-24 beta.
    # D=(omega1-1)/6=4 beta-1, hence
    # D*(omega1^{-1}-1)=-18.
    identity_records = {
        "omega1": "24*beta-5",
        "omega1_inverse": "115-24*beta",
        "D": "4*beta-1",
        "D_times_omega1_inverse_minus_one": "-18",
        "tilde_u_minus_u": "(19*N-s)/4",
        "orientation_root": "i^(19*N-s)=-1",
        "second_q_argument": "x2=w/x",
    }

    bailey_product = {
        "numerator_base_q": ["-q"],
        "numerator_base_q_squared": [
            "w^(-1)*q^2",
            "w*q^2",
            "q^2",
            "w^(-1)*x^2*q",
            "q*w*x^(-2)",
        ],
        "denominator_base_q": [
            "q*w^(-1)*x",
            "-q*x",
            "q/x",
            "-q*w/x",
            "q",
        ],
    }
    simplified_alias_packet = {
        "formula": (
            "(-q;q)_inf/(q;q)_inf * "
            "(w^(-1)q^2,wq^2,q^2;q^2)_inf * "
            "theta(w^(-1)x^2q;q^2) / "
            "(theta(x;q)*theta(w/x;q))"
        ),
        "theta_definition": "theta(z;q)=(z;q)_inf*(q/z;q)_inf",
        "cancelled_factors": [
            "-q*x",
            "-q*w/x",
            "x paired with q/x",
            "w/x paired with q*w^(-1)*x",
        ],
    }

    numerical = numerical_bailey_check()
    assert numerical["relative_error"] < 1e-12

    result = {
        "schema": "sic-stark-dimension-six-bailey-product-v1",
        "fixed_point_identities": identity_records,
        "initial_alias_term": (
            "T(x)=(-q*x,-q*w/x;q)_inf/(x,w/x;q)_inf"
        ),
        "Bailey_product": bailey_product,
        "simplified_alias_packet": simplified_alias_packet,
        "numerical_interior_check": numerical,
        "conditional_Bailey_comparison_proved": True,
        "required_extra_dual_alias_weight_present": False,
        "modular_boundary_evaluation_proved": False,
        "remaining_gate": (
            "Evaluate the actual well-poised 2-psi-2 alias packet at "
            "argument -q (or prove a further TCC gauge contributes the "
            "missing dual sign).  Only then apply fixed-point modular "
            "continuation and compare with the endpoint correction."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
