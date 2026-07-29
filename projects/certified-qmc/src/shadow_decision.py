"""Reference three-level CBC comparison layer.

The double-double ball keeps an exact rational audit radius around its
binary64 pair.  This is deliberately a correctness reference for the
future compiled EFT/FMA radius, not the production-scale implementation.
Arb is imported lazily from the pinned python-flint dependency.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import isfinite
from typing import Sequence

from .exact_error import RuleSpec
from .scaled_integer import factor_denominator, factor_numerator


SPLITTER = 134217729.0


def two_sum(left: float, right: float) -> tuple[float, float]:
    total = left + right
    right_virtual = total - left
    error = (left - (total - right_virtual)) + (right - right_virtual)
    return total, error


def quick_two_sum(left: float, right: float) -> tuple[float, float]:
    total = left + right
    return total, right - (total - left)


def two_product(left: float, right: float) -> tuple[float, float]:
    product = left * right
    left_split = SPLITTER * left
    left_high = left_split - (left_split - left)
    left_low = left - left_high
    right_split = SPLITTER * right
    right_high = right_split - (right_split - right)
    right_low = right - right_high
    error = (
        ((left_high * right_high - product)
         + left_high * right_low)
        + left_low * right_high
    ) + left_low * right_low
    return product, error


@dataclass(frozen=True)
class DoubleDouble:
    high: float
    low: float = 0.0

    def exact_value(self) -> Fraction:
        return Fraction.from_float(self.high) + Fraction.from_float(self.low)

    def add(self, other: "DoubleDouble") -> "DoubleDouble":
        first, second = two_sum(self.high, other.high)
        third, fourth = two_sum(self.low, other.low)
        second += third
        first, second = quick_two_sum(first, second)
        second += fourth
        high, low = quick_two_sum(first, second)
        if not isfinite(high) or not isfinite(low):
            raise ArithmeticError("nonfinite double-double addition")
        return DoubleDouble(high, low)

    def multiply(self, other: "DoubleDouble") -> "DoubleDouble":
        first, second = two_product(self.high, other.high)
        second += self.high * other.low + self.low * other.high
        first, second = quick_two_sum(first, second)
        second += self.low * other.low
        high, low = quick_two_sum(first, second)
        if not isfinite(high) or not isfinite(low):
            raise ArithmeticError("nonfinite double-double multiplication")
        return DoubleDouble(high, low)


@dataclass(frozen=True)
class DoubleDoubleBall:
    midpoint: DoubleDouble
    radius: Fraction

    @classmethod
    def exact(cls, value: Fraction | int) -> "DoubleDoubleBall":
        exact = Fraction(value)
        high = float(exact)
        remainder = exact - Fraction.from_float(high)
        low = float(remainder)
        midpoint = DoubleDouble(high, low)
        radius = abs(exact - midpoint.exact_value())
        return cls(midpoint, radius)

    @property
    def lower(self) -> Fraction:
        return self.midpoint.exact_value() - self.radius

    @property
    def upper(self) -> Fraction:
        return self.midpoint.exact_value() + self.radius

    def contains(self, value: Fraction) -> bool:
        return self.lower <= value <= self.upper

    def add(self, other: "DoubleDoubleBall") -> "DoubleDoubleBall":
        midpoint = self.midpoint.add(other.midpoint)
        ideal = self.midpoint.exact_value() + other.midpoint.exact_value()
        rounding = abs(ideal - midpoint.exact_value())
        return DoubleDoubleBall(
            midpoint,
            self.radius + other.radius + rounding,
        )

    def multiply(self, other: "DoubleDoubleBall") -> "DoubleDoubleBall":
        left = self.midpoint.exact_value()
        right = other.midpoint.exact_value()
        midpoint = self.midpoint.multiply(other.midpoint)
        rounding = abs(left * right - midpoint.exact_value())
        radius = (
            abs(left) * other.radius
            + abs(right) * self.radius
            + self.radius * other.radius
            + rounding
        )
        return DoubleDoubleBall(midpoint, radius)


def _factor_fraction(
    residue: int,
    modulus: int,
    weight: Fraction,
) -> Fraction:
    return Fraction(
        factor_numerator(residue, modulus, weight),
        factor_denominator(modulus, weight),
    )


def candidate_score_fraction(
    modulus: int,
    prefix: Sequence[int],
    weights: Sequence[Fraction | int | str],
    candidate: int,
) -> Fraction:
    spec = RuleSpec.create(modulus, [*prefix, candidate], weights)
    total = Fraction(0)
    for k in range(modulus):
        term = Fraction(1)
        for component, weight in zip(spec.generator, spec.weights):
            term *= _factor_fraction(k * component, modulus, weight)
        total += term
    return total


def candidate_score_dd_ball(
    modulus: int,
    prefix: Sequence[int],
    weights: Sequence[Fraction | int | str],
    candidate: int,
) -> DoubleDoubleBall:
    spec = RuleSpec.create(modulus, [*prefix, candidate], weights)
    total = DoubleDoubleBall.exact(0)
    for k in range(modulus):
        term = DoubleDoubleBall.exact(1)
        for component, weight in zip(spec.generator, spec.weights):
            term = term.multiply(
                DoubleDoubleBall.exact(
                    _factor_fraction(k * component, modulus, weight)
                )
            )
        total = total.add(term)
    return total


def candidate_score_arb(
    modulus: int,
    prefix: Sequence[int],
    weights: Sequence[Fraction | int | str],
    candidate: int,
    *,
    precision: int = 128,
):
    import flint
    from flint import arb

    spec = RuleSpec.create(modulus, [*prefix, candidate], weights)
    with flint.ctx.workprec(precision):
        total = arb(0)
        for k in range(modulus):
            term = arb(1)
            for component, weight in zip(spec.generator, spec.weights):
                factor = _factor_fraction(
                    k * component, modulus, weight
                )
                term *= arb(factor.numerator) / factor.denominator
            total += term
        return +total


def compare_candidate_scores(
    modulus: int,
    prefix: Sequence[int],
    weights: Sequence[Fraction | int | str],
    candidate_left: int,
    candidate_right: int,
    *,
    arb_precision: int = 128,
) -> dict[str, object]:
    """Compare scores through DD ball, Arb ball, then exact rational."""

    left_dd = candidate_score_dd_ball(
        modulus, prefix, weights, candidate_left
    )
    right_dd = candidate_score_dd_ball(
        modulus, prefix, weights, candidate_right
    )
    if left_dd.upper < right_dd.lower:
        return {"comparison": -1, "resolved_by": "double-double"}
    if right_dd.upper < left_dd.lower:
        return {"comparison": 1, "resolved_by": "double-double"}

    import flint

    with flint.ctx.workprec(arb_precision):
        left_arb = candidate_score_arb(
            modulus,
            prefix,
            weights,
            candidate_left,
            precision=arb_precision,
        )
        right_arb = candidate_score_arb(
            modulus,
            prefix,
            weights,
            candidate_right,
            precision=arb_precision,
        )
        if left_arb.upper() < right_arb.lower():
            return {"comparison": -1, "resolved_by": "arb"}
        if right_arb.upper() < left_arb.lower():
            return {"comparison": 1, "resolved_by": "arb"}

    left_exact = candidate_score_fraction(
        modulus, prefix, weights, candidate_left
    )
    right_exact = candidate_score_fraction(
        modulus, prefix, weights, candidate_right
    )
    comparison = (left_exact > right_exact) - (left_exact < right_exact)
    return {
        "comparison": comparison,
        "resolved_by": "exact-crt-reference",
        "exact_equality": comparison == 0,
    }
