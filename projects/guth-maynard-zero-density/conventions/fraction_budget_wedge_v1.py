"""Exact Cycle 71 primitive-fraction wedge ledger."""
from __future__ import annotations

from fractions import Fraction as Q


COUNT_TARGET_BASE = Q(6, 25)
PACKET_WEIGHT_BASE = Q(11, 25)
PAIR_TARGET = Q(17, 25)
ADMISSIBLE_TOTAL = Q(11, 25)


def fraction_cell(theta: Q, kappa: Q) -> dict[str, object]:
    if theta < 0 or kappa < 0 or theta + kappa > ADMISSIBLE_TOTAL:
        raise ValueError("cell outside admissible packet region")
    count_bound = 2 * theta
    count_target = COUNT_TARGET_BASE - kappa
    pair_bound = PACKET_WEIGHT_BASE + kappa + count_bound
    return {
        "theta": theta,
        "kappa": kappa,
        "primitive_fraction_count_exponent": count_bound,
        "packet_count_target_exponent_open": count_target,
        "strict_count_margin": count_target - count_bound,
        "weighted_pair_bound_exponent": pair_bound,
        "pair_target_exponent_open": PAIR_TARGET,
        "strictly_closed": count_bound < count_target,
        "closure_condition": "2*theta+kappa<6/25",
    }


def verify_all() -> dict[str, object]:
    interior = fraction_cell(Q(1, 10), Q(0))
    boundary = fraction_cell(Q(3, 25), Q(0))
    deep_interior = fraction_cell(Q(0), Q(1, 5))
    if not interior["strictly_closed"] or interior["strict_count_margin"] != Q(1, 25):
        raise RuntimeError("interior wedge")
    if boundary["strictly_closed"] or boundary["strict_count_margin"] != 0:
        raise RuntimeError("boundary tie")
    if not deep_interior["strictly_closed"] or deep_interior["strict_count_margin"] != Q(1, 25):
        raise RuntimeError("depth-axis wedge")
    if interior["weighted_pair_bound_exponent"] != Q(16, 25):
        raise RuntimeError("weighted pair margin")
    return {
        "fraction_count": "N(theta,kappa)<=sum_(q~Q)O(q)=X^(2theta+o(1))",
        "closed_wedge": "2theta+kappa<6/25",
        "boundary": "2theta+kappa=6/25 ties and needs a logarithmic or constant margin",
        "weighted_pair_bound": "11/25+kappa+2theta<17/25",
        "residual_shallow_region": "2theta+kappa>=6/25, theta+kappa<=11/25, 0<=kappa<=6/25",
        "gate": "apply unfurled curvature only on the residual region; route kappa>=6/25 through the seeded structured branch",
    }


if __name__ == "__main__":
    print(verify_all())
