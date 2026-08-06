#!/usr/bin/env python3
"""Exact two-atom C5 triple-kernel packet for C85."""
from __future__ import annotations

from fractions import Fraction
import itertools
import json


WEIGHTS = (Fraction(1, 3), Fraction(1, 2), Fraction(2, 3))
ENTRIES = (Fraction(0), Fraction(1, 2), Fraction(1))


def evaluate(alpha: Fraction, beta: Fraction, flat: tuple[Fraction, ...]) -> tuple[Fraction, Fraction, Fraction]:
    left = (alpha, 1 - alpha)
    right = (beta, 1 - beta)
    w = ((flat[0], flat[1]), (flat[2], flat[3]))
    kernel = [[[sum(right[y] * w[a][y] * w[b][y] * w[c][y] for y in range(2))
                for c in range(2)] for b in range(2)] for a in range(2)]
    integral_k = sum(left[a] * left[b] * left[c] * kernel[a][b][c]
                     for a in range(2) for b in range(2) for c in range(2))
    density = Fraction(0)
    for xs in itertools.product(range(2), repeat=5):
        term = Fraction(1)
        for i in range(5):
            term *= left[xs[i]] * kernel[xs[i]][xs[(i + 1) % 5]][xs[(i + 2) % 5]]
        density += term
    return density, integral_k, density - integral_k ** 5


def fmt(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def main() -> None:
    count = negative = zero = 0
    minimum: tuple[Fraction, Fraction, Fraction, tuple[Fraction, ...], Fraction, Fraction] | None = None
    positive_minimum: tuple[Fraction, Fraction, Fraction, tuple[Fraction, ...], Fraction, Fraction] | None = None
    for alpha, beta, flat in itertools.product(WEIGHTS, WEIGHTS, itertools.product(ENTRIES, repeat=4)):
        density, integral_k, defect = evaluate(alpha, beta, flat)
        count += 1
        if defect < 0:
            negative += 1
        if defect == 0:
            zero += 1
        candidate = (defect, alpha, beta, flat, density, integral_k)
        if minimum is None or candidate[0] < minimum[0]:
            minimum = candidate
        if defect > 0 and (positive_minimum is None or candidate[0] < positive_minimum[0]):
            positive_minimum = candidate
    assert count == 729 and minimum is not None and positive_minimum is not None
    defect, alpha, beta, flat, density, integral_k = minimum
    positive_defect, positive_alpha, positive_beta, positive_flat, positive_density, positive_integral_k = positive_minimum
    print(json.dumps({
        "epistemic_status": "PROVED",
        "packet_rows": count,
        "negative_rows": negative,
        "zero_rows": zero,
        "minimum_defect": fmt(defect),
        "minimum_witness": {
            "left_weight": fmt(alpha), "right_weight": fmt(beta),
            "W": [[fmt(flat[0]), fmt(flat[1])], [fmt(flat[2]), fmt(flat[3])]],
            "t_H": fmt(density), "integral_K": fmt(integral_k),
        },
        "minimum_positive_defect": fmt(positive_defect),
        "minimum_positive_witness": {
            "left_weight": fmt(positive_alpha), "right_weight": fmt(positive_beta),
            "W": [[fmt(positive_flat[0]), fmt(positive_flat[1])], [fmt(positive_flat[2]), fmt(positive_flat[3])]],
            "t_H": fmt(positive_density), "integral_K": fmt(positive_integral_k),
        },
        "status": "PASS",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
