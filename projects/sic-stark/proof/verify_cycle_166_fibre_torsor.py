#!/usr/bin/env python3
"""Exact Cycle-166 fibre-resolved C6 multiplier-torsor prototype."""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path


DIMENSION = 6
MODULUS = 48
RADEMACHER = 6
A6 = ((115, -24), (24, -5))
ANCHORS = {(3, 5): 1, (3, 4): 2}
ROOT = Path(__file__).resolve().parents[1]
SECTION = ROOT / "discovery/cycle-164-oriented-ray-monoid-section-prototype-v1.json"


def mod_one(value: Fraction) -> Fraction:
    return value - value.numerator // value.denominator


def shintani_step(point: tuple[int, int]) -> tuple[int, int]:
    a, b = point
    return ((5 * a + b) % DIMENSION, (-a) % DIMENSION)


def phase_exponent(point: tuple[int, int]) -> int:
    a, b = point
    form = a * a - 5 * a * b + b * b
    return (24 * (DIMENSION + 7 * (1 + a) * (1 + b)) - 2 * RADEMACHER - 28 * form) % MODULUS


def theta_exponent(point: tuple[int, int]) -> Fraction:
    first, second = point
    a, b = A6[0]
    c, d = A6[1]
    r1 = Fraction(first, DIMENSION)
    r2 = Fraction(second, DIMENSION)
    return mod_one(Fraction(1, 2) * (
        (c - d + 1) * r1 + (-a + b + 1) * r2 - c * d * r1 * r1
        + 2 * (a - 1) * d * r1 * r2 - (a - 2) * b * r2 * r2
    ))


def orbit(start: tuple[int, int]) -> list[tuple[int, int]]:
    result = []
    point = start
    while point not in result:
        result.append(point)
        point = shintani_step(point)
    if point != start:
        raise AssertionError("T orbit did not return to its start")
    return result


def build_payload() -> dict[str, object]:
    section = json.loads(SECTION.read_text())
    labels = {tuple(row["characteristic"]): row["least_section_exponent"] for row in section["rows"]}
    points = sorted(labels)
    if len(points) != 36:
        raise AssertionError("sealed section has wrong domain")
    if {anchor: labels[anchor] for anchor in ANCHORS} != ANCHORS:
        raise AssertionError("sealed orientation anchors changed")

    difference = {}
    multiplier_rows = []
    for point in points:
        successor = shintani_step(point)
        phase = phase_exponent(point)
        successor_phase = phase_exponent(successor)
        delta_48 = (successor_phase - phase) % MODULUS
        if delta_48 % 8:
            raise AssertionError(("phase difference is not a sixth-root exponent", point, delta_48))
        transport = (delta_48 // 8) % DIMENSION
        difference[point] = transport
        if (phase + 8 * transport) % MODULUS != successor_phase:
            raise AssertionError(("phase transport equation failed", point))
        multiplier_square = mod_one(Fraction(phase, 24))
        expected_square = mod_one(Fraction(1, 2) - theta_exponent(point))
        if multiplier_square != expected_square:
            raise AssertionError(("Cycle-149 multiplier square mismatch", point))
        multiplier_rows.append({
            "characteristic": list(point), "phase_exponent_mod_48": phase,
            "successor": list(successor), "transport_exponent_mod_6": transport,
            "multiplier_square_exponent_mod_1": str(multiplier_square),
        })

    seen = set()
    orbit_rows = []
    lift = {}
    for point in points:
        if point in seen:
            continue
        raw_orbit = orbit(point)
        seen.update(raw_orbit)
        anchors = [anchor for anchor in ANCHORS if anchor in raw_orbit]
        if len(anchors) > 1:
            raise AssertionError("anchors unexpectedly share an orbit")
        base = anchors[0] if anchors else min(raw_orbit)
        ordered = orbit(base)
        lift[base] = labels[base]
        for current in ordered[:-1]:
            lift[shintani_step(current)] = (lift[current] + difference[current]) % DIMENSION
        if (lift[ordered[-1]] + difference[ordered[-1]]) % DIMENSION != lift[base]:
            raise AssertionError(("nonzero C6 holonomy", ordered))
        orbit_rows.append({
            "orbit": [list(item) for item in ordered], "base": list(base),
            "base_rule": "anchor" if anchors else "lexicographic_minimum",
            "transport_sum_mod_6": sum(difference[item] for item in ordered) % DIMENSION,
            "lift_labels": [lift[item] for item in ordered],
        })
    if len(lift) != 36:
        raise AssertionError("lift did not cover the base")
    if {anchor: lift[anchor] for anchor in ANCHORS} != ANCHORS:
        raise AssertionError(("anchor normalization failed", {anchor: lift[anchor] for anchor in ANCHORS}))

    def lifted_step(state: tuple[tuple[int, int], int]) -> tuple[tuple[int, int], int]:
        point, fibre = state
        return shintani_step(point), (fibre + difference[point]) % DIMENSION

    torsor_states_checked = 0
    for point in points:
        for fibre in range(DIMENSION):
            state = (point, fibre)
            first = lifted_step(state)
            second = lifted_step(first)
            third = lifted_step(second)
            if third != state:
                raise AssertionError(("lifted third-return failed", state, third))
            graph_image = lifted_step((point, lift[point]))
            if graph_image != (shintani_step(point), lift[shintani_step(point)]):
                raise AssertionError(("graph intertwining failed", point, graph_image))
            torsor_states_checked += 1
    return {
        "schema": "sic-stark-cycle-166-fibre-torsor-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "This exact finite result constructs a phase-derived fibre-resolved C6 transport torsor. "
            "It defines no additive coefficient-to-logarithm operation, analytic continuation, finite part, "
            "AFK-interface identification, Stark identity, fusion theorem, or TCC identity."
        ),
        "conventions": {
            "base": "X=(Z/6Z)^2", "shintani_action": "T(a,b)=(5a+b,-a) mod 6",
            "fibre": "right C6 torsor with zeta_6=zeta_48^8",
            "phase": "Phi(a,b)=zeta_48^p(a,b) from Cycle-149 AFK/Kopp ledger",
            "transport": "T_tilde(x,e)=(Tx,e+d(x))",
            "graph": "anchor-normalized s(Tx)=s(x)+d(x)",
        },
        "summary": {
            "base_rows_checked": len(points), "torsor_states_checked": torsor_states_checked,
            "phase_differences_all_divisible_by_8": True,
            "all_multiplier_square_identities_match": True,
            "all_t_orbit_holonomies_zero": True,
            "lifted_third_return_identity": True,
            "graph_intertwining": True,
            "orientation_anchors": {f"{a},{b}": lift[(a, b)] for a, b in ANCHORS},
            "orbit_count": len(orbit_rows),
        },
        "multiplier_rows": multiplier_rows,
        "transport_orbits": orbit_rows,
        "gate_outcome": {
            "fibre_resolved_multiplier_torsor": "SURVIVES_EXACT_FINITE_TRANSPORT_TEST",
            "scope": "finite phase-derived state space only; no analytic coefficient operation",
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
