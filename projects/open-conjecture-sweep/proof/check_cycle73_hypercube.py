#!/usr/bin/env python3
import argparse
import json


def cube(n):
    edges = []
    edge_set = set()
    for d in range(n):
        for u in range(1 << n):
            if (u >> d) & 1:
                continue
            v = u ^ (1 << d)
            edge = (min(u, v), max(u, v))
            edges.append(edge)
            edge_set.add(edge)
    squares = []
    for i in range(n):
        for j in range(i + 1, n):
            for b in range(1 << n):
                if ((b >> i) & 1) or ((b >> j) & 1):
                    continue
                bi, bj = b ^ (1 << i), b ^ (1 << j)
                bij = b ^ (1 << i) ^ (1 << j)
                squares.append({
                    (min(b, bi), max(b, bi)),
                    (min(b, bj), max(b, bj)),
                    (min(bi, bij), max(bi, bij)),
                    (min(bj, bij), max(bj, bij)),
                })
    return edges, edge_set, squares


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("result")
    ap.add_argument("--minimum", type=int, required=True)
    ap.add_argument("--dimension", type=int)
    args = ap.parse_args()
    with open(args.result, encoding="utf-8") as f:
        raw = f.read()
    if raw.lstrip().startswith("{"):
        payload = json.loads(raw)
        n = int(payload.get("dimension", payload.get("n", args.dimension)))
        raw_edges = payload.get("selected_edges", payload.get("edges"))
        assert raw_edges is not None, "JSON has no edge list"
        chosen_list = [tuple(map(int, edge)) for edge in raw_edges]
    else:
        assert args.dimension is not None, "--dimension required for SAT output"
        n = args.dimension
        edge_count = n * (1 << (n - 1))
        literals = []
        for line in raw.splitlines():
            if line.startswith("v "):
                literals.extend(int(x) for x in line.split()[1:] if x != "0")
        assert literals, "no DIMACS model lines"
        model = {abs(x): x > 0 for x in literals}
        assert all(var in model for var in range(1, edge_count + 1))
        all_edges, _, _ = cube(n)
        chosen_list = [all_edges[var - 1] for var in range(1, edge_count + 1)
                       if model[var]]
    edges, universe, squares = cube(n)
    chosen = set(chosen_list)
    assert len(chosen) == len(chosen_list), "duplicate selected edge"
    assert chosen <= universe, "edge outside Q_n"
    assert len(chosen) >= args.minimum, "cardinality below requested bound"
    violations = [idx for idx, square in enumerate(squares) if square <= chosen]
    assert not violations, f"four-cycle violations: {violations[:10]}"
    assert len(edges) == n * (1 << (n - 1))
    assert len(squares) == n * (n - 1) // 2 * (1 << (n - 2))
    print(json.dumps({
        "epistemic_status": "PROVED",
        "status": "PASS",
        "dimension": n,
        "checked_selected_edges": len(chosen),
        "checked_edge_universe": len(edges),
        "checked_squares": len(squares),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
