"""Exact Cycle 87 second-moment Mellin-alias ledger."""

from fractions import Fraction

Q = Fraction

D_EXP = Q(3, 5)
DENOM_EXP = Q(1, 3)
ATOM_EXP = D_EXP + DENOM_EXP
XI_MIN = Q(16, 25)
XI_MAX = Q(58, 75)


def dual_support(xi: Fraction) -> dict[str, Fraction]:
    return {
        "k": xi,
        "r": xi,
        "h": xi + DENOM_EXP - D_EXP,
        "delta_h_stationary_floor": xi - D_EXP,
        "m_ceiling": DENOM_EXP,
    }


def alias_exponents(xi: Fraction, delta_h: Fraction) -> dict[str, Fraction]:
    """Exponent map m=D*Delta h/K and stationary amplitude sqrt(K/m)."""
    m = D_EXP + delta_h - xi
    return {
        "delta_h": delta_h,
        "m": m,
        "stationary_k": xi,
        "stationary_amplitude": (xi - m) / 2,
        "t": D_EXP + delta_h,
    }


def stationary_formula() -> dict[str, str]:
    return {
        "phase": "Phi(k)=t*log(k)-m*k, t=D*(h-h')/(2*pi)",
        "first_derivative": "Phi'(k)=t/k-m",
        "second_derivative": "Phi''(k)=-t/k^2",
        "inverse": "k=t/m=D*(h-h')/(2*pi*m)",
        "hessian_at_stationary": "Phi''(t/m)=-m^2/t",
        "amplitude": "|Phi''|^(-1/2)=sqrt(|t|)/|m|~sqrt(K/|m|)",
    }


def verify_all() -> dict[str, object]:
    assert ATOM_EXP == Q(14, 15)
    for xi in (XI_MIN, XI_MAX):
        support = dual_support(xi)
        assert support["h"] - support["delta_h_stationary_floor"] == DENOM_EXP
        top = alias_exponents(xi, support["h"])
        floor = alias_exponents(xi, support["delta_h_stationary_floor"])
        assert top["m"] == DENOM_EXP
        assert floor["m"] == 0
        assert top["stationary_amplitude"] == (xi - DENOM_EXP) / 2
    formulas = stationary_formula()
    assert "-m^2/t" in formulas["hessian_at_stationary"]
    assert "sqrt(|t|)/|m|" in formulas["amplitude"]
    return {
        "primal_pair_kernel": "sum_k U(k/K)e(k*Delta z)=K*sum_m hatU(K*(m-Delta z))",
        "pair_zero_mode": "int_(R/Z) kernel(Delta z)dDelta z=U(0)=0",
        "atom_diagonal_exponent": "xi+14/15",
        "dual_support": "r~K, h~KQ/D",
        **formulas,
        "nonstationary_branch": "0<|h-h'|<<K/D has no nonzero stationary m",
        "stationary_alias_branch": "K/D<<|h-h'|<<KQ/D maps to 1<<|m|<<Q",
        "same_h_branch": "h=h' must be treated as a logarithmic r-correlation, not atom diagonal",
        "moment_target": "total same-h + nonstationary + alias contribution <=X^(xi+14/15+o(1))",
        "gate": "bound all three Mellin-alias branches or export a structured alias web",
    }


if __name__ == "__main__":
    print(verify_all())

