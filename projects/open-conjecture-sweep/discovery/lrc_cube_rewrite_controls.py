#!/usr/bin/env python3
"""Exact generic controls for Cycle 48 Möbius and cube rewrites."""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import itertools
import json
from pathlib import Path

from lrc_cube_rewrite import chosen_cubes, mobius_tensor, normal_form, normalized_cube, pair_marginals, subtract_normalized

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle48-cube-rewrite"


def main():
    delta = {(0, 0): Fraction(1)}
    cycle = {(0, 0): Fraction(1), (0, 1): Fraction(-1), (1, 0): Fraction(-1), (1, 1): Fraction(1)}
    pair_flows = {}
    for index, pair in enumerate(itertools.combinations(range(3), 2), start=1):
        flow = defaultdict(Fraction, delta)
        for cell, value in cycle.items():
            flow[cell] += Fraction(index, 5) * value
        pair_flows[pair] = {cell: value for cell, value in flow.items() if value}
    mobius = mobius_tensor(pair_flows, (0, 0, 0))
    assert pair_marginals(mobius) == pair_flows

    cube_checks = 0
    for size0 in range(2, 5):
        for size1 in range(2, 5):
            for size2 in range(2, 5):
                supports = tuple(tuple(range(size)) for size in (size0, size1, size2))
                for pivot in itertools.product(*supports):
                    alternatives = tuple(next(owner for owner in supports[index] if owner != pivot[index]) for index in range(3))
                    cube = normalized_cube(pivot, alternatives)
                    assert all(not values for values in pair_marginals(cube).values())
                    cube_checks += 1

    supports = ((0, 1), (0, 1), (0, 1))
    forbidden = {(0, 0, 0)}
    reducers, counts = chosen_cubes(supports, forbidden)
    repaired = normal_form({(0, 0, 0): Fraction(3)}, forbidden, reducers)
    assert repaired["status"] == "REPAIRED" and not (set(repaired["tensor"]) & forbidden)
    # The repaired tensor and source differ by a cube, so their marginals agree.
    assert pair_marginals(repaired["tensor"]) == pair_marginals({(0, 0, 0): Fraction(3)})

    multi_forbidden = {(0, 0, 0), (0, 0, 1)}
    multi_reducers, _ = chosen_cubes(((0, 1), (0, 1), (0, 1, 2)), multi_forbidden)
    multi = normal_form({(0, 0, 0): Fraction(2), (0, 0, 1): Fraction(-1)}, multi_forbidden, multi_reducers)
    assert multi["status"] == "REPAIRED" and len(multi["steps"]) >= 1

    missing_reducers, _ = chosen_cubes(((0,), (0, 1), (0, 1)), {(0, 0, 0)})
    missing = normal_form({(0, 0, 0): Fraction(1)}, {(0, 0, 0)}, missing_reducers)
    assert missing["status"] == "UNREPAIRED" and missing["first_missing"] == (0, 0, 0)

    diamond_supports = ((0, 1, 2),) * 3
    diamond_forbidden = {(0, 0, 0)}
    diamond_reducers, _ = chosen_cubes(diamond_supports, diamond_forbidden)
    first = normalized_cube((0, 0, 0), (1, 1, 1))
    second = normalized_cube((0, 0, 0), (2, 2, 2))
    difference = subtract_normalized(first, second, (0, 0, 0))
    diamond = normal_form(difference, diamond_forbidden, diamond_reducers)
    assert diamond["status"] == "REPAIRED" and diamond["tensor"]
    assert all(not values for values in pair_marginals(diamond["tensor"]).values())

    bad_move = {(0, 0, 0): Fraction(1), (1, 1, 1): Fraction(-1)}
    assert any(pair_marginals(bad_move).values())

    result = {
        "status": "PASS", "epistemic_status": "PROVED", "stage": "GENERIC_MOBIUS_CUBE_CONTROLS",
        "mobius_symbolic_instance": "PASS", "cube_kernel_checks": cube_checks,
        "full_cube_repair": {"status": repaired["status"], "steps": len(repaired["steps"]), "choices": counts[(0, 0, 0)]},
        "multi_defect_repair": {"status": multi["status"], "steps": len(multi["steps"])},
        "unrepaired_structural_zero": {"status": missing["status"], "first_missing": list(missing["first_missing"])},
        "literal_nonjoinable_diamond": {"status": "NONJOINABLE", "normal_form_nonzero": len(diamond["tensor"])},
        "nonkernel_move_rejected": True,
        "claim_boundary": "Generic exact identity and rewrite controls only; no p199 principal face is classified.",
    }
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / "generic-controls.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "cube_kernel_checks": cube_checks, "nonjoinable": True}, sort_keys=True))


if __name__ == "__main__":
    main()
