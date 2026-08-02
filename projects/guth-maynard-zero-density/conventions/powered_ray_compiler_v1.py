"""Cycle 105 perfect-power rational-ray compiler."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from typing import Any, Iterable


def max_power_under_height(base_height: int, height_budget: int) -> int:
    if base_height <= 1 or height_budget < 1:
        raise ValueError("nonunit base and positive height budget required")
    exponent = 0
    value = 1
    while value * base_height <= height_budget:
        value *= base_height
        exponent += 1
    return exponent


def exact_root_error_bound(
    base: Fraction, target: Fraction, degree: int, power_error: Fraction
) -> Fraction:
    """Exact replay of |a-b| <= |a^d-b^d|/(d min(a,b)^(d-1))."""
    if min(base, target) <= 0 or degree < 1 or power_error < 0:
        raise ValueError("invalid root-error data")
    actual = abs(base**degree - target**degree)
    if actual > power_error:
        raise ValueError("power_error is not a valid upper bound")
    bound = power_error / (degree * min(base, target) ** (degree - 1))
    if abs(base - target) > bound:
        raise AssertionError("root error transfer failed")
    return bound


@dataclass(frozen=True)
class PoweredRayAtom:
    n0: int
    r0: int
    d: int
    h: int
    H: int
    M: int
    payload: Any = None

    def __post_init__(self) -> None:
        if min(self.n0, self.r0, self.d, self.H, self.M) <= 0 or self.h == 0:
            raise ValueError("positive ray data and nonzero base mode required")
        if gcd(self.n0, self.r0) != 1:
            raise ValueError("base ray must be reduced")
        if max(self.n0**self.d, self.r0**self.d) > self.H:
            raise ValueError("powered label exceeds height budget")
        if abs(self.h) * self.d > 2 * self.M:
            raise ValueError("powered mode exceeds frozen range")

    @property
    def base(self) -> Fraction:
        return Fraction(self.n0, self.r0)

    @property
    def label(self) -> Fraction:
        return self.base**self.d

    @property
    def w(self) -> int:
        return self.h * self.d

    @property
    def base_height(self) -> int:
        return max(self.n0, self.r0)

    def exponent_cap(self) -> int | None:
        if self.base_height == 1:
            return None
        return min(
            max_power_under_height(self.base_height, self.H),
            (2 * self.M) // abs(self.h),
        )


def compile_powered_rays(atoms: Iterable[PoweredRayAtom]) -> dict[str, Any]:
    rows = tuple(atoms)
    if not rows:
        raise ValueError("at least one powered ray required")
    groups: dict[tuple[int, Fraction], list[PoweredRayAtom]] = defaultdict(list)
    for atom in rows:
        groups[(atom.h, atom.base)].append(atom)
    compiled = []
    for (h, base), group in sorted(groups.items(), key=lambda item: (item[0][0], item[0][1])):
        ordered = sorted(group, key=lambda atom: atom.d)
        exponents = tuple(atom.d for atom in ordered)
        if len(exponents) != len(set(exponents)):
            raise ValueError("duplicate powered-ray exponent")
        compiled.append(
            {
                "h": h,
                "base": base,
                "exponents": exponents,
                "modes": tuple(h * d for d in exponents),
                "labels": tuple(base**d for d in exponents),
                "payloads": tuple(atom.payload for atom in ordered),
                "repeated": len(exponents) >= 2,
                "complete_exponent_interval": (
                    exponents == tuple(range(exponents[0], exponents[-1] + 1))
                ),
            }
        )
    return {
        "group_count": len(compiled),
        "repeated_group_count": sum(bool(row["repeated"]) for row in compiled),
        "groups": tuple(compiled),
    }


def theorem_record() -> dict[str, object]:
    return {
        "powered_ray": "N/R=(n0/r0)^d and w=h*d",
        "root_error": (
            "|n0/r0-exp(h*x)|<=delta/(d*min(n0/r0,exp(h*x))^(d-1))"
        ),
        "frozen_envelope": (
            "if |h*d*x|<=L and delta<=exp(-L)/2, the minimum base is at least "
            "(exp(-L)/2)^(1/d)"
        ),
        "height_cap": "d<=floor(log(H)/log(Z)) for nonunit base height Z",
        "repeated_output": "modes h*d and labels (n0/r0)^d on the exact observed exponent set",
        "boundary": "missing exponents are not filled and a powered ray is not yet a realized packet seed",
    }
