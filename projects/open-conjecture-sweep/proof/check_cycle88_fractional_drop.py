#!/usr/bin/env python3
"""Exact finite gate for C88's residual fractional-cover-drop mechanism.

SciPy is deliberately used only to suggest rational vectors.  A row is
accepted only after its primal fractional cover and dual fractional matching
are reconstructed as ``Fraction`` values and independently checked.
"""

from __future__ import annotations

from fractions import Fraction
import importlib.util
import json
import math
from pathlib import Path
import time

from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[1]
CONTROL = ROOT / "discovery" / "cycle69_r6_extremal_control.py"
MAX_DEPTH = 5
WALL_SECONDS = 180
DENOMINATOR_CAP = 100_000


def load_edges() -> tuple[tuple[tuple[int, int], ...], ...]:
    spec = importlib.util.spec_from_file_location("cycle69_control", CONTROL)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return tuple(tuple(sorted(edge)) for edge in module.EDGES)


def rationalize(values: list[float]) -> tuple[Fraction, ...]:
    return tuple(Fraction(0) if abs(value) < 1e-9 else Fraction(value).limit_denominator(DENOMINATOR_CAP)
                 for value in values)


def exact_certificate(edge_ids: tuple[int, ...], edges: tuple[tuple[tuple[int, int], ...], ...]):
    """Return exact, mutually bounding primal/dual certificates, or None."""
    if not edge_ids:
        return ((), (), Fraction(0), ())
    vertices = tuple(sorted({v for edge_id in edge_ids for v in edges[edge_id]}))
    incidence = [[int(vertex in edges[edge_id]) for vertex in vertices] for edge_id in edge_ids]
    # Candidate primal cover: min 1.x subject to A x >= 1.
    primal_float = linprog([1.0] * len(vertices), A_ub=[[-entry for entry in row] for row in incidence],
                            b_ub=[-1.0] * len(edge_ids), bounds=(0, None), method="highs")
    # Candidate dual matching: max 1.y subject to A^T y <= 1.
    dual_float = linprog([-1.0] * len(edge_ids), A_ub=list(map(list, zip(*incidence))),
                          b_ub=[1.0] * len(vertices), bounds=(0, None), method="highs")
    if not primal_float.success or not dual_float.success:
        return None
    primal = rationalize(primal_float.x.tolist())
    dual = rationalize(dual_float.x.tolist())
    if any(value < 0 for value in primal) or any(value < 0 for value in dual):
        return None
    if any(sum(primal[index] for index, vertex in enumerate(vertices) if vertex in edges[edge_id]) < 1
           for edge_id in edge_ids):
        return None
    if any(sum(dual[index] for index, edge_id in enumerate(edge_ids) if vertex in edges[edge_id]) > 1
           for vertex in vertices):
        return None
    primal_value, dual_value = sum(primal), sum(dual)
    if primal_value != dual_value:
        return None
    return (vertices, primal, primal_value, dual)


def main() -> None:
    started = time.monotonic()
    edges = load_edges()
    all_ids = tuple(range(len(edges)))
    certificate_cache = {}
    states = {all_ids}
    layer_counts = [1]
    checked_rows = []
    failures = []
    unreconstructed = []
    all_vertices = tuple(sorted({vertex for edge in edges for vertex in edge}))

    def certificate(residual):
        if residual not in certificate_cache:
            certificate_cache[residual] = exact_certificate(residual, edges)
        return certificate_cache[residual]

    for depth in range(MAX_DEPTH + 1):
        next_states = set()
        for residual in sorted(states):
            if time.monotonic() - started > WALL_SECONDS:
                raise TimeoutError("C88 aggregate wall cap exceeded")
            cert = certificate(residual)
            if cert is None:
                unreconstructed.append({"depth": depth, "residual_edges": list(residual)})
                continue
            vertices, primal, value, dual = cert
            row = {"depth": depth, "residual_edges": [edge_id + 1 for edge_id in residual],
                   "tau_star": str(value), "primal_support": [
                       [list(vertices[i]), str(weight)] for i, weight in enumerate(primal) if weight],
                   "dual_support": [[edge_id + 1, str(weight)] for edge_id, weight in zip(residual, dual) if weight]}
            if depth < MAX_DEPTH:
                children = {}
                for vertex in all_vertices:
                    child = tuple(edge_id for edge_id in residual if vertex not in edges[edge_id])
                    children[vertex] = child
                    next_states.add(child)
                # For this residual the least integer k with tau* <= k is the
                # strongest applicable FD_k instance; failure there refutes
                # the universal formulation (and makes larger k irrelevant).
                k = math.ceil(value)
                row["k"] = k
                row["premise"] = 1 <= k <= MAX_DEPTH
                if row["premise"]:
                    child_values = {}
                    for vertex, child in children.items():
                        child_cert = certificate(child)
                        if child_cert is None:
                            unreconstructed.append({"depth": depth + 1, "residual_edges": list(child)})
                            continue
                        child_values[vertex] = child_cert[2]
                    drops = [vertex for vertex, child_value in child_values.items() if child_value <= k - 1]
                    row["drop_vertices"] = [list(vertex) for vertex in drops]
                    if not drops:
                        failures.append(row.copy())
                checked_rows.append(row)
        if depth == MAX_DEPTH:
            break
        states = next_states
        layer_counts.append(len(states))

    if unreconstructed:
        status, epistemic_status = "UNRECONSTRUCTED", "OBSERVED"
    elif failures:
        status, epistemic_status = "FD_REFUTED", "PROVED"
    else:
        status, epistemic_status = "FINITE_PASS", "PROVED"
    print(json.dumps({
        "status": status,
        "epistemic_status": epistemic_status,
        "claim_boundary": "Exact result only for the published 13-edge control and all deduplicated residuals through depth five; a finite pass does not prove FD universally.",
        "maximum_depth": MAX_DEPTH,
        "layer_counts": layer_counts,
        "residuals_checked": len(checked_rows),
        "certificate_cache_size": len(certificate_cache),
        "unreconstructed": unreconstructed,
        "failures": failures,
        "rows": checked_rows,
        "wall_seconds": round(time.monotonic() - started, 6),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
