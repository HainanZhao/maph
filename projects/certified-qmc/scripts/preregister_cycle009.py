#!/usr/bin/env python3
"""Freeze the N=2^16,d=50 three-representation experiment."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import argparse
import json
from pathlib import Path
import sys

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT))

from src.ntt_prime import generate_ntt_prime_schedule
from src.scaled_integer import (
    balanced_crt_bits,
    candidate_difference_bound,
    error_numerator_bound,
)


FROZEN_AT = "2026-07-29T04:24:47Z"
MODULUS = 2**16
DIMENSION = 50
SCHEDULE_COUNT = 40


def canonical_digest(value) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
    ).hexdigest()


def shortest_prefix(primes: list[int], bound: int) -> tuple[int, int]:
    product = 1
    for count, prime in enumerate(primes, 1):
        product *= prime
        if product > 2 * bound:
            return count, product.bit_length()
    raise ArithmeticError("frozen schedule does not cover bound")


def write(path: Path | None, value) -> None:
    rendered = json.dumps(value, indent=2, sort_keys=True) + "\n"
    if path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schedule-output", type=Path)
    parser.add_argument("--checkpoint-output", type=Path)
    args = parser.parse_args()

    schedule = generate_ntt_prime_schedule(SCHEDULE_COUNT)
    schedule_payload = {
        "schema": "certified-qmc-ntt-prime-schedule-v2",
        "tag": "VERIFIED",
        "frozen_at_utc": FROZEN_AT,
        "purpose": "cycle009-N65536-d50-with-two-prime-overflow-check",
        "generation": {
            "order": "descending coefficient",
            "coefficient_start": 2**30 - 1,
            "family": "p=c*2^32+1",
            "primality": "deterministic-Miller-Rabin-u64",
            "primitive_root": "least root passing complete-factor tests",
        },
        "count": len(schedule),
        "primes": schedule,
    }
    schedule_payload["schedule_sha256"] = canonical_digest(schedule_payload)

    weights = [Fraction(1, j * j) for j in range(1, DIMENSION + 1)]
    difference_bound = candidate_difference_bound(
        MODULUS, weights[:-1], weights[-1]
    )
    final_error_bound = error_numerator_bound(MODULUS, weights)
    prime_values = [int(row["prime"]) for row in schedule]
    difference_count, difference_product_bits = shortest_prefix(
        prime_values, difference_bound
    )
    error_count, error_product_bits = shortest_prefix(
        prime_values, final_error_bound
    )
    comparisons = (DIMENSION - 1) * (MODULUS // 4 - 1)
    maximum_escalations = (comparisons - 1) // 1000

    checkpoint = {
        "schema": "certified-qmc-cycle009-preregistration-v1",
        "tag": "PREREGISTERED",
        "frozen_at_utc": FROZEN_AT,
        "data_run_started": False,
        "target": {
            "modulus": MODULUS,
            "dimension": DIMENSION,
            "convention": "DKS2013-eq5.13-beta0-product-B2",
            "weights": "gamma_j=1/j^2",
            "first_component": 1,
            "candidate_classes_per_stage": MODULUS // 4,
            "candidate_order": "5^a mod N for ascending 0<=a<N/4",
            "tie_rule": "smallest candidate exponent a",
        },
        "three_representations": {
            "ground_truth": (
                "compiled prime-major scaled products and valuation-"
                "stratified NTT residues"
            ),
            "decision_shadow": (
                "double-double midpoint plus rigorous EFT/FMA-derived "
                "outward radius"
            ),
            "first_escalation": (
                "Arb balls at 128-bit precision; precision may only increase"
            ),
            "final_escalation": (
                "balanced exact CRT reconstruction of candidate difference"
            ),
        },
        "decision_protocol": {
            "comparison_order": (
                "deterministic tournament in ascending candidate exponent"
            ),
            "ball_separation": "upper(smaller)<lower(larger)",
            "overlap_ladder": "double-double -> Arb-128 -> exact CRT",
            "comparison_count": comparisons,
            "counters": [
                "double_double_separated",
                "arb_escalated",
                "arb_separated",
                "exact_crt_escalated",
                "exact_equalities"
            ],
            "exact_crt_escalation_rate": (
                "exact_crt_escalated/comparison_count"
            ),
            "acceptance_predicate": "exact_crt_escalation_rate<0.001",
            "maximum_exact_crt_escalations": maximum_escalations,
            "structural_sign_symmetry_quotiented": True,
            "exact_equalities_count_as_exact_crt_escalations": True,
            "failure_action": (
                "halt certified-optimal search claim; retain exact final-"
                "vector certification and report measured rate"
            ),
        },
        "crt_budget": {
            "schedule_count": SCHEDULE_COUNT,
            "schedule_sha256": schedule_payload["schedule_sha256"],
            "candidate_difference_bound": str(difference_bound),
            "candidate_difference_bound_bits": difference_bound.bit_length(),
            "candidate_crt_required_bits": balanced_crt_bits(
                difference_bound
            ),
            "candidate_minimum_primes": difference_count,
            "candidate_product_bits": difference_product_bits,
            "final_error_bound": str(final_error_bound),
            "final_error_bound_bits": final_error_bound.bit_length(),
            "final_error_crt_required_bits": balanced_crt_bits(
                final_error_bound
            ),
            "final_error_minimum_primes": error_count,
            "final_error_product_bits": error_product_bits,
            "overflow_check_extra_primes": 2,
            "schedule_covers_final_plus_overflow": (
                SCHEDULE_COUNT >= error_count + 2
            ),
        },
        "correctness_gates_before_target_run": [
            "compiled NTT equals Python NTT on all candidates through N=2^12",
            "double-double balls contain an independent Arb replay",
            "every Arb-separated comparison replays on frozen small cases",
            "every exact escalation agrees with direct integer oracle",
            "per-dimension checkpoint and SHA manifest replay"
        ],
        "optimization_order": {
            "correctness_kernel": (
                "plain __int128 modular reduction is frozen for first banked "
                "N=2^16 correctness run"
            ),
            "post_correctness": (
                "Montgomery multiplication and lazy reduction in 62-bit "
                "headroom"
            ),
            "promotion_gate": (
                "optimized residues and winners must be bit-identical to "
                "the banked plain-reduction transcript"
            ),
            "speedup": "PROJECTED_ONLY; no 3-5x claim promoted"
        },
        "external_audit_data_used": False,
    }
    checkpoint["checkpoint_sha256"] = canonical_digest(checkpoint)

    write(args.schedule_output, schedule_payload)
    write(args.checkpoint_output, checkpoint)


if __name__ == "__main__":
    main()
