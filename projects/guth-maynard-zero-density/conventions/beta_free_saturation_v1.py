"""Cycle 106 rational scale saturation and beta-free seed boundary."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any

from conventions.radical_alias_separation_v1 import RadicalAliasCore


def exact_nth_root(value: int, degree: int) -> int:
    if value <= 0 or degree <= 0:
        raise ValueError("positive value and degree required")
    low, high = 1, 2
    while high**degree < value:
        high *= 2
    while low <= high:
        middle = (low + high) // 2
        power = middle**degree
        if power == value:
            return middle
        if power < value:
            low = middle + 1
        else:
            high = middle - 1
    raise ValueError("value is not an exact power")


@dataclass(frozen=True)
class RationalScaleOrbit:
    u: int
    v: int
    d: int
    x: int
    y: int
    n0: int
    r0: int

    @classmethod
    def from_radical(cls, radical: RadicalAliasCore) -> "RationalScaleOrbit":
        if not radical.rational_alias:
            raise ValueError("radical core is not in the rational class")
        return cls(
            u=radical.u,
            v=radical.v,
            d=radical.d,
            x=radical.x,
            y=radical.y,
            n0=exact_nth_root(radical.N, radical.d),
            r0=exact_nth_root(radical.R, radical.d),
        )

    def __post_init__(self) -> None:
        if min(self.u, self.v, self.d, self.x, self.y, self.n0, self.r0) <= 0:
            raise ValueError("positive orbit data required")
        if self.d != self.u + self.v:
            raise ValueError("degree must equal u+v")
        if self.r0**self.d % self.x or self.n0**self.d % self.y:
            raise ValueError("cross factors do not divide powered label")

    @property
    def K(self) -> Fraction:
        return Fraction(
            self.d * self.n0**self.u * self.r0**self.v,
            self.x * self.y,
        )

    @property
    def denominator(self) -> int:
        return self.K.denominator

    def verify_against(self, radical: RadicalAliasCore) -> None:
        if self.K**self.d != radical.K_power:
            raise AssertionError("simplified rational K disagrees with Cycle 104")

    def tight_hits(self, *, Lambda: int, epsilon: Fraction) -> dict[str, Any]:
        if Lambda < 1 or epsilon < 0:
            raise ValueError("invalid scale range or tolerance")
        if epsilon >= Fraction(1, self.denominator):
            raise ValueError("tolerance does not satisfy the frozen tight-hit gate")
        scales = tuple(range(self.denominator, Lambda + 1, self.denominator))
        integers = tuple(scale * self.K.numerator // self.denominator for scale in scales)
        return {
            "K": self.K,
            "S0": self.denominator,
            "scales": scales,
            "integers": integers,
            "count": Lambda // self.denominator,
            "all_scales": self.denominator == 1,
        }


def paired_beta_witness(
    *, alpha: Fraction, h0: int, j0: int, strip_radius: Fraction
) -> dict[str, Fraction | bool]:
    if h0 == 0 or strip_radius < 0 or strip_radius >= Fraction(1, 2):
        raise ValueError("nonzero row and strip radius below 1/2 required")
    seeded_beta = h0 * alpha - j0
    unseeded_beta = seeded_beta + Fraction(1, 2)
    seeded_residual = abs(Fraction(j0) + seeded_beta - h0 * alpha)
    unseeded_residual = abs(Fraction(j0) + unseeded_beta - h0 * alpha)
    return {
        "seeded_beta": seeded_beta,
        "unseeded_beta": unseeded_beta,
        "seeded_residual": seeded_residual,
        "unseeded_residual": unseeded_residual,
        "seeded": seeded_residual <= strip_radius,
        "unseeded": unseeded_residual <= strip_radius,
    }


def theorem_record() -> dict[str, object]:
    return {
        "rational_scale": "K=d*n0^u*r0^v/(x*y)=A0/S0 in lowest terms",
        "tight_hits": (
            "if 0<=epsilon<1/S0, the hit scales are exactly lambda in [1,Lambda] "
            "with S0|lambda"
        ),
        "hit_count": "floor(Lambda/S0); all scales survive iff S0=1",
        "saturator": "u=2,v=1,d=3,x=2,y=1,n0=3,r0=2 gives K=27",
        "seed_boundary": (
            "the same beta-free ray data admits beta=h0*alpha-j0 (an exact seed) "
            "and beta+1/2 (a miss when C0/X<1/2)"
        ),
        "positive_interface": (
            "a retained payload that verifies the Cycle-67 seed inequality may invoke propagation"
        ),
        "boundary": (
            "no seed follows from beta-free powered-ray data alone; payload-aware realization "
            "and signed phase cancellation remain open"
        ),
    }
