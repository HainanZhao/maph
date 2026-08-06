#!/usr/bin/env python3
"""Independent table proof for C84's named Z_14 target-box obstruction."""
from __future__ import annotations

import json


UNITS = (1, 3, 5, 9, 11, 13)
VECTOR = (0, 7) + (0,) * 11
TARGET = set(range(1, 13))


def main() -> None:
    assert all((s * 7) % 14 == 7 for s in UNITS)
    failures = []
    for r in UNITS:
        bad_coordinates = [
            index + 1
            for index, value in enumerate(VECTOR)
            if ((7 if value else 0) + r * (index + 1)) % 14 not in TARGET
        ]
        # The scalar s is a unit, so s*7=7 modulo 14 for every s in UNITS.
        assert bad_coordinates
        failures.append({"r": r, "bad_coordinates": bad_coordinates})
    print(json.dumps({
        "epistemic_status": "PROVED",
        "modulus": 14,
        "vector": VECTOR,
        "all_unit_s_have_s_times_7_equal_7": True,
        "r_rows": failures,
        "status": "PASS",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
