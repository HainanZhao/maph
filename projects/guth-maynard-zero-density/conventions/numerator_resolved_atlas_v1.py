"""Exact Cycle 73 numerator-resolved packet and curvature ledger."""
from __future__ import annotations

from fractions import Fraction as Q


DELTA = Q(3, 5)
TARGET_BASE = Q(6, 25)
PAIR_WEIGHT_BASE = Q(11, 25)
PAIR_TARGET = Q(17, 25)


def numerator_cell(theta: Q, kappa: Q, alpha: Q) -> dict[str, object]:
    if min(theta, kappa, alpha) < 0 or alpha > theta or theta + kappa > Q(11, 25):
        raise ValueError("cell outside numerator-resolved atlas")
    count = theta + alpha
    target = TARGET_BASE - kappa
    ell_scale = DELTA + alpha - theta
    hessian_exponent = alpha - theta
    pair_bound = PAIR_WEIGHT_BASE + kappa + count
    return {
        "theta": theta,
        "kappa": kappa,
        "alpha": alpha,
        "fraction_count_exponent": count,
        "packet_target_exponent_open": target,
        "strict_margin": target - count,
        "strictly_closed": count < target,
        "ell_exponent": ell_scale,
        "hessian_exponent": hessian_exponent,
        "hessian_loss_exponent": theta - alpha,
        "weighted_pair_bound_exponent": pair_bound,
        "weighted_pair_target_open": PAIR_TARGET,
    }


def verify_all() -> dict[str, object]:
    bounded_numerator = numerator_cell(Q(1, 5), Q(0), Q(0))
    bulk = numerator_cell(Q(1, 5), Q(0), Q(1, 5))
    boundary = numerator_cell(Q(1, 5), Q(1, 25), Q(0))
    if not bounded_numerator["strictly_closed"] or bounded_numerator["strict_margin"] != Q(1, 25):
        raise RuntimeError("bounded-numerator closure")
    if bulk["strictly_closed"] or bulk["hessian_loss_exponent"] != 0:
        raise RuntimeError("bulk cell")
    if boundary["strict_margin"] != 0 or boundary["strictly_closed"]:
        raise RuntimeError("boundary tie")
    if bounded_numerator["ell_exponent"] != Q(2, 5):
        raise RuntimeError("ell/numerator relation")
    return {
        "cell_count": "N(theta,kappa,alpha)<=X^(theta+alpha+o(1))",
        "closed_region": "theta+alpha+kappa<6/25",
        "boundary": "theta+alpha+kappa=6/25 ties",
        "scale_relation": "alpha=theta+lambda-3/5",
        "hessian": "det asymp ell/Delta asymp a/q=X^(alpha-theta)",
        "hessian_loss": "theta-alpha",
        "weighted_pair": "11/25+kappa+theta+alpha<17/25 on the same open region",
        "residual_atlas": "theta+alpha+kappa>=6/25, 0<=alpha<=theta, theta+kappa<=11/25",
        "gate": "apply factored curvature only on the numerator-resolved residual atlas",
    }


if __name__ == "__main__":
    print(verify_all())
