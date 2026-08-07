#!/usr/bin/env python3
"""Independent modular-recurrence check of the width-six structure table."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REFERENCE = Path(__file__).with_name("qfib_width6_structural_test.json")
DEMAND = ((2, 2), (3, 1), (4, 1), (5, 1), (8, 1))


def zero_offsets(start: int, modulus: int) -> list[int]:
    previous, current = 0, 1
    values = [0]
    for _ in range(start + 6):
        previous, current = current, (previous + current) % modulus
        values.append(previous)
    return [offset for offset in range(1, 7) if values[start + offset] == 0]


def choose_two(count: int) -> int:
    return count * (count - 1) // 2


def independent_rows() -> dict[str, dict]:
    rows = {}
    for residue in range(60):
        representative = 120 if residue == 0 else 60 + residue
        eligible = {
            modulus: zero_offsets(representative, modulus)
            for modulus, _ in DEMAND
        }
        assignments = choose_two(len(eligible[2]))
        for modulus, multiplicity in DEMAND:
            if multiplicity == 1:
                assignments *= len(eligible[modulus])
        rows[str(residue)] = {
            "assignment_count": assignments,
            "eligible_offsets": {
                str(modulus): eligible[modulus] for modulus, _ in DEMAND
            },
        }
    return rows


def canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main() -> None:
    reference = json.loads(REFERENCE.read_text())["residue_rows_mod_60"]
    independent = independent_rows()
    reference_bytes = canonical(reference)
    independent_bytes = canonical(independent)
    assert independent_bytes == reference_bytes
    assert all(row["assignment_count"] > 0 for row in independent.values())
    print(
        json.dumps(
            {
                "canonical_table_sha256": hashlib.sha256(reference_bytes).hexdigest(),
                "residue_classes": len(independent),
                "status": "BYTE_IDENTICAL",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
