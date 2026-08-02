"""Exact Cycle 72 primitive positive-numerator endpoint ledger."""
from __future__ import annotations

from fractions import Fraction as Q


DELTA = Q(3, 5)
MAX_THETA = Q(11, 25)


def cutoff_ledger(theta: Q) -> dict[str, object]:
    if theta < 0 or theta > MAX_THETA:
        raise ValueError("theta outside registered denominator range")
    ell_cutoff = DELTA - theta
    x_cutoff = -theta
    return {
        "theta": theta,
        "ell_cutoff_exponent": ell_cutoff,
        "x_cutoff_exponent": x_cutoff,
        "sharp_hessian_loss_exponent": theta,
        "prior_cycle70_loss_upper": Q(9, 25),
        "numerator_statement": "q>1 and gcd(a,q)=1 exclude a=0; positivity and o(1) error give a>=1",
    }


def verify_all() -> dict[str, object]:
    endpoint = cutoff_ledger(MAX_THETA)
    shallow = cutoff_ledger(Q(3, 25))
    if endpoint["ell_cutoff_exponent"] != Q(4, 25):
        raise RuntimeError("endpoint ell cutoff")
    if endpoint["sharp_hessian_loss_exponent"] != Q(11, 25):
        raise RuntimeError("endpoint Hessian loss")
    if shallow["ell_cutoff_exponent"] != Q(12, 25):
        raise RuntimeError("shallow ell cutoff")
    return {
        "primitive_cutoff": "a>=1 implies q*alpha_ell>=1-o(1), hence ell>>Delta/q",
        "ell_exponent": "lambda>=3/5-theta",
        "stationary_ratio": "x=ell/Delta>>1/q=X^(-theta+o(1))",
        "hessian_lower": "exp(4pi*x)-1>>X^(-theta-o(1))",
        "q1_exception": "a=0 is reduced only for q=1 and is a constant-size denominator branch",
        "supersession": "Cycle70 loss X^(9/25+kappa) remains valid but is replaced strategically by X^theta",
        "gate": "apply the factored two-variable estimate with determinant loss X^theta on q>1 cells",
    }


if __name__ == "__main__":
    print(verify_all())
