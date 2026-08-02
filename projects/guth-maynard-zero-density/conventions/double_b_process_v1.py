"""Exact Cycle 79 double-B-process geometry and exponent contract."""
from __future__ import annotations

from fractions import Fraction as Q


D_EXP = Q(3, 5)
Q_EXP = Q(1, 3)
ETA_EXP = -Q(83, 75)
COUNT_TARGET = Q(2, 15)
K_MAX = -ETA_EXP
RAW_TARGET = COUNT_TARGET - ETA_EXP
LOW_K_CUTOFF = D_EXP - Q_EXP


Matrix2 = tuple[tuple[Q, Q], tuple[Q, Q]]


def det2(matrix: Matrix2) -> Q:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def primal_hessian(beta: Q, dual_r: Q, q: Q, d_scale: Q) -> Matrix2:
    """Hessian of k*c*q*exp(beta*d/D), expressed at r=partial_q phi."""
    if min(beta, dual_r, q, d_scale) <= 0:
        raise ValueError("positive parameters required")
    dd = beta**2 * dual_r * q / d_scale**2
    dq = beta * dual_r / d_scale
    return ((dd, dq), (dq, Q(0)))


def dual_hessian(legendre_scale: Q, k: Q, dual_r: Q) -> Matrix2:
    """Hessian in (k,r) of A*log(k*c/r), with A=hD/beta."""
    if min(legendre_scale, k, dual_r) <= 0:
        raise ValueError("positive parameters required")
    return ((-legendre_scale / k**2, Q(0)), (Q(0), legendre_scale / dual_r**2))


def exponent_ledger(k_exponent: Q) -> dict[str, object]:
    if k_exponent < 0 or k_exponent > K_MAX:
        raise ValueError("Fourier exponent outside support")
    h_exponent = k_exponent + Q_EXP - D_EXP
    return {
        "k_exponent": k_exponent,
        "r_exponent": k_exponent,
        "h_exponent": h_exponent,
        "positive_h_stationary": h_exponent >= 0,
        "stationary_amplitude_exponent": D_EXP - k_exponent,
        "dual_phase_variation_exponent": k_exponent + Q_EXP,
    }


def verify_all() -> dict[str, object]:
    beta, r, q, d_scale = Q(7, 5), Q(11, 4), Q(9, 7), Q(13, 3)
    primal = primal_hessian(beta, r, q, d_scale)
    if det2(primal) != -(beta * r / d_scale) ** 2:
        raise RuntimeError("primal determinant")
    scale, k = Q(8, 3), Q(5, 2)
    dual = dual_hessian(scale, k, r)
    if det2(dual) != -scale**2 / (k**2 * r**2):
        raise RuntimeError("dual determinant")
    top = exponent_ledger(K_MAX)
    boundary = exponent_ledger(LOW_K_CUTOFF)
    if RAW_TARGET != Q(31, 25):
        raise RuntimeError("raw Fourier target")
    if top["h_exponent"] != Q(21, 25):
        raise RuntimeError("dual h ceiling")
    if boundary["h_exponent"] != 0:
        raise RuntimeError("low-frequency boundary")
    low_trivial = LOW_K_CUTOFF + D_EXP + Q_EXP
    low_margin = RAW_TARGET - low_trivial
    if low_trivial != Q(6, 5) or low_margin != Q(1, 25):
        raise RuntimeError("low-frequency trivial closure")
    return {
        "fourier_contract": "N<<eta*(D*Q+sum_(1<=k<=eta^-1)|S_k|); require L1 exponent <31/25",
        "stationary_map": "r=k*c0*exp(beta*d/D), h=beta*q*r/D",
        "inverse_map": "d=(D/beta)log(r/(k*c0)), q=hD/(beta*r)",
        "primal_determinant": "-(beta*r/D)^2",
        "stationary_amplitude": "D/(beta*r)",
        "dual_phase": "Psi=(hD/beta)log(k*c0/r)",
        "dual_determinant": "-(hD/beta)^2/(k^2*r^2)",
        "dual_support": "r~k, h~kQ/D; h_max=X^(21/25+o(1))",
        "low_frequency": "k<D/Q=X^(4/15) is trivially <=X^(6/5), margin 1/25 to raw target",
        "gate": "control stationary remainders and prove cancellation in the high-frequency dual logarithmic saddle",
    }


if __name__ == "__main__":
    print(verify_all())
