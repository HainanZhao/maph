#!/usr/bin/env python3
"""Exact deletion-cover exchange lemma and r=6 extremal control."""

from __future__ import annotations

import itertools
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
from cycle69_r6_extremal_control import EDGES, cover, minimum_cover


def exchangeable(edge, rest, transversal):
    """Return replacements c->v that preserve coverage after adding edge."""
    result = []
    for c in transversal:
        essential = [f for f in rest if not ((set(transversal) - {c}) & f)]
        for v in edge:
            if all(v in f for f in essential):
                candidate = tuple(x for x in transversal if x != c) + (v,)
                if cover(candidate, rest + [edge]):
                    result.append((c, v, len(essential)))
    return result


def main():
    edges = [set(edge) for edge in EDGES]
    # General proof obligation, checked mechanically on arbitrary finite input:
    # if c->v is returned, C-c+v covers every old edge and the deleted edge.
    control = []
    for i, edge in enumerate(edges):
        rest = edges[:i] + edges[i + 1:]
        C = minimum_cover(rest, 4)
        assert len(C) == 4
        vertices = sorted(set().union(*edges))
        all_minimum = [candidate for candidate in itertools.combinations(vertices, 4) if cover(candidate, rest)]
        assert all(not(set(candidate) & edge) for candidate in all_minimum)
        all_moves = [exchangeable(edge, rest, candidate) for candidate in all_minimum]
        assert all(not moves for moves in all_moves)
        control.append({"deleted_edge": i + 1, "minimum_cover_count": len(all_minimum),
                        "all_disjoint_from_deleted_edge": True, "all_exchange_move_counts": [len(moves) for moves in all_moves]})
    # Formal necessary condition for a minimal tau>=6 counterexample:
    # every size-five deletion cover must have no exchange move.  Otherwise the
    # exchange is a size-five cover of H.
    print(json.dumps({"status":"PASS", "epistemic_status":"PROVED",
      "lemma":"If C covers H-e and c in C may be replaced by v in e while covering every edge uniquely hit by c, then (C-c)+v covers H.",
      "counterexample_necessary_condition":"For every e and every five-cover C of H-e, every c in C has essential edges with no common vertex in e.",
      "control":"Every minimum four-cover of every edge-deletion of the published 13-edge tau=5 system is disjoint from the deleted edge and has no one-vertex exchange. Thus raw local exchange is not sufficient to distinguish a tau=6 counterexample.",
      "control_rows": control,
      "claim_boundary":"A necessary local condition only; it does not establish tau(H)<=5 for arbitrary intersecting 6-partite H."}, sort_keys=True))


if __name__ == "__main__":
    main()
