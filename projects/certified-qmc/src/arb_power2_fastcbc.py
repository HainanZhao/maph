"""Rigorous Arb shadow scores for power-of-two fast CBC.

The transform work is executed by FLINT/Arb through python-flint's
compiled ``acb.dft`` binding. Inputs are exact rational balls, and only
the real part of a rigorously enclosed cyclic correlation is consumed.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Sequence

from flint import acb, arb, ctx

from .power2_fastcbc import power2_candidate_classes
from .scaled_integer import factor_denominator, factor_numerator


def fraction_arb(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def kernel_factor_arb(
    residue: int,
    modulus: int,
    weight: Fraction,
) -> arb:
    return arb(factor_numerator(residue, modulus, weight)) / (
        factor_denominator(modulus, weight)
    )


def arb_plus_correlation(
    left: Sequence[arb], right: Sequence[arb]
) -> list[arb]:
    """Enclose c[a] = sum_j left[j] right[j+a] cyclically."""

    if len(left) != len(right) or not left:
        raise ValueError("correlation inputs must have equal positive length")
    length = len(left)
    if length & (length - 1):
        raise ValueError("correlation length must be a power of two")
    reversed_left = [left[-index % length] for index in range(length)]
    left_hat = acb.dft([acb(value) for value in reversed_left])
    right_hat = acb.dft([acb(value) for value in right])
    transformed = acb.dft(
        [
            left_value * right_value
            for left_value, right_value in zip(left_hat, right_hat)
        ],
        inverse=True,
    )
    result = []
    for value in transformed:
        if not value.imag.contains(0):
            raise ArithmeticError(
                "rigorous real correlation has nonzero imaginary enclosure"
            )
        result.append(+value.real)
    return result


def initial_running_product(modulus: int) -> list[arb]:
    if modulus < 8 or modulus & (modulus - 1):
        raise ValueError("modulus must be 2^m with m>=3")
    return [arb(1) for _ in range(modulus)]


def update_running_product(
    state: Sequence[arb],
    component: int,
    weight: Fraction,
) -> list[arb]:
    modulus = len(state)
    return [
        value
        * kernel_factor_arb(
            k * component % modulus, modulus, weight
        )
        for k, value in enumerate(state)
    ]


def arb_power2_candidate_scores(
    modulus: int,
    state: Sequence[arb],
    new_weight: Fraction,
    *,
    precision: int = 106,
) -> tuple[list[int], list[arb]]:
    """Enclose every sign-quotiented candidate score at one CBC stage."""

    if len(state) != modulus:
        raise ValueError("state length does not match modulus")
    if any(
        not state[k].overlaps(state[-k % modulus])
        for k in range(modulus)
    ):
        raise ArithmeticError("running product lacks sign symmetry")
    exponent = modulus.bit_length() - 1
    candidates = power2_candidate_classes(modulus)
    full_length = len(candidates)

    with ctx.workprec(precision):
        zero = state[0] * kernel_factor_arb(
            0, modulus, new_weight
        )
        scores = [+zero for _ in range(full_length)]
        for valuation in range(exponent):
            unit_exponent = exponent - valuation
            unit_modulus = 2**unit_exponent
            scale = 2**valuation
            if unit_exponent <= 2:
                contribution = arb(0)
                for odd_part in range(1, unit_modulus, 2):
                    k = scale * odd_part
                    contribution += state[k] * kernel_factor_arb(
                        k, modulus, new_weight
                    )
                scores = [
                    score + contribution for score in scores
                ]
                continue

            cyclic_length = 2 ** (unit_exponent - 2)
            left = []
            right = []
            for index in range(cyclic_length):
                odd_part = pow(5, index, unit_modulus)
                k = scale * odd_part
                left.append(2 * state[k])
                right.append(
                    kernel_factor_arb(
                        k, modulus, new_weight
                    )
                )
            correlation = arb_plus_correlation(left, right)
            scores = [
                score + correlation[index % cyclic_length]
                for index, score in enumerate(scores)
            ]
        return candidates, [+score for score in scores]


def compare_arb_scores(left: arb, right: arb) -> int | None:
    """Return sign(left-right), or None when the balls overlap."""

    if left.upper() < right.lower():
        return -1
    if right.upper() < left.lower():
        return 1
    return None
