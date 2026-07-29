"""Executable forward-error bounds for the frozen direct CU:P2 producer.

This module mirrors LatNet Builder's unilevel, symmetric, product-weight
``CoordUniformCBC`` evaluation path.  A binary64 midpoint is carried beside an
Arb upper bound for its distance from the corresponding exact real value.
Local binary64 rounding errors are measured exactly from the two dyadic input
midpoints; input conversion and the transcendental P2 scaling are enclosed by
Arb.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import math
from typing import Iterable, MutableMapping, Sequence

from flint import arb, ctx


def _fraction_arb(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def _float_fraction(value: float) -> Fraction:
    if not math.isfinite(value):
        raise ArithmeticError("non-finite binary64 midpoint")
    return Fraction.from_float(value)


def _upper(value: arb) -> arb:
    return value.abs_upper()


@dataclass(frozen=True)
class FloatErrorBall:
    """Binary64 midpoint with an Arb-certified absolute error radius."""

    value: float
    radius: arb
    counts: MutableMapping[str, int]

    @classmethod
    def exact_fraction(
        cls,
        exact: Fraction | int,
        counts: MutableMapping[str, int],
        *,
        approximation: float | None = None,
        label: str = "input",
    ) -> "FloatErrorBall":
        exact_fraction = Fraction(exact)
        midpoint = float(exact_fraction) if approximation is None else approximation
        delta = abs(_float_fraction(midpoint) - exact_fraction)
        counts[label] = counts.get(label, 0) + 1
        return cls(midpoint, _upper(_fraction_arb(delta)), counts)

    @classmethod
    def exact_arb(
        cls,
        exact: arb,
        approximation: float,
        counts: MutableMapping[str, int],
        *,
        label: str,
    ) -> "FloatErrorBall":
        center = _fraction_arb(_float_fraction(approximation))
        counts[label] = counts.get(label, 0) + 1
        return cls(approximation, _upper(exact - center), counts)

    def _record(self, operation: str) -> None:
        self.counts[operation] = self.counts.get(operation, 0) + 1

    def add(self, other: "FloatErrorBall") -> "FloatErrorBall":
        self._record("add")
        value = self.value + other.value
        exact_center = _float_fraction(self.value) + _float_fraction(other.value)
        local = abs(_float_fraction(value) - exact_center)
        radius = _upper(self.radius + other.radius + _fraction_arb(local))
        return FloatErrorBall(value, radius, self.counts)

    def sub(self, other: "FloatErrorBall") -> "FloatErrorBall":
        self._record("sub")
        value = self.value - other.value
        exact_center = _float_fraction(self.value) - _float_fraction(other.value)
        local = abs(_float_fraction(value) - exact_center)
        radius = _upper(self.radius + other.radius + _fraction_arb(local))
        return FloatErrorBall(value, radius, self.counts)

    def mul(self, other: "FloatErrorBall") -> "FloatErrorBall":
        self._record("mul")
        left = _float_fraction(self.value)
        right = _float_fraction(other.value)
        value = self.value * other.value
        local = abs(_float_fraction(value) - left * right)
        propagated = (
            _fraction_arb(abs(left)) * other.radius
            + _fraction_arb(abs(right)) * self.radius
            + self.radius * other.radius
        )
        radius = _upper(propagated + _fraction_arb(local))
        return FloatErrorBall(value, radius, self.counts)

    def div_exact_integer(self, denominator: int) -> "FloatErrorBall":
        if denominator <= 0:
            raise ValueError("denominator must be positive")
        self._record("div")
        value = self.value / denominator
        center = _float_fraction(self.value)
        local = abs(_float_fraction(value) - center / denominator)
        radius = _upper(
            self.radius / denominator + _fraction_arb(local)
        )
        return FloatErrorBall(value, radius, self.counts)

    def contains(self, exact: arb) -> bool:
        center = _fraction_arb(_float_fraction(self.value))
        distance = _upper(exact - center)
        return bool(distance.upper() <= self.radius.lower())


def _coerce_weights(weights: Iterable[Fraction | int | str]) -> tuple[Fraction, ...]:
    return tuple(Fraction(weight) for weight in weights)


def _p2_kernel(
    modulus: int,
    counts: MutableMapping[str, int],
    scaling_hex: str,
) -> list[FloatErrorBall]:
    scaling = FloatErrorBall.exact_arb(
        2 * arb.pi() ** 2,
        float.fromhex(scaling_hex),
        counts,
        label="p2_scaling_input",
    )
    one = FloatErrorBall.exact_fraction(1, counts)
    one_sixth = FloatErrorBall.exact_fraction(
        Fraction(1, 6), counts, label="one_sixth_input"
    )
    output: list[FloatErrorBall] = []
    for index in range(modulus // 2 + 1):
        x = FloatErrorBall.exact_fraction(
            Fraction(index, modulus), counts, label="abscissa_input"
        )
        bernoulli = x.mul(x.sub(one)).add(one_sixth)
        output.append(scaling.mul(bernoulli))
    return output


def _folded_stride_index(index: int, generator: int, modulus: int) -> int:
    residue = (index * generator) % modulus
    return min(residue, modulus - residue)


def independent_p2_merit(
    modulus: int,
    generator: Sequence[int],
    weights: Sequence[Fraction | int | str],
) -> arb:
    """Independently enclose the mathematical CU:P2 product-weight merit."""

    rational_weights = _coerce_weights(weights)
    total = arb(0)
    scaling = 2 * arb.pi() ** 2
    for point in range(modulus):
        product = arb(1)
        for coordinate, weight in zip(generator, rational_weights):
            residue = (point * coordinate) % modulus
            x = Fraction(residue, modulus)
            bernoulli = x * x - x + Fraction(1, 6)
            product *= 1 + _fraction_arb(weight * bernoulli) * scaling
        total += product
    return total / modulus - 1


def p2_merit_polynomial(
    modulus: int,
    generator: Sequence[int],
    weights: Sequence[Fraction | int | str],
) -> tuple[Fraction, ...]:
    """Return exact coefficients in t for P2 merit with t = 2*pi^2."""

    rational_weights = _coerce_weights(weights)
    total = [Fraction(0) for _ in range(len(generator) + 1)]
    for point in range(modulus):
        product = [Fraction(1)]
        for coordinate, weight in zip(generator, rational_weights):
            residue = (point * coordinate) % modulus
            x = Fraction(residue, modulus)
            bernoulli = x * x - x + Fraction(1, 6)
            factor = weight * bernoulli
            expanded = [Fraction(0) for _ in range(len(product) + 1)]
            for degree, coefficient in enumerate(product):
                expanded[degree] += coefficient
                expanded[degree + 1] += coefficient * factor
            product = expanded
        for degree, coefficient in enumerate(product):
            total[degree] += coefficient
    total = [coefficient / modulus for coefficient in total]
    total[0] -= 1
    return tuple(total)


def _evaluate_p2_polynomial(coefficients: Sequence[Fraction]) -> arb:
    value = arb(0)
    scaling = 2 * arb.pi() ** 2
    for coefficient in reversed(coefficients):
        value = value * scaling + _fraction_arb(coefficient)
    return value


def direct_product_p2_bound(
    modulus: int,
    generator: Sequence[int],
    weights: Sequence[Fraction | int | str],
    *,
    scaling_hex: str = "0x1.3bd3cc9be45dep+4",
    precision: int = 256,
) -> dict[str, object]:
    """Replay direct LatNet evaluation and certify its absolute forward error."""

    if modulus <= 1 or modulus % 2:
        raise ValueError("the frozen direct model requires an even modulus")
    if len(generator) == 0 or len(generator) != len(weights):
        raise ValueError("generator and weights must have equal positive length")
    if any(math.gcd(int(value), modulus) != 1 for value in generator):
        raise ValueError("all generator coordinates must be units modulo N")

    old_precision = ctx.prec
    ctx.prec = precision
    try:
        rational_weights = _coerce_weights(weights)
        counts: dict[str, int] = {}
        kernel = _p2_kernel(modulus, counts, scaling_hex)
        one = FloatErrorBall.exact_fraction(1, counts)
        two = FloatErrorBall.exact_fraction(2, counts)
        zero = FloatErrorBall.exact_fraction(0, counts)
        state = [one for _ in kernel]
        base_merit = zero

        for generator_value, exact_weight in zip(generator, rational_weights):
            weight = FloatErrorBall.exact_fraction(
                exact_weight, counts, label="weight_input"
            )
            weighted_state = [weight.mul(value) for value in state]
            products = [
                weighted_state[index].mul(
                    kernel[
                        _folded_stride_index(
                            index, int(generator_value), modulus
                        )
                    ]
                )
                for index in range(len(kernel))
            ]
            compressed_sum = zero
            for value in products:
                compressed_sum = compressed_sum.add(value)
            compressed_sum = compressed_sum.mul(two)
            compressed_sum = compressed_sum.sub(products[0])
            compressed_sum = compressed_sum.sub(products[-1])
            candidate = compressed_sum.div_exact_integer(modulus).add(base_merit)
            base_merit = candidate

            state = [
                one.add(
                    weight.mul(
                        kernel[
                            _folded_stride_index(
                                index, int(generator_value), modulus
                            )
                        ]
                    )
                ).mul(state[index])
                for index in range(len(kernel))
            ]

        exact = independent_p2_merit(modulus, generator, rational_weights)
        if not base_merit.contains(exact):
            raise ArithmeticError("propagated forward-error ball missed Arb target")
        center = _fraction_arb(_float_fraction(base_merit.value))
        observed_distance = _upper(exact - center)
        return {
            "float_value": base_merit.value,
            "float_hex": base_merit.value.hex(),
            "forward_error_bound": base_merit.radius.str(40),
            "observed_error_enclosure": observed_distance.str(40),
            "exact_merit_enclosure": exact.str(40),
            "contains_independent_arb_target": True,
            "precision_bits": precision,
            "operation_counts": dict(sorted(counts.items())),
            "model": "LatNet direct symmetric unilevel CoordUniformCBC CU:P2",
            "scaling_hex": scaling_hex,
        }
    finally:
        ctx.prec = old_precision


def certify_p2_cbc_branches(
    modulus: int,
    generator: Sequence[int],
    weights: Sequence[Fraction | int | str],
    *,
    precision: int = 256,
) -> dict[str, object]:
    """Certify a supplied power-of-two CBC vector by direct Arb enumeration."""

    if modulus <= 2 or modulus & (modulus - 1):
        raise ValueError("branch certification requires a power-of-two modulus")
    if len(generator) == 0 or len(generator) != len(weights):
        raise ValueError("generator and weights must have equal positive length")
    if generator[0] != 1:
        raise ValueError("the frozen CBC convention forces z_1=1")
    if any(math.gcd(int(value), modulus) != 1 for value in generator):
        raise ValueError("all generator coordinates must be units")

    rational_weights = _coerce_weights(weights)
    candidates = tuple(range(1, modulus // 2, 2))
    old_precision = ctx.prec
    ctx.prec = precision
    try:
        stages = []
        for stage in range(1, len(generator)):
            selected = min(
                int(generator[stage]) % modulus,
                (-int(generator[stage])) % modulus,
            )
            if selected not in candidates:
                raise ValueError("selected component is outside sign quotient")
            selected_polynomial = p2_merit_polynomial(
                modulus,
                [*generator[:stage], selected],
                rational_weights[: stage + 1],
            )
            selected_merit = _evaluate_p2_polynomial(selected_polynomial)
            gaps = []
            exact_ties = []
            all_nonnegative = True
            for candidate in candidates:
                if candidate == selected:
                    continue
                polynomial = p2_merit_polynomial(
                    modulus,
                    [*generator[:stage], candidate],
                    rational_weights[: stage + 1],
                )
                difference = tuple(
                    right - left
                    for left, right in zip(selected_polynomial, polynomial)
                )
                if all(coefficient == 0 for coefficient in difference):
                    exact_ties.append(candidate)
                    continue
                gap = _evaluate_p2_polynomial(difference)
                if not bool(gap.lower() > 0):
                    all_nonnegative = False
                gaps.append(gap)
            minimum_gap = min(gap.lower() for gap in gaps) if gaps else arb(0)
            stages.append(
                {
                    "stage_dimension": stage + 1,
                    "selected_component": selected,
                    "candidate_count": len(candidates),
                    "selected_merit_enclosure": selected_merit.str(40),
                    "minimum_nontied_competitor_gap_lower": minimum_gap.str(40),
                    "exact_tied_competitors": exact_ties,
                    "all_competitors_nonnegative_or_exact_ties": all_nonnegative,
                }
            )
        return {
            "precision_bits": precision,
            "candidate_convention": "odd units modulo N quotiented by z~-z",
            "stages": stages,
            "all_branches_certified": all(
                stage["all_competitors_nonnegative_or_exact_ties"]
                for stage in stages
            ),
        }
    finally:
        ctx.prec = old_precision
