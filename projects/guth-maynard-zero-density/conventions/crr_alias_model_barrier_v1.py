"""Pinned parameters and exact scale checks for the CRR alias-model barrier.

This is an analytic countermodel to an implication using only generic node
spacing, real additive energy, and width-``H**-1`` smoothing.  It deliberately
does not specify a Dirichlet-polynomial coefficient sequence, a Farey net, or
a CRR witness.
"""
from __future__ import annotations

from fractions import Fraction


MIN_Q = 256
BLOCK_DIVISOR = 64
BLOCK_STEP = 8
JITTER_WIDTH_MULTIPLIER = 2
ALIAS_DILATION = 1024
BLOCK_LENGTH_MULTIPLIER = 64
HEIGHT_FACTOR = 16 * ALIAS_DILATION * BLOCK_LENGTH_MULTIPLIER
ALIAS_CYCLES = ALIAS_DILATION // 128


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def scales(q: int) -> dict[str, int]:
    """Return the exact finite parameters for an admissible integer q."""
    require(isinstance(q, int) and q >= MIN_Q, f"q must be an integer at least {MIN_Q}")
    m = q // BLOCK_DIVISOR
    K = q * q
    L = BLOCK_LENGTH_MULTIPLIER * q
    H = HEIGHT_FACTOR * q**3
    result = {
        "q": q,
        "m": m,
        "K": K,
        "L": L,
        "C": ALIAS_DILATION,
        "H": H,
        "R": m * L,
        "A_max_upper": BLOCK_STEP * q * (m - 1) + JITTER_WIDTH_MULTIPLIER * q - 1,
        "minimum_A_gap": (BLOCK_STEP - JITTER_WIDTH_MULTIPLIER) * q + 1,
    }
    require(BLOCK_STEP * q * m + JITTER_WIDTH_MULTIPLIER * q <= K // 4, "A containment bound failed")
    require(result["A_max_upper"] < K // 4, "A must lie below K/4")
    require(result["minimum_A_gap"] >= 6 * q, "hard-core gap bound failed")
    require(H == 16 * ALIAS_DILATION * K * L, "height normalization mismatch")
    require(q * q // 2 <= result["R"] <= q * q, "cardinality scale mismatch")
    return result


def interval_energy(length: int) -> int:
    """Exact additive energy of {0,...,length-1} in the integers."""
    require(isinstance(length, int) and length >= 1, "interval length must be positive")
    value = (2 * length**3 + length) // 3
    require(3 * value == 2 * length**3 + length, "interval energy integrality mismatch")
    return value


def energy_expectation_upper(q: int) -> Fraction:
    """Expected energy upper bound for the independent jittered A construction."""
    data = scales(q)
    m = data["m"]
    jitter_width = JITTER_WIDTH_MULTIPLIER * q
    index_energy = Fraction(2 * m**3 + m, 3)
    trivial_energy = 2 * m * m - m
    bound = Fraction(trivial_energy) + index_energy / jitter_width
    require(bound <= 3 * m * m, "probabilistic small-energy bound failed")
    return bound


def exponent_rows() -> dict[str, Fraction]:
    """Exact q-exponents of the alias construction's scale quantities."""
    rows = {
        "K": Fraction(2),
        "L": Fraction(1),
        "H": Fraction(3),
        "cardinality_R": Fraction(2),
        "real_energy": Fraction(5),
        "alias_amplitude": Fraction(3, 2),
        "alias_packet_measure": Fraction(-1),
        "first_smoothed_moment": Fraction(2),
        "second_smoothed_moment": Fraction(5),
    }
    require(rows["cardinality_R"] == rows["L"] + 1, "cardinality exponent mismatch")
    require(rows["real_energy"] == 2 + 3 * rows["L"], "energy exponent mismatch")
    require(rows["alias_amplitude"] == rows["L"] + Fraction(1, 2), "amplitude exponent mismatch")
    require(rows["alias_packet_measure"] == rows["K"] - rows["H"], "packet-measure exponent mismatch")
    require(rows["first_smoothed_moment"] == rows["alias_packet_measure"] + 2 * rows["alias_amplitude"], "first moment exponent mismatch")
    require(rows["second_smoothed_moment"] == rows["alias_packet_measure"] + 4 * rows["alias_amplitude"], "second moment exponent mismatch")
    return rows


def alias_count_lower(q: int) -> Fraction:
    """The integral lower bound from Parseval and Paley--Zygmund counting."""
    data = scales(q)
    K = data["K"]
    # E_K(A)<=3m^2 gives at least K/12 good residues; eight full alias
    # cycles give at least 2K/3 node indices.
    value = Fraction(2 * K, 3)
    require(value > 0, "Paley--Zygmund alias lower bound must be positive")
    return value

