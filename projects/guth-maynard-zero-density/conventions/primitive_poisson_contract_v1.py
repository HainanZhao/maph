"""Exact Cycle 66 primitive Möbius--Poisson exponent contract."""
from __future__ import annotations

from fractions import Fraction as Q


DELTA = Q(3, 5)
ADMISSIBLE_TOTAL = Q(11, 25)
PACKET_TARGET_BASE = Q(6, 25)


def scale_contract(theta: Q, kappa: Q) -> dict[str, object]:
    if theta < 0 or kappa < 0:
        raise ValueError("scale exponents must be nonnegative")
    packet_target = PACKET_TARGET_BASE - kappa
    diagonal = DELTA + theta - kappa - 1
    prefactor = -1 - kappa
    raw_off_diagonal_target = packet_target - prefactor
    frequency_ceiling = 1 + theta + kappa
    return {
        "theta": theta,
        "kappa": kappa,
        "admissible": theta + kappa <= ADMISSIBLE_TOTAL,
        "packet_count_target_exponent_open": packet_target,
        "poisson_prefactor_exponent": prefactor,
        "diagonal_exponent": diagonal,
        "diagonal_margin_to_target": packet_target - diagonal,
        "raw_off_diagonal_target_exponent_open": raw_off_diagonal_target,
        "frequency_ceiling_exponent": frequency_ceiling,
    }


def verify_all() -> dict[str, object]:
    boundary = scale_contract(Q(11, 25), Q(0))
    deep = scale_contract(Q(1, 5), Q(6, 25))
    if boundary["diagonal_margin_to_target"] != Q(1, 5):
        raise RuntimeError("boundary diagonal margin")
    if deep["diagonal_margin_to_target"] != Q(11, 25):
        raise RuntimeError("deep diagonal margin")
    if boundary["raw_off_diagonal_target_exponent_open"] != Q(31, 25):
        raise RuntimeError("scale-invariant raw target")
    if deep["raw_off_diagonal_target_exponent_open"] != Q(31, 25):
        raise RuntimeError("deep raw target")
    if boundary["frequency_ceiling_exponent"] != Q(36, 25):
        raise RuntimeError("frequency ceiling")
    return {
        "identity": {
            "coprimality": "1_gcd(a,q)=1=sum_(b|a,b|q)mu(b)",
            "majorant": "f_C(u)=A_C*sinc(u/(2C))^4>=1 for |u|<=C",
            "poisson": "sum_a' f_C(b*K*X*(q'*alpha-a'))=(b*K*X)^-1 sum_r fhat_C(r/(b*K*X))*e(r*q'*alpha)",
            "primitive_form": "(KX)^-1 sum_(b,q': bq'~Q) mu(b)/b sum_r fhat_C(r/(bKX)) sum_ell e(rq'alpha_ell)",
        },
        "exponents": {
            "packet_target": "6/25-kappa",
            "diagonal": "theta-kappa-2/5",
            "diagonal_margin": "16/25-theta>=1/5",
            "raw_off_diagonal_target": "31/25 independent of theta,kappa",
            "frequency_ceiling": "1+theta+kappa<=36/25",
        },
        "analytic_gate": "bound the signed primitive Mobius-Poisson off-diagonal by X^(31/25-epsilon), or extract its structured major arcs",
    }


if __name__ == "__main__":
    print(verify_all())
