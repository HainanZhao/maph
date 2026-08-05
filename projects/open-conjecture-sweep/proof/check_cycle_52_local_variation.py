#!/usr/bin/env python3
"""Audit the Cycle 52 exact local step-graphon census."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle52-local-variation"


def read_rows(name: str):
    with (OUT / name).open() as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def expected_matrices(q: int):
    slots = [(i, j) for i in range(q) for j in range(i, q)]
    result = []

    def visit(at, upper):
        if at == len(slots):
            if not any(upper) or math.gcd(*map(abs, upper)) != 1:
                return
            if next(x for x in upper if x) >= 0:
                return
            if sum((1 if i == j else 2) * x for (i, j), x in zip(slots, upper)):
                return
            matrix = [[0] * q for _ in range(q)]
            for (i, j), x in zip(slots, upper):
                matrix[i][j] = matrix[j][i] = x
            result.append(",".join(str(matrix[i][j]) for i in range(q) for j in range(q)))
            return
        for x in range(-2, 3):
            visit(at + 1, upper + [x])

    visit(0, [])
    return result


def audit():
    principal = json.loads((OUT / "summary.json").read_text())
    independent = json.loads((OUT / "independent-summary.json").read_text())
    one, two = read_rows("rows.tsv"), read_rows("independent-rows.tsv")
    assert principal["status"] == independent["status"] == "PASS"
    assert principal["epistemic_status"] == "PROVED"
    assert principal["edge_count"] == 15
    assert len(one) == len(two) == principal["direction_count"] == independent["direction_count"] == 512
    assert principal["q2_directions"] == 4 and principal["q3_directions"] == 508
    assert principal["local_negative"] == independent["local_negative"] == 0
    assert principal["local_positive"] == independent["local_positive"] == 512
    assert principal["identically_zero"] == independent["identically_zero"] == 0
    assert {row["matrix"] for row in one if row["q"] == "2"} == set(expected_matrices(2))
    assert {row["matrix"] for row in one if row["q"] == "3"} == set(expected_matrices(3))
    assert sorted(tuple(row.items()) for row in one) == sorted(tuple(row.items()) for row in two)
    first_counts = {}
    for row in one:
        q = int(row["q"])
        b = [int(x) for x in row["matrix"].split(",")]
        coefficients = [int(x) for x in row["coefficients_Q"].split(",")]
        assert len(b) == q * q and len(coefficients) == 16
        assert all(b[i * q + j] == b[j * q + i] for i in range(q) for j in range(q))
        assert sum(b) == 0 and max(map(abs, b)) <= 2
        assert math.gcd(*(abs(x) for x in b if x)) == 1
        assert coefficients[0] == coefficients[1] == 0
        first = next(k for k in range(1, 16) if coefficients[k])
        assert first == int(row["first_degree"])
        assert coefficients[first] > 0
        assert row["classification"] == "LOCAL_POSITIVE" and row["realized_epsilon"] == "-"
        first_counts[first] = first_counts.get(first, 0) + 1
    assert first_counts == {2: 489, 4: 23}
    return {
        "status": "PASS", "epistemic_status": "PROVED", "edge_count": 15,
        "directions": len(one), "q2_directions": 4, "q3_directions": 508,
        "local_negative": 0, "local_positive": 512, "identically_zero": 0,
        "first_degree_counts": {str(k): v for k, v in sorted(first_counts.items())},
        "claim_boundary": "Exact nonnegativity of the first nonzero local coefficient for the frozen primitive symmetric zero-mean 2/3-step directions at p=1/2 only; no arbitrary-step local theorem or Sidorenko proof.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
