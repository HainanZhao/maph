"""Exact Cycle 57 Hilbert-valued support-collapse ledger."""
from __future__ import annotations

from fractions import Fraction as Q
from math import factorial


def collapse_ledger(s: int, prime_count: int) -> dict[str, object]:
    if not isinstance(s, int) or s < 1:
        raise RuntimeError("positive ordinary-coordinate count")
    if not isinstance(prime_count, int) or prime_count < 2:
        raise RuntimeError("prime block has at least two elements")
    fiber_bound = (1 + s // 2) * factorial(s)
    raw_precollapse_energy = (prime_count - 1) ** (s + 1)
    raw_collapsed_upper = fiber_bound * raw_precollapse_energy
    normalized_precollapse_energy = Q(prime_count - 1, prime_count) ** (s + 1)
    normalized_collapsed_upper = fiber_bound * normalized_precollapse_energy
    return {
        "s": s,
        "prime_count": prime_count,
        "fiber_bound_uniform_m_ge_2": fiber_bound,
        "raw_precollapse_energy": raw_precollapse_energy,
        "raw_collapsed_energy_upper": raw_collapsed_upper,
        "normalized_precollapse_energy": normalized_precollapse_energy,
        "normalized_collapsed_energy_upper": normalized_collapsed_upper,
        "raw_energy_exponent_in_M": s + 1,
        "support_collapse_power_loss": Q(0),
        "status": "CONSTANT_COST",
    }


def verify_all() -> dict[str, object]:
    s3 = collapse_ledger(3, 5)
    s4 = collapse_ledger(4, 5)
    if s3["fiber_bound_uniform_m_ge_2"] != 12:
        raise RuntimeError("s3 fiber bound")
    if s4["fiber_bound_uniform_m_ge_2"] != 72:
        raise RuntimeError("s4 fiber bound")
    if s3["raw_precollapse_energy"] != 4**4:
        raise RuntimeError("s3 raw energy")
    if s4["raw_precollapse_energy"] != 4**5:
        raise RuntimeError("s4 raw energy")
    return {
        "s3": s3,
        "s4": s4,
        "uniform_statement": "sum_n||a_n||^2<=D_s sum_tau||c_tau||^2 for every m>=2",
        "analytic_gate": "prove_3_50_edge_cumulant_restriction_or_extract_two_scale_approximate_multiplicativity",
    }


if __name__ == "__main__":
    print(verify_all())
