#!/usr/bin/env python3
"""Cycle 46 exact semantic controls for the Cech total-complex map."""
from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
from lrc_cech_total import cone, direct_boundary_class, downward_closure, owner_star_cover, solve_injected_class, solve_total_class
from lrc_morse_critical_projection import add, boundary, boundary_cell


def tetrahedron_controls():
    vertices = tuple((part, 0) for part in range(4))
    full = downward_closure([vertices])
    sphere = downward_closure(boundary_cell(vertices))
    cycle = boundary({vertices: Fraction(1)})
    _owners, full_cover = owner_star_cover(full, 0)
    _owners, sphere_cover = owner_star_cover(sphere, 0)
    full_result = solve_total_class(full, full_cover, cycle)
    sphere_result = solve_total_class(sphere, sphere_cover, cycle)
    full_injected = solve_injected_class(full, full_cover, cycle)
    sphere_injected = solve_injected_class(sphere, sphere_cover, cycle)
    assert direct_boundary_class(full, cycle) == "BOUNDARY"
    assert direct_boundary_class(sphere, cycle) == "NONBOUNDARY"
    assert full_result["status"] == "BOUNDARY"
    assert sphere_result["status"] == "UNCOVERED"
    assert full_injected["status"] == full_result["status"]
    assert sphere_injected["status"] == sphere_result["status"]
    return {"full_simplex": full_result, "full_simplex_injected": full_injected, "tetrahedron_boundary": sphere_result, "tetrahedron_boundary_injected": sphere_injected}


def covered_sphere_control():
    apex = ((0, 0), (0, 1))
    left = ((1, 0), (1, 1))
    right = ((2, 0), (2, 1))
    base_edges = ((left[0], right[0]), (left[1], right[0]), (left[1], right[1]), (left[0], right[1]))
    # An oriented K_{2,2} cycle obtained exactly as a boundary-kernel vector.
    base_cycle = {
        tuple(sorted(base_edges[0])): Fraction(1),
        tuple(sorted(base_edges[1])): Fraction(-1),
        tuple(sorted(base_edges[2])): Fraction(1),
        tuple(sorted(base_edges[3])): Fraction(-1),
    }
    if boundary(base_cycle):
        base_cycle = {cell: -value for cell, value in base_cycle.items()}
    assert not boundary(base_cycle)
    cycle = add(cone(apex[0], base_cycle), cone(apex[1], base_cycle), scale=Fraction(-1))
    assert not boundary(cycle)
    facets = [tuple(sorted((vertex,) + edge)) for vertex in apex for edge in base_edges]
    complex_cells = downward_closure(facets)
    _owners, cover = owner_star_cover(complex_cells, 0)
    result = solve_total_class(complex_cells, cover, cycle)
    injected = solve_injected_class(complex_cells, cover, cycle)
    assert direct_boundary_class(complex_cells, cycle) == "NONBOUNDARY"
    assert result["status"] == "NONBOUNDARY"
    assert injected["status"] == result["status"]
    return {"full_total": result, "injected": injected}


def main():
    result = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "tetrahedron_controls": tetrahedron_controls(),
        "covered_nonboundary": covered_sphere_control(),
        "claim_boundary": "Generic exact semantic controls only; no p199 residual has been tested.",
    }
    out = ROOT / "discovery/out/cycle46-global-cech-quotient"
    out.mkdir(parents=True, exist_ok=True)
    target = out / "generic-controls.json"
    target.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": result["status"], "full_simplex": result["tetrahedron_controls"]["full_simplex"]["status"], "tetrahedron_boundary": result["tetrahedron_controls"]["tetrahedron_boundary"]["status"], "covered_nonboundary": result["covered_nonboundary"]["injected"]["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
