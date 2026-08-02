"""Exact residual spectral-shift conventions, Cycle 23."""
from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def critical_exponents() -> dict[str, Fraction]:
    rows = Q(21, 25)
    normalized_projection = Q(-3, 5)
    shift = rows + normalized_projection
    require(shift == Q(6, 25), "residual shift exponent mismatch")
    return {
        "rows": rows,
        "rho": normalized_projection,
        "k_rho": shift,
        "inverse_leverage_log_scale": shift,
    }


def finite_diagonal_residual() -> dict[str, Fraction | int]:
    k = 4
    rho = Q(1, 4)
    residual_diagonal = 1 - rho
    leverage = Q(k) * rho / residual_diagonal
    product_factor = residual_diagonal**k
    determinant_ratio = product_factor * (1 + leverage)
    direct_residual_eigenvalue = residual_diagonal
    direct_top_eigenvalue = residual_diagonal + k * rho
    direct_determinant = direct_residual_eigenvalue ** (k - 1) * direct_top_eigenvalue
    require(leverage == Q(4, 3), "finite leverage mismatch")
    require(determinant_ratio == direct_determinant, "determinant lemma mismatch")
    require(direct_top_eigenvalue == Q(7, 4), "top eigenvalue mismatch")
    return {
        "k": k,
        "rho": rho,
        "residual_diagonal": residual_diagonal,
        "normalized_residual_B_diagonal": Q(1),
        "inverse_leverage": leverage,
        "product_factor": product_factor,
        "determinant_ratio": determinant_ratio,
        "direct_residual_eigenvalue": direct_residual_eigenvalue,
        "direct_top_eigenvalue": direct_top_eigenvalue,
        "direct_determinant": direct_determinant,
    }


def verify_all() -> dict[str, object]:
    return {
        "critical_exponents": critical_exponents(),
        "finite_diagonal_residual": finite_diagonal_residual(),
        "residual_identity": "Z=H-qq*=U(I-aa*/A)U*/M",
        "determinant_identity": "det(H)/det(B)=product_t(1-rho_t)[1+s*B^-1s]",
        "small_leverage_branch": "L<=exp(epsilon k rho) implies shift<=-(1-epsilon)k rho+log 2",
        "large_leverage_branch": "shift>-c k rho implies L>=exp((1-c)k rho)-1",
        "singular_branch": "if Z is singular, record RESIDUAL_SINGULAR and do not invoke B^-1",
    }
