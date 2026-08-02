#!/usr/bin/env python3
"""Exact Cycle-168 census of canonical carry-cocycle torsor products."""
from __future__ import annotations

import argparse
from itertools import product
import json
from pathlib import Path

from verify_cycle_166_fibre_torsor import build_payload as build_torsor_payload, shintani_step


DIMENSION = 6
PROBES = (
    ((1, 0), (1, 0)), ((1, 0), (0, 1)), ((0, 1), (1, 0)),
    ((0, 1), (0, 1)), ((5, 0), (1, 0)), ((0, 5), (0, 1)),
)


def add(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return ((left[0] + right[0]) % DIMENSION, (left[1] + right[1]) % DIMENSION)


def cocycle(parameters: tuple[int, int, int, int, int, int], left: tuple[int, int], right: tuple[int, int]) -> int:
    m00, m01, m10, m11, r0, r1 = parameters
    a, b = left
    c, d = right
    return (a * m00 * c + a * m01 * d + b * m10 * c + b * m11 * d + r0 * ((a + c) // DIMENSION) + r1 * ((b + d) // DIMENSION)) % DIMENSION


def basis_cocycle(index: int, left: tuple[int, int], right: tuple[int, int]) -> int:
    parameters = tuple(1 if position == index else 0 for position in range(6))
    return cocycle(parameters, left, right)


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

    associativity_checks = 0
    normalization_checks = 0
    zero = (0, 0)
    for index in range(6):
        for left in points:
            if basis_cocycle(index, zero, left) or basis_cocycle(index, left, zero):
                raise AssertionError(("non-normalized basis cocycle", index, left))
            normalization_checks += 2
            for right in points:
                for third in points:
                    left_side = (basis_cocycle(index, left, right) + basis_cocycle(index, add(left, right), third)) % DIMENSION
                    right_side = (basis_cocycle(index, right, third) + basis_cocycle(index, left, add(right, third))) % DIMENSION
                    if left_side != right_side:
                        raise AssertionError(("basis cocycle associativity failed", index, left, right, third))
                    associativity_checks += 1

    candidates = list(product(range(DIMENSION), repeat=6))
    probe_survivors = []
    first_probe_failure = None
    probe_checks = 0
    for parameters in candidates:
        passed = True
        for left, right in PROBES:
            expected = graph[add(left, right)]
            actual = (graph[left] + graph[right] + cocycle(parameters, left, right)) % DIMENSION
            probe_checks += 1
            if actual != expected:
                passed = False
                if first_probe_failure is None:
                    first_probe_failure = {"parameters": list(parameters), "left": list(left), "right": list(right), "expected_graph_label": expected, "actual_product_label": actual}
                break
        if passed:
            probe_survivors.append(parameters)
    if probe_checks > len(candidates) * len(PROBES):
        raise AssertionError("probe accounting overflow")

    graph_passing = []
    transport_passing = []
    compatible = []
    graph_checks = 0
    transport_checks = 0
    first_graph_failure = None
    first_transport_failure = None
    for parameters in probe_survivors:
        graph_ok = True
        transport_ok = True
        for left in points:
            for right in points:
                twist = cocycle(parameters, left, right)
                total = add(left, right)
                expected_graph = graph[total]
                actual_graph = (graph[left] + graph[right] + twist) % DIMENSION
                graph_checks += 1
                if actual_graph != expected_graph:
                    graph_ok = False
                    if first_graph_failure is None:
                        first_graph_failure = {"parameters": list(parameters), "left": list(left), "right": list(right), "expected_graph_label": expected_graph, "actual_product_label": actual_graph}
                expected_transport = (twist + transport[total]) % DIMENSION
                actual_transport = (transport[left] + transport[right] + cocycle(parameters, shintani_step(left), shintani_step(right))) % DIMENSION
                transport_checks += 1
                if actual_transport != expected_transport:
                    transport_ok = False
                    if first_transport_failure is None:
                        first_transport_failure = {"parameters": list(parameters), "left": list(left), "right": list(right), "expected_transported_product_label": expected_transport, "actual_product_of_transports_label": actual_transport}
        if graph_ok:
            graph_passing.append(list(parameters))
        if transport_ok:
            transport_passing.append(list(parameters))
        if graph_ok and transport_ok:
            compatible.append(list(parameters))
    return {
        "schema": "sic-stark-cycle-168-carry-cocycle-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "This exact finite census concerns only canonical normalized bilinear-plus-coordinate-carry C6 cocycles on the Cycle-166 torsor. It defines no coefficient-to-logarithm operation, AFK interface, Stark identity, fusion theorem, or TCC identity.",
        "summary": {"cocycle_candidates_checked": len(candidates), "fixed_probe_pairs": len(PROBES), "probe_evaluations": probe_checks, "probe_survivor_count": len(probe_survivors), "basis_cocycle_associativity_checks": associativity_checks, "basis_cocycle_normalization_checks": normalization_checks, "full_graph_identity_checks": graph_checks, "full_transport_identity_checks": transport_checks, "graph_passing_parameter_count": len(graph_passing), "transport_passing_parameter_count": len(transport_passing), "compatible_parameter_count": len(compatible), "carry_cocycle_completion_exists": bool(compatible)},
        "probe_survivors": [list(parameters) for parameters in probe_survivors],
        "graph_passing_parameters": graph_passing,
        "transport_passing_parameters": transport_passing,
        "compatible_parameters": compatible,
        "first_probe_failure": first_probe_failure,
        "first_graph_failure": first_graph_failure,
        "first_transport_failure": first_transport_failure,
        "gate_outcome": {"canonical_carry_cocycle": "SURVIVES_EXACT_FINITE_TEST" if compatible else "FALSIFIED_EXACT_FINITE_CLASS", "scope": "bilinear-plus-coordinate-carry normalized C6 cocycle representatives only"},
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
