"""Cycle 104 single-radical classification and norm separation."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import Any

from conventions.cross_valuation_inverse_v1 import CrossCore


def is_perfect_power(n: int, degree: int) -> bool:
    if n <= 0 or degree <= 0:
        raise ValueError("positive integer and degree required")
    if degree == 1 or n == 1:
        return True
    low, high = 1, 2
    while high**degree < n:
        high *= 2
    while low <= high:
        middle = (low + high) // 2
        value = middle**degree
        if value == n:
            return True
        if value < n:
            low = middle + 1
        else:
            high = middle - 1
    return False


@dataclass(frozen=True)
class RadicalAliasCore:
    h: int
    u: int
    v: int
    d: int
    x: int
    y: int
    s2: int
    t2: int
    N: int
    R: int
    R2: int
    B0: int

    @classmethod
    def from_cross_core(cls, core: CrossCore) -> "RadicalAliasCore":
        h = gcd(core.s, core.t)
        u, v = core.s // h, core.t // h
        return cls(
            h=h,
            u=u,
            v=v,
            d=u + v,
            x=core.x,
            y=core.y,
            s2=core.s2,
            t2=core.t2,
            N=core.N,
            R=core.R,
            R2=core.R2,
            B0=core.base_B,
        )

    def __post_init__(self) -> None:
        if min(
            self.h,
            self.u,
            self.v,
            self.d,
            self.x,
            self.y,
            self.s2,
            self.t2,
            self.N,
            self.R,
            self.R2,
            self.B0,
        ) <= 0:
            raise ValueError("positive radical-core data required")
        if self.d != self.u + self.v or gcd(self.u, self.v) != 1:
            raise ValueError("primitive mode data failed")
        if self.u != self.x * self.s2 or self.v != self.y * self.t2:
            raise ValueError("cross-core mode factorization failed")
        if self.B0 != self.t2 * self.R2 or self.R != self.x * self.R2:
            raise ValueError("cross-core coefficient factorization failed")
        if gcd(self.N, self.R) != 1:
            raise ValueError("label must be reduced")

    @property
    def prefactor(self) -> Fraction:
        return Fraction(self.d * self.R2, self.y)

    @property
    def K_power(self) -> Fraction:
        return self.prefactor**self.d * Fraction(self.N, self.R) ** self.u

    @property
    def rational_alias(self) -> bool:
        return is_perfect_power(self.N, self.d) and is_perfect_power(self.R, self.d)

    def record(self) -> dict[str, Any]:
        direct_prefactor = Fraction(self.h * self.d, self.h * self.v) * self.B0
        if direct_prefactor != self.prefactor:
            raise AssertionError("single-radical prefactors disagree")
        if gcd(self.u, self.d) != 1:
            raise AssertionError("radical exponent is not primitive")
        power = self.K_power
        return {
            "h": self.h,
            "u": self.u,
            "v": self.v,
            "d": self.d,
            "prefactor": self.prefactor,
            "K_power_numerator": power.numerator,
            "K_power_denominator": power.denominator,
            "rational_alias": self.rational_alias,
        }

    def exact_norm_numerator(self, q: int, m: int) -> int:
        if q <= 0:
            raise ValueError("positive alias denominator required")
        power = self.K_power
        numerator = q**self.d * power.numerator - m**self.d * power.denominator
        if not self.rational_alias and numerator == 0:
            raise AssertionError("irrational radical has an exact rational alias")
        return numerator

    def safe_norm_bound(self, Lambda: int) -> Fraction:
        if Lambda < 1:
            raise ValueError("positive scale range required")
        power = self.K_power
        upper_K = max(Fraction(1), power)
        envelope = 2 * Lambda * upper_K + Fraction(1, 2)
        return Fraction(1, power.denominator) / envelope ** (self.d - 1)

    def separation_closes(self, epsilon: Fraction, Lambda: int) -> bool:
        if epsilon < 0:
            raise ValueError("nonnegative tolerance required")
        if self.rational_alias:
            return False
        return 2 * epsilon < self.safe_norm_bound(Lambda)


def theorem_record() -> dict[str, object]:
    return {
        "primitive_degree": "h=(s,t), u=s/h, v=t/h, d=u+v=W/h, (u,d)=1",
        "single_radical": "K=(W/t)*B0*r^(s/W)=(d*R2/y)*r^(u/d)",
        "power": "K^d=(d*R2/y)^d*(N/R)^u=P/S in lowest terms",
        "rational_classification": "K is rational iff N and R are both perfect dth powers",
        "norm_separation": "|qK-m|>=1/(S*(qK+abs(m))^(d-1))",
        "safe_separation": "|qK-m|>=1/(S*(2*Lambda*U+1/2)^(d-1)), U=max(1,P/S)",
        "closure": "2epsilon below the safe bound implies no q<=Lambda alias and at most one scale hit",
        "boundary": "large radical degree and aggregation across cores remain open",
    }
