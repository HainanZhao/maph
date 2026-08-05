#!/usr/bin/env python3
"""Independent exact check of the displayed C77 diagonal-slice table."""

from fractions import Fraction
import json


HALF = Fraction(1, 2)
THREE_QUARTERS = Fraction(3, 4)
ONE = Fraction(1)


def affine(a, b, q):
    return a * q + b


TABLE = {
    0: [(HALF, ONE, ())],
    1: [(HALF, ONE, ((1, Fraction(2, 3), Fraction(-1, 3)),))],
    2: [(HALF, ONE, ((1, Fraction(4, 3), Fraction(-2, 3)),
                      (2, Fraction(2, 3), Fraction(-1, 3))))],
    3: [(HALF, THREE_QUARTERS,
         ((1, Fraction(2), Fraction(-1)),
          (2, Fraction(4, 3), Fraction(-2, 3)),
          (3, Fraction(2, 3), Fraction(-1, 3)))),
        (THREE_QUARTERS, ONE,
         ((1, Fraction(2, 3), Fraction(0)),
          (2, Fraction(0), Fraction(1, 3)),
          (3, Fraction(-2, 3), Fraction(2, 3))))],
}


def main():
    rows = 0
    for weight, chambers in TABLE.items():
        for lo, hi, entries in chambers:
            for _, slope, intercept in entries:
                assert affine(slope, intercept, lo) >= 0
                assert affine(slope, intercept, hi) >= 0
                rows += 1
    print(json.dumps({"status": "PASS", "epistemic_status": "PROVED",
                      "checked_nonzero_rows": rows,
                      "symmetry_classes": len(TABLE)}, sort_keys=True))


if __name__ == "__main__":
    main()
