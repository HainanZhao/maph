#!/usr/bin/env python3
"""Exact finite descent test for Cycle 165's pointwise section pushforward."""
from __future__ import annotations

import argparse
from itertools import product
import json
from pathlib import Path


DIMENSION = 6
ROOT = Path(__file__).resolve().parents[1]
SECTION = ROOT / "discovery/cycle-164-oriented-ray-monoid-section-prototype-v1.json"


def shintani_step(point: tuple[int, int]) -> tuple[int, int]:
    a, b = point
    return ((5 * a + b) % DIMENSION, (-a) % DIMENSION)


def build_payload() -> dict[str, object]:
    section = json.loads(SECTION.read_text())
    labels = {
        tuple(row["characteristic"]): row["least_section_exponent"]
        for row in section["rows"]
    }
    points = sorted(labels)
    if len(points) != DIMENSION * DIMENSION:
        raise AssertionError(f"expected 36 section labels, found {len(points)}")
    successors = {
        label: sorted({labels[shintani_step(point)] for point in points if labels[point] == label})
        for label in range(DIMENSION)
    }
    fibre_witnesses = []
    for label in range(DIMENSION):
        fibre = [point for point in points if labels[point] == label]
        if len(successors[label]) > 1:
            first_successor = labels[shintani_step(fibre[0])]
            partner = next(
                point for point in fibre if labels[shintani_step(point)] != first_successor
            )
            fibre_witnesses.append(
                {
                    "source_label": label,
                    "first_point": list(fibre[0]),
                    "first_successor_label": first_successor,
                    "second_point": list(partner),
                    "second_successor_label": labels[shintani_step(partner)],
                    "successor_labels": successors[label],
                }
            )
    compatible_actions = []
    for action in product(range(DIMENSION), repeat=DIMENSION):
        if all(action[labels[point]] == labels[shintani_step(point)] for point in points):
            compatible_actions.append(list(action))
    descent_exists = bool(compatible_actions)
    if descent_exists != all(len(values) == 1 for values in successors.values()):
        raise AssertionError("descent criterion disagrees with exhaustive action census")
    if compatible_actions:
        expected = [successors[label][0] for label in range(DIMENSION)]
        if compatible_actions != [expected]:
            raise AssertionError((compatible_actions, expected))
    return {
        "schema": "sic-stark-cycle-165-section-equivariance-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "This exact finite result tests only deterministic pointwise label-respecting "
            "pushforwards from the formal 36-characteristic module through the sealed "
            "section. It does not rule out non-pointwise, non-fibrewise, nonlinear, or "
            "analytically regularized coefficient-to-logarithm operations."
        ),
        "conventions": {
            "input_module": "Q[(Z/6Z)^2] with basis delta_(a,b)",
            "shintani_action": "T(a,b)=(5a+b,-a) mod 6",
            "section": "Cycle-164 least exponent lambda(a,b) in C6",
            "operation": "A(delta_x)=delta_(lambda(x))",
            "target_action": "U_u(delta_e)=delta_(u(e)) for u:C6->C6",
            "compatibility": "A*T_*=U_u*A on every basis vector",
        },
        "summary": {
            "rows_checked": len(points),
            "target_actions_checked": DIMENSION ** DIMENSION,
            "compatible_target_actions": len(compatible_actions),
            "section_equivariant_descent_exists": descent_exists,
            "successor_labels_by_source_label": {str(label): successors[label] for label in range(DIMENSION)},
            "fibre_instability_witness_count": len(fibre_witnesses),
            "first_fibre_instability_witness": fibre_witnesses[0] if fibre_witnesses else None,
        },
        "fibre_instability_witnesses": fibre_witnesses,
        "compatible_target_actions": compatible_actions,
        "gate_outcome": {
            "pointwise_section_equivariant_operation": (
                "FALSIFIED_BY_FIBRE_INSTABILITY" if not descent_exists else "SURVIVES_EXACT_DESCENT"
            ),
            "scope": "deterministic pointwise label-respecting pushforwards only",
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
