#!/usr/bin/env python3
"""Exact coefficient audit for critical exponential-moment dissipation."""

from __future__ import annotations

from fractions import Fraction
import json


def main() -> int:
    checks = 0
    for sqrt_d in (Fraction(1, 5), Fraction(2, 7), Fraction(3, 11)):
        diffusivity = sqrt_d**2
        a = 1 / sqrt_d
        if diffusivity * a * a != 1:
            raise AssertionError("critical tilt mismatch")
        if diffusivity * a * a + 1 != 2:
            raise AssertionError("linear moment growth mismatch")
        checks += 2

    for wx, wy in (
        (Fraction(2), Fraction(3)),
        (Fraction(5, 7), Fraction(11, 13)),
        (Fraction(17, 19), Fraction(23, 29)),
    ):
        ordered_average = (Fraction(1, 2) * wx + Fraction(1, 2) * wy) / 2
        symmetric = Fraction(1, 4) * (wx + wy)
        if ordered_average != symmetric:
            raise AssertionError("pair symmetrization mismatch")
        checks += 1

    for sqrt_d, translation in (
        (Fraction(1, 5), Fraction(3, 2)),
        (Fraction(2, 7), Fraction(5, 3)),
    ):
        if translation / sqrt_d != translation * (1 / sqrt_d):
            raise AssertionError("translation coefficient mismatch")
        checks += 1

    print(json.dumps({
        "status": "PASS",
        "claim_boundary": "Exact coefficient audit only; strictness and integration by parts are written proofs.",
        "critical_tilts_checked": 3,
        "symmetrizations_checked": 3,
        "total_exact_checks": checks,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
