#!/usr/bin/env python3
"""Tabulate exact structural correlates of the 88 odd-index FRONTIER rows."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from statistics import median


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
FRONTIER = ROOT / "artifacts/frontier-index-inventory-v1.json"
W1 = ROOT / "artifacts/w1-full-census-v1.json"
OUTPUT = ROOT / "artifacts/frontier-odd-index-correlates-v1.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prime_factors(value: int) -> list[int]:
    factors = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1 if divisor == 2 else 2
    if value > 1:
        factors.append(value)
    return factors


def ratio(numerator: int, denominator: int) -> dict:
    value = Fraction(numerator, denominator)
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "reduced": f"{value.numerator}/{value.denominator}",
        "decimal": float(value),
    }


def summarize(rows: list[dict]) -> dict:
    return {
        "row_count": len(rows),
        "field_count": len({row["d"] for row in rows}),
        "split_predicate_pass_count": sum(
            bool(row["exactly_one_real_place_splitting"]) for row in rows
        ),
        "fundamental_unit_norm_minus_one_count": sum(
            row["fundamental_unit_norm"] == -1 for row in rows
        ),
        "d_divisible_by_3_count": sum(row["d"] % 3 == 0 for row in rows),
        "finite_norm_divisible_by_3_count": sum(
            row["finite_norm"] % 3 == 0 for row in rows
        ),
        "support_has_order_divisible_by_3_count": sum(
            any(order % 3 == 0 for order in row["support_orders"])
            for row in rows
        ),
        "support_shares_odd_prime_with_index_count": sum(
            any(
                any(order % prime == 0 for prime in prime_factors(
                    row["shintani_index"]
                ))
                for order in row["support_orders"]
            )
            for row in rows
        ),
        "commutator_equals_shintani_index_count": sum(
            row["commutator_size"] == row["shintani_index"]
            for row in rows
        ),
        "finite_norm_median": median(
            [row["finite_norm"] for row in rows]
        ),
    }


def main() -> None:
    frontier = json.loads(FRONTIER.read_text(encoding="utf-8"))
    w1 = json.loads(W1.read_text(encoding="utf-8"))
    by_id = {row["case_id"]: row for row in w1["records"]}
    odd_ids = [
        row["case_id"]
        for row in frontier["index_obstruction_audit"][
            "odd_index_above_two_cases"
        ]
    ]
    odd = [by_id[case_id] for case_id in odd_ids]
    if len(odd) != 88:
        raise RuntimeError("odd-index population changed")
    index_rows = [
        row
        for row in w1["records"]
        if row["verdict"] == "FRONTIER"
        and row["obstruction"] == "INDEX_GT_2"
    ]
    comparison = [
        row for row in index_rows if row["shintani_index"] % 2 == 0
    ]
    odd_support = Counter(
        tuple(row["support_orders"]) for row in odd
    )
    per_index = []
    for index in (3, 5, 9):
        rows = [row for row in odd if row["shintani_index"] == index]
        per_index.append(
            {
                "index": index,
                **summarize(rows),
                "support_patterns": [
                    {"orders": list(pattern), "count": count}
                    for pattern, count in sorted(
                        Counter(
                            tuple(row["support_orders"]) for row in rows
                        ).items(),
                        key=lambda item: (-item[1], item[0]),
                    )
                ],
            }
        )
    odd_three = sum(
        any(order % 3 == 0 for order in row["support_orders"])
        for row in odd
    )
    even_three = sum(
        any(order % 3 == 0 for order in row["support_orders"])
        for row in comparison
    )
    records = []
    for row in odd:
        records.append(
            {
                "case_id": row["case_id"],
                "d": row["d"],
                "field_discriminant": row["field_discriminant"],
                "finite_ideal_hnf": row["finite_ideal_hnf"],
                "finite_norm": row["finite_norm"],
                "finite_norm_prime_factors": prime_factors(
                    row["finite_norm"]
                ),
                "shintani_index": row["shintani_index"],
                "commutator_size": row["commutator_size"],
                "commutator_equals_index": (
                    row["commutator_size"] == row["shintani_index"]
                ),
                "split_predicate": bool(
                    row["exactly_one_real_place_splitting"]
                ),
                "fundamental_unit_norm": row["fundamental_unit_norm"],
                "one_place_cyclic_structure": row["one_cyc"],
                "two_place_cyclic_structure": row["both_cyc"],
                "support_orders": row["support_orders"],
                "support_has_3_primary_component": any(
                    order % 3 == 0 for order in row["support_orders"]
                ),
                "support_shares_odd_prime_with_index": any(
                    any(
                        order % prime == 0
                        for prime in prime_factors(row["shintani_index"])
                    )
                    for order in row["support_orders"]
                ),
                "source_case_sha256": row["source_case_sha256"],
            }
        )
    payload = {
        "schema": "effective-stark-frontier-odd-index-correlates-v1",
        "claim_tag": "VERIFIED_EXACT_CENSUS_STATISTICS",
        "odd_population": summarize(odd),
        "per_index": per_index,
        "support_pattern_distribution": [
            {"orders": list(pattern), "count": count}
            for pattern, count in sorted(
                odd_support.items(), key=lambda item: (-item[1], item[0])
            )
        ],
        "comparison_population": {
            "definition": (
                "FRONTIER rows carrying the historical INDEX_GT_2 "
                "label and an even Shintani index"
            ),
            **summarize(comparison),
        },
        "three_primary_support_contingency": {
            "odd_index": {
                "with_3_primary_support": odd_three,
                "without_3_primary_support": len(odd) - odd_three,
                "share": ratio(odd_three, len(odd)),
            },
            "even_index": {
                "with_3_primary_support": even_three,
                "without_3_primary_support": len(comparison) - even_three,
                "share": ratio(even_three, len(comparison)),
            },
        },
        "interpretation": (
            "The Shintani index equals the normal-closure commutator "
            "size in 85/88 rows; the three exceptions have index 3 and "
            "commutator size 6. Support shares an odd prime with the "
            "index in 86/88 rows. In particular, 3-primary support "
            "occurs in 80/88 odd-index rows versus 298/721 even-index "
            "controls. These are census statistics, not a causal theorem."
        ),
        "records": records,
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (FRONTIER, W1, SELF)
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("ODD_INDEX_ROW_COUNT=88")
    print(
        "COMMUTATOR_EQUALS_INDEX_COUNT="
        f"{payload['odd_population']['commutator_equals_shintani_index_count']}"
    )
    print(f"THREE_PRIMARY_SUPPORT_COUNT={odd_three}")
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")


if __name__ == "__main__":
    main()
