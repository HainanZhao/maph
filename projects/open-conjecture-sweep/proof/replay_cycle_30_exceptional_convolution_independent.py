#!/usr/bin/env python3
"""Independent translated-support replay of Cycle 30 convolution closure."""
from __future__ import annotations

from collections import Counter
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "discovery/out/cycle30-crt-synchronization/convolution-result.json"
OUTPUT = ROOT / "discovery/out/cycle30-crt-synchronization/convolution-independent.json"
Q = 2786


def support(speed: int) -> tuple[int, ...]:
    rows = []
    for point in range(Q):
        residue = speed * point % Q
        if 14 * min(residue, Q - residue) < Q:
            rows.append(point)
    return tuple(rows)


def main() -> None:
    masks: dict[tuple[int, ...], int] = {}
    for speed in range(Q - 1, -1, -1):
        if math.gcd(speed, Q) in {1, 2, 7, 14}:
            masks[support(speed)] = speed
    generators = sorted((speed, points) for points, speed in masks.items())
    generator_sets = [set(points) for _speed, points in generators]
    classes: dict[tuple[int, ...], list[int]] = {}
    for point in range(Q):
        signature = tuple(index for index, points in enumerate(generator_sets) if point in points)
        classes.setdefault(signature, []).append(point)
    atoms = sorted(classes.values(), key=lambda row: row[0])
    labels = [0] * Q
    for index, atom in enumerate(atoms):
        for point in atom:
            labels[point] = index
    exceptional = [atom for atom in atoms if len(atom) == 6]
    failures = []
    distinct_profiles = set()
    incidence_additions = 0
    for exceptional_index, source_atom in enumerate(exceptional):
        for speed, generator_support in generators:
            values = [0] * Q
            for left in source_atom:
                for right in generator_support:
                    values[(left + right) % Q] += 1
                    incidence_additions += 1
            compressed = []
            for atom_index, atom in enumerate(atoms):
                row = {values[point] for point in atom}
                if len(row) != 1:
                    failures.append({"exceptional_atom_index": exceptional_index, "generator_speed": speed, "target_atom_index": atom_index, "values": sorted(row)})
                    break
                compressed.append(next(iter(row)))
            if failures:
                break
            distinct_profiles.add(tuple(compressed))
        if failures:
            break
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    if failures or source["status"] != "PASS" or source["first_splitting_witness"] is not None:
        raise AssertionError("independent convolution closure")
    result = {
        "status": "PASS",
        "epistemic_status": "OBSERVED",
        "generator_count": len(generators),
        "atom_count": len(atoms),
        "atom_size_counts": {str(size): count for size, count in sorted(Counter(map(len, atoms)).items())},
        "exceptional_atom_count": len(exceptional),
        "profiles_checked": len(exceptional) * len(generators),
        "distinct_compressed_profiles": len(distinct_profiles),
        "incidence_additions": incidence_additions,
        "failures": failures,
    }
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUTPUT)
    print(json.dumps({"status": "PASS", "profiles": result["profiles_checked"], "distinct_profiles": result["distinct_compressed_profiles"]}, sort_keys=True))


if __name__ == "__main__":
    main()
