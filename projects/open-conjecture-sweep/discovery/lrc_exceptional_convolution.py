#!/usr/bin/env python3
"""Cycle 30 exceptional-atom additive convolution closure test."""
from __future__ import annotations

from collections import Counter
import json
import math
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle30-crt-synchronization"
Q, K = 2786, 13


def mask(speed: int) -> int:
    value = 0
    for point in range(Q):
        residue = speed * point % Q
        if (K + 1) * min(residue, Q - residue) < Q:
            value |= 1 << point
    return value


def algebra() -> tuple[list[tuple[int, int]], list[list[int]]]:
    rows: dict[int, int] = {}
    for speed in range(Q):
        if math.gcd(speed, Q) not in {1, 2, 7, 14}:
            continue
        value = mask(speed)
        rows.setdefault(value, speed)
    generators = sorted(((speed, value) for value, speed in rows.items()))
    classes: dict[bytes, list[int]] = {}
    ordered_masks = [value for _speed, value in generators]
    for point in range(Q):
        signature = bytes((value >> point) & 1 for value in ordered_masks)
        classes.setdefault(signature, []).append(point)
    atoms = sorted(classes.values(), key=lambda points: points[0])
    if len(generators) != 1386 or Counter(map(len, atoms)) != Counter({2: 1386, 1: 2, 6: 2}):
        raise AssertionError("frozen p199 algebra")
    return generators, atoms


def convolution(exceptional: list[int], generator: int) -> list[int]:
    return [sum((generator >> ((point - source) % Q)) & 1 for source in exceptional) for point in range(Q)]


def main() -> None:
    started = time.monotonic()
    generators, atoms = algebra()
    exceptional_atoms = [atom for atom in atoms if len(atom) == 6]
    if exceptional_atoms != [
        [199, 597, 995, 1791, 2189, 2587],
        [398, 796, 1194, 1592, 1990, 2388],
    ]:
        raise AssertionError("exceptional atom identity")
    witness = None
    checked_profiles = 0
    incidence_checks = 0
    for exceptional_index, exceptional in enumerate(exceptional_atoms):
        for speed, generator in generators:
            profile = convolution(exceptional, generator)
            checked_profiles += 1
            incidence_checks += len(exceptional) * Q
            for atom_index, atom in enumerate(atoms):
                values = [(point, profile[point]) for point in atom]
                if len({value for _point, value in values}) > 1:
                    left = values[0]
                    right = next(row for row in values[1:] if row[1] != left[1])
                    witness = {
                        "exceptional_atom_index": exceptional_index,
                        "exceptional_atom": exceptional,
                        "generator_speed": speed,
                        "generator_gcd": math.gcd(speed, Q),
                        "target_atom_index": atom_index,
                        "target_atom": atom,
                        "left_point": left[0],
                        "left_value": left[1],
                        "right_point": right[0],
                        "right_value": right[1],
                    }
                    break
            if witness is not None:
                break
        if witness is not None:
            break
    result = {
        "status": "CONTAINED" if witness else "PASS",
        "epistemic_status": "OBSERVED",
        "q": Q,
        "generator_count": len(generators),
        "pointwise_atom_count": len(atoms),
        "negation_orbit_count": (Q + 2) // 2,
        "exceptional_atom_count": len(exceptional_atoms),
        "planned_profiles": len(exceptional_atoms) * len(generators),
        "checked_profiles": checked_profiles,
        "incidence_checks": incidence_checks,
        "first_splitting_witness": witness,
        "wall_seconds": time.monotonic() - started,
    }
    temporary = OUT / "convolution-result.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "convolution-result.json")
    print(json.dumps({"status": result["status"], "checked_profiles": checked_profiles, "witness": witness}, sort_keys=True))


if __name__ == "__main__":
    main()
