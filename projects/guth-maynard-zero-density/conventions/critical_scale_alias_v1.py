"""Cycle 103 critical-scale algebraic alias inverse."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import floor
from typing import Any, Iterable

import sympy as sp

from conventions.cross_valuation_inverse_v1 import CrossCore


def nearest_integer_distance(value: Fraction) -> Fraction:
    lower = value.numerator // value.denominator
    return min(value - lower, lower + 1 - value)


@dataclass(frozen=True)
class CriticalScalePhase:
    s: int
    t: int
    N: int
    R: int
    B0: int
    C0: int

    def __post_init__(self) -> None:
        if min(self.s, self.t, self.N, self.R, self.B0, self.C0) <= 0:
            raise ValueError("positive critical data required")
        if Fraction(self.C0 * self.t, self.B0 * self.s) != self.label:
            raise ValueError("critical label identity failed")

    @classmethod
    def from_cross_core(cls, core: CrossCore) -> "CriticalScalePhase":
        return cls(
            s=core.s,
            t=core.t,
            N=core.N,
            R=core.R,
            B0=core.base_B,
            C0=core.base_C,
        )

    @property
    def W(self) -> int:
        return self.s + self.t

    @property
    def label(self) -> Fraction:
        return Fraction(self.N, self.R)

    @property
    def alpha(self) -> sp.Expr:
        return sp.Pow(sp.Rational(self.N, self.R), sp.Rational(1, self.W))

    @property
    def K(self) -> sp.Expr:
        return sp.simplify(self.B0 * self.alpha**self.s + self.C0 * self.alpha**(-self.t))

    def verify(self) -> dict[str, Any]:
        derivative_left = self.B0 * self.s * self.alpha**self.s
        derivative_right = self.C0 * self.t * self.alpha**(-self.t)
        if sp.simplify(derivative_left - derivative_right) != 0:
            raise AssertionError("critical derivative does not vanish")
        z = sp.symbols("z")
        defining_polynomial = self.R * z**self.W - self.N
        if sp.simplify(defining_polynomial.subs(z, self.alpha)) != 0:
            raise AssertionError("root-field encoding failed")
        return {
            "label": self.label,
            "W": self.W,
            "alpha": self.alpha,
            "K": self.K,
            "positive": bool(self.K.is_positive),
            "degree_bound": self.W,
            "critical_value": "f(t*)=A-lambda*K",
        }


def critical_value_tolerance(
    delta: Fraction, eta: Fraction, lower_curvature: Fraction, upper_curvature: Fraction
) -> Fraction:
    """Cycle-97 upper bound for |f(t*)| in the localized branch."""
    if min(delta, eta) < 0 or min(lower_curvature, upper_curvature) <= 0:
        raise ValueError("invalid near-double ledger")
    return (
        delta
        + 2 * eta * eta / lower_curvature
        + 2 * upper_curvature * eta * eta / (lower_curvature * lower_curvature)
    )


def least_alias(theta: Fraction, epsilon: Fraction, Lambda: int) -> int | None:
    if epsilon < 0 or Lambda < 1:
        raise ValueError("invalid alias range")
    for q in range(1, Lambda):
        if nearest_integer_distance(q * theta) <= 2 * epsilon:
            return q
    return None


def scale_alias_inverse(
    *,
    theta: Fraction,
    epsilon: Fraction,
    Lambda: int,
    hits: Iterable[tuple[int, int]],
) -> dict[str, Any]:
    """Exact rational replay of the real-number spacing lemma."""
    if epsilon < 0 or Lambda < 1:
        raise ValueError("invalid alias input")
    rows = tuple(sorted(hits))
    scales = [scale for scale, _ in rows]
    if len(scales) != len(set(scales)):
        raise ValueError("hit scales must be distinct")
    for scale, integer in rows:
        if not 1 <= scale <= Lambda:
            raise ValueError("scale outside frozen range")
        if abs(Fraction(integer) - scale * theta) > epsilon:
            raise ValueError("row is not an epsilon hit")

    q_epsilon = least_alias(theta, epsilon, Lambda)
    J = len(rows)
    if q_epsilon is None:
        support_bound = 1
    else:
        support_bound = 1 + floor((Lambda - 1) / q_epsilon)
    if J > support_bound:
        raise AssertionError("least-alias support bound failed")

    witness = None
    if J >= 2:
        adjacent = [
            (rows[index + 1][0] - rows[index][0], rows[index], rows[index + 1])
            for index in range(J - 1)
        ]
        q, left, right = min(adjacent, key=lambda item: item[0])
        max_q = floor((Lambda - 1) / (J - 1))
        integer_difference = right[1] - left[1]
        distance = abs(Fraction(integer_difference) - q * theta)
        if q > max_q or distance > 2 * epsilon:
            raise AssertionError("adjacent-hit alias inverse failed")
        witness = {
            "q": q,
            "integer": integer_difference,
            "distance": distance,
            "max_q": max_q,
        }

    return {
        "hit_count": J,
        "least_alias": q_epsilon,
        "support_bound": support_bound,
        "witness": witness,
    }


def theorem_record() -> dict[str, object]:
    return {
        "critical_point": "t*=log(N/R)/W is independent of lambda",
        "critical_number": "K=B0*r^(s/W)+C0*r^(-t/W)>0",
        "homogeneity": "B=lambda*B0, C=lambda*C0 gives f(t*)=A-lambda*K",
        "algebraicity": "K lies in Q(r^(1/W)), hence deg(K)<=W",
        "near_double_transfer": (
            "Cycle 97 gives |A-lambda*K|<=delta+2eta^2/ell+2Leta^2/ell^2"
        ),
        "inverse": (
            "J>=2 hits force 1<=q<=floor((Lambda-1)/(J-1)) and ||qK||<=2epsilon"
        ),
        "least_alias_bound": (
            "J<=1+floor((Lambda-1)/q_epsilon), or J<=1 if no q_epsilon exists"
        ),
        "boundary": (
            "no useful irrationality measure, aggregate core count, phase cancellation, "
            "or density/interval gain is proved"
        ),
    }
