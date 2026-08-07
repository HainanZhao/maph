#!/usr/bin/env python3
"""Exact width-six denominator and kernel structural prediction test."""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path


OUTPUT = Path(__file__).with_suffix(".json")


def fibonacci(limit: int) -> list[int]:
    values = [0, 1]
    while len(values) <= limit:
        values.append(values[-1] + values[-2])
    return values


def divisors_above_one(number: int) -> tuple[int, ...]:
    return tuple(candidate for candidate in range(2, number + 1) if number % candidate == 0)


def denominator_cyclotomic_demand(fib: list[int], width: int) -> Counter[int]:
    demand: Counter[int] = Counter()
    for index in range(1, width + 1):
        demand.update(divisors_above_one(fib[index]))
    return demand


def entry_rank(modulus: int) -> int:
    previous, current = 0, 1
    for index in itertools.count(1):
        previous, current = current, (previous + current) % modulus
        if previous == 0:
            return index


def row_for(m: int, fib: list[int], demand: Counter[int]) -> dict:
    eligible = {
        cyclotomic: [
            offset
            for offset in range(1, 7)
            if fib[m + offset] % cyclotomic == 0
        ]
        for cyclotomic in sorted(demand)
    }
    count = 1
    for cyclotomic, multiplicity in sorted(demand.items()):
        count *= math.comb(len(eligible[cyclotomic]), multiplicity)
    return {
        "assignment_count": count,
        "eligible_offsets": {str(key): value for key, value in eligible.items()},
    }


def main() -> None:
    maximum_m = 240
    fib = fibonacci(maximum_m + 6)
    denominator_lengths = [fib[index] for index in range(1, 7)]
    demand = denominator_cyclotomic_demand(fib, 6)
    assert demand == Counter({2: 2, 3: 1, 4: 1, 5: 1, 8: 1})
    ranks = {cyclotomic: entry_rank(cyclotomic) for cyclotomic in demand}
    assert ranks == {2: 3, 3: 4, 4: 6, 5: 5, 8: 6}
    structural_modulus = math.lcm(*ranks.values())
    assert structural_modulus == 60

    stable = {}
    signature_counts: Counter[str] = Counter()
    minimum_assignments = None
    for m in range(1, maximum_m + 1):
        row = row_for(m, fib, demand)
        assert row["assignment_count"] > 0
        residue = m % structural_modulus
        if m <= structural_modulus:
            stable[str(residue)] = row
        else:
            assert stable[str(residue)] == row
        signature_counts[json.dumps(row["eligible_offsets"], sort_keys=True)] += 1
        if minimum_assignments is None or row["assignment_count"] < minimum_assignments:
            minimum_assignments = row["assignment_count"]

    result = {
        "claim_boundary": "exact structural prediction only; no width-six unimodality claim",
        "denominator_cyclotomic_demand": {
            str(key): value for key, value in sorted(demand.items())
        },
        "denominator_lengths": denominator_lengths,
        "entry_ranks": {str(key): value for key, value in sorted(ranks.items())},
        "first_difference_kernel": {
            "parts": [1, 2, 3, 5, 8],
            "quasipolynomial_degree": 4,
            "quasipolynomial_period_divides": 120,
        },
        "maximum_m": maximum_m,
        "minimum_assignment_count": minimum_assignments,
        "residue_rows_mod_60": dict(sorted(stable.items(), key=lambda item: int(item[0]))),
        "signature_type_count": len(signature_counts),
        "status": "PASS",
        "structural_modulus": structural_modulus,
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "minimum_assignment_count": minimum_assignments,
                "signature_type_count": len(signature_counts),
                "status": "PASS",
                "structural_modulus": structural_modulus,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
