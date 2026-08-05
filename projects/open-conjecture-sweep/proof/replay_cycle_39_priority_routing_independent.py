#!/usr/bin/env python3
"""Independent exact replay of Cycle 39 priority-span certificates."""
from __future__ import annotations

from fractions import Fraction
import itertools
import json
import math
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_coupled_incidence as coupled
import lrc_pair_choice as direct
import lrc_width_four_stage_a as width4

SOURCE = ROOT / "discovery/out/cycle39-priority-routing/result.json"
OUTPUT = ROOT / "discovery/out/cycle39-priority-routing/independent-replay.json"


def factor_row(root, types, normals):
    rank = len(types)
    others = tuple(coordinate for coordinate in range(13) if coordinate != root)
    row = []
    for predecessor in range(4096):
        total = 0
        for uncovered in range(1 << rank):
            root_sum = 0
            for option, weight in enumerate(normals[root]):
                if all(bool(types[index][root] & (1 << option)) != bool(uncovered & (1 << index)) for index in range(rank)):
                    root_sum += weight
            if not root_sum:
                continue
            value = root_sum
            for offset, coordinate in enumerate(others):
                required = (1 << rank) - 1 if predecessor & (1 << offset) else uncovered
                local = sum(weight for option, weight in enumerate(normals[coordinate]) if all(not (types[index][coordinate] & (1 << option)) for index in range(rank) if required & (1 << index)))
                value *= local
                if not value:
                    break
            total += value
        row.append(total)
    return row


def direct_support_row(root, points, normals, allowed, coverage):
    others = tuple(coordinate for coordinate in range(13) if coordinate != root)
    supports = tuple(tuple((offset, weight) for offset, weight in enumerate(normal) if weight) for normal in normals)
    forbidden_weights = [0] * 4096
    assignments = 0
    for assignment in itertools.product(*supports):
        assignments += 1
        offsets = tuple(row[0] for row in assignment)
        weight = math.prod(row[1] for row in assignment)
        forbidden = 0
        possible = True
        for point in points:
            covering = []
            for coordinate in range(13):
                digit = allowed[coordinate][offsets[coordinate]]
                if coverage[point, coordinate, digit]:
                    covering.append(coordinate)
            if not covering:
                continue
            if root not in covering:
                possible = False
                break
            for offset, coordinate in enumerate(others):
                if coordinate in covering:
                    forbidden |= 1 << offset
        if possible:
            forbidden_weights[forbidden] += weight
    subset_sums = forbidden_weights[:]
    for bit in range(12):
        for mask in range(4096):
            if mask & (1 << bit):
                subset_sums[mask] += subset_sums[mask ^ (1 << bit)]
    full = 4095
    row = [subset_sums[full ^ predecessor] for predecessor in range(4096)]
    return row, assignments


def main() -> None:
    started = time.monotonic()
    result = json.loads(SOURCE.read_text(encoding="utf-8"))
    c37 = json.loads((ROOT / "artifacts/cycle-37-b037-lrc-degree-two-product-v1.json").read_text(encoding="utf-8"))
    normals = tuple(tuple(map(int, row)) for row in c37["breakthrough"]["local_normals_by_allowed_option_offset"])
    base = coupled.read_bases()[4]
    allowed = tuple(tuple(row) for row in direct.allowed_digits(base, 78))
    coverage = width4.raw_coverage(direct.CNFS[4])
    if result["status"] != "PASS" or result["feasible_roots"] or result["capped_roots"] or [sum(row) for row in normals] != [1] * 13:
        raise AssertionError("frozen outcome")

    replay_roots = []
    direct_assignments = 0
    maximum_certificate_bits = 0
    for root_result in result["roots"]:
        root = int(root_result["root"])
        witnesses = root_result["witnesses"]
        rows = []
        for witness in witnesses:
            types = tuple(tuple(map(int, row)) for row in witness["global_types"])
            rows.append(factor_row(root, types, normals))
        certificate = list(map(int, root_result["left_null_certificate"]))
        if len(certificate) != len(rows) + 1 or not certificate[0]:
            raise AssertionError("certificate shape")
        products = [certificate[0] + sum(certificate[index + 1] * rows[index][column] for index in range(len(rows))) for column in range(4096)]
        if any(products):
            raise AssertionError("full priority-column left-null replay")
        maximum_certificate_bits = max(maximum_certificate_bits, max(abs(value).bit_length() for value in certificate))

        selected = sorted({0, len(witnesses) // 2, len(witnesses) - 1})
        controls = []
        for index in selected:
            witness = witnesses[index]
            direct_row, assignments = direct_support_row(root, tuple(map(int, witness["representative_times"])), normals, allowed, coverage)
            direct_assignments += assignments
            if direct_row != rows[index]:
                raise AssertionError("direct signed-support priority row")
            controls.append({"witness_index": index, "representative_times": witness["representative_times"], "empty_predecessor_moment": direct_row[0], "distinct_row_values": len(set(direct_row))})
        replay_roots.append({"root": root, "selected_rows": len(rows), "certificate_mass_coefficient": certificate[0], "all_4096_columns_zero": True, "direct_controls": controls})

    if direct_assignments > 2_000_000:
        raise AssertionError("direct control cap")
    replay = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "roots": replay_roots,
        "total_selected_rows": sum(row["selected_rows"] for row in replay_roots),
        "priority_columns_per_root": 4096,
        "total_priority_columns": 53248,
        "direct_support_assignment_checks": direct_assignments,
        "maximum_certificate_coefficient_bits": maximum_certificate_bits,
        "mass_one_priority_span_extension_exists": False,
        "wall_seconds": time.monotonic() - started,
    }
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(replay, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUTPUT)
    print(json.dumps({"status": "PASS", "rows": replay["total_selected_rows"], "columns": replay["total_priority_columns"], "direct_checks": direct_assignments, "wall_seconds": replay["wall_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    main()
