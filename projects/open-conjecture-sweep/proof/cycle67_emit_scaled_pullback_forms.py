#!/usr/bin/env python3
"""Emit six-times-scaled integer z-coordinate forms for all C67 charts."""

import argparse
import csv
from pathlib import Path

from cycle67_equality_blowup import charts, scale


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        rows = csv.writer(handle, delimiter="\t", lineterminator="\n")
        rows.writerow(("chart", "family", "value", "x", "y", "r", "h", "coefficient"))
        for name, (family, forms) in charts().items():
            for value, form in enumerate(forms):
                for exponent, coefficient in sorted(scale(form, 6).items()):
                    assert coefficient.denominator == 1
                    rows.writerow((name, family, value, *exponent, coefficient.numerator))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
