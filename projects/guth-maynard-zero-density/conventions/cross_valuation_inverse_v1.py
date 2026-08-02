"""Cycle 102 exact cross-valuation cores and weighted concentration."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from math import floor, gcd, log2
from typing import Any, Iterable

from conventions.critical_fiber_atlas_v1 import FiberAtlas


def full_prime_powers(n: int) -> tuple[int, ...]:
    """Return p^v for every prime p exactly dividing n to exponent v."""
    if n <= 0:
        raise ValueError("positive integer required")
    powers: list[int] = []
    remaining = n
    prime = 2
    while prime * prime <= remaining:
        power = 1
        while remaining % prime == 0:
            remaining //= prime
            power *= prime
        if power > 1:
            powers.append(power)
        prime += 1
    if remaining > 1:
        powers.append(remaining)
    return tuple(powers)


def prime_power_count(limit: int) -> int:
    if limit < 1:
        raise ValueError("positive limit required")
    return sum(bool(full_prime_powers(n) == (n,)) for n in range(2, limit + 1))


def dyadic_index(n: int) -> int:
    if n <= 0:
        raise ValueError("positive integer required")
    return n.bit_length() - 1


@dataclass(frozen=True)
class CrossCore:
    w: int
    s: int
    t: int
    N: int
    R: int
    Q: int
    g0: int
    s1: int
    t1: int
    x: int
    y: int
    s2: int
    t2: int
    N2: int
    R2: int
    base_B: int
    base_C: int
    lambda_max: int
    payload: Any = None

    @property
    def exceptional(self) -> bool:
        return self.x > 1 or self.y > 1

    @property
    def colours(self) -> tuple[tuple[str, int], ...]:
        rows = [("R", q) for q in full_prime_powers(self.x)]
        rows.extend(("N", q) for q in full_prime_powers(self.y))
        return tuple(sorted(rows))


def extract_cross_core(
    *, w: int, N: int, R: int, Q: int, s: int, payload: Any = None
) -> CrossCore:
    atlas = FiberAtlas(w=w, N=N, R=R, Q=Q)
    row = atlas.split(s)
    t = atlas.W - s
    g0 = int(row["g0"])
    s1, t1 = s // g0, t // g0
    x, y = int(row["cross_R"]), int(row["cross_N"])
    s2, R2 = s1 // x, R // x
    t2, N2 = t1 // y, N // y
    base_B, base_C = t2 * R2, s2 * N2

    if gcd(s1, t1) != 1:
        raise AssertionError("primitive modes are not coprime")
    if gcd(s2, R2) != 1 or gcd(t2, N2) != 1:
        raise AssertionError("cross cores are not coprime")
    if gcd(x, y) != 1 or gcd(y * N2, x * R2) != 1:
        raise AssertionError("reduced label coprimality failed")
    if atlas.W != g0 * (x * s2 + y * t2):
        raise AssertionError("additive core equation failed")
    if base_B != row["base_B"] or base_C != row["base_C"]:
        raise AssertionError("primitive coefficient bases changed")

    return CrossCore(
        w=w,
        s=s,
        t=t,
        N=N,
        R=R,
        Q=Q,
        g0=g0,
        s1=s1,
        t1=t1,
        x=x,
        y=y,
        s2=s2,
        t2=t2,
        N2=N2,
        R2=R2,
        base_B=base_B,
        base_C=base_C,
        lambda_max=Q // max(base_B, base_C),
        payload=payload,
    )


@dataclass(frozen=True)
class ExceptionalAtom:
    w: int
    x: int
    y: int
    weight: Fraction | int
    payload: Any = None

    def __post_init__(self) -> None:
        if self.w == 0 or self.x <= 0 or self.y <= 0:
            raise ValueError("nonzero mode and positive cross gcds required")
        if self.x == 1 and self.y == 1:
            raise ValueError("atom must be exceptional")
        if Fraction(self.weight) <= 0:
            raise ValueError("concentration weights must be positive")

    def canonical_colour(self) -> tuple[str, int]:
        colours = [("R", q) for q in full_prime_powers(self.x)]
        colours.extend(("N", q) for q in full_prime_powers(self.y))
        if not colours:
            raise AssertionError("exceptional atom has no prime-power colour")
        return min(colours, key=lambda item: (-item[1], item[0]))


def concentration_record(
    atoms: Iterable[ExceptionalAtom], *, M: int, refined: bool
) -> dict[str, Any]:
    if M < 1:
        raise ValueError("positive M required")
    rows = tuple(atoms)
    if not rows:
        raise ValueError("at least one atom required")
    height = 2 * M
    for atom in rows:
        if max(atom.x, atom.y) > height:
            raise ValueError("cross gcd exceeds frozen 2M range")

    mass_by_w: dict[int, Fraction] = defaultdict(Fraction)
    mass_by_colour: dict[tuple[object, ...], Fraction] = defaultdict(Fraction)
    support_by_colour: dict[tuple[object, ...], set[int]] = defaultdict(set)
    payload_by_colour: dict[tuple[object, ...], list[Any]] = defaultdict(list)
    for atom in rows:
        weight = Fraction(atom.weight)
        side, power = atom.canonical_colour()
        colour: tuple[object, ...]
        if refined:
            colour = (dyadic_index(atom.x), dyadic_index(atom.y), side, power)
        else:
            colour = (side, power)
        mass_by_w[atom.w] += weight
        mass_by_colour[colour] += weight
        support_by_colour[colour].add(atom.w)
        payload_by_colour[colour].append(atom.payload)

    total_mass = sum(mass_by_w.values(), Fraction())
    per_w_cap = max(mass_by_w.values())
    p_count = prime_power_count(height)
    dyadic_count = 1 + floor(log2(height))
    colour_bound = 2 * p_count * (dyadic_count**2 if refined else 1)
    selected = max(mass_by_colour, key=lambda colour: mass_by_colour[colour])
    support = len(support_by_colour[selected])
    guaranteed_support = total_mass / (colour_bound * per_w_cap)
    if Fraction(support) < guaranteed_support:
        raise AssertionError("weighted colour concentration failed")
    return {
        "total_mass": total_mass,
        "per_w_cap": per_w_cap,
        "prime_power_count": p_count,
        "dyadic_count": dyadic_count,
        "colour_bound": colour_bound,
        "selected_colour": selected,
        "selected_mass": mass_by_colour[selected],
        "selected_w": tuple(sorted(support_by_colour[selected])),
        "selected_payloads": tuple(payload_by_colour[selected]),
        "support": support,
        "guaranteed_support": guaranteed_support,
    }


def theorem_record() -> dict[str, object]:
    return {
        "core": (
            "s1=x*s2, R=x*R2, t1=y*t2, N=y*N2 gives "
            "B0=t2*R2, C0=s2*N2 and W=g0*(x*s2+y*t2)"
        ),
        "coprimality": (
            "(s2,R2)=(t2,N2)=(x,y)=(y*N2,x*R2)=1"
        ),
        "valuation_signature": (
            "q|x divides s/g0 and R but not t/g0 or N; "
            "q|y has the side-reversed signature"
        ),
        "unrefined_concentration": (
            "some side/full-prime-power colour supports at least "
            "E/(2*P(2M)*A) distinct w"
        ),
        "refined_concentration": (
            "retaining both dyadic cross-gcd indices gives support at least "
            "E/(2*P(2M)*L_M^2*A)"
        ),
        "boundary": (
            "the conclusion needs total nonnegative mass E and a per-w cap A; "
            "it proves no phase cancellation or common anchor"
        ),
    }
