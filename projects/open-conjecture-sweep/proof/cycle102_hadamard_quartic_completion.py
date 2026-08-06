#!/usr/bin/env python3
"""Exact E001 reciprocal-even quartic-character completion search."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


Q = 167
HALF_SHIFTS = (Q - 1) // 2


def chi(value: int) -> int:
    value %= Q
    if value == 0:
        return 0
    return 1 if pow(value, (Q - 1) // 2, Q) == 1 else -1


def paf(sequence: list[int]) -> tuple[int, ...]:
    return tuple(sum(sequence[index] * sequence[(index + shift) % Q] for index in range(Q))
                 for shift in range(1, HALF_SHIFTS + 1))


def vector(sequence: list[int]) -> tuple[int, ...]:
    return (sum(sequence) ** 2, *paf(sequence))


def admissible_sequences() -> tuple[list[int], dict[int, list[int]]]:
    sequences: dict[int, list[int]] = {}
    for parameter in range(Q):
        sequence = [chi(index**4 + parameter * index * index + 1) for index in range(Q)]
        if 0 not in sequence:
            assert all(sequence[index] == sequence[(-index) % Q] for index in range(Q))
            sequences[parameter] = sequence
    return sorted(sequences), sequences


def search() -> dict[str, object]:
    a = [1] + [chi(index) for index in range(1, Q)]
    a_vector = vector(a)
    assert a_vector == (1,) + (-1,) * HALF_SHIFTS
    parameters, sequences = admissible_sequences()
    vectors = {parameter: vector(sequence) for parameter, sequence in sequences.items()}
    target = (4 * Q - a_vector[0],) + tuple(-entry for entry in a_vector[1:])
    pairs: dict[tuple[int, ...], list[tuple[int, int]]] = defaultdict(list)
    for left_index, left in enumerate(parameters):
        for right in parameters[left_index:]:
            pairs[tuple(vectors[left][index] + vectors[right][index] for index in range(HALF_SHIFTS + 1))].append((left, right))
    hits: list[tuple[int, int, int]] = []
    for third in parameters:
        needed = tuple(target[index] - vectors[third][index] for index in range(HALF_SHIFTS + 1))
        for left, right in pairs.get(needed, []):
            if right <= third:
                hits.append((left, right, third))
    return {"q": Q, "admissible_parameters": parameters, "parameter_count": len(parameters),
            "pair_count": len(parameters) * (len(parameters) + 1) // 2,
            "a_vector": a_vector, "target": target, "hits": hits}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(search(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
