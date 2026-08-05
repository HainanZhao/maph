#!/usr/bin/env python3
"""Independent reversed-order/highest-pivot replay for Cycle 46."""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import itertools
import json
import multiprocessing
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_ownership_functional as c38
from lrc_cech_total import canonical_cycle_lift, closed_star, clean, serialize_chain, total_chain_boundary
from lrc_morse_critical_projection import boundary, boundary_cell, build_complex

OUT = ROOT / "discovery/out/cycle46-global-cech-quotient"
WORK_DATA = None


def prepare_reverse():
    c29 = json.loads((ROOT / "discovery/out/cycle29-ownership-blocker/result.json").read_text())["p199"]
    c38._COORDINATES = c29["coordinates"]
    with c38.coupled.P199_INPUT.open(encoding="utf-8") as handle:
        lines = itertools.islice(handle, 4, 5)
        base = tuple(map(int, next(lines).split()))
    allowed = tuple(tuple(row) for row in c38.direct.allowed_digits(base, 78))
    coverage = c38.width4.raw_coverage(c38.direct.CNFS[4])
    global_types = [tuple(sum(1 << offset for offset, digit in enumerate(allowed[owner]) if coverage[point, owner, digit]) for owner in range(13)) for point in range(2786)]
    type_rows = []
    for owner in reversed(range(13)):
        grouped = defaultdict(set)
        for global_type in reversed(global_types):
            grouped[global_type[owner]].add(global_type)
        type_rows.append((owner, {signature: tuple(sorted(values, reverse=True)) for signature, values in grouped.items()}))
    return global_types, dict(type_rows)


def reverse_deletions(residuals):
    global_types, type_rows = prepare_reverse()
    complete_types = sorted(set(global_types))
    type_id = {value: index for index, value in enumerate(complete_types)}
    masks = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete_types]
    target_types = {value for row in residuals for value in row["types"]}
    target_pairs = {tuple(sorted((row["types"][a], row["types"][b]))) for row in residuals for a, b in itertools.combinations(range(4), 2)}
    target_triples = {tuple(sorted(row["types"][part] for part in parts)) for row in residuals for parts in itertools.combinations(range(4), 3)}
    pair_deleted = defaultdict(int)
    triple_deleted = defaultdict(int)
    for owner in reversed(range(13)):
        for pattern in reversed(c38._COORDINATES[owner]["patterns"]):
            rank = int(pattern["rank"])
            if rank not in (2, 3):
                continue
            groups = []
            for signature in reversed(pattern["signatures"]):
                ids = [type_id[value] for value in type_rows[owner][int(signature)] if type_id[value] in target_types]
                if not ids:
                    break
                groups.append(ids)
            if len(groups) != rank:
                continue
            for values in itertools.product(*groups):
                key = tuple(sorted(values))
                if rank == 2 and key in target_pairs:
                    pair_deleted[key] |= 1 << owner
                elif rank == 3 and key in target_triples:
                    triple_deleted[key] |= 1 << owner
    return masks, dict(pair_deleted), dict(triple_deleted)


def highest_solve(rows, rhs, variables):
    basis = {}
    for source in reversed(range(len(rows))):
        row = {index: Fraction(value) for index, value in rows[source].items() if value}
        value = Fraction(rhs[source])
        relation = {source: Fraction(1)}
        while row:
            pivot = max(row)
            if pivot not in basis:
                scale = row[pivot]
                row = {index: coefficient / scale for index, coefficient in row.items()}
                value /= scale
                relation = {index: coefficient / scale for index, coefficient in relation.items()}
                basis[pivot] = (row, value, relation)
                break
            base, base_rhs, base_relation = basis[pivot]
            factor = row[pivot]
            for index, coefficient in base.items():
                row[index] = row.get(index, Fraction(0)) - factor * coefficient
                if not row[index]:
                    del row[index]
            value -= factor * base_rhs
            for index, coefficient in base_relation.items():
                relation[index] = relation.get(index, Fraction(0)) - factor * coefficient
                if not relation[index]:
                    del relation[index]
        else:
            if value:
                return {"status": "INCONSISTENT", "rank": len(basis), "relation": relation, "pairing": value}
    solution = [Fraction(0)] * variables
    for pivot in sorted(basis):
        row, value, _relation = basis[pivot]
        solution[pivot] = value - sum(coefficient * solution[index] for index, coefficient in row.items() if index != pivot)
    return {"status": "CONSISTENT", "rank": len(basis), "solution": solution}


def parse_chain(serialized):
    return {tuple(tuple(vertex) for vertex in cell): Fraction(numerator, denominator) for cell, numerator, denominator in serialized}


def replay_row(primary, source, masks, pair_global, triple_global):
    types = tuple(source["types"])
    supports = tuple(tuple(owner for owner in range(13) if masks[value] & (1 << owner)) for value in types)
    pairs = {(a, b): pair_global.get(tuple(sorted((types[a], types[b]))), 0) for a, b in itertools.combinations(range(4), 2)}
    triples = {parts: triple_global.get(tuple(sorted(types[part] for part in parts)), 0) for parts in itertools.combinations(range(4), 3)}
    cells, all_cells = build_complex(supports, pairs, triples)
    cycle = parse_chain(source["extended_projection"])
    selected = None
    for pivot in range(4):
        vertices = sorted((cell[0] for cell in all_cells if len(cell) == 1 and cell[0][0] == pivot), reverse=True)
        cover = [closed_star(all_cells, vertex) for vertex in vertices]
        union = set().union(*cover)
        if all(cell in union for cell in cycle):
            selected = (pivot, vertices, cover)
            break
    if selected is None:
        status = "UNCOVERED_ALL_PIVOTS"
        witness = None
        lift = None
    else:
        pivot, vertices, cover = selected
        triangles = sorted(cells[2], reverse=True)
        tetrahedra = sorted(cells[3], reverse=True)
        triangle_id = {cell: index for index, cell in enumerate(triangles)}
        rows = [dict() for _ in triangles]
        for column, tetrahedron in enumerate(tetrahedra):
            for face, coefficient in boundary_cell(tetrahedron).items():
                rows[triangle_id[face]][column] = coefficient
        rhs = [cycle.get(cell, Fraction(0)) for cell in triangles]
        solved = highest_solve(rows, rhs, len(tetrahedra))
        status = "BOUNDARY" if solved["status"] == "CONSISTENT" else "NONBOUNDARY"
        if status == "BOUNDARY":
            witness = {tetrahedra[index]: value for index, value in enumerate(solved["solution"]) if value}
            assert boundary(witness) == cycle
        else:
            witness = None
            relation = solved["relation"]
            assert sum(relation[index] * rhs[index] for index in relation)
        lift, uncovered = canonical_cycle_lift(cycle, cover)
        assert not uncovered and not total_chain_boundary(lift)
    assert status == primary["status"]
    assert selected is None or selected[0] == primary["selected_pivot"]
    return {
        "source": source["source"], "ordinal": source["ordinal"], "status": status,
        "selected_pivot": None if selected is None else selected[0],
        "witness_nonzero": None if witness is None else len(witness),
        "witness": None if witness is None else [[[list(vertex) for vertex in cell], value.numerator, value.denominator] for cell, value in sorted(witness.items())],
        "lift_nonzero": None if lift is None else len(lift),
    }


def worker_init(masks, pairs, triples):
    global WORK_DATA
    resource.setrlimit(resource.RLIMIT_AS, (3_000_000_000, 3_000_000_000))
    WORK_DATA = (masks, pairs, triples)


def replay_worker(job):
    primary, source = job
    return replay_row(primary, source, *WORK_DATA)


def main():
    started = time.monotonic()
    primary = json.loads((OUT / "actual-quotient-localized.json").read_text())
    source_data = json.loads((ROOT / "discovery/out/cycle45-critical-projection/actual-corpus-layered.json").read_text())
    sources = {(row["source"], row["ordinal"]): row for row in source_data["records"] if row["extended_projection_nonzero"]}
    primary_rows = primary["records"]
    selected_keys = {(primary_rows[0]["source"], primary_rows[0]["ordinal"]), (primary_rows[len(primary_rows) // 2]["source"], primary_rows[len(primary_rows) // 2]["ordinal"]), (primary_rows[-1]["source"], primary_rows[-1]["ordinal"])}
    classes = {}
    for row in primary_rows:
        key = (row["status"], row.get("selected_pivot"), row["total"].get("solve_route"), row["total"].get("solve_radius"))
        rank = row["total"].get("witness_nonzero", 10**9)
        candidate = (rank, row["source"], row["ordinal"])
        if key not in classes or candidate < classes[key]:
            classes[key] = candidate
    selected_keys.update((source, ordinal) for _rank, source, ordinal in classes.values())
    ordered = [row for row in primary_rows if (row["source"], row["ordinal"]) in selected_keys]
    residuals = [sources[(row["source"], row["ordinal"])] for row in primary_rows]
    masks, pairs, triples = reverse_deletions(residuals)
    cache = json.loads((OUT / "target-structure-cache.json").read_text())
    assert masks == cache["masks"]
    assert [[a, b, value] for (a, b), value in sorted(pairs.items())] == cache["pair_deleted"]
    assert [[a, b, c, value] for (a, b, c), value in sorted(triples.items())] == cache["triple_deleted"]
    jobs = [(row, sources[(row["source"], row["ordinal"])]) for row in ordered]
    with multiprocessing.Pool(2, initializer=worker_init, initargs=(masks, pairs, triples)) as pool:
        records = pool.map(replay_worker, jobs, chunksize=1)
    result = {"status": "PASS", "epistemic_status": "PROVED", "selected_records": len(records), "selection_classes": len(classes), "records": records, "wall_seconds": time.monotonic() - started, "claim_boundary": "Independent reversed-order/highest-pivot replay of frozen material outcome classes, not the full corpus."}
    target = OUT / "independent-replay.json"
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: result[key] for key in result if key not in ("records", "claim_boundary")}, sort_keys=True))


if __name__ == "__main__":
    main()
