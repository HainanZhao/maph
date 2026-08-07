#!/usr/bin/env python3
"""Exact probe of the smallest proof-valid adaptive allocation extension."""

from __future__ import annotations

import functools
import importlib.util
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE_CHECKER = ROOT / "experiments" / "multi_spacer_adversarial_and_width5_overlap.py"
SPEC = importlib.util.spec_from_file_location("multispacer_base", BASE_CHECKER)
assert SPEC and SPEC.loader
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)


@functools.lru_cache(maxsize=None)
def adaptive_single_column(
    ordinary: tuple[int, ...], spacers: tuple[tuple[int, int], ...]
) -> bool:
    """Hybrid closure plus a recursively scheduled all-to-one spacer row."""
    if BASE.hybrid_feasible(ordinary, spacers):
        return True
    for spacer_index, (step, length) in enumerate(spacers):
        remaining = spacers[:spacer_index] + spacers[spacer_index + 1 :]
        total_charge = step * (length - 1)
        for ordinary_index, final_length in enumerate(ordinary):
            base_length = final_length - total_charge
            if base_length < 1:
                continue
            base = list(ordinary)
            base[ordinary_index] = base_length
            if not adaptive_single_column(tuple(base), remaining):
                continue

            # The first correction is the smallest. Matrix feasibility there
            # persists as this selected bracket grows by 2*step per increment.
            first_correction = base[:]
            first_correction[ordinary_index] = base_length + 2 * step
            if BASE.matrix_feasible(tuple(first_correction), remaining):
                return True
    return False


def main() -> None:
    assert not BASE.hybrid_feasible((5,), ((2, 2), (3, 2)))
    assert adaptive_single_column((5,), ((2, 2), (3, 2)))

    fib = BASE.fibonacci(125)
    steps = (2, 3, 5)
    hybrid_classes: set[int] = set()
    adaptive_classes: set[int] = set()
    for residue in range(60):
        m = 120 if residue == 0 else 60 + residue
        decompositions = []
        for offsets in itertools.permutations(range(1, 6), 3):
            if not all(fib[m + offset] % step == 0 for step, offset in zip(steps, offsets)):
                continue
            assigned = set(offsets)
            ordinary = tuple(
                fib[m + offset] for offset in range(1, 6) if offset not in assigned
            )
            spacers = tuple(
                (step, fib[m + offset] // step)
                for step, offset in zip(steps, offsets)
            )
            decompositions.append((ordinary, spacers))
        if any(BASE.hybrid_feasible(*row) for row in decompositions):
            hybrid_classes.add(residue)
        if any(adaptive_single_column(*row) for row in decompositions):
            adaptive_classes.add(residue)

    assert adaptive_classes == hybrid_classes
    print(
        json.dumps(
            {
                "a5_near_miss_certified": True,
                "adaptive_classes": sorted(adaptive_classes),
                "hybrid_classes": sorted(hybrid_classes),
                "status": "NO_WIDTH5_COVERAGE_GAIN",
                "width5_new_classes": [],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
