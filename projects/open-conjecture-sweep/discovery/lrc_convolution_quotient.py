#!/usr/bin/env python3
"""Cycle 31 targeted exact atom-convolution quotient test."""
from __future__ import annotations

from collections import Counter
import json
import math
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle31-convolution-quotient"
Q = 2786


def support(speed: int) -> tuple[int, ...]:
    return tuple(point for point in range(Q) if 14 * min(speed * point % Q, (-speed * point) % Q) < Q)


def atoms() -> tuple[list[list[int]], int]:
    generators = sorted({support(speed) for speed in range(Q) if math.gcd(speed, Q) in {1, 2, 7, 14}})
    sets = [set(row) for row in generators]
    classes: dict[bytes, list[int]] = {}
    for point in range(Q):
        signature = bytes(point in row for row in sets)
        classes.setdefault(signature, []).append(point)
    rows = sorted(classes.values(), key=lambda row: row[0])
    if len(generators) != 1386 or Counter(map(len, rows)) != Counter({2: 1386, 1: 2, 6: 2}):
        raise AssertionError("sealed partition reconstruction")
    return rows, len(generators)


def split_witness(stage: str, left_index: int, right_index: int, target_index: int, left: list[int], right: list[int], target: list[int]) -> tuple[dict[str, object] | None, int]:
    counts = Counter((a + b) % Q for a in left for b in right)
    values = [(point, counts[point]) for point in target]
    additions = len(left) * len(right)
    if len({value for _point, value in values}) == 1:
        return None, additions
    left_value = values[0]
    right_value = next(row for row in values[1:] if row[1] != left_value[1])
    return {
        "stage": stage,
        "left_atom_index": left_index,
        "left_atom": left,
        "right_atom_index": right_index,
        "right_atom": right,
        "target_atom_index": target_index,
        "target_atom": target,
        "left_point": left_value[0],
        "left_value": left_value[1],
        "right_point": right_value[0],
        "right_value": right_value[1],
        "sum_multiplicities": [[point, counts[point]] for point in sorted(counts)],
    }, additions


def main() -> None:
    started = time.monotonic()
    rows, generator_count = atoms()
    singletons = [(index, row) for index, row in enumerate(rows) if len(row) == 1]
    pairs = [(index, row) for index, row in enumerate(rows) if len(row) == 2]
    exceptional = [(index, row) for index, row in enumerate(rows) if len(row) == 6]
    witness = None
    singleton_profiles = pair_profiles = pair_target_evaluations = exceptional_profiles = 0
    additions = 0

    for left_index, left in singletons:
        for right_index, right in enumerate(rows):
            singleton_profiles += 1
            translated = sorted((left[0] + point) % Q for point in right)
            labels = []
            for target_index, target in enumerate(rows):
                if any(point in target for point in translated):
                    labels.append((target_index, target))
            additions += len(right)
            if len(labels) != 1 or labels[0][1] != translated:
                target_index, target = labels[0]
                witness, used = split_witness("SINGLETON_TRANSLATION", left_index, right_index, target_index, left, right, target)
                additions += used
                break
        if witness is not None:
            break

    if witness is None:
        for left_offset, (left_index, left) in enumerate(pairs):
            for right_index, right in pairs[left_offset:]:
                pair_profiles += 1
                for target_index, target in exceptional:
                    pair_target_evaluations += 1
                    witness, used = split_witness("PAIR_ON_EXCEPTIONAL", left_index, right_index, target_index, left, right, target)
                    additions += used
                    if witness is not None:
                        break
                if witness is not None:
                    break
            if witness is not None:
                break

    if witness is None:
        for left_index, left in exceptional:
            for right_index, right in pairs:
                exceptional_profiles += 1
                for target_index, target in enumerate(rows):
                    witness, used = split_witness("EXCEPTIONAL_BY_PAIR", left_index, right_index, target_index, left, right, target)
                    additions += used
                    if witness is not None:
                        break
                if witness is not None:
                    break
            if witness is not None:
                break

    result = {
        "status": "CONTAINED" if witness else "PASS",
        "epistemic_status": "OBSERVED",
        "q": Q,
        "generator_count": generator_count,
        "atom_count": len(rows),
        "atom_size_counts": {str(size): count for size, count in sorted(Counter(map(len, rows)).items())},
        "singleton_profiles_checked": singleton_profiles,
        "pair_profiles_checked": pair_profiles,
        "pair_target_evaluations": pair_target_evaluations,
        "exceptional_profiles_checked": exceptional_profiles,
        "representation_additions": additions,
        "first_splitting_witness": witness,
        "wall_seconds": time.monotonic() - started,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    temporary = OUT / "result.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "result.json")
    print(json.dumps({"status": result["status"], "singleton_profiles": singleton_profiles, "pair_profiles": pair_profiles, "witness": witness}, sort_keys=True))


if __name__ == "__main__":
    main()
