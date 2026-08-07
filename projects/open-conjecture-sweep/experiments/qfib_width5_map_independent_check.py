#!/usr/bin/env python3
"""Independent second implementation of the width-five class map."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REFERENCE = Path(__file__).with_name("qfib_width_5_6_denominator_map.json")
ATOMS = (2, 3, 5)


def fibonacci_mod(index: int, modulus: int) -> int:
    previous, current = 0, 1
    for _ in range(index):
        previous, current = current, (previous + current) % modulus
    return previous


def enumerate_matchings(
    adjacency: dict[int, tuple[int, ...]],
    atoms: tuple[int, ...],
    position: int = 0,
    used: frozenset[int] = frozenset(),
) -> int:
    if position == len(atoms):
        return 1
    total = 0
    atom = atoms[position]
    for offset in adjacency[atom]:
        if offset not in used:
            total += enumerate_matchings(
                adjacency, atoms, position + 1, used | {offset}
            )
    return total


def independent_table() -> dict[str, dict]:
    table = {}
    for residue in range(60):
        representative = 120 if residue == 0 else 60 + residue
        adjacency = {
            atom: tuple(
                offset
                for offset in range(1, 6)
                if fibonacci_mod(representative + offset, atom) == 0
            )
            for atom in ATOMS
        }
        count = enumerate_matchings(adjacency, ATOMS)
        table[str(residue)] = {
            "adjacency": {
                str(atom): list(adjacency[atom]) for atom in ATOMS
            },
            "injective_assignment_count": count,
            "minimum_effective_spacers": 3 if count else None,
            "optimal_step_multisets": [[2, 3, 5]] if count else [],
        }
    return table


def canonical_bytes(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main() -> None:
    reference_document = json.loads(REFERENCE.read_text())
    reference = reference_document["widths"]["5"][
        "residue_rows_mod_60_stable_from_m_61"
    ]
    independent = independent_table()
    reference_bytes = canonical_bytes(reference)
    independent_bytes = canonical_bytes(independent)
    assert independent_bytes == reference_bytes

    bad = [
        int(residue)
        for residue, row in independent.items()
        if row["injective_assignment_count"] == 0
    ]
    good = [row for row in independent.values() if row["injective_assignment_count"]]
    assert len(bad) == 18
    assert all(row["minimum_effective_spacers"] == 3 for row in good)
    print(
        json.dumps(
            {
                "bad_class_count": len(bad),
                "bad_classes": bad,
                "canonical_table_sha256": hashlib.sha256(reference_bytes).hexdigest(),
                "good_classes": len(good),
                "good_class_spacers": [2, 3, 5],
                "status": "BYTE_IDENTICAL",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
