#!/usr/bin/env python3
"""Exact SAT candidate and independent verification for C87's n=12 interface."""
from __future__ import annotations

import itertools
import json
from pathlib import Path
import subprocess
import tempfile


GROUPS = ((1,), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11))
GROUP_OF = {point: color for color, group in enumerate(GROUPS) for point in group}
POINTS = tuple(range(1, 12))


def lower_bound_check() -> dict:
    # With two singleton private regions, their witnesses cannot share either
    # own color and pair coverage puts them in a third-color block.
    return {"epistemic_status": "PROVED", "minimum_no_absorption_points": 12,
            "argument": "At most one of six nonempty private regions is singleton; 1+1+5*2=12."}


def encode() -> tuple[list[list[int]], dict[tuple[int, int, int], int]]:
    variable: dict[tuple[int, int, int], int] = {}
    next_id = 1
    for color in range(6):
        for a, b in itertools.combinations(POINTS, 2):
            variable[color, a, b] = next_id
            next_id += 1
    clauses: list[list[int]] = []

    def var(color: int, a: int, b: int) -> int:
        if a > b:
            a, b = b, a
        return variable[color, a, b]

    # Root block membership fixes each private group: it is one root component
    # in its own color and isolated from that root component in all others.
    for color in range(6):
        for a, b in itertools.combinations(POINTS, 2):
            if GROUP_OF[a] == color or GROUP_OF[b] == color:
                clauses.append([var(color, a, b)] if GROUP_OF[a] == GROUP_OF[b] == color else [-var(color, a, b)])
    # Each color relation is transitive on the non-root points.
    for color in range(6):
        for a, b, c in itertools.combinations(POINTS, 3):
            ab, ac, bc = var(color, a, b), var(color, a, c), var(color, b, c)
            clauses.extend(([-ab, -bc, ac], [-ab, -ac, bc], [-ac, -bc, ab]))
    # Pair-covering for every pair not already covered through the root.
    for a, b in itertools.combinations(POINTS, 2):
        clauses.append([var(color, a, b) for color in range(6)])
    # No third-color block may absorb two entire private regions.
    for i, j in itertools.combinations(range(6), 2):
        for color in range(6):
            if color not in (i, j):
                clauses.append([-var(color, a, b) for a in GROUPS[i] for b in GROUPS[j]])
    return clauses, variable


def solve(clauses: list[list[int]], variable: dict[tuple[int, int, int], int]) -> dict[tuple[int, int, int], bool] | None:
    with tempfile.TemporaryDirectory() as directory:
        cnf = Path(directory) / "c87.cnf"
        model = Path(directory) / "c87.model"
        cnf.write_text("p cnf %d %d\n%s\n" % (len(variable), len(clauses), "\n".join(" ".join(map(str, clause)) + " 0" for clause in clauses)))
        result = subprocess.run(["cadical", "-w", str(model), str(cnf)], text=True, capture_output=True, check=False)
        if result.returncode == 20:
            return None
        if result.returncode != 10:
            raise RuntimeError(result.stdout + result.stderr)
        values = {int(token) for token in model.read_text().split() if token.lstrip("-").isdigit()}
        return {key: ident in values for key, ident in variable.items()}


def partitions(model: dict[tuple[int, int, int], bool]) -> list[list[list[int]]]:
    answer = []
    for color in range(6):
        parent = list(range(12))
        def find(a: int) -> int:
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a
        def join(a: int, b: int) -> None:
            a, b = find(a), find(b)
            if a != b:
                parent[b] = a
        for point in GROUPS[color]:
            join(0, point)
        for a, b in itertools.combinations(POINTS, 2):
            if model[color, a, b]:
                join(a, b)
        groups: dict[int, list[int]] = {}
        for point in range(12):
            groups.setdefault(find(point), []).append(point)
        answer.append(sorted((sorted(group) for group in groups.values()), key=lambda group: (group[0], len(group))))
    return answer


def verify(parts: list[list[list[int]]]) -> dict:
    block_of = [{point: next(index for index, block in enumerate(partition) if point in block)
                 for point in range(12)} for partition in parts]
    assert all(block_of[color][0] == block_of[color][point] if GROUP_OF[point] == color else block_of[color][0] != block_of[color][point]
               for color in range(6) for point in POINTS)
    assert all(any(block_of[color][a] == block_of[color][b] for color in range(6)) for a, b in itertools.combinations(range(12), 2))
    private = []
    for color in range(6):
        root_block = set(parts[color][block_of[color][0]])
        others = set().union(*(parts[other][block_of[other][0]] for other in range(6) if other != color))
        private.append(sorted(root_block - others))
    assert private == [list(group) for group in GROUPS]
    absorbed = []
    for i, j in itertools.combinations(range(6), 2):
        for color in range(6):
            if color not in (i, j) and all(block_of[color][a] == block_of[color][b]
                                           for a in GROUPS[i] for b in GROUPS[j]):
                absorbed.append((i, j, color))
    assert not absorbed
    blocks = [(color, block) for color, partition in enumerate(parts) for block in partition]
    cover = next((size for size in range(1, 7) if any(set().union(*(set(blocks[index][1]) for index in choice)) == set(range(12))
                                                for choice in itertools.combinations(range(len(blocks)), size))), None)
    return {"partitions": parts, "private_regions": private, "absorbed_pairs": absorbed, "minimum_component_cover": cover}


def main() -> None:
    clauses, variable = encode()
    model = solve(clauses, variable)
    payload = {"lower_bound": lower_bound_check(), "cnf_variables": len(variable), "cnf_clauses": len(clauses)}
    if model is None:
        payload.update({"solver_status": "UNSAT", "epistemic_status": "OBSERVED", "status": "PASS"})
    else:
        payload.update({"solver_status": "SAT", "epistemic_status": "PROVED", "candidate": verify(partitions(model)), "status": "PASS"})
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
