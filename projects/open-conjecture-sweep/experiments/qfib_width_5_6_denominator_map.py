#!/usr/bin/env python3
"""Exact denominator/decomposition map for q-Fibonomial widths 5 and 6."""

from __future__ import annotations

import itertools
import json
import math
from collections import Counter
from pathlib import Path


OUTPUT = Path(__file__).with_suffix(".json")
RANK = {2: 3, 3: 4, 5: 5, 8: 6}


def fibonacci(limit: int) -> list[int]:
    values = [0, 1]
    while len(values) <= limit:
        values.append(values[-1] + values[-2])
    return values


def assignments(adjacency: dict[int, tuple[int, ...]]):
    atoms = tuple(sorted(adjacency))
    for targets in itertools.product(*(adjacency[atom] for atom in atoms)):
        if len(set(targets)) == len(targets):
            yield dict(zip(atoms, targets))


def signature_for(m: int, width: int, fib: list[int]) -> dict:
    atoms = tuple(fib[j] for j in range(1, width + 1) if fib[j] > 1)
    assert len(atoms) == len(set(atoms))
    offsets = tuple(range(1, width + 1))
    adjacency = {}
    for atom in atoms:
        direct = tuple(offset for offset in offsets if fib[m + offset] % atom == 0)
        periodic = tuple(
            offset for offset in offsets if (m + offset) % RANK[atom] == 0
        )
        assert direct == periodic
        adjacency[atom] = direct

    injective = list(assignments(adjacency))
    descriptions = []
    for assignment in injective:
        spacers = []
        for atom, offset in sorted(assignment.items()):
            quotient_length = fib[m + offset] // atom
            if quotient_length > 1:
                spacers.append(atom)
        descriptions.append(
            {
                "assignment": {str(atom): offset for atom, offset in sorted(assignment.items())},
                "effective_spacers": spacers,
            }
        )

    minimum = min((len(row["effective_spacers"]) for row in descriptions), default=None)
    optimal_steps = sorted(
        {
            tuple(row["effective_spacers"])
            for row in descriptions
            if len(row["effective_spacers"]) == minimum
        }
    ) if minimum is not None else []
    return {
        "adjacency": {str(atom): list(targets) for atom, targets in adjacency.items()},
        "injective_assignment_count": len(injective),
        "minimum_effective_spacers": minimum,
        "optimal_step_multisets": [list(row) for row in optimal_steps],
    }


def main() -> None:
    maximum_m = 240
    fib = fibonacci(maximum_m + 6)
    result = {
        "claim_boundary": (
            "exact structural census only; no unimodality conjecture is asserted"
        ),
        "maximum_m": maximum_m,
        "period": 60,
        "status": "OBSERVED",
        "widths": {},
    }
    for width in (5, 6):
        denominator_lengths = [fib[j] for j in range(1, width + 1)]
        nontrivial = [value for value in denominator_lengths if value > 1]
        kernel_parts = [1, *nontrivial]
        kernel_period = math.lcm(*kernel_parts)
        kernel_degree = len(kernel_parts) - 1
        rows_by_m = {}
        stable_rows = {}
        repeated = Counter()
        for m in range(1, maximum_m + 1):
            row = signature_for(m, width, fib)
            rows_by_m[str(m)] = row
            residue = m % 60
            if 61 <= m <= 120:
                stable_rows[str(residue)] = row
            elif m >= 121:
                assert stable_rows[str(residue)] == row
            key = (
                row["injective_assignment_count"],
                row["minimum_effective_spacers"],
                tuple(tuple(x) for x in row["optimal_step_multisets"]),
            )
            repeated[key] += 1

        result["widths"][str(width)] = {
            "denominator_lengths": denominator_lengths,
            "nontrivial_denominator_atoms": nontrivial,
            "first_difference_kernel": {
                "parts": kernel_parts,
                "quasipolynomial_degree": kernel_degree,
                "quasipolynomial_period_divides": kernel_period,
            },
            "early_exceptions_m_1_to_60": {
                str(m): rows_by_m[str(m)]
                for m in range(1, 61)
                if rows_by_m[str(m)] != stable_rows[str(m % 60)]
            },
            "residue_rows_mod_60_stable_from_m_61": dict(
                sorted(stable_rows.items(), key=lambda x: int(x[0]))
            ),
            "summary": [
                {
                    "injective_assignment_count": key[0],
                    "minimum_effective_spacers": key[1],
                    "optimal_step_multisets": [list(x) for x in key[2]],
                    "rows_m_1_to_240": count,
                }
                for key, count in sorted(repeated.items(), key=lambda x: repr(x[0]))
            ],
        }

    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(rendered)
    print(
        json.dumps(
            {
                "maximum_m": maximum_m,
                "output": str(OUTPUT),
                "status": "PASS",
                "widths": [5, 6],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
