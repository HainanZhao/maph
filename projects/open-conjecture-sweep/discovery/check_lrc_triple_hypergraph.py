#!/usr/bin/env python3
"""Exact forbidden-triple construction and weak-colorability checks."""

from __future__ import annotations

import argparse
import itertools
import json


def prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    return factors


def primitive_root(prime: int) -> int:
    factors = prime_factors(prime - 1)
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise AssertionError("primitive root not found")


def cover_data(k: int, p: int) -> tuple[int, int, list[set[int]]]:
    h = (p - 1) // 2
    root = primitive_root(p)
    bad: set[int] = set()
    residue = 1
    for exponent in range(h):
        if (k + 1) * min(residue, p - residue) < p:
            bad.add(exponent)
        residue = residue * root % p
    covers = [{time for time in range(h) if (center + time) % h in bad} for center in range(h)]
    return h, root, covers


def forbidden_triples(h: int, covers: list[set[int]]) -> list[tuple[int, int, int]]:
    triples: list[tuple[int, int, int]] = []
    for triple in itertools.combinations(range(h), 3):
        if not any(set(triple).issubset(cover) for cover in covers):
            triples.append(triple)
    return triples


def validate_triples(h: int, covers: list[set[int]], triples: list[tuple[int, int, int]]) -> None:
    triple_set = set(triples)
    for triple in itertools.combinations(range(h), 3):
        expected = not any(set(triple).issubset(cover) for cover in covers)
        if (triple in triple_set) != expected:
            raise AssertionError(f"forbidden-triple mismatch: {triple}")


def weak_colorable_bruteforce(vertices: list[int], triples: list[tuple[int, int, int]], colors: int) -> bool:
    vertex_set = set(vertices)
    relevant = [triple for triple in triples if set(triple).issubset(vertex_set)]
    for assignment in itertools.product(range(colors), repeat=len(vertices)):
        color = dict(zip(vertices, assignment))
        if all(not (color[a] == color[b] == color[c]) for a, b, c in relevant):
            return True
    return False


def weak_colorable_backtracking(vertices: list[int], triples: list[tuple[int, int, int]], colors: int) -> bool:
    vertex_set = set(vertices)
    relevant = [triple for triple in triples if set(triple).issubset(vertex_set)]
    incident = {vertex: 0 for vertex in vertices}
    for triple in relevant:
        for vertex in triple:
            incident[vertex] += 1
    order = sorted(vertices, key=lambda vertex: (-incident[vertex], vertex))
    assigned: dict[int, int] = {}

    def search(index: int) -> bool:
        if index == len(order):
            return True
        vertex = order[index]
        for color in range(colors):
            assigned[vertex] = color
            valid = True
            for triple in relevant:
                if vertex not in triple or any(other not in assigned for other in triple):
                    continue
                if len({assigned[other] for other in triple}) == 1:
                    valid = False
                    break
            if valid and search(index + 1):
                return True
        del assigned[vertex]
        return False

    return search(0)


def nae_two_color(vertices: list[int], triples: list[tuple[int, int, int]], node_cap: int) -> tuple[str, list[int] | None, int]:
    vertex_set = set(vertices)
    relevant = [triple for triple in triples if set(triple).issubset(vertex_set)]
    index = {vertex: offset for offset, vertex in enumerate(vertices)}
    constraints = [tuple(index[vertex] for vertex in triple) for triple in relevant]
    incident: list[list[tuple[int, int, int]]] = [[] for _ in vertices]
    for triple in constraints:
        for vertex in triple:
            incident[vertex].append(triple)
    assignment = [-1] * len(vertices)
    nodes = 0

    def propagate(changes: list[int]) -> bool:
        cursor = 0
        while cursor < len(changes):
            vertex = changes[cursor]
            cursor += 1
            for triple in incident[vertex]:
                values = [assignment[item] for item in triple]
                assigned = [value for value in values if value >= 0]
                if len(assigned) == 3:
                    if assigned[0] == assigned[1] == assigned[2]:
                        return False
                elif len(assigned) == 2 and assigned[0] == assigned[1]:
                    target = triple[values.index(-1)]
                    forced = 1 - assigned[0]
                    if assignment[target] < 0:
                        assignment[target] = forced
                        changes.append(target)
                    elif assignment[target] != forced:
                        return False
        return True

    def undo(changes: list[int]) -> None:
        for vertex in reversed(changes):
            assignment[vertex] = -1

    def search() -> bool | None:
        nonlocal nodes
        if nodes >= node_cap:
            return None
        nodes += 1
        try:
            vertex = max((item for item, value in enumerate(assignment) if value < 0), key=lambda item: len(incident[item]))
        except ValueError:
            return True
        for color in (0, 1):
            changes = [vertex]
            assignment[vertex] = color
            if propagate(changes):
                outcome = search()
                if outcome is not False:
                    return outcome
            undo(changes)
        return False

    assignment[0] = 0
    initial = [0]
    if not propagate(initial):
        return "UNSAT", None, nodes
    result = search()
    if result is None:
        return "CAP", None, nodes
    if result is False:
        return "UNSAT", None, nodes
    return "SAT", assignment, nodes


def verify_coloring(coloring: list[int], triples: list[tuple[int, int, int]]) -> None:
    for left, middle, right in triples:
        if coloring[left] == coloring[middle] == coloring[right]:
            raise AssertionError(f"monochromatic forbidden triple: {(left, middle, right)}")


def run_h11_oracle() -> dict[str, int | str]:
    h, root, covers = cover_data(3, 11)
    triples = forbidden_triples(h, covers)
    validate_triples(h, covers, triples)
    rows = 0
    for subset in range(1 << h):
        vertices = [vertex for vertex in range(h) if subset & (1 << vertex)]
        for colors in range(1, 4):
            brute = weak_colorable_bruteforce(vertices, triples, colors)
            solver = weak_colorable_backtracking(vertices, triples, colors)
            if brute != solver:
                raise AssertionError(f"H11 colorability mismatch subset={subset} colors={colors}")
            rows += 1
    return {"status": "PASS", "h": h, "primitive_root": root, "forbidden_triples": len(triples), "rows": rows}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--h11-oracle", action="store_true")
    parser.add_argument("--global-2", action="store_true")
    parser.add_argument("--node-cap", type=int, default=10_000_000)
    args = parser.parse_args()
    if args.h11_oracle:
        print(json.dumps(run_h11_oracle(), sort_keys=True))
    if args.global_2:
        h, root, covers = cover_data(13, 199)
        triples = forbidden_triples(h, covers)
        validate_triples(h, covers, triples)
        status, coloring, nodes = nae_two_color(list(range(h)), triples, args.node_cap)
        result: dict[str, object] = {
            "status": status,
            "h": h,
            "primitive_root": root,
            "forbidden_triples": len(triples),
            "nodes": nodes,
            "node_cap": args.node_cap,
        }
        if coloring is not None:
            verify_coloring(coloring, triples)
            result["coloring"] = coloring
            result["color_class_sizes"] = [coloring.count(0), coloring.count(1)]
        print(json.dumps(result, sort_keys=True))
    if not args.h11_oracle and not args.global_2:
        parser.error("select --h11-oracle and/or --global-2")


if __name__ == "__main__":
    main()
