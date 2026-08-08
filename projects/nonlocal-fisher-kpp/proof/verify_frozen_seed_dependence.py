#!/usr/bin/env python3
"""Exact exponent audit for the step-barrier seed-dependence witness."""

from __future__ import annotations

from fractions import Fraction
import json


def main() -> int:
    # On x<0 for the height-three step, phi=e^x H=(2/3)e^(2x).
    phi_coefficient = Fraction(2, 3)
    phi_exponent = Fraction(2)
    first_shift = Fraction(-2)
    second_shift = Fraction(-3)
    log_ratio = phi_exponent * (first_shift - second_shift)
    if log_ratio != 2:
        raise AssertionError("translated-seed phase ratio mismatch")

    # Both translates of a bump on [0,1] remain strictly left of the barrier.
    supports = ((first_shift, first_shift + 1), (second_shift, second_shift + 1))
    if any(right > 0 for _left, right in supports):
        raise AssertionError("seed crosses barrier")

    print(json.dumps({
        "status": "PASS",
        "claim_boundary": "Exact translated-step witness; nonlinear seed universality is not addressed.",
        "phi_coefficient": f"{phi_coefficient.numerator}/{phi_coefficient.denominator}",
        "phi_exponent": int(phi_exponent),
        "equal_mass_translations": [int(first_shift), int(second_shift)],
        "critical_phase_separation": int(log_ratio),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
