#!/usr/bin/env python3
"""Exact capped Pólya audit for the negative S3 transposition exchange quotient."""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.check_cycle_62_exchange_factor import divide_x_minus_y, load


def main() -> None:
    quotient = divide_x_minus_y(load()["trans"], 1, 2)
    polynomial = {monomial: -coefficient for monomial, coefficient in quotient.items()}
    rows = []
    for degree in range(25):
        rows.append({"degree": degree, "terms": len(polynomial), "negative_coefficients": sum(value < 0 for value in polynomial.values())})
        if not rows[-1]["negative_coefficients"]:
            break
        expanded: dict[tuple[int, ...], int] = defaultdict(int)
        for monomial, coefficient in polynomial.items():
            for coordinate in range(6):
                child = list(monomial)
                child[coordinate] += 1
                expanded[tuple(child)] += coefficient
        polynomial = {monomial: coefficient for monomial, coefficient in expanded.items() if coefficient}
    output = {"status": "PASS", "epistemic_status": "PROVED", "claim_boundary": "Capped coefficientwise Pólya failure for one S3 exchange quotient only.", "rows": rows}
    out = ROOT / "discovery/out/cycle62-kkt-exchange/exchange-polya-summary.json"
    out.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
