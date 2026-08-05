#!/usr/bin/env python3
"""Exact factor audit for C61 central-transverse curvature terms."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "discovery/out/cycle61-flat-stratum/transverse-curvature.tsv"
OUT = ROOT / "discovery/out/cycle61-flat-stratum/transverse-audit.json"

Monomial = tuple[int, int, int]  # e, t, c exponents
Poly = dict[Monomial, int]


def load() -> dict[tuple[str, int], Poly]:
    rows: dict[tuple[str, int], Poly] = defaultdict(dict)
    with RAW.open() as source:
        for row in csv.DictReader(source, delimiter="\t"):
            key = (row["direction"], int(row["degree"]))
            monomial = (int(row["e"]), int(row["t"]), int(row["c"]))
            rows[key][monomial] = int(row["coefficient"])
    return rows


def divide_by_c_minus_e(poly: Poly) -> Poly:
    """Exact sparse division by c-e, with a zero-remainder assertion."""
    grouped: dict[tuple[int, int], dict[int, int]] = defaultdict(dict)
    for (ep, tp, cp), coefficient in poly.items():
        grouped[(ep, tp)][cp] = coefficient
    # The recurrence must couple e exponents, so use the c-coefficients as
    # polynomials in e for each fixed t.
    by_t: dict[int, dict[int, dict[int, int]]] = defaultdict(lambda: defaultdict(dict))
    for (ep, tp, cp), coefficient in poly.items():
        by_t[tp][cp][ep] = coefficient
    quotient: Poly = {}
    for tp, coefficients in by_t.items():
        degree = max(coefficients)
        q: dict[int, dict[int, int]] = {}
        q[degree - 1] = dict(coefficients[degree])
        for cp in range(degree - 1, 0, -1):
            current = dict(coefficients.get(cp, {}))
            for ep, coefficient in q[cp].items():
                current[ep + 1] = current.get(ep + 1, 0) + coefficient
            q[cp - 1] = {ep: coefficient for ep, coefficient in current.items() if coefficient}
        remainder = dict(coefficients.get(0, {}))
        for ep, coefficient in q[0].items():
            remainder[ep + 1] = remainder.get(ep + 1, 0) + coefficient
        assert not {ep: coefficient for ep, coefficient in remainder.items() if coefficient}
        for cp, ep_coefficients in q.items():
            for ep, coefficient in ep_coefficients.items():
                if coefficient:
                    quotient[(ep, tp, cp)] = coefficient
    return quotient


def factor(poly: Poly, power: int) -> Poly:
    result = poly
    for _ in range(power):
        result = divide_by_c_minus_e(result)
    return result


def audit() -> dict[str, object]:
    rows = load()
    expected = {
        ("standard_axis", 2): 2,
        ("standard_generic", 2): 2,
        ("sign", 2): 2,
        ("standard_generic", 3): 4,
    }
    assert set(rows) == set(expected)
    factors: dict[str, object] = {}
    for key, power in expected.items():
        quotient = factor(rows[key], power)
        assert quotient and all(coefficient > 0 for coefficient in quotient.values())
        factors[f"{key[0]}_degree_{key[1]}"] = {
            "factor": f"(c-e)^{power}",
            "quotient_terms": len(quotient),
            "quotient_all_coefficients_positive": True,
        }
    result = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "claim_boundary": "Exact S3 C61 transverse Taylor-factor audit only; not a universal Zhao or Sidorenko proof.",
        "raw_sha256": hashlib.sha256(RAW.read_bytes()).hexdigest(),
        "factors": factors,
        "consequence": "At positive central parameters the standard and sign Hessian coefficients are nonnegative and vanish only on c=e; the generic standard cubic is O((c-e)^4).",
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    return result


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
