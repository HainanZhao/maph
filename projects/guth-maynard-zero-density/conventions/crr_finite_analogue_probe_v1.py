"""Frozen symbolic conventions for the CRR finite-analogue probe v1.

This module defines a discovery schedule and its finite surrogate only.  It
does not evaluate a candidate, run a search, or assert an asymptotic claim.
"""
from __future__ import annotations

from fractions import Fraction


MASTER_SEED = 0x43525255424F4C44
MASK64 = (1 << 64) - 1
SPLITMIX64_GAMMA = 0x9E3779B97F4A7C15
SPLITMIX64_MUL1 = 0xBF58476D1CE4E5B9
SPLITMIX64_MUL2 = 0x94D049BB133111EB

N_VALUES = (256, 512, 1024, 2048)
EXPONENTS = {
    "H": Fraction(6, 5),
    "R": Fraction(4, 5),
    "Q": Fraction(2, 5),
    "V": Fraction(7, 10),
    "rational_height": Fraction(3, 5),
    "cubic": Fraction(18, 5),
}

FAMILY_ORDER = (
    "F1-phase-rounded-frame",
    "F2-macrocell-resonant-layers",
    "F3-near-product-rational-packet",
    "F4-quadratic-modular-chirp",
    "F5-symmetric-positive-trace-spectral",
)
FAMILY_VARIANTS = {
    "F1-phase-rounded-frame": (
        {"id": "V1", "phase_denominator": 8},
        {"id": "V2", "phase_denominator": 12},
        {"id": "V3", "phase_denominator": 16},
        {"id": "V4", "phase_denominator": 24},
    ),
    "F2-macrocell-resonant-layers": (
        {"id": "V1", "macrocells": 2},
        {"id": "V2", "macrocells": 3},
        {"id": "V3", "macrocells": 4},
        {"id": "V4", "macrocells": 6},
    ),
    "F3-near-product-rational-packet": (
        {"id": "V1", "packet_denominator": 2},
        {"id": "V2", "packet_denominator": 3},
        {"id": "V3", "packet_denominator": 5},
        {"id": "V4", "packet_denominator": 7},
    ),
    "F4-quadratic-modular-chirp": (
        {"id": "V1", "prime_modulus": 257},
        {"id": "V2", "prime_modulus": 263},
        {"id": "V3", "prime_modulus": 269},
        {"id": "V4", "prime_modulus": 271},
    ),
    "F5-symmetric-positive-trace-spectral": (
        {"id": "V1", "spectral_rank": 2},
        {"id": "V2", "spectral_rank": 3},
        {"id": "V3", "spectral_rank": 4},
        {"id": "V4", "spectral_rank": 5},
    ),
}
REPLICATES = (0, 1)

MUTATIONS_PER_ROW = 128
PROXY_QUADRATURE_NODES = 16
FINAL_QUADRATURE_NODES = 32
PROXY_CUBIC_MODE = 8
FINAL_CUBIC_MODE = 12
QUADRATURE_RELATIVE_DISAGREEMENT = Fraction(1, 100)
CUBIC_RELATIVE_DISAGREEMENT = Fraction(5, 100)
RETAINED_HIT_MARGIN = Fraction(5, 100)
ENERGY_INTERVAL = (Fraction(1, 4), Fraction(4))
LARGE_VALUE_FACTOR = Fraction(3, 4)
RATIONAL_HEIGHT_FACTOR = Fraction(3, 4)
RATIONAL_MEASURE_FACTOR = Fraction(1, 5)
CUBIC_FACTOR = Fraction(1, 20)
RECOGNITION_RADIUS_FACTOR = Fraction(1, 10**30)
RESOURCE_WALL_SECONDS = 55 * 60
RESOURCE_MAX_RSS_BYTES = 1 << 30
PROXY_ACCEPTANCE_INCREMENT = Fraction(1, 1 << 40)

FINITE_SURROGATE = {
    "ambient_group": "G_H=Z/HZ, represented by {0,...,H-1}",
    "large_value_polynomial": "D_b(t)=sum_{n=0}^{N-1} b_n exp(2*pi*i*n*t/H), with |b_n|<=1",
    "set_energy": "E_H(W)=#{(a,b,c,d) in W^4:a+b=c+d mod H}",
    "rational_sum": "R_W(x)=sum_{t in W} exp(2*pi*i*t*x), x in [0,1]",
    "cubic_matrix": "B_M(x,y)=1_{x!=y}*2*sum_{m=1}^M(1-m/(M+1))*cos(2*pi*m*(x-y)/H)",
    "cubic_proxy": "C_M(W)=N^3*tr(B_M^3), a signed finite proxy",
}


class SplitMix64:
    """Reference unsigned-64 SplitMix64 stream with explicit wraparound."""

    def __init__(self, seed: int) -> None:
        self.state = seed & MASK64

    def next_u64(self) -> int:
        self.state = (self.state + SPLITMIX64_GAMMA) & MASK64
        z = self.state
        z = ((z ^ (z >> 30)) * SPLITMIX64_MUL1) & MASK64
        z = ((z ^ (z >> 27)) * SPLITMIX64_MUL2) & MASK64
        return (z ^ (z >> 31)) & MASK64


def integer_nth_root_floor(value: int, degree: int) -> int:
    if value < 0 or degree < 1:
        raise ValueError("integer_nth_root_floor requires value>=0 and degree>=1")
    low, high = 0, 1
    while high**degree <= value:
        high *= 2
    while low + 1 < high:
        middle = (low + high) // 2
        if middle**degree <= value:
            low = middle
        else:
            high = middle
    return low


def floor_rational_power(base: int, exponent: Fraction) -> int:
    if base < 1 or exponent < 0:
        raise ValueError("base must be positive and exponent nonnegative")
    return integer_nth_root_floor(base**exponent.numerator, exponent.denominator)


def scale_row(n_value: int) -> dict[str, int]:
    return {label: floor_rational_power(n_value, exponent) for label, exponent in EXPONENTS.items()}


def expected_scale_rows() -> dict[int, dict[str, int]]:
    rows = {n_value: scale_row(n_value) for n_value in N_VALUES}
    expected = {
        256: {"H": 776, "R": 84, "Q": 9, "V": 48, "rational_height": 27, "cubic": 467373274},
        512: {"H": 1782, "R": 147, "Q": 12, "V": 78, "rational_height": 42, "cubic": 5667243323},
        1024: {"H": 4096, "R": 256, "Q": 16, "V": 128, "rational_height": 64, "cubic": 68719476736},
        2048: {"H": 9410, "R": 445, "Q": 21, "V": 207, "rational_height": 97, "cubic": 833273994645},
    }
    if rows != expected:
        raise RuntimeError("finite analogue scale rounding mismatch")
    return rows


def scheduled_rows() -> list[dict[str, object]]:
    """Return the 160 rows in the sole seed-consumption order."""
    stream = SplitMix64(MASTER_SEED)
    rows: list[dict[str, object]] = []
    row_number = 0
    for n_value in N_VALUES:
        for family in FAMILY_ORDER:
            for variant in FAMILY_VARIANTS[family]:
                for replicate in REPLICATES:
                    rows.append({
                        "row_number": row_number,
                        "id": f"N{n_value}-{family}-{variant['id']}-R{replicate}",
                        "N": n_value,
                        "family": family,
                        "variant": dict(variant),
                        "replicate": replicate,
                        "row_seed": f"0x{stream.next_u64():016X}",
                    })
                    row_number += 1
    if len(rows) != 160 or len({str(row["id"]) for row in rows}) != 160:
        raise RuntimeError("finite analogue schedule must contain exactly 160 unique rows")
    if row_number != 4 * 5 * 4 * 2:
        raise RuntimeError("finite analogue schedule factorization mismatch")
    return rows


def frozen_thresholds() -> dict[str, str]:
    return {
        "large_value": "min(t in W)|D_b(t)| >= (1+0.05)*(3/4)*N^(7/10)",
        "energy": "(1+0.05)*(1/4)*N^2 <= E_H(W) <= 4*N^2/(1+0.05)",
        "rational_height": "Farey-node |R_W(x)| threshold is (1+0.05)*(3/4)*N^(3/5)",
        "rational_measure": "mu_32 >= (1+0.05)*(1/5)*N^(-2/5)",
        "cubic": "C_8,C_12 > 0 and C_12 >= (1+0.05)*(1/20)*N^(18/5)",
        "recognition_radius": "every retained final value has empirical recognition-ball radius < 10^(-30)*N^(7/10)",
    }

