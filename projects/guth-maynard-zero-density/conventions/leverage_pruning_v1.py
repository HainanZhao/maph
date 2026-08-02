"""Exact leverage-pruning and near-Cauchy conventions, Cycle 24."""
from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def critical_exponents() -> dict[str, Fraction]:
    rows = Q(21, 25)
    rho = Q(-3, 5)
    structure_scale = rows + rho
    require(structure_scale == Q(6, 25), "pruning structure exponent mismatch")
    return {
        "rows": rows,
        "rho": rho,
        "k_rho": structure_scale,
        "near_cauchy_deficit_exponential_scale": structure_scale,
        "small_eigenvalue_exponential_scale": structure_scale,
    }


def frozen_constants() -> dict[str, Fraction | str]:
    shift_fraction = Q(1, 2)
    delta_fraction = Q(1, 8)
    leverage_exponent = Q(1, 4)
    eigenvalue_exponent = Q(1, 8)
    require(leverage_exponent - delta_fraction == eigenvalue_exponent, "leverage/eigenvalue constants mismatch")
    return {
        "shift_fraction": shift_fraction,
        "delta": "exp(-k rho/8)",
        "delta_exponent_fraction": delta_fraction,
        "leverage_lower_exponent_fraction": leverage_exponent,
        "small_eigenvalue_exponent_fraction": eigenvalue_exponent,
        "large_k_condition": "k rho/4>=log 2",
    }


def finite_near_cauchy_check() -> dict[str, Fraction]:
    delta = Q(1, 8)
    rho_t = 1 - delta
    aligned_common = rho_t
    worst_residual = delta
    kernel_lower = aligned_common - worst_residual
    require(kernel_lower == 1 - 2 * delta, "near-Cauchy kernel lower bound mismatch")
    return {
        "delta": delta,
        "rho_t": rho_t,
        "aligned_common_term": aligned_common,
        "worst_residual_term": worst_residual,
        "kernel_lower": kernel_lower,
    }


def finite_regular_check() -> dict[str, Fraction | int]:
    k = 8
    n = 4
    delta = Q(1, 4)
    s_norm_upper = Q(k) / delta
    leverage_lower = Q(8)
    eigenvalue_upper = s_norm_upper / leverage_lower
    require(n >= k // 2, "regular subsystem too small")
    require(s_norm_upper == 32, "regular s-norm bound mismatch")
    require(eigenvalue_upper == 4, "finite eigenvalue implication mismatch")
    return {
        "k": k,
        "n": n,
        "delta": delta,
        "s_norm_squared_upper": s_norm_upper,
        "leverage_lower": leverage_lower,
        "lambda_min_upper": eigenvalue_upper,
    }


def verify_all() -> dict[str, object]:
    return {
        "critical_exponents": critical_exponents(),
        "frozen_constants": frozen_constants(),
        "finite_near_cauchy_check": finite_near_cauchy_check(),
        "finite_regular_check": finite_regular_check(),
        "trichotomy": "half-size near-Cauchy complete recurrence, shift<=-n rho/2, residual singularity, or lambda_min(B)<=2k exp(-k rho/8)",
    }
