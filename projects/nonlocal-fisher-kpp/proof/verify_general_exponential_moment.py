#!/usr/bin/env python3
"""Exact algebra audit for the general exponential-moment identity."""

from __future__ import annotations

from fractions import Fraction
import json


def main() -> int:
    checks = 0

    # Audit the linear dispersion coefficient and its critical minimum at
    # several exact rational square roots of D.
    for sqrt_d in (Fraction(1, 5), Fraction(2, 7), Fraction(3, 11)):
        diffusivity = sqrt_d**2
        critical_a = 1 / sqrt_d
        if 1 + diffusivity * critical_a**2 != 2:
            raise AssertionError("critical linear growth mismatch")
        if diffusivity * critical_a + 1 / critical_a != 2 * sqrt_d:
            raise AssertionError("dispersion minimum mismatch")
        checks += 2

    # The ordered interaction and its x/y-swapped copy have equal kernel
    # coefficient for an even kernel. Averaging yields the symmetric factor.
    for wx, wy, kernel_value in (
        (Fraction(2), Fraction(3), Fraction(5, 7)),
        (Fraction(11, 13), Fraction(17, 19), Fraction(23, 29)),
        (Fraction(31, 37), Fraction(41, 43), Fraction(47, 53)),
    ):
        ordered_pair_sum = kernel_value * wx + kernel_value * wy
        symmetric_pair_sum = kernel_value * (wx + wy)
        if ordered_pair_sum / 2 != symmetric_pair_sum / 2:
            raise AssertionError("even-kernel symmetrization mismatch")
        checks += 1

    # Audit the rearrangement from logarithmic moment growth to speed.
    for diffusivity, a, delay, duration in (
        (Fraction(1, 25), Fraction(5), Fraction(2, 3), Fraction(7, 2)),
        (Fraction(4, 49), Fraction(7, 2), Fraction(5, 11), Fraction(13, 3)),
    ):
        phase = (1 + diffusivity * a**2) * duration - delay
        speed_from_phase = phase / (a * duration)
        speed_from_formula = diffusivity * a + 1 / a - delay / (a * duration)
        if speed_from_phase != speed_from_formula:
            raise AssertionError("translation-delay rearrangement mismatch")
        checks += 1

    print(json.dumps({
        "status": "PASS",
        "claim_boundary": (
            "Exact coefficient and rearrangement audit only; integration by "
            "parts, kernel exchange, finiteness, and strictness are written proofs."
        ),
        "critical_dispersion_checks": 6,
        "symmetrizations_checked": 3,
        "translation_checks": 2,
        "total_exact_checks": checks,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
