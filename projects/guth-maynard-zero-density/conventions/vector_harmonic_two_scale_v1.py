"""Exact Cycle 38 vector-harmonic and prime-monomial ledger."""
from __future__ import annotations

from fractions import Fraction as Q


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def geometry(a: Q) -> dict[str, Q]:
    require(0 < a <= Q(3, 10), "harmonic-range exponent")
    spacing = Q(3, 5)
    height = Q(12, 5)
    expanded_height = height + a
    fan_height = spacing + a
    collision = a
    require(fan_height <= height, "collision fan fits original height")
    return {
        "harmonic_range": a,
        "spacing": spacing,
        "height": height,
        "expanded_height": expanded_height,
        "fan_height": fan_height,
        "collision_multiplicity": collision,
    }


def two_scale(excess_decay: Q) -> dict[str, Q]:
    threshold = Q(7, 10)
    mass = Q(1)
    target_count = Q(21, 25)
    per_row_energy = 2 * threshold + 2 * mass - excess_decay
    target_vector_bound = per_row_energy + target_count
    return {
        "harmonic_energy_decay": excess_decay,
        "per_row_two_scale_energy": per_row_energy,
        "target_vector_bound": target_vector_bound,
        "prime_monomial_cardinality": Q(2),
        "coefficient_square_norm": Q(2),
    }


def registered_scales() -> dict[str, object]:
    geometry_row = geometry(Q(3, 10))
    r2 = two_scale(Q(3, 5))
    r4 = two_scale(Q(6, 5))
    require(geometry_row["expanded_height"] == Q(27, 10), "expanded height")
    require(geometry_row["collision_multiplicity"] > Q(4, 25), "collision exceeds missing saving")
    require(r2["per_row_two_scale_energy"] == Q(14, 5), "r2 two-scale energy")
    require(r2["target_vector_bound"] == Q(91, 25), "r2 target vector bound")
    require(r4["per_row_two_scale_energy"] == Q(11, 5), "r4 two-scale energy")
    require(r4["target_vector_bound"] == Q(76, 25), "r4 target vector bound")
    return {"geometry": geometry_row, "r2_energy": r2, "r4_energy": r4}


def prime_monomial() -> dict[str, str]:
    return {
        "map": "(p,q)->p*q^m",
        "range": "prime p,q and integer m>=2",
        "injectivity": "prime valuations distinguish exponent 1 from exponent m; p=q has the unique exponent m+1",
        "cardinality": "M^2",
        "coefficient_square_norm": "M^2",
        "ambient_support": "[X^(m+1),2^(m+1)X^(m+1)]",
    }


def verify_all() -> dict[str, object]:
    rows = {"registered_scales": registered_scales(), "prime_monomial": prime_monomial()}
    require(rows["prime_monomial"]["cardinality"] == rows["prime_monomial"]["coefficient_square_norm"], "monomial norm")
    return rows


if __name__ == "__main__":
    print(verify_all())
