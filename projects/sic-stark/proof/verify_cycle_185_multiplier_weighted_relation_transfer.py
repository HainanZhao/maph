#!/usr/bin/env python3
"""Exact multiplier-weighted C6 relation transfer for Cycle 185."""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PREVIOUS = ROOT / "discovery/cycle-184-multiplier-refined-correspondence-prototype-v1.json"
TRANSPORT = ROOT / "discovery/cycle-181-shintani-local-action-prototype-v1.json"
Field = tuple[Fraction, Fraction]  # a + b*zeta_6, zeta_6^2-zeta_6+1=0
Element = tuple[Field, ...]
ZERO: Field = (Fraction(0), Fraction(0))
ONE: Field = (Fraction(1), Fraction(0))
ZETA: Field = (Fraction(0), Fraction(1))


def add(left: Field, right: Field) -> Field:
    return left[0] + right[0], left[1] + right[1]


def multiply(left: Field, right: Field) -> Field:
    # (a+bz)(c+dz)=(ac-bd)+(ad+bc+bd)z for z^2=z-1.
    a, b = left
    c, d = right
    return a * c - b * d, a * d + b * c + b * d


def power(base: Field, exponent: int) -> Field:
    result = ONE
    for _ in range(exponent % 6):
        result = multiply(result, base)
    return result


def measure(relation: list[int]) -> Element:
    if not relation:
        raise AssertionError("empty relation")
    denominator = Fraction(1, len(relation))
    return tuple((denominator, Fraction(0)) if index in relation else ZERO for index in range(6))


def weighted(relation: list[int], phase_step: int) -> Element:
    scalar = power(ZETA, phase_step)
    return tuple(multiply(scalar, coefficient) for coefficient in measure(relation))


def convolution(left: Element, right: Element) -> Element:
    output = [ZERO for _ in range(6)]
    for first, first_value in enumerate(left):
        for second, second_value in enumerate(right):
            target = (first + second) % 6
            output[target] = add(output[target], multiply(first_value, second_value))
    return tuple(output)


def serialise(element: Element) -> list[list[str]]:
    return [[str(real), str(imaginary)] for real, imaginary in element]


def payload() -> dict[str, object]:
    correspondence = json.loads(PREVIOUS.read_text())
    transport = json.loads(TRANSPORT.read_text())
    rows = {tuple(row["characteristic"]): row for row in correspondence["rows"]}
    transport_rows = {tuple(row["characteristic"]): row for row in transport["rows"]}
    if len(rows) != 36 or set(rows) != set(transport_rows):
        raise AssertionError("frozen source domain drift")

    label_types = set()
    products = []
    for characteristic in sorted(rows):
        row = rows[characteristic]
        ray_row = transport_rows[characteristic]
        successor = tuple(row["successor"])
        second = tuple(rows[successor]["successor"])
        if tuple(rows[second]["successor"]) != characteristic:
            raise AssertionError(("third return", characteristic))
        if row["relation"] != ray_row["direct_action_relation"]:
            raise AssertionError(("direct relation drift", characteristic))
        phase_steps = []
        transfers = []
        for point in (characteristic, successor, second):
            source = rows[point]
            delta = source["phase_delta_mod_48"]
            if delta % 8:
                raise AssertionError(("nonintegral phase step", point, delta))
            phase_step = delta // 8
            phase_steps.append(phase_step)
            transfers.append(weighted(source["relation"], phase_step))
            label_types.add((tuple(source["relation"]), phase_step))
        product = convolution(convolution(transfers[0], transfers[1]), transfers[2])
        expected = measure(ray_row["third_return_kernel"])
        if product != expected:
            raise AssertionError(("kernel product", characteristic, serialise(product), serialise(expected)))
        if sum(phase_steps) % 6:
            raise AssertionError(("phase holonomy", characteristic, phase_steps))
        products.append({
            "characteristic": list(characteristic),
            "successor": list(successor),
            "relation": row["relation"],
            "phase_step_mod_6": phase_steps[0],
            "transfer": serialise(transfers[0]),
            "triple_kernel": ray_row["third_return_kernel"],
            "triple_product": serialise(product),
        })

    anchors = {point: rows[point] for point in ((3, 5), (3, 4))}
    expected_anchors = {
        (3, 5): weighted([3], 0),
        (3, 4): weighted([3], 3),
    }
    for point, expected in expected_anchors.items():
        row = anchors[point]
        actual = weighted(row["relation"], row["phase_delta_mod_48"] // 8)
        if actual != expected:
            raise AssertionError(("orientation anchor", point, serialise(actual), serialise(expected)))
    if not 0 < len(label_types) < 36:
        raise AssertionError(("label compression", len(label_types)))
    return {
        "schema": "sic-stark-cycle-185-multiplier-weighted-relation-transfer-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "This exact finite result linearizes the multiplier-refined relation correspondence in Q(zeta_6)[C6]. It defines no AFK spectral coefficient, coefficient-to-ray interface, Stark regulator equality, fusion theorem, or TCC identity.",
        "conventions": {"field": "Q(zeta_6), zeta_6^2-zeta_6+1=0", "transfer": "W_x=zeta_6^(delta_x/8) mu(D_x)", "measure": "mu(D)=|D|^-1 sum_(d in D)[d]", "product": "C6 group-algebra convolution"},
        "summary": {"rows_checked": len(rows), "relation_label_count": len(label_types), "strict_label_compression": len(label_types) < 36, "phase_integrality_checks": len(rows), "direct_relation_agreements": len(rows), "triple_products_checked": len(products), "all_triple_products_equal_independent_kernels": True, "anchors": {"3,5": serialise(expected_anchors[(3, 5)]), "3,4": serialise(expected_anchors[(3, 4)])}},
        "relation_labels": [{"relation": list(relation), "phase_step_mod_6": step} for relation, step in sorted(label_types)],
        "products": products,
        "gate_outcome": {"multiplier_weighted_relation_transfer": "EXACT_GROUP_ALGEBRA_COMPOSITION_VALIDATED", "scope": "finite phase-decorated relation transfer only"},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(payload(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
