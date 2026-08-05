#!/usr/bin/env python3
import argparse
import json
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix


def cube(n):
    edges = []
    edge_id = {}
    for d in range(n):
        for u in range(1 << n):
            if (u >> d) & 1:
                continue
            v = u ^ (1 << d)
            edge_id[(min(u, v), max(u, v))] = len(edges)
            edges.append((u, v))
    squares = []
    for i in range(n):
        for j in range(i + 1, n):
            for b in range(1 << n):
                if ((b >> i) & 1) or ((b >> j) & 1):
                    continue
                bi, bj = b ^ (1 << i), b ^ (1 << j)
                bij = b ^ (1 << i) ^ (1 << j)
                pairs = [(b, bi), (b, bj), (bi, bij), (bj, bij)]
                squares.append([edge_id[(min(a, z), max(a, z))] for a, z in pairs])
    return edges, squares


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dimension", type=int)
    ap.add_argument("--time-limit", type=float, default=3600.0)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    edges, squares = cube(args.dimension)
    a = lil_matrix((len(squares), len(edges)), dtype=np.float64)
    for row, square in enumerate(squares):
        a[row, square] = 1.0
    start = time.monotonic()
    result = milp(
        -np.ones(len(edges)),
        integrality=np.ones(len(edges)),
        bounds=Bounds(np.zeros(len(edges)), np.ones(len(edges))),
        constraints=LinearConstraint(a.tocsr(), -np.inf, 3.0),
        options={"time_limit": args.time_limit, "presolve": True},
    )
    selected = []
    if result.x is not None:
        selected = [list(edges[i]) for i, x in enumerate(result.x) if x > 0.5]
    payload = {
        "epistemic_status": "OBSERVED",
        "dimension": args.dimension,
        "edge_variables": len(edges),
        "square_constraints": len(squares),
        "solver": "scipy.optimize.milp/HiGHS",
        "scipy_version": __import__("scipy").__version__,
        "status": int(result.status),
        "message": str(result.message),
        "objective_edges": len(selected),
        "mip_gap": None if getattr(result, "mip_gap", None) is None else float(result.mip_gap),
        "mip_node_count": None if getattr(result, "mip_node_count", None) is None else int(result.mip_node_count),
        "wall_seconds": time.monotonic() - start,
        "selected_edges": selected,
    }
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(payload, f, sort_keys=True, separators=(",", ":"))
        f.write("\n")
    print(json.dumps({k: v for k, v in payload.items() if k != "selected_edges"}, sort_keys=True))


if __name__ == "__main__":
    main()

