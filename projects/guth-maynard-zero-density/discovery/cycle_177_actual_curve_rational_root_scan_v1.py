#!/usr/bin/env python3
"""Frozen non-proof sanity check for Cycle 177's symbolic rational-root family."""
from __future__ import annotations

from decimal import Decimal, ROUND_FLOOR, getcontext
import json


getcontext().prec = 100
PI = Decimal("3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679")
C = Decimal(1)
LABEL_FRACTION = Decimal(1) / Decimal(4)
R_VALUES = (1, 2, 3, 5, 8)
L_VALUES = (10, 100, 1000)


def floor_decimal(value: Decimal) -> int:
    return int(value.to_integral_value(rounding=ROUND_FLOOR))


def scan_one(r: int, label: int) -> dict[str, object]:
    r_value = Decimal(r)
    base = Decimal(1) + Decimal(1) / r_value
    delta = Decimal(2) * PI * Decimal(label) / base.ln()
    x_value = delta ** (Decimal(5) / Decimal(3))
    height = floor_decimal(x_value ** (Decimal(11) / Decimal(25)))
    alpha = (Decimal(2) * PI * Decimal(label) / delta).exp() - Decimal(1)
    max_multiplier = height // r
    failures = []
    for multiplier in range(1, max_multiplier + 1):
        value = Decimal(r * multiplier) * alpha
        if abs(value - Decimal(multiplier)) > C / x_value:
            failures.append(multiplier)
    return {
        "r": r,
        "L": label,
        "ell_over_delta": str(Decimal(label) / delta),
        "allowed": Decimal(label) <= LABEL_FRACTION * delta,
        "height": height,
        "alpha_minus_1_over_r": str(alpha - Decimal(1) / r_value),
        "multipliers": max_multiplier,
        "failed_multipliers": failures,
    }


def main() -> int:
    rows = [scan_one(r, label) for r in R_VALUES for label in L_VALUES]
    if any(not row["allowed"] or row["failed_multipliers"] for row in rows):
        raise SystemExit("frozen rational-root sanity check failed")
    print(json.dumps({"epistemic_status": "RECOGNIZED", "precision": getcontext().prec, "rows": rows}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
