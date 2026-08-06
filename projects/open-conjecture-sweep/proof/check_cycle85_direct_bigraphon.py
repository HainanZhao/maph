#!/usr/bin/env python3
"""Independent direct 15-edge calculation for C85's two-atom packet."""
from __future__ import annotations

from fractions import Fraction
import itertools
import json


WEIGHTS = (Fraction(1, 3), Fraction(1, 2), Fraction(2, 3))
ENTRIES = (Fraction(0), Fraction(1, 2), Fraction(1))


def direct(alpha: Fraction, beta: Fraction, flat: tuple[Fraction, ...]) -> tuple[Fraction, Fraction, Fraction]:
    left, right = (alpha, 1 - alpha), (beta, 1 - beta)
    w = ((flat[0], flat[1]), (flat[2], flat[3]))
    t_h = Fraction(0)
    for xs in itertools.product(range(2), repeat=5):
        for ys in itertools.product(range(2), repeat=5):
            term = Fraction(1)
            for value in xs:
                term *= left[value]
            for value in ys:
                term *= right[value]
            for i in range(5):
                for shift in (0, 1, 2):
                    term *= w[xs[(i + shift) % 5]][ys[i]]
            t_h += term
    integral_k = sum(
        left[a] * left[b] * left[c] * right[y] * w[a][y] * w[b][y] * w[c][y]
        for a in range(2) for b in range(2) for c in range(2) for y in range(2)
    )
    return t_h, integral_k, t_h - integral_k ** 5


def fmt(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def main() -> None:
    negative = rows = zero = 0
    minimum: tuple[Fraction, Fraction, Fraction, tuple[Fraction, ...], Fraction, Fraction] | None = None
    positive_minimum: tuple[Fraction, Fraction, Fraction, tuple[Fraction, ...], Fraction, Fraction] | None = None
    for alpha, beta, flat in itertools.product(WEIGHTS, WEIGHTS, itertools.product(ENTRIES, repeat=4)):
        t_h, integral_k, defect = direct(alpha, beta, flat)
        rows += 1
        negative += defect < 0
        zero += defect == 0
        candidate = (defect, alpha, beta, flat, t_h, integral_k)
        if minimum is None or candidate[0] < minimum[0]:
            minimum = candidate
        if defect > 0 and (positive_minimum is None or candidate[0] < positive_minimum[0]):
            positive_minimum = candidate
    assert rows == 729 and minimum is not None and positive_minimum is not None
    defect, alpha, beta, flat, t_h, integral_k = minimum
    positive_defect, positive_alpha, positive_beta, positive_flat, positive_t_h, positive_integral_k = positive_minimum
    print(json.dumps({
        "epistemic_status": "PROVED", "packet_rows": rows, "negative_rows": negative, "zero_rows": zero,
        "minimum_defect": fmt(defect),
        "minimum_witness": {"left_weight": fmt(alpha), "right_weight": fmt(beta),
                            "W": [[fmt(flat[0]), fmt(flat[1])], [fmt(flat[2]), fmt(flat[3])]],
                            "t_H": fmt(t_h), "integral_K": fmt(integral_k)},
        "minimum_positive_defect": fmt(positive_defect),
        "minimum_positive_witness": {"left_weight": fmt(positive_alpha), "right_weight": fmt(positive_beta),
                                      "W": [[fmt(positive_flat[0]), fmt(positive_flat[1])], [fmt(positive_flat[2]), fmt(positive_flat[3])]],
                                      "t_H": fmt(positive_t_h), "integral_K": fmt(positive_integral_k)},
        "status": "PASS",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
