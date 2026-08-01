"""Frozen, non-analytic conventions for the Cycle-3 G1 discovery atlas.

This module deliberately contains only the finite protocol specified in
``docs/cycle-3-g1-atlas-preregistration-v1.md``.  It is shared by discovery
code and its tests, never by ``proof/``.  In particular, none of these
definitions is a new large-values inequality.
"""
from __future__ import annotations

from fractions import Fraction


MASK64 = (1 << 64) - 1
SPLITMIX64_GAMMA = 0x9E3779B97F4A7C15
SPLITMIX64_MUL1 = 0xBF58476D1CE4E5B9
SPLITMIX64_MUL2 = 0x94D049BB133111EB

BASE_SEED = 0x47554D41594E4731
COEFFICIENT_XOR = 0x434F454646000001
SET_XOR = 0x57414C5545000001

SCREEN_SCALE = 1 << 12
VALIDATION_SCALES = (1 << 15, 1 << 18)
PRECISIONS_BITS = (256, 384)

COEFFICIENT_FAMILIES = (
    "C0-flat", "C1-tent", "C2-two-tent", "C3-root-chirp",
    "C4-rademacher", "C5-point-aligned",
)
SET_FAMILIES = (
    "W0-sidon", "W1-uniform", "W2-jitter", "W3-AP",
    "W4-four-block", "W5-rational",
)
REGISTERED_PAIRS = (
    ("C0-flat", "W0-sidon"),
    ("C0-flat", "W1-uniform"),
    ("C0-flat", "W3-AP"),
    ("C1-tent", "W1-uniform"),
    ("C1-tent", "W3-AP"),
    ("C2-two-tent", "W2-jitter"),
    ("C2-two-tent", "W4-four-block"),
    ("C3-root-chirp", "W0-sidon"),
    ("C3-root-chirp", "W5-rational"),
    ("C4-rademacher", "W0-sidon"),
    ("C4-rademacher", "W1-uniform"),
    ("C4-rademacher", "W2-jitter"),
    ("C5-point-aligned", "W3-AP"),
    ("C5-point-aligned", "W5-rational"),
)


def q(value: Fraction) -> str:
    """Use the preregistration's reduced rational serialization."""
    return f"{value.numerator}/{value.denominator}"


def local_s_grid() -> tuple[Fraction, ...]:
    return tuple(Fraction(7, 10) + Fraction(i, 100) for i in range(11))


def local_n_grid() -> tuple[Fraction, ...]:
    return tuple(Fraction(3, 4) + Fraction(i, 60) for i in range(16))


def local_v_grid() -> tuple[Fraction, ...]:
    return local_s_grid()


def local_w_grid() -> tuple[Fraction, ...]:
    return (Fraction(1, 2), Fraction(7, 12), Fraction(2, 3), Fraction(3, 4))


def primary_spine() -> tuple[tuple[Fraction, Fraction, Fraction, Fraction], ...]:
    """Return the frozen 42 local coordinates in their declared order."""
    rows = []
    for s in (Fraction(7, 10), Fraction(3, 4), Fraction(4, 5)):
        nearby = tuple(
            value for value in (s - Fraction(1, 100), s, s + Fraction(1, 100))
            if Fraction(7, 10) <= value <= Fraction(4, 5)
        )
        for n in (Fraction(4, 5), Fraction(5, 6)):
            for v in nearby:
                for w in (Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)):
                    rows.append((s, n, v, w))
    if len(rows) != 42 or len(set(rows)) != 42:
        raise RuntimeError("frozen G1 primary spine does not have 42 distinct rows")
    return tuple(rows)


def energy_regime(set_family: str) -> str:
    """The finite family-to-target convention required by the protocol."""
    if set_family == "W0-sidon":
        return "low"
    if set_family == "W3-AP":
        return "high"
    if set_family in {"W1-uniform", "W2-jitter", "W4-four-block", "W5-rational"}:
        return "intermediate"
    raise ValueError(f"unknown set family: {set_family}")
