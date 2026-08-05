#!/usr/bin/env python3
"""Certify the S6 x S5 orbit of the C71 equality-core witness."""

from itertools import permutations

PAIR = ((0, 4), (0, 3), (0, 2), (0, 1), (0, 1))
MAP = ((0, 1, 3, 2, 0, 4), (1, 0, 3, 1, 4, 2),
       (2, 1, 2, 0, 4, 3), (3, 3, 0, 2, 4, 1),
       (4, 4, 3, 0, 2, 1))


def valid(pairs, maps):
    if len(pairs) != 5 or len(maps) != 5:
        return False
    for j, mapping in enumerate(maps):
        if len(mapping) != 6 or any(not 0 <= q < 5 for q in mapping):
            return False
        for i, q in enumerate(mapping):
            if i in pairs[j]:
                if q != j: return False
            elif q == j or i in pairs[q]:
                return False
    return all(sum(a == b for a, b in zip(maps[j], maps[k])) == 1
               for j in range(5) for k in range(j))


def transformed(stars, labels):
    pairs = [None] * 5
    maps = [[None] * 6 for _ in range(5)]
    for old_j in range(5):
        new_j = labels[old_j]
        pairs[new_j] = tuple(sorted(stars[i] for i in PAIR[old_j]))
        for old_i, old_q in enumerate(MAP[old_j]):
            maps[new_j][stars[old_i]] = labels[old_q]
    return tuple(pairs), tuple(tuple(row) for row in maps)


def main():
    orbit = set()
    for stars in permutations(range(6)):
        for labels in permutations(range(5)):
            pairs, maps = transformed(stars, labels)
            assert valid(pairs, maps)
            orbit.add((pairs, maps))
    assert len(orbit) == 86400, len(orbit)
    print("PASS: C71 equality-core S6xS5 orbit has 86400 distinct valid labelled assignments")


if __name__ == "__main__":
    main()
