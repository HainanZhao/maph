#!/usr/bin/env python3
"""Exact phase audit for the maximal-order dimension-eight AFK cocycle.

The generic continued-fraction formula contains finite q-Pochhammer
products, exponential phases, and real reciprocal double sines.  The
fundamental reciprocal double sine is positive.  Its shift recurrences
therefore reduce its sign to signs of ordinary real sine factors.

For real t not in Z,

    1 - exp(2*pi*i*t)
      = -2*i*exp(pi*i*t)*sin(pi*t).

Consequently every phase in the six-factor cocycle can be tracked exactly
as a multiple of pi in Q(beta), beta^2 - 3*beta + 1 = 0.  This script
checks that the beta coefficient cancels, that the remaining coefficient
is integral, and that its parity agrees with every sign in the exact
overlap table used by dimension_eight_maximal_exact_tcc.py.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_FLOOR, getcontext
from fractions import Fraction


getcontext().prec = 80


@dataclass(frozen=True)
class Quadratic:
    """An exact element a + b*beta with beta^2 = 3*beta - 1."""

    rational: Fraction = Fraction(0)
    beta: Fraction = Fraction(0)

    def __add__(self, other: object) -> Quadratic:
        value = coerce(other)
        return Quadratic(
            self.rational + value.rational,
            self.beta + value.beta,
        )

    __radd__ = __add__

    def __neg__(self) -> Quadratic:
        return Quadratic(-self.rational, -self.beta)

    def __sub__(self, other: object) -> Quadratic:
        return self + (-coerce(other))

    def __rsub__(self, other: object) -> Quadratic:
        return coerce(other) - self

    def __mul__(self, other: object) -> Quadratic:
        value = coerce(other)
        return Quadratic(
            self.rational * value.rational
            - self.beta * value.beta,
            self.rational * value.beta
            + self.beta * value.rational
            + 3 * self.beta * value.beta,
        )

    __rmul__ = __mul__

    def inverse(self) -> Quadratic:
        norm = (
            self.rational**2
            + 3 * self.rational * self.beta
            + self.beta**2
        )
        if norm == 0:
            raise ZeroDivisionError
        return Quadratic(
            (self.rational + 3 * self.beta) / norm,
            -self.beta / norm,
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
        """Return the exact sign after writing the value as c+d*sqrt(5)."""

        constant = self.rational + 3 * self.beta / 2
        radical = self.beta / 2
        if radical == 0:
            return (constant > 0) - (constant < 0)
        if constant == 0:
            return (radical > 0) - (radical < 0)
        if constant > 0 and radical > 0:
            return 1
        if constant < 0 and radical < 0:
            return -1
        comparison = constant**2 - 5 * radical**2
        if constant > 0:
            return 1 if comparison > 0 else -1
        return -1 if comparison > 0 else 1

    def floor(self) -> int:
        """Find the floor numerically, then prove both inequalities exactly."""

        beta_decimal = (Decimal(3) + Decimal(5).sqrt()) / 2
        approximation = (
            Decimal(self.rational.numerator)
            / Decimal(self.rational.denominator)
            + Decimal(self.beta.numerator)
            / Decimal(self.beta.denominator)
            * beta_decimal
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


BETA = Quadratic(Fraction(0), Fraction(1))
DIMENSION = 8


def sum_quadratics(values) -> Quadratic:
    result = Quadratic()
    for value in values:
        result += value
    return result


def linear_factor_phase(argument: Quadratic) -> Quadratic:
    """Return arg(1-exp(2*pi*i*argument))/pi exactly."""

    floor = argument.floor()
    if argument.beta == 0 and argument.rational.denominator == 1:
        raise AssertionError("vanishing q-Pochhammer factor")
    return argument - Fraction(1, 2) + (floor & 1)


def q_pochhammer_phase(
    argument: Quadratic,
    period: Quadratic,
    count: int,
) -> Quadratic:
    """Phase divided by pi, matching Zauner.jl's signed-count convention."""

    if count >= 0:
        return sum_quadratics(
            linear_factor_phase(argument + index * period)
            for index in range(count)
        )
    return -sum_quadratics(
        linear_factor_phase(argument - index * period)
        for index in range(1, -count + 1)
    )


def reciprocal_double_sine_sign(argument: Quadratic) -> int:
    """Sign obtained from shifts into 0 < z < beta+1."""

    def sine_sign(value: Quadratic) -> int:
        if value.beta == 0 and value.rational.denominator == 1:
            raise AssertionError("double-sine recurrence met a zero sine")
        return 1 if value.floor() % 2 == 0 else -1

    sign = 1
    while argument.sign() <= 0:
        sign *= sine_sign(argument / BETA)
        argument += 1
    while (argument - BETA - 1).sign() >= 0:
        argument -= 1
        sign *= sine_sign(argument / BETA)
    return sign


def sigma_phase(argument: Quadratic) -> Quadratic:
    """Phase divided by pi of one continued-fraction sigma factor."""

    shift = (-argument).floor() + (BETA / 2).floor()
    finite_phase = q_pochhammer_phase(
        argument / BETA,
        -1 / BETA,
        -shift,
    )
    shifted = argument + shift
    bernoulli_phase = (
        6 * shifted**2
        + 6 * (1 - BETA) * shifted
        + BETA**2
        - 3 * BETA
        + 1
    ) / (24 * BETA)
    double_sine_sign = reciprocal_double_sine_sign(shifted + 1)
    return (
        finite_phase
        + 2 * bernoulli_phase
        + (0 if double_sine_sign > 0 else 1)
    )


def overlap_phase(first: int, second: int) -> Quadratic:
    """Phase divided by pi of the full six-factor AFK overlap."""

    finite_numerator = -144 * first + 376 * second
    if finite_numerator % DIMENSION:
        raise AssertionError("nonintegral finite-product count")
    finite_count = finite_numerator // DIMENSION
    form_value = (
        first * first - 3 * first * second + second * second
    )
    parity = (1 + first) * (1 + second)

    # tau=-exp(pi*i/8)=exp(9*pi*i/8).
    phase = Quadratic(
        Fraction(-27 * form_value, 8) + (parity & 1)
    )
    phase -= q_pochhammer_phase(
        (second * BETA - first) / DIMENSION,
        BETA,
        finite_count,
    )
    for index in range(6):
        # The continued-fraction periods are beta^7,...,beta,1.
        argument = (
            second * BETA ** (index + 2)
            - first * BETA ** (index + 1)
        ) / DIMENSION
        phase += sigma_phase(argument)
    return phase


EXPECTED_SIGNS = (
    "+-++-++-",
    "------++",
    "+-+-+-+-",
    "+--+--+-",
    "--+--+++",
    "+---+++-",
    "++++++++",
    "-+--+-+-",
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
            if phase.beta != 0:
                raise AssertionError(
                    f"uncancelled beta phase at {(first, second)}: {phase}"
                )
            if phase.rational.denominator != 1:
                raise AssertionError(
                    f"nonintegral pi phase at {(first, second)}: {phase}"
                )
            sign = "+" if int(phase.rational) % 2 == 0 else "-"
            expected = EXPECTED_SIGNS[first][second]
            if sign != expected:
                raise AssertionError(
                    f"sign mismatch at {(first, second)}: "
                    f"{sign} != {expected}"
                )
            signs.append(sign)
            audited += 1
            print(
                f"CHARACTERISTIC={first},{second} "
                f"PHASE_PI={phase.rational} SIGN={sign}"
            )
        row = "".join(signs)
        if row != EXPECTED_SIGNS[first]:
            raise AssertionError(f"row mismatch at {first}")
        rows.append(row)

    print(f"PSL2_WORD=[3,3,3,3,3,3,0]")
    print(f"CHARACTERISTICS_AUDITED={audited}")
    print("BETA_PHASE_COEFFICIENTS_ZERO=1")
    print("INTEGRAL_PI_PHASES=1")
    print(f"SIGN_ROWS={','.join(rows)}")
    print("SIGN_TABLE_MATCH=1")


if __name__ == "__main__":
    main()
