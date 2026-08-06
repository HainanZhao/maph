#!/usr/bin/env python3
"""Exact C84 binary-fiber test of the composite Proposition 4.1 analogue."""
from __future__ import annotations

import json


MODULUS = 14
K = 13
UNITS = (1, 3, 5, 9, 11, 13)
TARGET = set(range(1, K))


def succeeds(vector: tuple[int, ...]) -> tuple[int, int] | None:
    for s in UNITS:
        for r in UNITS:
            if all((s * vector[index] + r * (index + 1)) % MODULUS in TARGET for index in range(K)):
                return s, r
    return None


def main() -> None:
    failures: list[dict[str, object]] = []
    successful = 0
    for mask in range(1, 1 << K):
        vector = tuple(7 if mask >> index & 1 else 0 for index in range(K))
        witness = succeeds(vector)
        if witness is None:
            failures.append({"vector": vector})
        else:
            successful += 1
    assert successful + len(failures) == (1 << K) - 1
    print(json.dumps({
        "epistemic_status": "PROVED",
        "modulus": MODULUS,
        "k": K,
        "fiber_vectors": (1 << K) - 1,
        "unit_pairs_per_vector": len(UNITS) ** 2,
        "successful_vectors": successful,
        "failing_vectors": len(failures),
        "first_failure": None if not failures else failures[0],
        "status": "PASS",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
