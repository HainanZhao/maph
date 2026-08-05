#!/usr/bin/env python3
"""Exact sparse factor audit for the two S3 class-exchange derivatives."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "discovery/out/cycle62-kkt-exchange/exchange-derivatives.tsv"
OUT = ROOT / "discovery/out/cycle62-kkt-exchange/exchange-factor-audit.json"
Monomial = tuple[int, int, int, int, int, int]


def load() -> dict[str, dict[Monomial, int]]:
    result: dict[str, dict[Monomial, int]] = defaultdict(dict)
    with RAW.open() as source:
        for row in csv.DictReader(source, delimiter="\t"):
            monomial = tuple(int(row[name]) for name in ("a0", "a1", "a2", "a5", "a3", "a4"))
            result[row["class"]][monomial] = int(row["coefficient"])
    return result


def poly_add(left: dict[int, int], right: dict[int, int], sign: int = 1) -> dict[int, int]:
    answer = dict(left)
    for exponent, coefficient in right.items():
        answer[exponent] = answer.get(exponent, 0) + sign * coefficient
        if answer[exponent] == 0:
            del answer[exponent]
    return answer


def shift_x(poly: dict[int, int]) -> dict[int, int]:
    return {exponent + 1: coefficient for exponent, coefficient in poly.items()}


def divide_x_minus_y(poly: dict[Monomial, int], x: int, y: int) -> dict[Monomial, int]:
    """Divide a sparse polynomial by x-y, exactly, with a remainder check."""
    groups: dict[tuple[int, int, int, int], dict[int, dict[int, int]]] = defaultdict(lambda: defaultdict(dict))
    remaining = [index for index in range(6) if index not in (x, y)]
    for monomial, coefficient in poly.items():
        rest = tuple(monomial[index] for index in remaining)
        groups[rest][monomial[y]][monomial[x]] = coefficient
    quotient: dict[Monomial, int] = {}
    for rest, coefficients in groups.items():
        top = max(coefficients)
        q: dict[int, dict[int, int]] = {top - 1: {power: -value for power, value in coefficients[top].items()}}
        for ypower in range(top - 1, 0, -1):
            q[ypower - 1] = poly_add(shift_x(q[ypower]), coefficients.get(ypower, {}), -1)
        assert poly_add(coefficients.get(0, {}), shift_x(q[0]), -1) == {}
        for ypower, xpoly in q.items():
            for xpower, coefficient in xpoly.items():
                monomial = [0] * 6
                monomial[x], monomial[y] = xpower, ypower
                for index, exponent in zip(remaining, rest):
                    monomial[index] = exponent
                quotient[tuple(monomial)] = coefficient
    return quotient


def audit() -> dict[str, object]:
    derivatives = load()
    assert set(derivatives) == {"trans", "cycle"}
    # D_trans = d/da2 - d/da1 = (a1-a2) Q_trans;
    # D_cycle = d/da4 - d/da3 = (a3-a4) Q_cycle.
    trans = divide_x_minus_y(derivatives["trans"], 1, 2)
    cycle = divide_x_minus_y(derivatives["cycle"], 4, 5)
    assert trans and cycle
    result = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "raw_sha256": hashlib.sha256(RAW.read_bytes()).hexdigest(),
        "transposition_exchange": {"factor": "a1-a2", "quotient_terms": len(trans), "positive_coefficients": sum(value > 0 for value in trans.values()), "negative_coefficients": sum(value < 0 for value in trans.values())},
        "cycle_exchange": {"factor": "a3-a4", "quotient_terms": len(cycle), "positive_coefficients": sum(value > 0 for value in cycle.values()), "negative_coefficients": sum(value < 0 for value in cycle.values())},
        "claim_boundary": "Exact S3 exchange derivative factorization only. Mixed quotient coefficients reject a coefficientwise exchange proof but do not establish an exchange reversal or an arbitrary finite-group conclusion.",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
