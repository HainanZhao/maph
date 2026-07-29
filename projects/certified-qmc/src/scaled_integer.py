"""Scaled-integer form and proved CRT reconstruction bounds."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import prod
from typing import Sequence

from .exact_error import RuleSpec


def b2_numerator(residue: int, modulus: int) -> int:
    """Numerator of B2(r/N) over the fixed denominator 6*N^2."""

    r = residue % modulus
    return 6 * r * r - 6 * r * modulus + modulus * modulus


def b2_numerator_span(modulus: int) -> int:
    """Exact maximum difference between two B2 numerators."""

    if modulus < 2:
        raise ValueError("modulus must be at least 2")
    if modulus % 2 == 0:
        return 3 * modulus * modulus // 2
    return 3 * (modulus * modulus - 1) // 2


def factor_denominator(modulus: int, weight: Fraction) -> int:
    return 6 * weight.denominator * modulus * modulus


def factor_numerator(
    residue: int,
    modulus: int,
    weight: Fraction,
) -> int:
    """Integer F with 1+gamma*B2(r/N) = F/(6*b*N^2)."""

    return (
        6 * weight.denominator * modulus * modulus
        + weight.numerator * b2_numerator(residue, modulus)
    )


@dataclass(frozen=True)
class ScaledError:
    numerator: int
    denominator: int
    numerator_bound: int

    @property
    def value(self) -> Fraction:
        return Fraction(self.numerator, self.denominator)


def scaled_squared_error(
    modulus: int,
    generator: Sequence[int],
    weights: Sequence[Fraction | int | str],
) -> ScaledError:
    """Evaluate e^2 as E/D without intermediate rational arithmetic."""

    spec = RuleSpec.create(modulus, generator, weights)
    denominators = [
        factor_denominator(modulus, weight)
        for weight in spec.weights
    ]
    common_product = prod(denominators)
    summand_sum = 0
    for k in range(modulus):
        summand_sum += prod(
            factor_numerator(k * z, modulus, weight)
            for z, weight in zip(spec.generator, spec.weights)
        )
    numerator = summand_sum - modulus * common_product
    denominator = modulus * common_product
    bound = error_numerator_bound(modulus, spec.weights)
    if abs(numerator) > bound:
        raise ArithmeticError("scaled numerator exceeded its proved bound")
    return ScaledError(numerator, denominator, bound)


def error_numerator_bound(
    modulus: int,
    weights: Sequence[Fraction | int | str],
) -> int:
    """Prove |E| <= N*(prod M_j + prod C_j).

    Here C_j=6*b_j*N^2 and
    M_j=N^2*(6*b_j+a_j) bounds |F_j| for gamma_j=a_j/b_j >= 0.
    """

    spec = RuleSpec.create(modulus, [1] * len(weights), weights)
    c_values = [
        factor_denominator(modulus, weight)
        for weight in spec.weights
    ]
    m_values = [
        modulus * modulus * (6 * weight.denominator + weight.numerator)
        for weight in spec.weights
    ]
    return modulus * (prod(m_values) + prod(c_values))


def candidate_difference_integer(
    modulus: int,
    prefix: Sequence[int],
    weight_values: Sequence[Fraction | int | str],
    candidate_u: int,
    candidate_v: int,
) -> int:
    """Common-scaled score E(u)-E(v) for one CBC stage."""

    if len(weight_values) != len(prefix) + 1:
        raise ValueError("weights must contain prefix weights plus one")
    spec = RuleSpec.create(
        modulus,
        [*prefix, candidate_u],
        weight_values,
    )
    previous_weights = spec.weights[:-1]
    new_weight = spec.weights[-1]
    difference = 0
    for k in range(modulus):
        previous_product = prod(
            factor_numerator(k * z, modulus, weight)
            for z, weight in zip(spec.generator[:-1], previous_weights)
        )
        f_u = factor_numerator(k * candidate_u, modulus, new_weight)
        f_v = factor_numerator(k * candidate_v, modulus, new_weight)
        difference += previous_product * (f_u - f_v)
    bound = candidate_difference_bound(
        modulus,
        previous_weights,
        new_weight,
    )
    if abs(difference) > bound:
        raise ArithmeticError("candidate difference exceeded proved bound")
    return difference


def candidate_difference_bound(
    modulus: int,
    previous_weights: Sequence[Fraction | int | str],
    new_weight: Fraction | int | str,
) -> int:
    """Bound a common-scaled CBC score difference."""

    prefix_spec = RuleSpec.create(
        modulus,
        [1] * max(1, len(previous_weights)),
        list(previous_weights) if previous_weights else [0],
    )
    normalized_previous = (
        prefix_spec.weights if previous_weights else tuple()
    )
    weight = Fraction(new_weight)
    if weight < 0:
        raise ValueError("weights must be nonnegative")
    previous_bound = prod(
        modulus * modulus * (6 * w.denominator + w.numerator)
        for w in normalized_previous
    )
    return (
        modulus
        * previous_bound
        * weight.numerator
        * b2_numerator_span(modulus)
    )


def balanced_crt_bits(bound: int) -> int:
    """Minimum modulus-product bit length sufficient for |x| <= bound."""

    if bound < 0:
        raise ValueError("bound must be nonnegative")
    return (2 * bound + 1).bit_length()
