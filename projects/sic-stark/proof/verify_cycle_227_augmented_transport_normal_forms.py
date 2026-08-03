#!/usr/bin/env python3
"""Exact augmented F2/F3 semigroup normal-form audit for Cycle 227/B064."""
from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from verify_cycle_226_signed_product_groupoid import AugmentedState, NODES, f2, f3, node_name, transition


WORDS_UP_TO = 12
SCALE = 576


def run_word(start: str, word: tuple[str, ...]) -> AugmentedState:
    current = AugmentedState(NODES[start], ((1, 0), (0, 1)), (1, 0), "m")
    for generator in word:
        current = transition(current, generator)
    return current


def expected_raw(start: str, word: tuple[str, ...]) -> str:
    """Raw maps commute; only their parities select the square endpoint."""
    state = NODES[start]
    if sum(generator == "F2" for generator in word) % 2:
        state = f2(state)
    if sum(generator == "F3" for generator in word) % 2:
        state = f3(state)
    return node_name(state)


def one_step_periods(start: str, generator: str) -> tuple[tuple[int, int], tuple[int, int]]:
    state = AugmentedState(NODES[start], ((1, 0), (0, 1)), (1, 0), "m")
    return transition(state, generator).periods


def expected_periods(start: str, word: tuple[str, ...]) -> tuple[tuple[int, int], tuple[int, int]]:
    """Closed form obtained from the paired transport identities.

    Length 2j gives 576^j times I or the swap S; length 2j+1 gives
    576^j times the one-step map selected by the raw endpoint.
    """
    n = len(word)
    f2_odd = sum(generator == "F2" for generator in word) % 2 == 1
    f3_odd = sum(generator == "F3" for generator in word) % 2 == 1
    if n == 0:
        return ((1, 0), (0, 1))
    power = SCALE ** (n // 2)
    if n % 2 == 0:
        assert f2_odd == f3_odd
        return ((power, 0), (0, power)) if not f2_odd else ((0, power), (power, 0))
    generator = "F2" if f2_odd else "F3"
    assert f2_odd != f3_odd
    base = one_step_periods(start, generator)
    return tuple(tuple(power * entry for entry in row) for row in base)  # type: ignore[return-value]


def expected_argument(start: str, word: tuple[str, ...]) -> tuple[int, int]:
    """Exact ordered sign of 24^n(mu+m omega2).

    If F2 occurs at one-indexed position j in a word of length n, its
    contribution is (-1)^(n-j+1); the sign of the starting s contributes once
    per generator.  This is an independent closed form for the affine action.
    """
    n = len(word)
    if n == 0:
        return (1, 0)
    start_s_sign = 1 if NODES[start][3] > 0 else -1
    exponent = sum(n - index for index, generator in enumerate(word) if generator == "F2")
    sign = (start_s_sign ** n) * ((-1) ** exponent)
    coefficient = sign * (24**n)
    return (coefficient, coefficient)


def source_product_path(start: str, word: tuple[str, ...]) -> bool:
    """A source product is available at every input iff no negative node occurs."""
    return NODES[start][1] > 0 and all(generator == "F3" for generator in word)


def residual_word(start: str, word: tuple[str, ...]) -> list[dict[str, object]]:
    """Ordered factorization blocks; their contents are never commuted or cancelled."""
    state = NODES[start]
    blocks = []
    for generator in word:
        blocks.append(
            {
                "generator": generator,
                "source": node_name(state),
                "source_product_defined": state[1] > 0,
                "ordinary_gamma_factor_count": 2,
            }
        )
        state = f2(state) if generator == "F2" else f3(state)
    return blocks


def paired_generator_induction_audit() -> dict[str, object]:
    """Verify the finite relations that induct on consecutive two-letter blocks."""
    rows = []
    expected_periods = {
        ("F2", "F2"): ((SCALE, 0), (0, SCALE)),
        ("F3", "F3"): ((SCALE, 0), (0, SCALE)),
        ("F2", "F3"): ((0, SCALE), (SCALE, 0)),
        ("F3", "F2"): ((0, SCALE), (SCALE, 0)),
    }
    expected_argument_sign = {
        ("F2", "F2"): -1,
        ("F3", "F3"): 1,
        ("F2", "F3"): 1,
        ("F3", "F2"): -1,
    }
    for start in NODES:
        for pair, periods in expected_periods.items():
            actual = run_word(start, pair)
            assert actual.periods == periods
            assert actual.argument == (expected_argument_sign[pair] * SCALE,) * 2
            assert actual.label == "0"
            rows.append(
                {
                    "start": start,
                    "pair": " ".join(pair),
                    "period_relation": "576*I" if pair[0] == pair[1] else "576*S",
                    "argument_sign": expected_argument_sign[pair],
                    "label": 0,
                }
            )
    assert len(rows) == 16
    return {
        "epistemic_status": "PROVED",
        "rows": rows,
        "induction_rule": "Every two-letter block contributes 576*I or 576*S independently of the raw start; its affine sign is (-,+,+,-) for F2F2,F3F3,F2F3,F3F2. Concatenation gives the even normal form, and one final letter gives the odd form.",
        "conclusion": "These sixteen exact identities are the finite induction step; the length-12 census is a regression check of their closed form, not its only support.",
    }


def normal_form_audit() -> dict[str, object]:
    total = 0
    all_rows_match = True
    source_path_count = 0
    length_summary = []
    for length in range(WORDS_UP_TO + 1):
        rows = 0
        for start in NODES:
            for word in itertools.product(("F2", "F3"), repeat=length):
                actual = run_word(start, word)
                predicted_raw = expected_raw(start, word)
                predicted_periods = expected_periods(start, word)
                predicted_argument = expected_argument(start, word)
                predicted_label = "m" if length == 0 else "0"
                blocks = residual_word(start, word)
                match = (
                    actual.raw == NODES[predicted_raw]
                    and actual.periods == predicted_periods
                    and actual.argument == predicted_argument
                    and actual.label == predicted_label
                )
                assert match
                assert len(blocks) == length
                assert sum(block["ordinary_gamma_factor_count"] for block in blocks) == 2 * length
                if source_product_path(start, word):
                    source_path_count += 1
                total += 1
                rows += 1
                all_rows_match = all_rows_match and match
        length_summary.append({"length": length, "rows": rows, "all_match": all_rows_match})
    assert total == 4 * sum(2**length for length in range(WORDS_UP_TO + 1))
    assert all_rows_match
    paired = paired_generator_induction_audit()
    return {
        "epistemic_status": "PROVED",
        "word_length_cap": WORDS_UP_TO,
        "rows_checked": total,
        "source_defined_path_count": source_path_count,
        "all_rows_match_closed_form": all_rows_match,
        "closed_form": {
            "raw_endpoint": "apply F2 iff count_F2 is odd and F3 iff count_F3 is odd",
            "periods_even": "length 2j: 576^j*I when both counts are even, 576^j*S when both are odd",
            "periods_odd": "length 2j+1: 576^j times the start's one-step map selected by the odd generator count",
            "affine_argument": "sign(start_s)^n*(-1)^(sum_{F2 at position j}(n-j+1))*24^n*(mu+m*omega2)",
            "label": "m at length zero and 0 at every positive length",
            "residual_word": "ordered two-ordinary-gamma block per generator; no commuting or cancellation",
        },
        "length_summary": length_summary,
        "paired_generator_induction": paired,
        "conclusion": "The exact census agrees with the paired-generator normal form through the frozen cap. The sixteen paired-generator identities supply the induction step, and one final letter supplies the odd form; this is not a bounded-search claim.",
    }


def quotient_audit() -> dict[str, object]:
    """Classify C218 scaling candidates without dropping a residual word."""
    generic_survivors = []
    zero_label_survivors = []
    rejected_counts: Counter[str] = Counter()
    for length in range(1, WORDS_UP_TO + 1):
        for start in NODES:
            for word in itertools.product(("F2", "F3"), repeat=length):
                actual = run_word(start, word)
                path_defined = source_product_path(start, word)
                raw_return = actual.raw == NODES[start]
                period_scale = actual.periods[0][1] == 0 and actual.periods[1][0] == 0 and actual.periods[0][0] == actual.periods[1][1] > 0
                factor = actual.periods[0][0] if period_scale else None
                # Generic label m must remain m; C218 scaling does not change it.
                generic = path_defined and raw_return and period_scale and actual.argument == (factor, 0) and actual.label == "m"
                if generic:
                    generic_survivors.append((start, word))
                # At the separately declared m=0 specialization, the m*omega2
                # coefficient vanishes and label zero is preserved.
                zero_label = path_defined and raw_return and period_scale and actual.argument[0] == factor and actual.label == "0"
                if zero_label:
                    zero_label_survivors.append(
                        {
                            "start": start,
                            "word": " ".join(word),
                            "scale": factor,
                            "residual_blocks": len(residual_word(start, word)),
                            "ordinary_gamma_factors_retained": 2 * len(word),
                        }
                    )
                if raw_return and not zero_label:
                    if not path_defined:
                        rejected_counts["crosses_negative_k_product_boundary"] += 1
                    elif not period_scale:
                        rejected_counts["period_swap_or_nonscalar_transport"] += 1
                    else:
                        rejected_counts["affine_or_label_defect"] += 1
    assert not generic_survivors
    assert zero_label_survivors
    assert all(item["start"] in {"A", "C"} for item in zero_label_survivors)
    assert all(set(item["word"].split()) == {"F3"} for item in zero_label_survivors)
    assert all(item["ordinary_gamma_factors_retained"] > 0 for item in zero_label_survivors)
    return {
        "epistemic_status": "PROVED",
        "generic_full_label_scaling_quotient_count": len(generic_survivors),
        "zero_label_product_node_scaling_candidates": zero_label_survivors,
        "zero_label_candidate_count": len(zero_label_survivors),
        "rejected_raw_return_count": sum(rejected_counts.values()),
        "rejected_raw_return_counts": dict(sorted(rejected_counts.items())),
        "conclusion": "C218 scaling yields no quotient of the generic augmented state: every nonempty word loses the initial label. At m=0 only, the source-defined paths F3^(2j) from A or C return their product node with positive common scale 576^j, but their ordered ordinary-gamma residual blocks remain. They are product-node identifications, not closed factorization/cochain loops.",
    }


def run() -> dict[str, object]:
    normal = normal_form_audit()
    quotient = quotient_audit()
    assert normal["all_rows_match_closed_form"]
    assert quotient["generic_full_label_scaling_quotient_count"] == 0
    return {
        "schema": "sic-stark-cycle-227-augmented-transport-normal-forms-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "The exact F2/F3 augmented transport has the stated normal form through the preregistered census and its paired-generator recurrence. No C218 positive-scaling quotient preserves the generic period/argument/label state. At label zero only, positive all-F3 even paths from A/C return the product node up to positive scaling, while retaining a nonempty ordered ordinary-gamma residual word; this is not a closed factorization or cochain loop. This does not construct a signed-k product, a source cross-sign law, a packet cocycle, AFK covariance, fusion, Stark, or TCC.",
        "normal_form_audit": normal,
        "quotient_audit": quotient,
        "gate_outcome": {
            "augmented_transport_normal_form": "PROVED",
            "generic_augmented_scaling_quotient": "FALSIFIED_BY_LABEL_LOSS",
            "zero_label_positive_product_node_quotient": "PROVED_WITH_RESIDUAL_WORD_RETAINED",
            "remaining_design_problem": "Determine whether the retained residual-word monoid admits a source-derived reduction or a new signed-k completion without treating zero-label product-node scaling as a factorization loop.",
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
