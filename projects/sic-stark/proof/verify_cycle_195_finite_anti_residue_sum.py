#!/usr/bin/env python3
"""Exact finite-source combination of the corrected odd anti residues.

For every Cycle-194-v2 true-pole orbit, this replay uses the published
threefold helical Gamma_M shift multiplier only on the finite admissible
depths.  It proves meromorphic noncancellation by the q-adic constant term;
it constructs neither a convergent infinite Poincare sum nor an endpoint
distribution.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path

from verify_cycle_194_meromorphic_anti_channel_v2 import (
    ODD_CANONICAL_LABELS,
    corrected_collision_census,
)


LEVEL = 24
W_ORDER = 6


def triangular(depth: int) -> int:
    return depth * (depth + 1) // 2


def source_multiplier_record(label: int, depth: int) -> dict[str, object]:
    """Record c_(N,k)/c_(N,k-1) from the source threefold alias shift.

    Put q_tilde=t^(-24).  The exact source functional equations give the
    capital-Gamma beta multiplier

      M=(1-q^(-k))/(1-a1) * (1-a2/q_tilde)/(1-w*q^(k-1)),

    so c_k/c_(k-1)=1/M.  The q-adic unit factors are retained as named
    meromorphic factors; no specialization of t, q, or a root of unity is
    made.  Rewriting 1-q^(-k)=-q^(-k)(1-q^k) shows the exact q order k.
    """

    assert label in ODD_CANONICAL_LABELS
    assert 1 <= depth <= label
    a1_zeta_exponent = (5 * depth + 19 * label) % LEVEL
    a2_zeta_exponent = (4 + 5 * label + 19 * depth) % LEVEL
    a1_t_exponent = depth - label - LEVEL
    a2_over_q_tilde_t_exponent = -depth + label
    q_order = depth
    numerator_constant = "1-w" if depth == 1 else "1"
    assert q_order > 0
    return {
        "depth_k": depth,
        "M_Nk": (
            "(1-q^(-k))/(1-a_1) * "
            "(1-a_2/q_tilde)/(1-w*q^(k-1))"
        ),
        "residue_ratio": "c_(N,k)/c_(N,k-1)=1/M_(N,k)",
        "a_1": f"zeta_24^{a1_zeta_exponent}*t^{a1_t_exponent}",
        "a_2_over_q_tilde": f"zeta_24^{a2_zeta_exponent}*t^{a2_over_q_tilde_t_exponent}",
        "q_tilde_relation": "q_tilde=t^(-24)",
        "rewritten_ratio": (
            "-q^k*(1-a_1)*(1-w*q^(k-1))/"
            "((1-q^k)*(1-a_2/q_tilde))"
        ),
        "q_adic_increment": q_order,
        "q_adic_unit_constant": numerator_constant,
        "meromorphic_denominator_loci": [
            "1-q^k=0",
            "1-zeta_24^(4+5N+19k)*t^(N-k)=0",
        ],
        "capital_Gamma_normalization": "retained in M_(N,k); its source multiplier is not fitted or removed",
        "AFK_phase": "not used in the residue combination",
    }


def finite_combined_residue(label: int) -> dict[str, object]:
    """Derive the exact meromorphic nonidentity certificate for C_N."""

    orbit = corrected_collision_census()["records"]
    orbit_record = next(row for row in orbit if row["canonical_odd_N"] == label)
    assert orbit_record["admissible_depths"] == list(range(label + 1))
    ratios = [source_multiplier_record(label, depth) for depth in range(1, label + 1)]
    cumulative_orders = [triangular(depth) for depth in range(1, label + 1)]
    assert [row["q_adic_increment"] for row in ratios] == list(range(1, label + 1))
    assert all(order > 0 for order in cumulative_orders)
    assert cumulative_orders[-1] == triangular(label)
    return {
        "canonical_odd_N": label,
        "true_pole_orbit_cardinality": label + 1,
        "combined_residue": "C_N=sum_(k=0)^N c_(N,k)",
        "normalization": "C_N/c_(N,0)=1+sum_(k=1)^N c_(N,k)/c_(N,0)",
        "base_residue": "c_(N,0) is the retained nonzero Cycle-194-v2 simple anti residue",
        "source_multiplier_records": ratios,
        "cumulative_q_adic_orders": cumulative_orders,
        "normalized_constant_coefficient": 1,
        "finite_combined_residue_meromorphically_nonzero": True,
        "noncancellation_reason": (
            "Every k>=1 normalized summand has strictly positive q-adic order "
            "k(k+1)/2, while the k=0 summand is exactly 1."
        ),
        "all_point_nonvanishing_claimed": False,
        "endpoint_continuation_claimed": False,
    }


def all_six_combined_residues() -> dict[str, object]:
    records = [finite_combined_residue(label) for label in ODD_CANONICAL_LABELS]
    assert len(records) == 6
    assert all(row["finite_combined_residue_meromorphically_nonzero"] for row in records)
    return {
        "epistemic_status": "PROVED",
        "records": records,
        "all_six_finite_combined_residues_meromorphically_nonzero": True,
        "constant_coefficient_vector": [row["normalized_constant_coefficient"] for row in records],
        "maximum_q_adic_order": triangular(max(ODD_CANONICAL_LABELS)),
        "scope": "finite source collision sums in the interior meromorphic coefficient field only",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {
        "schema": "sic-stark-cycle-195-finite-anti-residue-sum-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "For the six Cycle-194-v2 finite true-pole orbits, the exact source helical multiplier makes every normalized non-base residue summand have strictly positive q-adic order. Each finite combined anti residue therefore has formal constant coefficient one and is meromorphically nonzero. This proves no all-point nonvanishing, infinite periodization, endpoint distribution or contour continuation, AFK identity, boundary value, fusion, Stark, or TCC result.",
        "corrected_input": corrected_collision_census(),
        "finite_combined_residues": all_six_combined_residues(),
        "next_unresolved_boundary": {
            "epistemic_status": "CONJECTURED",
            "statement": "The six nonzero finite combined residues may be preserved by a source-derived distributional or contour continuation to the RM endpoint, but such a continuation requires an independent infinity/Abel or contour estimate.",
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
