#!/usr/bin/env python3
"""Evaluate preregistered coarse patterns for quadratic Euler degeneracy."""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from typing import Callable


ROOT = Path(__file__).resolve().parents[1]
FEATURES = ROOT / "discovery/q-euler-local-features-v1.json"
PREREG = ROOT / "docs/cycle-128-q-euler-degeneracy-pattern-preregistration.md"
OUT = ROOT / "discovery/q-euler-pattern-analysis-v2.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prime_factors(value: int) -> list[int]:
    factors = []
    candidate = 2
    while candidate * candidate <= value:
        while value % candidate == 0:
            factors.append(candidate)
            value //= candidate
        candidate += 1
    if value > 1:
        factors.append(value)
    return factors


def deleted(row: dict) -> list[dict]:
    return [prime for char in row["characters"] for prime in char["deleted_primes"]]


def split_deleted(row: dict) -> list[dict]:
    return [
        prime
        for char in row["characters"]
        for prime in char["deleted_primes"]
        if prime["split_in_character_field"]
    ]


def exact_local_predicate(row: dict) -> bool:
    return all(
        any(prime["split_in_character_field"] for prime in char["deleted_primes"])
        for char in row["characters"]
    )


def confusion(rows: list[dict], predicate: Callable[[dict], bool]) -> dict:
    cells: dict[str, list[str]] = {"tp": [], "fp": [], "tn": [], "fn": []}
    for row in rows:
        predicted = predicate(row)
        actual = row["all_supported_euler_factors_zero"]
        key = "tp" if predicted and actual else "fp" if predicted else "fn" if actual else "tn"
        cells[key].append(row["case_id"])
    return {
        key: {"count": len(case_ids), "least_case_id": min(case_ids, default=None)}
        for key, case_ids in cells.items()
    }


def prime_key(prime: dict) -> tuple:
    return tuple(tuple(row) for row in prime["prime_hnf"])


def rational_kill_sets(row: dict) -> list[set[int]]:
    return [
        {
            prime["rational_prime"]
            for prime in char["deleted_primes"]
            if prime["split_in_character_field"]
        }
        for char in row["characters"]
    ]


def ideal_kill_sets(row: dict) -> list[set[tuple]]:
    return [
        {
            prime_key(prime)
            for prime in char["deleted_primes"]
            if prime["split_in_character_field"]
        }
        for char in row["characters"]
    ]


def main() -> None:
    payload = json.loads(FEATURES.read_text())
    rows = payload["records"]
    if len(rows) != 1560:
        raise RuntimeError("quadratic population changed")

    predicates: dict[str, Callable[[dict], bool]] = {
        "at_least_one_deleted_prime": lambda row: bool(deleted(row)),
        "at_least_one_split_deleted_occurrence": lambda row: bool(split_deleted(row)),
        "every_character_has_a_deleted_prime": lambda row: all(
            char["deleted_primes"] for char in row["characters"]
        ),
        "support_at_most_two": lambda row: row["support_count"] <= 2,
        "support_one_and_some_split_deleted": lambda row: (
            row["support_count"] == 1 and bool(split_deleted(row))
        ),
        "split_occurrence_count_at_least_support_count": lambda row: (
            len(split_deleted(row)) >= row["support_count"]
        ),
        "distinct_deleted_ideal_count_at_least_support_count": lambda row: (
            len({prime_key(prime) for prime in deleted(row)}) >= row["support_count"]
        ),
        "all_deleted_occurrences_split": lambda row: (
            bool(deleted(row))
            and all(prime["split_in_character_field"] for prime in deleted(row))
        ),
        "finite_norm_even": lambda row: row["finite_norm"] % 2 == 0,
        "finite_norm_not_prime": lambda row: len(prime_factors(row["finite_norm"])) > 1,
        "finite_norm_meets_base_discriminant": lambda row: (
            math.gcd(row["finite_norm"], row["base_discriminant"]) > 1
        ),
        "exact_universal_local_criterion": exact_local_predicate,
    }
    matrices = {name: confusion(rows, predicate) for name, predicate in predicates.items()}
    exact = matrices["exact_universal_local_criterion"]
    if exact["fp"]["count"] or exact["fn"]["count"]:
        raise RuntimeError("exact universal local criterion failed")

    support_distribution = []
    for support in sorted({row["support_count"] for row in rows}):
        subset = [row for row in rows if row["support_count"] == support]
        support_distribution.append(
            {
                "support_count": support,
                "rows": len(subset),
                "all_zero_rows": sum(
                    row["all_supported_euler_factors_zero"] for row in subset
                ),
                "zero_euler_character_histogram": dict(
                    sorted(Counter(row["zero_euler_character_count"] for row in subset).items())
                ),
            }
        )

    positive_support_two = [
        row
        for row in rows
        if row["support_count"] == 2 and row["all_supported_euler_factors_zero"]
    ]
    shared_kill_geometry = {
        "rows": len(positive_support_two),
        "common_killing_prime_ideal": sum(
            bool(set.intersection(*ideal_kill_sets(row))) for row in positive_support_two
        ),
        "common_killing_rational_prime": sum(
            bool(set.intersection(*rational_kill_sets(row))) for row in positive_support_two
        ),
    }
    shared_kill_geometry["different_killing_rational_primes_required"] = (
        shared_kill_geometry["rows"]
        - shared_kill_geometry["common_killing_rational_prime"]
    )
    shared_kill_geometry["least_without_common_killing_rational_prime"] = min(
        (
            row["case_id"]
            for row in positive_support_two
            if not set.intersection(*rational_kill_sets(row))
        ),
        default=None,
    )

    local_split_counts = Counter()
    local_nonsplit_counts = Counter()
    for row in rows:
        for char in row["characters"]:
            for prime in char["deleted_primes"]:
                key = (
                    prime["rational_prime"],
                    prime["ramification_index"],
                    prime["residue_degree"],
                )
                target = local_split_counts if prime["split_in_character_field"] else local_nonsplit_counts
                target[key] += 1

    all_zero_rows = [row for row in rows if row["all_supported_euler_factors_zero"]]
    out = {
        "schema": "effective-stark-q-euler-pattern-analysis-v2",
        "supersedes": "discovery/q-euler-pattern-analysis-v1.json",
        "status": "EXPLORATORY_FULL_CORPUS_PATTERN_AUDIT",
        "claim_tag": "OBSERVED",
        "population": {
            "rows": len(rows),
            "all_zero_rows": len(all_zero_rows),
            "supported_character_occurrences": sum(len(row["characters"]) for row in rows),
        },
        "candidate_confusion_matrices": matrices,
        "support_distribution": support_distribution,
        "support_two_killing_geometry": shared_kill_geometry,
        "all_zero_norm_range": {
            "minimum": min(row["finite_norm"] for row in all_zero_rows),
            "maximum": max(row["finite_norm"] for row in all_zero_rows),
        },
        "all_zero_base_count": len({row["base_radicand"] for row in all_zero_rows}),
        "local_value_counts": {
            "split_trivial_value": sum(local_split_counts.values()),
            "nonsplit_negative_value": sum(local_nonsplit_counts.values()),
        },
        "local_split_counts_by_rational_prime_e_f": [
            {"rational_prime": key[0], "e": key[1], "f": key[2], "count": count}
            for key, count in sorted(local_split_counts.items())
        ],
        "local_nonsplit_counts_by_rational_prime_e_f": [
            {"rational_prime": key[0], "e": key[1], "f": key[2], "count": count}
            for key, count in sorted(local_nonsplit_counts.items())
        ],
        "source_hashes": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (FEATURES, PREREG, Path(__file__))
        },
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print("Q_EULER_PATTERN_ANALYSIS=PASS")
    print(f"Q_EULER_ALL_ZERO_ROWS={len(all_zero_rows)}")
    print(
        "Q_EULER_EXACT_LOCAL_ERRORS="
        f"{exact['fp']['count'] + exact['fn']['count']}"
    )


if __name__ == "__main__":
    main()
