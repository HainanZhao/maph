"""Exact Cycle 65 depth-refined Farey-packet exponent ledger."""
from __future__ import annotations

from fractions import Fraction as Q


DELTA = Q(3, 5)
H = Q(11, 25)
PAIR_TARGET = Q(17, 25)
RECURRENCE_DEPTH = PAIR_TARGET - H
DENOMINATOR_THRESHOLD = H - RECURRENCE_DEPTH


def scale_ledger(theta: Q, kappa: Q) -> dict[str, object]:
    if theta < 0 or kappa < 0:
        raise ValueError("scale exponents must be nonnegative")
    admissible = theta + kappa <= H
    packet_weight = H + kappa
    packet_count_target = PAIR_TARGET - packet_weight
    random_packet_count = DELTA + theta - kappa - 1
    return {
        "denominator_exponent": theta,
        "depth_exponent": kappa,
        "admissible": admissible,
        "packet_weight_exponent": packet_weight,
        "packet_count_target_exponent_open": packet_count_target,
        "random_packet_count_exponent": random_packet_count,
        "random_margin_to_target": packet_count_target - random_packet_count,
        "single_packet_reaches_pair_target": packet_weight >= PAIR_TARGET,
    }


def verify_all() -> dict[str, object]:
    maximal_at_threshold = scale_ledger(DENOMINATOR_THRESHOLD, RECURRENCE_DEPTH)
    generic = scale_ledger(Q(3, 25), Q(1, 5))
    if RECURRENCE_DEPTH != Q(6, 25):
        raise RuntimeError("recurrence depth threshold")
    if DENOMINATOR_THRESHOLD != Q(1, 5):
        raise RuntimeError("denominator threshold")
    if not maximal_at_threshold["admissible"]:
        raise RuntimeError("threshold packet must be admissible")
    if maximal_at_threshold["packet_weight_exponent"] != PAIR_TARGET:
        raise RuntimeError("threshold packet must tie pair target")
    if generic["packet_count_target_exponent_open"] != Q(1, 25):
        raise RuntimeError("generic count target")
    if generic["random_packet_count_exponent"] != -Q(12, 25):
        raise RuntimeError("generic random count")
    if generic["random_margin_to_target"] != Q(13, 25):
        raise RuntimeError("generic margin")
    if scale_ledger(H, Q(0))["random_margin_to_target"] != Q(1, 5):
        raise RuntimeError("minimum random margin")
    return {
        "constants": {
            "delta_exponent": DELTA,
            "h_exponent": H,
            "pair_target_exponent_open": PAIR_TARGET,
            "dangerous_depth_threshold": RECURRENCE_DEPTH,
            "deep_packet_denominator_threshold": DENOMINATOR_THRESHOLD,
        },
        "exact_packet_weight": "W(q,K)=K*H-q*K*(K+1)/2",
        "dyadic_packet_weight_exponent": "11/25+kappa",
        "admissible_region": "theta+kappa<=11/25",
        "dyadic_count_target": "N(theta,kappa)<X^(6/25-kappa) with strict margin",
        "random_count_exponent": "theta-kappa-2/5",
        "random_margin": "16/25-theta>=1/5",
        "maximal_depth_count_target": "N(theta,11/25-theta)<X^(theta-1/5)",
        "structural_branch": "a single target-reaching packet requires kappa>=6/25 and hence theta<=1/5; strict excess requires theta<1/5",
        "gate": "prove depth-packet discrepancy on shallow scales or route X^6/25-deep low-denominator packets to AP recurrence",
    }


if __name__ == "__main__":
    print(verify_all())
