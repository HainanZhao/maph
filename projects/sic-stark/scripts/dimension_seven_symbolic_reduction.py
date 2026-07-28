#!/usr/bin/env python3
"""Exact orbit count and finite-minor target for the d=7 packet."""

from __future__ import annotations

import json
from math import comb


DIMENSION = 7


def zauner(point: tuple[int, int]) -> tuple[int, int]:
    first, second = point
    return ((-first - second) % DIMENSION, first % DIMENSION)


def opposite(point: tuple[int, int]) -> tuple[int, int]:
    return ((-point[0]) % DIMENSION, (-point[1]) % DIMENSION)


def orbit(point: tuple[int, int]) -> tuple[tuple[int, int], ...]:
    result = []
    current = point
    while current not in result:
        result.append(current)
        current = zauner(current)
    return tuple(sorted(result))


def main() -> None:
    points = [
        (first, second)
        for first in range(DIMENSION)
        for second in range(DIMENSION)
        if (first, second) != (0, 0)
    ]
    orbits = sorted({orbit(point) for point in points})
    if len(orbits) != 16 or any(len(item) != 3 for item in orbits):
        raise AssertionError("unexpected Zauner orbit structure")

    orbit_index = {
        point: index
        for index, zauner_orbit in enumerate(orbits)
        for point in zauner_orbit
    }
    reciprocal_pairs = sorted(
        {
            tuple(
                sorted(
                    (
                        index,
                        orbit_index[opposite(zauner_orbit[0])],
                    )
                )
            )
            for index, zauner_orbit in enumerate(orbits)
        }
    )
    if len(reciprocal_pairs) != 8:
        raise AssertionError("unexpected reciprocal orbit count")

    minors_per_shift = comb(DIMENSION, 2) ** 2
    output = {
        "schema": "sic-stark-dimension-seven-symbolic-reduction-v1",
        "nonzero_characteristics": len(points),
        "zauner_orbits": [
            [list(point) for point in item] for item in orbits
        ],
        "zauner_orbit_count": len(orbits),
        "reciprocal_orbit_pairs": [
            list(pair) for pair in reciprocal_pairs
        ],
        "independent_reciprocal_variables": len(reciprocal_pairs),
        "rank_two_minors_per_shift": minors_per_shift,
        "rank_two_minors_for_two_shifts": 2 * minors_per_shift,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
