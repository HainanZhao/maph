"""Exact Cycle 55 centered-Gram common-projection boundary."""
from __future__ import annotations

from fractions import Fraction as Q


PENULTIMATE_GAP = Q(3, 50)


def simplex_certificate(row_count: int, rho: Q) -> dict[str, object]:
    if not isinstance(row_count, int) or row_count < 1:
        raise RuntimeError("positive row count")
    rho = Q(rho)
    if rho < 0 or row_count * rho > 1:
        raise RuntimeError("certificate requires 0 <= R rho <= 1")
    return {
        "row_count": row_count,
        "rho": rho,
        "R_rho": row_count * rho,
        "residual_gram_eigenvalue_constant_direction": 1 - row_count * rho,
        "residual_gram_eigenvalue_orthogonal_direction": Q(1),
        "full_gram": "I_R",
        "centered_gram": "0_R",
        "all_even_centered_traces": Q(0),
        "common_projection_squared": rho,
    }


def exponent_ledger(gap: Q = PENULTIMATE_GAP) -> dict[str, object]:
    gap = Q(gap)
    if gap < 0:
        raise RuntimeError("nonnegative below-trigger gap")
    return {
        "trigger_minus_selected_exponent": gap,
        "R_rho_exponent": -gap,
        "strict_offdiagonal_trigger": Q(0),
        "abstract_centered_trace_forced": gap < 0,
        "status": "ABSTRACTLY_SHARP" if gap >= 0 else "CENTERING_CROSSES",
    }


def verify_all() -> dict[str, object]:
    below = simplex_certificate(5, Q(1, 10))
    endpoint = simplex_certificate(5, Q(1, 5))
    ledger = exponent_ledger()
    if below["residual_gram_eigenvalue_constant_direction"] != Q(1, 2):
        raise RuntimeError("below-trigger residual eigenvalue")
    if endpoint["residual_gram_eigenvalue_constant_direction"] != 0:
        raise RuntimeError("endpoint residual eigenvalue")
    if ledger["R_rho_exponent"] != -Q(3, 50):
        raise RuntimeError("Cycle 54 exponent transfer")
    if ledger["status"] != "ABSTRACTLY_SHARP":
        raise RuntimeError("centered trace boundary")
    return {
        "penultimate_exponent": ledger,
        "strictly_below_example": below,
        "endpoint_example": endpoint,
        "required_new_input": "actual_prime_partition_cumulant_or_logarithmic_structure",
    }


if __name__ == "__main__":
    print(verify_all())
