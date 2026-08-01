#!/usr/bin/env python3
"""Exact exploratory D12 AFK sign audit in a reduced fixed-point chart.

This is deliberately a sign computation, not a packet-root relabelling.
For Q=x^2-3xy-y^2 the AFK fixed point is rho=(3+sqrt(13))/2.
The M=T^{-1} transformed form Q_M=x^2-5xy+3y^2 has reduced fixed
point beta=rho+1 and A_M=T A T^{-1}.  AFK Theorem
``MTransformNormalizedGhostOverlap`` relabels original (p,q) to
M^{-1}(p,q)=(p+q,q) in the reduced chart.

The continued-fraction factorization is evaluated exactly through the
q-Pochhammer and reciprocal-double-sine shift recurrences.  It is an
EXPLORATORY bridge component: no TCC conclusion is drawn here.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from decimal import Decimal, ROUND_FLOOR, getcontext
from fractions import Fraction
from pathlib import Path


getcontext().prec = 100
ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "projects/sic-stark/artifacts/tcc-sweep-d12-afk-signs-corrected-v2.json"


@dataclass(frozen=True)
class Quadratic:
    """a+b*beta, with beta=(5+sqrt(13))/2 and beta^2=5beta-3."""

    rational: Fraction = Fraction(0)
    beta: Fraction = Fraction(0)

    def __add__(self, other: object) -> "Quadratic":
        value = coerce(other)
        return Quadratic(self.rational + value.rational, self.beta + value.beta)

    __radd__ = __add__

    def __neg__(self) -> "Quadratic":
        return Quadratic(-self.rational, -self.beta)

    def __sub__(self, other: object) -> "Quadratic":
        return self + (-coerce(other))

    def __rsub__(self, other: object) -> "Quadratic":
        return coerce(other) - self

    def __mul__(self, other: object) -> "Quadratic":
        value = coerce(other)
        return Quadratic(
            self.rational * value.rational - 3 * self.beta * value.beta,
            self.rational * value.beta + self.beta * value.rational + 5 * self.beta * value.beta,
        )

    __rmul__ = __mul__

    def inverse(self) -> "Quadratic":
        norm = self.rational**2 + 5 * self.rational * self.beta + 3 * self.beta**2
        if norm == 0:
            raise ZeroDivisionError
        return Quadratic((self.rational + 5 * self.beta) / norm, -self.beta / norm)

    def __truediv__(self, other: object) -> "Quadratic":
        return self * coerce(other).inverse()

    def __rtruediv__(self, other: object) -> "Quadratic":
        return coerce(other) * self.inverse()

    def __pow__(self, exponent: int) -> "Quadratic":
        if exponent < 0:
            return self.inverse() ** (-exponent)
        result, base = Quadratic(Fraction(1)), self
        while exponent:
            if exponent & 1:
                result *= base
            base *= base
            exponent //= 2
        return result

    def sign(self) -> int:
        constant, radical = self.rational + 5 * self.beta / 2, self.beta / 2
        if radical == 0:
            return (constant > 0) - (constant < 0)
        if constant == 0:
            return (radical > 0) - (radical < 0)
        if constant > 0 and radical > 0:
            return 1
        if constant < 0 and radical < 0:
            return -1
        comparison = constant**2 - 13 * radical**2
        if constant > 0:
            return 1 if comparison > 0 else -1
        return -1 if comparison > 0 else 1

    def floor(self) -> int:
        beta_decimal = (Decimal(5) + Decimal(13).sqrt()) / 2
        approximation = Decimal(self.rational.numerator) / Decimal(self.rational.denominator)
        approximation += Decimal(self.beta.numerator) / Decimal(self.beta.denominator) * beta_decimal
        candidate = int(approximation.to_integral_value(rounding=ROUND_FLOOR))
        if (self - candidate).sign() < 0 or (self - candidate - 1).sign() >= 0:
            raise AssertionError(f"unproved floor {candidate} for {self}")
        return candidate


def coerce(value: object) -> Quadratic:
    if isinstance(value, Quadratic):
        return value
    if isinstance(value, (int, Fraction)):
        return Quadratic(Fraction(value))
    return NotImplemented


BETA = Quadratic(Fraction(0), Fraction(1))
DIMENSION = 12
# A_M = T A T^{-1}; word verifies A_M=T^5 S T^2 S T^2 S repeated thrice.
AT = ((1549, -1080), (360, -251))
WORD = (5, 2, 2, 5, 2, 2, 5, 2, 2, 0)


def linear_factor_phase(argument: Quadratic) -> Quadratic:
    if argument.beta == 0 and argument.rational.denominator == 1:
        raise AssertionError("vanishing q-Pochhammer factor")
    return argument - Fraction(1, 2) + (argument.floor() & 1)


def q_pochhammer_phase(argument: Quadratic, period: Quadratic, count: int) -> Quadratic:
    if count >= 0:
        return sum((linear_factor_phase(argument + index * period) for index in range(count)), Quadratic())
    return -sum((linear_factor_phase(argument - index * period) for index in range(1, -count + 1)), Quadratic())


def reciprocal_double_sine_sign(argument: Quadratic, period: Quadratic) -> int:
    def sine_sign(value: Quadratic) -> int:
        if value.beta == 0 and value.rational.denominator == 1:
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
    rows = [[Quadratic(Fraction(AT[0][0])), Quadratic(Fraction(AT[0][1]))], [Quadratic(Fraction(AT[1][0])), Quadratic(Fraction(AT[1][1]))]]
    for index in range(len(WORD) - 1):
        rows.append([-rows[index][0] + WORD[index] * rows[index + 1][0], -rows[index][1] + WORD[index] * rows[index + 1][1]])
    periods = [row[0] * BETA + row[1] for row in rows]
    return periods, [periods[index] / periods[(index + 1) % len(periods)] for index in range(len(periods))]


PERIODS, RATIOS = period_data()


def sigma_phase(argument: Quadratic, period: Quadratic) -> Quadratic:
    shift = (-argument).floor() + (period / 2).floor()
    finite = q_pochhammer_phase(argument / period, -1 / period, -shift)
    shifted = argument + shift
    bernoulli = (6 * shifted**2 + 6 * (1 - period) * shifted + period**2 - 3 * period + 1) / (24 * period)
    sign = reciprocal_double_sine_sign(shifted + 1, period)
    return finite + 2 * bernoulli + (0 if sign > 0 else 1)


def reduced_phase(first: int, second: int) -> Quadratic:
    z_value = (PERIODS[0] * second - PERIODS[1] * first) / DIMENSION
    finite_numerator = -AT[1][0] * first + (AT[0][0] - 1) * second
    if finite_numerator % DIMENSION:
        raise AssertionError("nonintegral outer finite-product count")
    finite_count = finite_numerator // DIMENSION
    form_value = first * first - 5 * first * second + 3 * second * second
    # f_{jm}/f=3, Phi(A)=0, tau_12=-exp(pi*i/12).
    phase = Quadratic(Fraction(-9 * form_value, 4) + ((1 + first) * (1 + second) & 1))
    phase -= q_pochhammer_phase((second * BETA - first) / DIMENSION, BETA, finite_count)
    for index in range(len(WORD) - 1):
        phase += sigma_phase(z_value / PERIODS[index + 2], RATIOS[index + 1])
    return phase


def main() -> None:
    signs, nonzero = [], 0
    for p in range(DIMENSION):
        row = []
        for q in range(DIMENSION):
            if (p, q) == (0, 0):
                # The AFK normalized-overlap formula is only used away from
                # dZ^2; the distinguished overlap is fixed separately.
                row.append("+")
                continue
            # AFK M-transform theorem, M=T^{-1}: reduced label T(p,q).
            phase = reduced_phase((p + q) % DIMENSION, q)
            if phase.beta != 0 or phase.rational.denominator != 1:
                raise AssertionError(f"nonintegral total phase at original {(p, q)}: {phase}")
            sign = "+" if phase.rational.numerator % 2 == 0 else "-"
            row.append(sign)
            nonzero += (p, q) != (0, 0)
        signs.append("".join(row))
    payload = {
        "schema": "tcc-sweep-d12-afk-signs-corrected-v2",
        "status": "EXPLORATORY",
        "tuple": {"d": 12, "r": 1, "original_form": [1, -3, -1], "reduced_form": [1, -5, 3]},
        "coordinate_change": {"M": [[1, -1], [0, 1]], "reduced_label_from_original": "(p+q,q) mod 12"},
        "reduced_fixed_point": "(5+sqrt(13))/2",
        "reduced_stabilizer": [list(AT[0]), list(AT[1])],
        "hj_word": list(WORD),
        "nonzero_characteristics": nonzero,
        "sign_rows_original_coordinates": signs,
        "source": "AFK arXiv:2501.03970v2, Theorem MTransformNormalizedGhostOverlap and Sec. Calculating the SF modular cocycle",
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["sha256"] = hashlib.sha256(canonical).hexdigest()
    payload["generated_at_utc"] = datetime.now(timezone.utc).isoformat()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"AUDITED_NONZERO_CHARACTERISTICS={nonzero}")
    for index, row in enumerate(signs):
        print(f"SIGN_ROW_{index}={row}")
    print("TCC_SWEEP_D12_AFK_SIGNS_CORRECTED_V2=PASS")


if __name__ == "__main__":
    main()
