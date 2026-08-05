#!/usr/bin/env python3
"""Exact chamber proof for C77's diagonal three-qubit slice.

For each computational-basis global state x, H_x and the aligned target are
diagonal with entries affine in q.  The script partitions [1/2,1] at every
entry crossing, fixes the order on each chamber, and checks every Ky Fan
difference exactly at both endpoints.
"""

from __future__ import annotations

from fractions import Fraction
import itertools
import json


BITS = tuple(itertools.product((0, 1), repeat=3))
HALF = Fraction(1, 2)
ONE = Fraction(1)


def add(left, right):
    return left[0] + right[0], left[1] + right[1]


def scale(value, factor):
    return value[0] * factor, value[1] * factor


def evaluate(value, q):
    return value[0] * q + value[1]


def q_entry(bit):
    return (Fraction(1), Fraction(0)) if bit == 0 else (Fraction(-1), Fraction(1))


def h_entries(x):
    entries = []
    for y in BITS:
        total = (Fraction(0), Fraction(0))
        if y[:2] == x[:2]:
            total = add(total, q_entry(y[2]))
        if (y[0], y[2]) == (x[0], x[2]):
            total = add(total, q_entry(y[1]))
        if y[1:] == x[1:]:
            total = add(total, q_entry(y[0]))
        entries.append(scale(total, Fraction(1, 3)))
    return entries


def breakpoints(*entry_lists):
    points = {HALF, ONE}
    for entries in entry_lists:
        for left, right in itertools.combinations(entries, 2):
            slope = left[0] - right[0]
            intercept = left[1] - right[1]
            if slope:
                root = -intercept / slope
                if HALF <= root <= ONE:
                    points.add(root)
    return tuple(sorted(points))


def ordered(entries, q):
    return sorted(entries, key=lambda entry: evaluate(entry, q), reverse=True)


def total_top(entries, k, q):
    return sum((evaluate(entry, q) for entry in ordered(entries, q)[:k]), Fraction(0))


def main():
    target = h_entries((0, 0, 0))
    certificate = []
    for x in BITS:
        entries = h_entries(x)
        points = breakpoints(entries, target)
        for lo, hi in zip(points, points[1:]):
            mid = (lo + hi) / 2
            ordered_h = ordered(entries, mid)
            ordered_t = ordered(target, mid)
            for k in range(1, 8):
                difference = tuple(
                    sum((ordered_t[i][j] - ordered_h[i][j] for i in range(k)), Fraction(0))
                    for j in (0, 1)
                )
                if evaluate(difference, lo) < 0 or evaluate(difference, hi) < 0:
                    raise AssertionError((x, lo, hi, k, difference))
                certificate.append({"x": "".join(map(str, x)), "lo": str(lo),
                                    "hi": str(hi), "k": k,
                                    "difference": [str(difference[0]), str(difference[1])],
                                    "endpoint_values": [str(evaluate(difference, lo)),
                                                        str(evaluate(difference, hi))]})
    print(json.dumps({"claim_tag": "PROVED", "basis_states": len(BITS),
                      "certificate_rows": len(certificate), "all_rows_nonnegative": True,
                      "certificate": certificate}, sort_keys=True))


if __name__ == "__main__":
    main()
