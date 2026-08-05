#!/usr/bin/env python3
"""Independent exact audit of the C72 equality-core extension result."""

from itertools import combinations, product


PAIR = ((0, 4), (0, 3), (0, 2), (0, 1), (0, 1))
ROW = ((0, 1, 3, 2, 0, 4), (1, 0, 3, 1, 4, 2),
       (2, 1, 2, 0, 4, 3), (3, 3, 0, 2, 4, 1),
       (4, 4, 3, 0, 2, 1))


def lines():
    answer = []
    for star in range(6):
        answer.append(frozenset([(0, "v")] + [
            (side + 1, f"r{side}" if star in PAIR[side] else f"b{side}_{star}")
            for side in range(5)]))
    for nonstar in range(5):
        line = [(0, f"f{nonstar}")]
        for side in range(5):
            if side == nonstar:
                line.append((side + 1, f"r{side}"))
            else:
                index, = (i for i, value in enumerate(ROW[nonstar]) if value == side)
                line.append((side + 1, f"b{side}_{index}"))
        answer.append(frozenset(line))
    return tuple(answer)


def tau(edge_set, cap=6):
    vertices = tuple(sorted(set().union(*edge_set)))
    for amount in range(cap + 1):
        for candidate in combinations(vertices, amount):
            choice = set(candidate)
            if all(choice & edge for edge in edge_set):
                return amount
    return None


def main():
    core = lines()
    assert len(core) == 11
    assert all(len(line) == 6 and {x[0] for x in line} == set(range(6)) for line in core)
    assert all(left & right for left, right in combinations(core, 2))
    assert sum(len(left & right) - 1 for left, right in combinations(core, 2)) == 5
    assert tau(core) == 3
    classes = []
    for part in range(6):
        old = sorted(vertex for line in core for vertex in line if vertex[0] == part)
        classes.append(tuple(sorted(set(old))) + ((part, "fresh"),))
    additions = tuple(
        frozenset(candidate) for candidate in product(*classes)
        if all(len(frozenset(candidate) & line) == 1 for line in core))
    assert len(additions) == 2
    assert all(all(vertex[1] != "fresh" for vertex in line) for line in additions)
    assert len(additions[0] & additions[1]) == 1
    assert tau(core + additions) == 4
    assert sum(len(left & right) - 1 for left, right in combinations(core + additions, 2)) == 5
    print("PASS: exact C72 core extension audit: core tau=3; two D=5 linear additions; maximal extension tau=4")


if __name__ == "__main__":
    main()
