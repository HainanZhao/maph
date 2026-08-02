"""Exact detector-reconstruction conventions for Cycle 26."""
from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def critical_exponents() -> dict[str, Fraction | str]:
    rows = Q(21, 25)
    rho = Q(-3, 5)
    k_rho = rows + rho
    leverage_fraction = Q(1, 4)
    reconstruction_error_fraction = leverage_fraction / 2
    require(k_rho == Q(6, 25), "critical reconstruction scale mismatch")
    require(reconstruction_error_fraction == Q(1, 8), "reconstruction error constant mismatch")
    return {
        "rows": rows,
        "rho": rho,
        "k_rho": k_rho,
        "leverage_lower": "exp(k rho/4)/2",
        "leverage_exponent_fraction": leverage_fraction,
        "reconstruction_error_upper": "sqrt(2) exp(-k rho/8)",
        "reconstruction_error_exponent_fraction": reconstruction_error_fraction,
    }


def finite_positive_definite_check() -> dict[str, object]:
    # B=I_2, s=(1,2), c=B^{-1}s.  Take W=I_2, so c*W=(1,2).
    s = (Q(1), Q(2))
    c = s
    leverage = sum(x * x for x in s)
    common_coefficient = sum(c[i] * s[i] for i in range(2))
    residual_norm_squared = sum(x * x for x in c)
    normalized_error_squared = residual_norm_squared / (leverage * leverage)
    require(leverage == 5, "finite leverage mismatch")
    require(common_coefficient == leverage, "common reconstruction coefficient mismatch")
    require(residual_norm_squared == leverage, "residual norm identity mismatch")
    require(normalized_error_squared == Q(1, 5), "normalized reconstruction error mismatch")
    return {
        "B": ((Q(1), Q(0)), (Q(0), Q(1))),
        "s": s,
        "c": c,
        "L": leverage,
        "c_star_s": common_coefficient,
        "norm_c_star_W_squared": residual_norm_squared,
        "normalized_error_squared": normalized_error_squared,
    }


def finite_singular_split() -> dict[str, object]:
    # W=diag(1,0), hence ker(B)=span((0,1)).
    null_vector = (Q(0), Q(1))
    reconstructing_s = (Q(0), Q(2))
    annihilating_s = (Q(1), Q(0))
    reconstruction_coefficient = sum(null_vector[i] * reconstructing_s[i] for i in range(2))
    annihilation_coefficient = sum(null_vector[i] * annihilating_s[i] for i in range(2))
    require(reconstruction_coefficient == 2, "singular reconstruction branch mismatch")
    require(annihilation_coefficient == 0, "singular annihilation branch mismatch")
    return {
        "B": ((Q(1), Q(0)), (Q(0), Q(0))),
        "null_vector": null_vector,
        "reconstructing_s": reconstructing_s,
        "reconstruction_coefficient": reconstruction_coefficient,
        "annihilating_s": annihilating_s,
        "annihilation_coefficient": annihilation_coefficient,
    }


def verify_all() -> dict[str, object]:
    return {
        "critical_exponents": critical_exponents(),
        "positive_definite_check": finite_positive_definite_check(),
        "singular_split_check": finite_singular_split(),
        "matrix_identity": "D^(-1)X=s b*+W",
        "reconstruction_identity": "||(B^(-1)s)^*D^(-1)X/L-b*||=L^(-1/2)",
        "singular_identity": "c in ker(B) implies c*D^(-1)X=(c*s)b*",
    }
