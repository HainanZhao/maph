#!/usr/bin/env python3
"""Reduced MIP discovery for the star-(4), repeated-degree-five branch.

The five canonical star blocks force a sixth block through the repeated point.
The remaining problem selects fourteen six-subsets of points 2,...,22, each
point occurring exactly four times.  A feasible incumbent is accepted only
after the full 23-point covering is recounted independently.
"""

from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import highspy
import numpy as np

from cover_23_6_2_sat import verify
from cover_23_6_2_star1_sat import STAR


POINTS = tuple(range(2, 23))
FORCED = (1, 18, 19, 20, 21, 22)
GROUPS = [set(range(2, 6)), set(range(6, 10)), set(range(10, 14)),
          set(range(14, 18)), set(range(18, 23))]
RESIDUAL_PAIRS = [
    pair for pair in itertools.combinations(POINTS, 2)
    if not any(set(pair) <= group for group in GROUPS)
]


def build_arrays() -> tuple[list[tuple[int, ...]], np.ndarray, np.ndarray]:
    blocks = list(itertools.combinations(POINTS, 6))
    pair_row = {pair: row for row, pair in enumerate(RESIDUAL_PAIRS)}
    degree_offset = len(RESIDUAL_PAIRS)
    count_row = degree_offset + len(POINTS)
    starts = [0]
    indices: list[int] = []
    for block in blocks:
        for pair in itertools.combinations(block, 2):
            row = pair_row.get(pair)
            if row is not None:
                indices.append(row)
        indices.extend(degree_offset + point - 2 for point in block)
        indices.append(count_row)
        starts.append(len(indices))
    return (
        blocks,
        np.asarray(starts, dtype=np.int32),
        np.asarray(indices, dtype=np.int32),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seconds", type=float, default=1800.0)
    parser.add_argument("--threads", type=int, default=3)
    parser.add_argument(
        "--result",
        type=Path,
        default=Path("discovery/out/cover-23-6-2-star1-degree5-mip.json"),
    )
    args = parser.parse_args()

    blocks, starts, indices = build_arrays()
    pair_rows = len(RESIDUAL_PAIRS)
    row_count = pair_rows + len(POINTS) + 1
    solver = highspy.Highs()
    infinity = solver.getInfinity()
    solver.setOptionValue("time_limit", args.seconds)
    solver.setOptionValue("threads", args.threads)
    solver.setOptionValue("mip_heuristic_effort", 0.5)

    lower = np.concatenate([
        np.ones(pair_rows),
        np.full(len(POINTS), 4.0),
        np.array([14.0]),
    ])
    upper = np.concatenate([
        np.full(pair_rows, infinity),
        np.full(len(POINTS), 4.0),
        np.array([14.0]),
    ])
    assert solver.addRows(
        row_count,
        lower,
        upper,
        0,
        np.zeros(row_count + 1, dtype=np.int32),
        np.empty(0, dtype=np.int32),
        np.empty(0, dtype=np.float64),
    ) == highspy.HighsStatus.kOk
    number = len(blocks)
    assert solver.addCols(
        number,
        np.zeros(number),
        np.zeros(number),
        np.ones(number),
        len(indices),
        starts,
        indices,
        np.ones(len(indices)),
    ) == highspy.HighsStatus.kOk
    columns = np.arange(number, dtype=np.int32)
    integrality = np.full(number, int(highspy.HighsVarType.kInteger), dtype=np.uint8)
    assert solver.changeColsIntegrality(
        number, columns, integrality
    ) == highspy.HighsStatus.kOk

    print(json.dumps({
        "blocks": number,
        "highs": solver.version(),
        "nonzeros": len(indices),
        "residual_pairs": pair_rows,
        "rows": row_count,
        "time_limit_seconds": args.seconds,
    }, sort_keys=True), flush=True)
    solver.run()
    info = solver.getInfo()
    solution = solver.getSolution()
    selected = [
        list(block)
        for block, value in zip(blocks, solution.col_value)
        if value > 0.5
    ] if solution.value_valid else []
    payload: dict[str, object] = {
        "model_status": solver.modelStatusToString(solver.getModelStatus()),
        "node_count": info.mip_node_count,
        "selected_remainder_blocks": len(selected),
        "status": "NO_VERIFIED_WITNESS",
    }
    if len(selected) == 14:
        full = [sorted(block) for block in STAR] + [list(FORCED)] + selected
        checked = verify(full)
        payload["verification"] = checked
        if checked["status"] == "VERIFIED_20_BLOCK_COVER":
            payload["status"] = "VERIFIED_20_BLOCK_COVER"
    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)


if __name__ == "__main__":
    main()
