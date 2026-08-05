#!/usr/bin/env python3
"""Independently reconstruct every C67 polynomial after factor stripping."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


VARIABLES = ("x", "y", "r", "h")


def load(path: Path) -> dict[tuple[int, ...], int]:
    result: defaultdict[tuple[int, ...], int] = defaultdict(int)
    with path.open(newline="") as handle:
        rows = csv.reader(handle, delimiter="\t")
        next(rows)
        for row in rows:
            result[tuple(map(int, row[:4]))] += int(row[4])
    return {key: value for key, value in result.items() if value}


def multiply(
    polynomial: dict[tuple[int, ...], int], axis: int, endpoint: int
) -> dict[tuple[int, ...], int]:
    result: defaultdict[tuple[int, ...], int] = defaultdict(int)
    for exponent, coefficient in polynomial.items():
        raised = exponent[:axis] + (exponent[axis] + 1,) + exponent[axis + 1 :]
        if endpoint == 0:
            result[raised] += coefficient
        else:
            result[exponent] += coefficient
            result[raised] -= coefficient
    return {key: value for key, value in result.items() if value}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("stripped_dir", type=Path)
    args = parser.parse_args()
    report = json.loads((args.stripped_dir / "factor-report.json").read_text())
    checked = 0
    for name, record in report["charts"].items():
        reconstructed = load(args.stripped_dir / f"{name}.tsv")
        for factor, multiplicity in record["factors"].items():
            endpoint = int(factor.startswith("1-"))
            variable = factor[2:] if endpoint else factor
            for _ in range(multiplicity):
                reconstructed = multiply(reconstructed, VARIABLES.index(variable), endpoint)
        expected = load(args.source_dir / f"{name}.tsv")
        assert reconstructed == expected, name
        checked += 1
    print(json.dumps({"status": "PASS", "epistemic_status": "PROVED", "charts": checked}))


if __name__ == "__main__":
    main()
