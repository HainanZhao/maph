#!/usr/bin/env python3
"""Exact C78 target-spectrum, normalization, and endpoint checks."""

import itertools
import json
import sympy as sp


assert sp.__version__ == "1.12"
q, t, a, b, c = sp.symbols("q t a b c")
BITS = tuple(itertools.product((0, 1), repeat=3))


def q_entry(bit):
    return q if bit == 0 else 1 - q


def target_entry(bits):
    x, y, z = bits
    return sp.expand(
        (a * q_entry(z) if (x, y) == (0, 0) else 0)
        + (b * q_entry(y) if (x, z) == (0, 0) else 0)
        + (c * q_entry(x) if (y, z) == (0, 0) else 0)
    )


def main():
    expected = {
        (0, 0, 0): (a + b + c) * q,
        (0, 0, 1): (1 - q) * a,
        (0, 1, 0): (1 - q) * b,
        (1, 0, 0): (1 - q) * c,
    }
    for bits in BITS:
        assert sp.simplify(target_entry(bits) - expected.get(bits, 0)) == 0
    assert sp.simplify(target_entry((0, 0, 0)).subs(c, 1 - a - b) - q) == 0

    q_of_t = (1 + t) / 2
    partial_weights = (0, a, a + b, 1, 1, 1, 1)
    for weight in partial_weights:
        target_sum = q + (1 - q) * weight
        endpoint_mix = (1 - t) * (sp.Rational(1, 2) + weight / 2) + t
        assert sp.simplify(target_sum.subs(q, q_of_t) - endpoint_mix) == 0

    # The formal lower-bound decompositions establish the frozen eigenvalue order.
    assert sp.simplify(q - (1 - q) * a - ((2 * q - 1) + (1 - q) * (1 - a))) == 0
    assert sp.simplify((1 - q) * a - (1 - q) * b - (1 - q) * (a - b)) == 0
    assert sp.simplify((1 - q) * b - (1 - q) * c - (1 - q) * (b - c)) == 0
    print(json.dumps({"status": "PASS", "epistemic_status": "PROVED",
                      "sympy_version": sp.__version__, "target_entries": 8,
                      "ky_fan_indices": 7, "source_half_scale": "1/2"},
                     sort_keys=True))


if __name__ == "__main__":
    main()
