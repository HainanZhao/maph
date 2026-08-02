"""Exact Cycle 70 factored stationary-Hessian ledger."""
from __future__ import annotations

from fractions import Fraction as Q


DELTA = Q(3, 5)
PACKET_TARGET_BASE = Q(6, 25)
MAX_KAPPA = Q(6, 25)


def endpoint_ledger(kappa: Q) -> dict[str, object]:
    if kappa < 0 or kappa > MAX_KAPPA:
        raise ValueError("kappa outside the shallow/critical registered range")
    packet_target = PACKET_TARGET_BASE - kappa
    weakest_ratio_exponent = packet_target - DELTA
    return {
        "kappa": kappa,
        "packet_target_exponent_open": packet_target,
        "automatic_small_ell_cutoff_exponent": packet_target,
        "weakest_surviving_x_exponent": weakest_ratio_exponent,
        "weakest_hessian_exponent": weakest_ratio_exponent,
        "factored_hessian": "det Hess_(r,q') Psi(rq',k)=(u/(rq'))^2-1=exp(4*pi*x)-1",
    }


def verify_all() -> dict[str, object]:
    shallow = endpoint_ledger(Q(0))
    critical = endpoint_ledger(MAX_KAPPA)
    if shallow["weakest_hessian_exponent"] != -Q(9, 25):
        raise RuntimeError("shallow curvature loss")
    if critical["weakest_hessian_exponent"] != -Q(3, 5):
        raise RuntimeError("critical curvature loss")
    return {
        "derivative_identity": {
            "psi_prime": "u/m-1",
            "psi_second": "-u/m^2",
            "product_hessian": "det=-(psi')^2-2m psi' psi''=(u/m)^2-1",
            "stationary_value": "u/m=exp(2*pi*x)",
        },
        "nondegeneracy": "positive for every x>0; asymptotic to 4*pi*x as x tends to zero",
        "small_ell_branch": "ell blocks with lambda<6/25-kappa contain fewer packets than the target by uniqueness alone",
        "surviving_curvature": "on lambda>=6/25-kappa, determinant exponent is at least -9/25-kappa",
        "gate": "prove a two-variable factored exponential-sum estimate with determinant loss X^(9/25+kappa), or improve the small-endpoint split",
    }


if __name__ == "__main__":
    print(verify_all())
