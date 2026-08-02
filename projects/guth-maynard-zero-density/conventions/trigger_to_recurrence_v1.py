"""Exact Cycle 59 trigger-surplus to popular-recurrence ledger."""
from __future__ import annotations

from fractions import Fraction as Q


TARGET_ROWS = Q(21, 25)
TARGET_DEFICIT = Q(7, 50)
MAX_SEPARATED_ROWS = Q(1)
PENULTIMATE_GAP = Q(3, 50)
FULL_CONTRACTION_SURPLUS = Q(47, 50)


def recurrence_ledger(row_exponent: Q, trigger_surplus: Q, desired_deficit: Q) -> dict[str, object]:
    row_exponent = Q(row_exponent)
    trigger_surplus = Q(trigger_surplus)
    desired_deficit = Q(desired_deficit)
    if row_exponent < 0 or trigger_surplus < 0 or desired_deficit < 0:
        raise RuntimeError("nonnegative exponents")
    minimum_deficit_open = row_exponent - trigger_surplus
    required_surplus_open = row_exponent - desired_deficit
    popular_edge_count_exponent = row_exponent + trigger_surplus
    maximum_edge_count_exponent = 2 * row_exponent
    return {
        "row_exponent": row_exponent,
        "trigger_surplus": trigger_surplus,
        "desired_deficit": desired_deficit,
        "generic_condition": "eta>r-mu",
        "minimum_deficit_open_endpoint": minimum_deficit_open,
        "required_surplus_open_endpoint": required_surplus_open,
        "desired_deficit_forced": trigger_surplus > required_surplus_open,
        "popular_edge_count_exponent": popular_edge_count_exponent,
        "average_degree_exponent": trigger_surplus,
        "all_edges_insufficient": popular_edge_count_exponent > maximum_edge_count_exponent,
    }


def verify_all() -> dict[str, object]:
    target = recurrence_ledger(TARGET_ROWS, Q(0), TARGET_DEFICIT)
    uniform = recurrence_ledger(MAX_SEPARATED_ROWS, Q(0), TARGET_DEFICIT)
    full_target = recurrence_ledger(TARGET_ROWS, FULL_CONTRACTION_SURPLUS, TARGET_DEFICIT)
    full_uniform = recurrence_ledger(MAX_SEPARATED_ROWS, FULL_CONTRACTION_SURPLUS, TARGET_DEFICIT)
    if target["required_surplus_open_endpoint"] != Q(7, 10):
        raise RuntimeError("target-row recurrence surplus")
    if uniform["required_surplus_open_endpoint"] != Q(43, 50):
        raise RuntimeError("uniform-row recurrence surplus")
    if not full_target["desired_deficit_forced"] or not full_uniform["desired_deficit_forced"]:
        raise RuntimeError("full contraction recurrence")
    if not full_target["all_edges_insufficient"]:
        raise RuntimeError("target-row direct contradiction")
    return {
        "target_rows": target,
        "uniform_rows": uniform,
        "full_contraction_target_rows": full_target,
        "full_contraction_uniform_rows": full_uniform,
        "hybrid_total_saving_for_target_7_50_open": PENULTIMATE_GAP + target["required_surplus_open_endpoint"],
        "hybrid_total_saving_for_uniform_7_50_open": PENULTIMATE_GAP + uniform["required_surplus_open_endpoint"],
        "status": "GRAPH_AMPLIFICATION_NEEDED_FOR_BARE_TRIGGER",
    }


if __name__ == "__main__":
    print(verify_all())
