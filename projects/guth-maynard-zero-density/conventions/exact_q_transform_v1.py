"""Frozen algebra and exponent ledger for Cycle 81."""

from fractions import Fraction

Q = Fraction

D_EXP = Q(3, 5)
Q_EXP = Q(1, 3)
CURRENT_XI = Q(163, 450)
MAX_XI = Q(83, 75)
RAW_L1_TARGET = Q(31, 25)
BETA_NAME = "2*pi"


def dual_support(xi: Fraction) -> dict[str, Fraction]:
    """Exponent support of the central (h,r) chart."""
    return {
        "r": xi,
        "h": xi + Q_EXP - D_EXP,
        "amplitude": D_EXP - xi,
    }


def central_error_ledger(xi: Fraction) -> dict[str, Fraction]:
    """Sum D/(Q r^2) over r~X^xi and h~X^(xi+Q-D)."""
    support = dual_support(xi)
    per_cell = D_EXP - Q_EXP - 2 * xi
    total = per_cell + support["r"] + support["h"]
    return {
        "per_cell": per_cell,
        "r_count": support["r"],
        "h_count": support["h"],
        "per_k_total": total,
    }


def transform_formula() -> dict[str, str]:
    return {
        "fourier": "hatV(y)=int V(t)e(-y*t)dt; V(a)=int hatV(y)e(a*y)dy",
        "u": "u=k*c0*exp(beta*d/D)",
        "y": "y=Q*(u-r)",
        "x_r": "x_r=beta^(-1)*log(r/(k*c0))",
        "a": "a=h*D/(beta*Q*r)",
        "exact_kernel": (
            "D/(beta*r)*e((h*D/beta)*log(k*c0/r))*"
            "int hatV(-y)*[r/(r+y/Q)]*"
            "W(x_r+beta^(-1)*log(1+y/(Q*r)))*"
            "e(-(h*D/beta)*log(1+y/(Q*r)))dy"
        ),
        "leading": (
            "D/(beta*r)*W(x_r)*V(a)*"
            "e((h*D/beta)*log(k*c0/r))"
        ),
        "central_error": "O_(W,V)(D/(Q*r^2))",
    }


def verify_all() -> dict[str, object]:
    formulas = transform_formula()
    current = central_error_ledger(CURRENT_XI)
    ceiling = central_error_ledger(MAX_XI)
    assert current["per_k_total"] == 0
    assert ceiling["per_k_total"] == 0
    assert MAX_XI + ceiling["per_k_total"] == MAX_XI
    margin = RAW_L1_TARGET - MAX_XI
    assert margin == Q(2, 15)
    assert dual_support(MAX_XI)["h"] == Q(21, 25)
    assert "V(a)" in formulas["leading"]
    assert "log(k*c0/r)" in formulas["leading"]
    return {
        "fourier_convention": formulas["fourier"],
        "exact_kernel": formulas["exact_kernel"],
        "leading_term": formulas["leading"],
        "central_error": formulas["central_error"],
        "per_k_error_exponent": str(ceiling["per_k_total"]),
        "accumulated_error_exponent": str(MAX_XI),
        "raw_target": str(RAW_L1_TARGET),
        "strict_margin": str(margin),
        "h_ceiling": str(dual_support(MAX_XI)["h"]),
        "gate": "stationary remainder removed; logarithmic dual cancellation open",
    }


if __name__ == "__main__":
    print(verify_all())

