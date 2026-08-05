#!/usr/bin/env python3
"""Independent exact replay of Cycle 31's first convolution split."""
from __future__ import annotations

from collections import Counter
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "discovery/out/cycle31-convolution-quotient/result.json"
OUTPUT = ROOT / "discovery/out/cycle31-convolution-quotient/independent-replay.json"
Q = 2786


def mask(speed: int) -> int:
    return sum(1 << point for point in range(Q) if 14 * min(speed * point % Q, (-speed * point) % Q) < Q)


def reconstruct() -> list[list[int]]:
    generators = sorted({mask(speed) for speed in range(Q - 1, -1, -1) if math.gcd(speed, Q) in {1, 2, 7, 14}}, reverse=True)
    classes: dict[tuple[int, ...], list[int]] = {}
    for point in range(Q - 1, -1, -1):
        signature = tuple(index for index, value in enumerate(generators) if value & (1 << point))
        classes.setdefault(signature, []).append(point)
    return sorted((sorted(row) for row in classes.values()), key=lambda row: row[0])


def profile(left: list[int], right: list[int]) -> Counter[int]:
    return Counter((a + b) % Q for b in reversed(right) for a in reversed(left))


def main() -> None:
    atoms = reconstruct()
    if Counter(map(len, atoms)) != Counter({2: 1386, 1: 2, 6: 2}):
        raise AssertionError("independent atom reconstruction")
    singletons = [(index, row) for index, row in enumerate(atoms) if len(row) == 1]
    pairs = [(index, row) for index, row in enumerate(atoms) if len(row) == 2]
    exceptional = [(index, row) for index, row in enumerate(atoms) if len(row) == 6]
    singleton_profiles = 0
    atom_lookup = {tuple(row): index for index, row in enumerate(atoms)}
    for _index, singleton in reversed(singletons):
        for _right_index, right in reversed(list(enumerate(atoms))):
            translated = tuple(sorted((singleton[0] + point) % Q for point in right))
            if translated not in atom_lookup:
                raise AssertionError("independent singleton translation")
            singleton_profiles += 1
    first = None
    pair_profiles = target_evaluations = 0
    for left_offset, (left_index, left) in enumerate(pairs):
        for right_index, right in pairs[left_offset:]:
            pair_profiles += 1
            counts = profile(left, right)
            for target_index, target in exceptional:
                target_evaluations += 1
                values = [counts[point] for point in target]
                if len(set(values)) > 1:
                    first = {
                        "left_atom_index": left_index,
                        "left_atom": left,
                        "right_atom_index": right_index,
                        "right_atom": right,
                        "target_atom_index": target_index,
                        "target_atom": target,
                        "sum_multiplicities": [[point, counts[point]] for point in sorted(counts)],
                        "values_on_target": [[point, counts[point]] for point in target],
                    }
                    break
            if first is not None:
                break
        if first is not None:
            break
    expected = json.loads(SOURCE.read_text(encoding="utf-8"))
    witness = expected["first_splitting_witness"]
    for key in ("left_atom_index", "left_atom", "right_atom_index", "right_atom", "target_atom_index", "target_atom", "sum_multiplicities"):
        if first[key] != witness[key]:
            raise AssertionError(f"independent witness {key}")
    if (singleton_profiles, pair_profiles, target_evaluations) != (2780, 198, 395):
        raise AssertionError("independent lexicographic counts")
    result = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "singleton_profiles_checked": singleton_profiles,
        "pair_profiles_to_first_split": pair_profiles,
        "target_evaluations_to_first_split": target_evaluations,
        "first_splitting_witness": first,
    }
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUTPUT)
    print(json.dumps({"status": "PASS", "pair_profiles": pair_profiles, "witness": first}, sort_keys=True))


if __name__ == "__main__":
    main()
