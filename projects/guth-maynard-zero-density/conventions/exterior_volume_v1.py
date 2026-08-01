"""Exact exterior-volume conventions, Cycle 20."""
from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def critical_exponents() -> dict[str, Fraction]:
    norm = Q(1)
    threshold = Q(7, 10)
    rows = Q(21, 25)
    w = 2 * threshold - norm
    rho = w - norm
    collapse = rows + rho
    require(w == Q(2, 5), "projection scale mismatch")
    require(rho == Q(-3, 5), "normalized correlation mismatch")
    require(collapse == Q(6, 25), "volume-collapse exponent mismatch")
    return {
        "A": norm,
        "M": norm,
        "V": threshold,
        "w": w,
        "rho": rho,
        "rows": rows,
        "k_rho": collapse,
        "sufficient_lower_bound_exponent_strictly_below": collapse,
    }


def sharp_finite_model() -> dict[str, Fraction | int]:
    k = 9
    A = Q(25)
    M = Q(16)
    w = Q(4)
    V_squared = A * w
    rho = w / M
    top = k * w
    residual = Q(k) * (M - w) / (k - 1)
    diagonal = residual + (top - residual) / k
    normalized_determinant = (top / M) * (residual / M) ** (k - 1)
    formula = Q(k) * rho * (Q(k) * (1 - rho) / (k - 1)) ** (k - 1)
    minimum_witness_norm = V_squared * k / top
    require(top >= M, "finite model is outside determinant-collapse regime")
    require(diagonal == M, "sharp Gram model has wrong diagonal")
    require(residual > 0, "sharp Gram model is not positive definite")
    require(normalized_determinant == formula, "determinant formula mismatch")
    require(minimum_witness_norm == A, "common-projection witness norm mismatch")
    return {
        "k": k,
        "A": A,
        "M": M,
        "w": w,
        "V_squared": V_squared,
        "rho": rho,
        "top_eigenvalue": top,
        "residual_eigenvalue": residual,
        "diagonal": diagonal,
        "normalized_determinant": normalized_determinant,
        "collapse_formula": formula,
        "minimum_witness_norm_squared": minimum_witness_norm,
    }


def verify_all() -> dict[str, object]:
    return {
        "critical_exponents": critical_exponents(),
        "sharp_finite_model": sharp_finite_model(),
        "determinant_theorem": "det(G)/M^k <= k rho [k(1-rho)/(k-1)]^(k-1) when kw>=M",
        "log_bound": "log D <= log(k rho)+1-(k-1)rho",
        "cauchy_binet": "det(UU*)=sum_(|S|=k)|det(U_S)|^2",
        "prime_gate": "a uniform normalized determinant lower bound exp(-X^(theta+o(1))) with theta<6/25 implies the target skeleton bound",
    }
