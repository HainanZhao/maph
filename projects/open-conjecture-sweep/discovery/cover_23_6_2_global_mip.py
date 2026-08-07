#!/usr/bin/env python3
"""Global block-variable MIP discovery for a 20-block C(23,6,2) cover.

This is a witness-finding engine, not a proof of infeasibility.  A feasible
solution is accepted only after a direct recount of all 253 pairs.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import highspy
import numpy as np

from cover_23_6_2_neighborhood import NEAR
from cover_23_6_2_sat import verify
from cover_23_6_2_star1_sat import STAR
from cover_23_6_2_star_cases import SUPPORTS, canonical_star


V = 23
K = 6
PAIR_COUNT = V * (V - 1) // 2
POINT_ROW = PAIR_COUNT
COUNT_ROW = PAIR_COUNT + V
ROW_COUNT = COUNT_ROW + 1
NONZEROS_PER_BLOCK = 15 + K + 1


def pair_index(left: int, right: int) -> int:
    assert 0 <= left < right < V
    return left * (2 * V - left - 1) // 2 + right - left - 1


def build_arrays() -> tuple[list[tuple[int, ...]], np.ndarray, np.ndarray]:
    blocks = list(itertools.combinations(range(V), K))
    starts = np.arange(
        0,
        NONZEROS_PER_BLOCK * len(blocks) + 1,
        NONZEROS_PER_BLOCK,
        dtype=np.int32,
    )
    indices = np.empty(NONZEROS_PER_BLOCK * len(blocks), dtype=np.int32)
    offset = 0
    for block in blocks:
        for left, right in itertools.combinations(block, 2):
            indices[offset] = pair_index(left, right)
            offset += 1
        for point in block:
            indices[offset] = POINT_ROW + point
            offset += 1
        indices[offset] = COUNT_ROW
        offset += 1
    assert offset == len(indices)
    return blocks, starts, indices


def canonical_repair_start() -> list[tuple[int, ...]]:
    replications = [sum(point in block for block in NEAR) for point in range(V)]
    anchor = NEAR[0]
    central = next(point for point in anchor if replications[point] == 5)
    other_anchor = sorted(point for point in anchor if point != central)
    remainder = sorted(point for point in range(V) if point not in anchor)
    image = {central: 0}
    image.update({point: new for point, new in zip(other_anchor, range(1, 6))})
    image.update({point: new for point, new in zip(remainder, range(6, V))})
    transformed = [tuple(sorted(image[point] for point in block)) for block in NEAR]
    assert tuple(range(6)) in transformed
    assert sum(0 in block for block in transformed) == 5
    return transformed


def selected_star(case: str) -> list[tuple[int, ...]]:
    if case == "4":
        star = [set(block) for block in STAR]
    else:
        star, _ = canonical_star(SUPPORTS[case])
    anchor = sorted(star[0])
    assert anchor[0] == 0
    remainder = sorted(point for point in range(V) if point not in star[0])
    image = {0: 0}
    image.update({point: new for point, new in zip(anchor[1:], range(1, 6))})
    image.update({point: new for point, new in zip(remainder, range(6, V))})
    transformed = [tuple(sorted(image[point] for point in block)) for block in star]
    assert transformed[0] == tuple(range(6))
    return transformed


def repair_start_for_star(case: str) -> list[tuple[int, ...]] | None:
    fixed = selected_star(case)
    canonical_groups: dict[tuple[int, ...], list[int]] = {}
    for point in range(1, V):
        support = tuple(row for row, block in enumerate(fixed) if point in block)
        canonical_groups.setdefault(support, []).append(point)

    replications = [sum(point in block for block in NEAR) for point in range(V)]
    for central in range(V):
        if replications[central] != 5:
            continue
        old_star = [block for block in NEAR if central in block]
        for row_image in itertools.permutations(range(5)):
            old_groups: dict[tuple[int, ...], list[int]] = {}
            for point in range(V):
                if point == central:
                    continue
                support = tuple(
                    sorted(
                        row_image[row]
                        for row, block in enumerate(old_star)
                        if point in block
                    )
                )
                old_groups.setdefault(support, []).append(point)
            if {
                support: len(points) for support, points in old_groups.items()
            } != {
                support: len(points) for support, points in canonical_groups.items()
            }:
                continue
            image = {central: 0}
            for support, old_points in old_groups.items():
                for old, new in zip(sorted(old_points), canonical_groups[support]):
                    image[old] = new
            transformed = [
                tuple(sorted(image[point] for point in block)) for block in NEAR
            ]
            assert set(fixed) <= set(transformed)
            return transformed
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=1800.0)
    parser.add_argument("--threads", type=int, default=3)
    parser.add_argument("--star-case", choices=["4", *sorted(SUPPORTS)])
    parser.add_argument(
        "--result",
        type=Path,
        default=Path("discovery/out/cover-23-6-2-global-mip.json"),
    )
    args = parser.parse_args()

    blocks, starts, indices = build_arrays()
    number = len(blocks)
    solver = highspy.Highs()
    infinity = solver.getInfinity()
    solver.setOptionValue("time_limit", args.seconds)
    solver.setOptionValue("threads", args.threads)
    solver.setOptionValue("mip_report_level", 1)
    solver.setOptionValue("mip_heuristic_effort", 0.30)

    row_lower = np.concatenate([
        np.ones(PAIR_COUNT, dtype=np.float64),
        np.full(V, 5.0, dtype=np.float64),
        np.array([-infinity]),
    ])
    row_upper = np.concatenate([
        np.full(PAIR_COUNT, infinity, dtype=np.float64),
        # The excess-spectrum reduction leaves only partitions of five with
        # largest part at most three, hence every replication is at most 8.
        np.full(V, 8.0, dtype=np.float64),
        np.array([20.0]),
    ])
    # Choose a replication-five point as 0 and one of its blocks as
    # {0,...,5}. Both choices are without loss of generality.
    row_upper[POINT_ROW] = 5.0
    empty_i = np.empty(0, dtype=np.int32)
    empty_v = np.empty(0, dtype=np.float64)
    empty_starts = np.zeros(ROW_COUNT + 1, dtype=np.int32)
    assert solver.addRows(
        ROW_COUNT,
        row_lower,
        row_upper,
        0,
        empty_starts,
        empty_i,
        empty_v,
    ) == highspy.HighsStatus.kOk

    assert solver.addCols(
        number,
        np.ones(number, dtype=np.float64),
        np.zeros(number, dtype=np.float64),
        np.ones(number, dtype=np.float64),
        len(indices),
        starts,
        indices,
        np.ones(len(indices), dtype=np.float64),
    ) == highspy.HighsStatus.kOk
    column_indices = np.arange(number, dtype=np.int32)
    integrality = np.full(number, int(highspy.HighsVarType.kInteger), dtype=np.uint8)
    assert solver.changeColsIntegrality(
        number, column_indices, integrality
    ) == highspy.HighsStatus.kOk
    block_to_column = {block: column for column, block in enumerate(blocks)}
    canonical_column = block_to_column[tuple(range(6))]
    assert solver.changeColBounds(
        canonical_column, 1.0, 1.0
    ) == highspy.HighsStatus.kOk
    if args.star_case:
        fixed_star = selected_star(args.star_case)
        for block in fixed_star:
            assert solver.changeColBounds(
                block_to_column[block], 1.0, 1.0
            ) == highspy.HighsStatus.kOk
        repair_start = repair_start_for_star(args.star_case)
        if repair_start:
            near_columns = np.array(
                [block_to_column[block] for block in repair_start], dtype=np.int32
            )
            assert solver.setSolution(
                len(near_columns), near_columns, np.ones(len(near_columns))
            ) == highspy.HighsStatus.kOk
            repair_start_blocks = len(near_columns)
        else:
            repair_start_blocks = 0
    else:
        near_columns = np.array(
            [block_to_column[block] for block in canonical_repair_start()],
            dtype=np.int32,
        )
        # Supply the two-pair-deficient, replication-feasible family as a
        # sparse repair start. It is guidance only, never accepted unchecked.
        assert solver.setSolution(
            len(near_columns), near_columns, np.ones(len(near_columns))
        ) == highspy.HighsStatus.kOk
        repair_start_blocks = len(near_columns)

    print(
        json.dumps(
            {
                "blocks": number,
                "canonical_block": list(range(6)),
                "canonical_point_degree": 5,
                "highs": solver.version(),
                "nonzeros": len(indices),
                "repair_start_blocks": repair_start_blocks,
                "rows": ROW_COUNT,
                "star_case": args.star_case,
                "time_limit_seconds": args.seconds,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    solver.run()
    model_status = solver.getModelStatus()
    info = solver.getInfo()
    solution = solver.getSolution()
    selected = [
        list(block)
        for block, value in zip(blocks, solution.col_value)
        if value > 0.5
    ] if solution.value_valid else []

    payload: dict[str, object] = {
        "dual_bound": info.mip_dual_bound,
        "model_status": solver.modelStatusToString(model_status),
        "node_count": info.mip_node_count,
        "primal_bound": info.objective_function_value,
        "selected_blocks": len(selected),
        "status": "NO_VERIFIED_WITNESS",
    }
    if len(selected) == 20:
        checked = verify(selected)
        payload["verification"] = checked
        if checked["status"] == "VERIFIED_20_BLOCK_COVER":
            payload["status"] = "VERIFIED_20_BLOCK_COVER"

    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
