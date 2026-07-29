#!/usr/bin/env python3
"""Exact sign audit for the discriminant-eight d=7 AFK cocycle."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_FLOOR, getcontext
from fractions import Fraction


getcontext().prec = 80


@dataclass(frozen=True)
class Quadratic:
    """Exact a+b*alpha, where alpha=2+sqrt(2), alpha^2=4alpha-2."""

    rational: Fraction = Fraction(0)
    alpha: Fraction = Fraction(0)

    def __add__(self, other: object) -> Quadratic:
        value = coerce(other)
        return Quadratic(
            self.rational + value.rational,
            self.alpha + value.alpha,
        )

    __radd__ = __add__

    def __neg__(self) -> Quadratic:
        return Quadratic(-self.rational, -self.alpha)

    def __sub__(self, other: object) -> Quadratic:
        return self + (-coerce(other))

    def __rsub__(self, other: object) -> Quadratic:
        return coerce(other) - self

    def __mul__(self, other: object) -> Quadratic:
        value = coerce(other)
        return Quadratic(
            self.rational * value.rational
            - 2 * self.alpha * value.alpha,
            self.rational * value.alpha
            + self.alpha * value.rational
            + 4 * self.alpha * value.alpha,
        )

    __rmul__ = __mul__

    def inverse(self) -> Quadratic:
        norm = (
            self.rational**2
            + 4 * self.rational * self.alpha
            + 2 * self.alpha**2
        )
        if norm == 0:
            raise ZeroDivisionError
        return Quadratic(
            (self.rational + 4 * self.alpha) / norm,
            -self.alpha / norm,
        )

    def __truediv__(self, other: object) -> Quadratic:
        return self * coerce(other).inverse()

    def __rtruediv__(self, other: object) -> Quadratic:
        return coerce(other) * self.inverse()

    def __pow__(self, exponent: int) -> Quadratic:
        if exponent < 0:
            return self.inverse() ** (-exponent)
        result = Quadratic(Fraction(1))
        base = self
        while exponent:
            if exponent & 1:
                result *= base
            base *= base
            exponent //= 2
        return result

    def sign(self) -> int:
        constant = self.rational + 2 * self.alpha
        radical = self.alpha
        if radical == 0:
            return (constant > 0) - (constant < 0)
        if constant == 0:
            return (radical > 0) - (radical < 0)
        if constant > 0 and radical > 0:
            return 1
        if constant < 0 and radical < 0:
            return -1
        comparison = constant**2 - 2 * radical**2
        if constant > 0:
            return 1 if comparison > 0 else -1
        return -1 if comparison > 0 else 1

    def floor(self) -> int:
        alpha_decimal = Decimal(2) + Decimal(2).sqrt()
        approximation = (
            Decimal(self.rational.numerator)
            / Decimal(self.rational.denominator)
            + Decimal(self.alpha.numerator)
            / Decimal(self.alpha.denominator)
            * alpha_decimal
        )
        candidate = int(
            approximation.to_integral_value(rounding=ROUND_FLOOR)
        )
        if (self - candidate).sign() < 0:
            raise AssertionError("lower floor inequality failed")
        if (self - candidate - 1).sign() >= 0:
            raise AssertionError("upper floor inequality failed")
        return candidate


def coerce(value: object) -> Quadratic:
    if isinstance(value, Quadratic):
        return value
    if isinstance(value, (int, Fraction)):
        return Quadratic(Fraction(value))
    return NotImplemented


ALPHA = Quadratic(Fraction(0), Fraction(1))
DIMENSION = 7
AT = ((239, -140), (70, -41))
WORD = (4, 2, 4, 2, 4, 2, 0)


def linear_factor_phase(argument: Quadratic) -> Quadratic:
    if argument.alpha == 0 and argument.rational.denominator == 1:
        raise AssertionError("vanishing q-Pochhammer factor")
    return argument - Fraction(1, 2) + (argument.floor() & 1)


def q_pochhammer_phase(
    argument: Quadratic,
    period: Quadratic,
    count: int,
) -> Quadratic:
    result = Quadratic()
    if count >= 0:
        for index in range(count):
            result += linear_factor_phase(argument + index * period)
    else:
        for index in range(1, -count + 1):
            result -= linear_factor_phase(argument - index * period)
    return result


def reciprocal_double_sine_sign(
    argument: Quadratic,
    period: Quadratic,
) -> int:
    def sine_sign(value: Quadratic) -> int:
        if value.alpha == 0 and value.rational.denominator == 1:
            raise AssertionError("double-sine recurrence met zero")
        return 1 if value.floor() % 2 == 0 else -1

    sign = 1
    while argument.sign() <= 0:
        sign *= sine_sign(argument / period)
        argument += 1
    while (argument - period - 1).sign() >= 0:
        argument -= 1
        sign *= sine_sign(argument / period)
    return sign


def period_data() -> tuple[list[Quadratic], list[Quadratic]]:
    rows = [
        [Quadratic(Fraction(AT[0][0])), Quadratic(Fraction(AT[0][1]))],
        [Quadratic(Fraction(AT[1][0])), Quadratic(Fraction(AT[1][1]))],
    ]
    for index in range(len(WORD) - 1):
        rows.append([
            -rows[index][0] + WORD[index] * rows[index + 1][0],
            -rows[index][1] + WORD[index] * rows[index + 1][1],
        ])
    periods = [row[0] * ALPHA + row[1] for row in rows]
    ratios = [
        periods[index] / periods[(index + 1) % len(periods)]
        for index in range(len(periods))
    ]
    return periods, ratios


PERIODS, RATIOS = period_data()


def sigma_phase(
    argument: Quadratic,
    period: Quadratic,
) -> Quadratic:
    shift = (-argument).floor() + (period / 2).floor()
    finite = q_pochhammer_phase(
        argument / period,
        -1 / period,
        -shift,
    )
    shifted = argument + shift
    bernoulli = (
        6 * shifted**2
        + 6 * (1 - period) * shifted
        + period**2
        - 3 * period
        + 1
    ) / (24 * period)
    sign = reciprocal_double_sine_sign(shifted + 1, period)
    return finite + 2 * bernoulli + (0 if sign > 0 else 1)


def overlap_phase(first: int, second: int) -> Quadratic:
    z_value = (
        PERIODS[0] * second - PERIODS[1] * first
    ) / DIMENSION
    finite_numerator = (
        -AT[1][0] * first + (AT[0][0] - 1) * second
    )
    if finite_numerator % DIMENSION:
        raise AssertionError("nonintegral outer finite-product count")
    finite_count = finite_numerator // DIMENSION
    form_value = (
        first * first - 4 * first * second + 2 * second * second
    )

    # Psi(A)=0 and (-1)^s=-1.  Since
    # tau_7=-exp(pi*i/7)=exp(8*pi*i/7), the SF phase contributes
    # 1-16Q/7 in units of pi.
    phase = Quadratic(Fraction(1) - Fraction(16 * form_value, 7))
    phase -= q_pochhammer_phase(
        (second * ALPHA - first) / DIMENSION,
        ALPHA,
        finite_count,
    )
    for index in range(len(WORD) - 1):
        phase += sigma_phase(
            z_value / PERIODS[index + 2],
            RATIOS[index + 1],
        )
    return phase


EXPECTED_SIGNS = (
    "+--++--",
    "----++-",
    "+-+-+--",
    "-------",
    "-------",
    "+--+-+-",
    "--++---",
)


def main() -> None:
    audited = 0
    rows: list[str] = []
    for first in range(DIMENSION):
        signs: list[str] = []
        for second in range(DIMENSION):
            if first == second == 0:
                signs.append("+")
                continue
            phase = overlap_phase(first, second)
            if phase.alpha != 0 or phase.rational.denominator != 1:
                raise AssertionError(
                    f"nonintegral phase at {(first, second)}: {phase}"
                )
            signs.append("+" if phase.rational.numerator % 2 == 0 else "-")
            audited += 1
        rows.append("".join(signs))
    if tuple(rows) != EXPECTED_SIGNS:
        raise AssertionError(
            f"sign table changed: expected {EXPECTED_SIGNS}, got {rows}"
        )
    print(f"PERIOD_RATIOS={[str(value) for value in RATIOS[:-1]]}")
    print(f"AUDITED_NONZERO_CHARACTERISTICS={audited}")
    for index, row in enumerate(rows):
        print(f"SIGN_ROW_{index}={row}")
    print("DIMENSION_SEVEN_DISCRIMINANT_EIGHT_SIGNS_CERTIFIED=1")


if __name__ == "__main__":
    main()
