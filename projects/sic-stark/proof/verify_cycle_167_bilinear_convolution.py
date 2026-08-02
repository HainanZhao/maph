#!/usr/bin/env python3
"""Exact Cycle-167 census of bilinear C6-twisted torsor convolutions."""
from __future__ import annotations

import argparse
from itertools import product
import json
from pathlib import Path

from verify_cycle_166_fibre_torsor import build_payload as build_torsor_payload, shintani_step


DIMENSION = 6


def add(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return ((left[0] + right[0]) % DIMENSION, (left[1] + right[1]) % DIMENSION)


def bilinear(matrix: tuple[int, int, int, int], left: tuple[int, int], right: tuple[int, int]) -> int:
    m00, m01, m10, m11 = matrix
    a, b = left
    c, d = right
    return (a * m00 * c + a * m01 * d + b * m10 * c + b * m11 * d) % DIMENSION


def build_payload() -> dict[str, object]:
    torsor = build_torsor_payload()
    phase_rows = torsor["multiplier_rows"]
    points = sorted(tuple(row["characteristic"]) for row in phase_rows)
    transport = {tuple(row["characteristic"]): row["transport_exponent_mod_6"] for row in phase_rows}
    graph = {}
    for orbit in torsor["transport_orbits"]:
        graph.update({tuple(point): label for point, label in zip(orbit["orbit"], orbit["lift_labels"], strict=True)})
    if len(points) != 36 or len(graph) != 36 or len(transport) != 36:
        raise AssertionError("sealed torsor domain drift")

    matrices = list(product(range(DIMENSION), repeat=4))
    graph_passing = []
    transport_passing = []
    compatible = []
    graph_checks = 0
    transport_checks = 0
    first_graph_failure = None
    first_transport_failure = None
    for matrix in matrices:
        graph_ok = True
        transport_ok = True
        for left in points:
            for right in points:
                twist = bilinear(matrix, left, right)
                total = add(left, right)
                expected_graph = graph[total]
                actual_graph = (graph[left] + graph[right] + twist) % DIMENSION
                graph_checks += 1
                if actual_graph != expected_graph:
                    graph_ok = False
                    if first_graph_failure is None:
                        first_graph_failure = {
                            "matrix": list(matrix), "left": list(left), "right": list(right),
                            "expected_graph_label": expected_graph, "actual_product_label": actual_graph,
                        }
                expected_transport = (twist + transport[total]) % DIMENSION
                actual_transport = (transport[left] + transport[right] + bilinear(matrix, shintani_step(left), shintani_step(right))) % DIMENSION
                transport_checks += 1
                if actual_transport != expected_transport:
                    transport_ok = False
                    if first_transport_failure is None:
                        first_transport_failure = {
                            "matrix": list(matrix), "left": list(left), "right": list(right),
                            "expected_transported_product_label": expected_transport,
                            "actual_product_of_transports_label": actual_transport,
                        }
        if graph_ok:
            graph_passing.append(list(matrix))
        if transport_ok:
            transport_passing.append(list(matrix))
        if graph_ok and transport_ok:
            compatible.append(list(matrix))
    if graph_checks != 1296 * 1296 or transport_checks != 1296 * 1296:
        raise AssertionError("incomplete census")
    return {
        "schema": "sic-stark-cycle-167-bilinear-convolution-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "This exact finite census concerns only translation-invariant bilinear C6-twisted convolutions "
            "on the Cycle-166 torsor. It defines no coefficient-to-logarithm operation, AFK interface, Stark identity, fusion theorem, or TCC identity."
        ),
        "conventions": {
            "base": "X=(Z/6Z)^2",
            "source_product": "delta_x*delta_y=delta_(x+y)",
            "target_product": "delta_(x,e) star_M delta_(y,f)=delta_(x+y,e+f+x^T M y)",
            "transport": "T_tilde(delta_(x,e))=delta_(Tx,e+d(x))",
            "graph": "J(delta_x)=delta_(x,s(x))",
        },
        "summary": {
            "matrices_checked": len(matrices),
            "basis_pairs_per_matrix": len(points) ** 2,
            "graph_identity_checks": graph_checks,
            "transport_identity_checks": transport_checks,
            "graph_passing_matrix_count": len(graph_passing),
            "transport_passing_matrix_count": len(transport_passing),
            "compatible_matrix_count": len(compatible),
            "bilinear_convolution_exists": bool(compatible),
        },
        "graph_passing_matrices": graph_passing,
        "transport_passing_matrices": transport_passing,
        "compatible_matrices": compatible,
        "first_graph_failure": first_graph_failure,
        "first_transport_failure": first_transport_failure,
        "gate_outcome": {
            "bilinear_c6_twisted_convolution": "SURVIVES_EXACT_FINITE_TEST" if compatible else "FALSIFIED_EXACT_FINITE_CLASS",
            "scope": "translation-invariant bilinear C6 twists only",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    encoded = json.dumps(build_payload(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
