#!/usr/bin/env python3
"""Exact corrected d=6 same-tuple AFK stabilizer-covariance audit."""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path


DIMENSION = 6
L = ((5, -1), (1, 0))
A = ((115, -24), (24, -5))
Point = tuple[int, int]


def matrix_multiply(left: tuple[tuple[int, int], tuple[int, int]], right: tuple[tuple[int, int], tuple[int, int]]) -> tuple[tuple[int, int], tuple[int, int]]:
    return tuple(tuple(sum(left[row][k] * right[k][column] for k in range(2)) for column in range(2)) for row in range(2))  # type: ignore[return-value]


def matrix_apply(matrix: tuple[tuple[int, int], tuple[int, int]], point: Point) -> Point:
    return tuple(sum(matrix[row][column] * point[column] for column in range(2)) for row in range(2))  # type: ignore[return-value]


def standard(point: Point) -> Point:
    return point[0] % DIMENSION, point[1] % DIMENSION


def negative(point: Point) -> Point:
    return standard((-point[0], -point[1]))


def pairing(left: Point, right: Point) -> int:
    """AFK's <left,right>=left_2 right_1-left_1 right_2."""
    return left[1] * right[0] - left[0] * right[1]


def form(point: Point) -> int:
    first, second = point
    return first * first - 5 * first * second + second * second


def transport(point: Point) -> tuple[Point, int, int]:
    """u_reduce(Lp)=xi_6^(-<Lp,reduce(Lp)>) u_p, as a sign."""
    lifted = matrix_apply(L, point)
    reduced = standard(lifted)
    exponent = pairing(lifted, reduced)
    if exponent % DIMENSION:
        raise AssertionError((point, lifted, reduced, exponent))
    return reduced, exponent, -1 if (exponent // DIMENSION) % 2 else 1


def signed_reciprocal(point: Point) -> tuple[Point, int]:
    """u_p*u_reduce(-p)=(-1)^<q,p>, reduce(-p)=-p+6q."""
    reduced = negative(point)
    lift = ((reduced[0] + point[0]) // DIMENSION, (reduced[1] + point[1]) // DIMENSION)
    return reduced, -1 if pairing(lift, point) % 2 else 1


def signed_orbits() -> tuple[list[list[Point]], dict[Point, int], list[dict[str, object]]]:
    unseen = {(a, b) for a in range(DIMENSION) for b in range(DIMENSION) if (a, b) != (0, 0)}
    orbits: list[list[Point]] = []
    signs: dict[Point, int] = {}
    records: list[dict[str, object]] = []
    while unseen:
        root = min(unseen)
        orbit: list[Point] = []
        current = root
        current_sign = 1
        while current not in orbit:
            orbit.append(current)
            signs[current] = current_sign
            target, exponent, sign = transport(current)
            records.append({"from": list(current), "to": list(target), "lift_pairing": exponent, "transport_sign": sign})
            current = target
            current_sign *= sign
        if current != root or current_sign != 1:
            raise AssertionError((root, orbit, current, current_sign))
        unseen.difference_update(orbit)
        orbits.append(orbit)
    return orbits, signs, records


def assignment(orbits: list[list[Point]], signs: dict[Point, int], target_seed: Fraction) -> dict[Point, Fraction]:
    orbit_index = {point: index for index, orbit in enumerate(orbits) for point in orbit}
    roots = [orbit[0] for orbit in orbits]
    target_index = orbit_index[(0, 1)]
    values: dict[Point, Fraction] = {}
    handled: set[int] = set()
    for index in range(len(orbits)):
        if index in handled:
            continue
        inverse_index = orbit_index[negative(roots[index])]
        if inverse_index == index:
            for point in orbits[index]:
                values[point] = Fraction(signs[point])
            handled.add(index)
            continue
        primary = target_index if target_index in {index, inverse_index} else min(index, inverse_index)
        secondary = inverse_index if primary == index else index
        seed = target_seed if primary == target_index else Fraction(1)
        for point in orbits[primary]:
            values[point] = signs[point] * seed
        reciprocal_of_root, reciprocal_sign = signed_reciprocal(roots[primary])
        secondary_seed = Fraction(reciprocal_sign, 1) / (signs[reciprocal_of_root] * seed)
        for point in orbits[secondary]:
            values[point] = signs[point] * secondary_seed
        handled.add(primary)
        handled.add(secondary)
    return values


def check_assignment(values: dict[Point, Fraction]) -> None:
    expected = {(a, b) for a in range(DIMENSION) for b in range(DIMENSION) if (a, b) != (0, 0)}
    if set(values) != expected:
        raise AssertionError("support")
    for point, value in values.items():
        if not value:
            raise AssertionError(("zero", point))
        target, _, transport_sign = transport(point)
        if values[target] != transport_sign * value:
            raise AssertionError(("transport", point, target, values[target], transport_sign * value))
        inverse, reciprocal_sign = signed_reciprocal(point)
        if value * values[inverse] != reciprocal_sign:
            raise AssertionError(("reciprocal", point, inverse, value, values[inverse], reciprocal_sign))


def payload() -> dict[str, object]:
    identity = ((1, 0), (0, 1))
    if matrix_multiply(matrix_multiply(L, L), L) != A:
        raise AssertionError("L cubed")
    if not all(form(matrix_apply(L, point)) == form(point) for point in ((a, b) for a in range(-6, 7) for b in range(-6, 7))):
        raise AssertionError("Q invariance")
    if not all(A[row][column] % DIMENSION == identity[row][column] for row in range(2) for column in range(2)):
        raise AssertionError("A mod 6")
    same_tuple = {"Q_L_equals_Q": True, "j_L_inverse_at_beta": "5-beta=beta^-1>0", "tuple_sign_l": 1, "source_conclusion": "nu_p=nu_(Lp) for integer p not congruent to zero mod 6"}

    orbits, signs, transport_records = signed_orbits()
    if len(orbits) != 13 or len(transport_records) != 35:
        raise AssertionError((len(orbits), len(transport_records)))
    self_inverse = [orbit for orbit in orbits if negative(orbit[0]) in orbit]
    inverse_pairs: list[tuple[list[Point], list[Point]]] = []
    seen: set[int] = set()
    for index, orbit in enumerate(orbits):
        if index in seen:
            continue
        inverse_index = next(candidate_index for candidate_index, candidate in enumerate(orbits) if negative(orbit[0]) in candidate)
        if inverse_index != index:
            inverse_pairs.append((orbit, orbits[inverse_index]))
        seen.add(index)
        seen.add(inverse_index)
    if len(self_inverse) != 1 or len(inverse_pairs) != 6:
        raise AssertionError((self_inverse, inverse_pairs))

    first = assignment(orbits, signs, Fraction(1))
    second = assignment(orbits, signs, Fraction(2))
    check_assignment(first)
    check_assignment(second)
    if first[(0, 1)] ** 2 == second[(0, 1)] ** 2:
        raise AssertionError("countermodels do not separate u_(0,1)^2")

    reciprocal_records = []
    for point in sorted(first):
        target, sign = signed_reciprocal(point)
        reciprocal_records.append({"point": list(point), "standard_negative": list(target), "product_sign": sign})
    return {
        "schema": "sic-stark-cycle-188-stabilizer-covariance-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "This exact result derives only the finite standard-representative consequence of cited AFK same-tuple covariance and quasiperiodicity for the canonical d=6 stabilizer, together with the corrected finite reciprocal convention. It neither evaluates the modular cocycle nor proves a q-series continuation, coefficient-to-ray interface, fusion-continuity theorem, or TCC.",
        "primary_source": {"paper": "Appleby--Flammia--Kopp arXiv:2501.03970v2", "source_sha256": "93a9f24403d761e29c019d0ad290d3fd8beba1bbf9d6834010639d3b04306e2d", "relations": ["dfn:GhostOverlaps / eq:ghostoverlapformula", "lem:nupperiodicity", "dfn:MTransformedt", "thm:MTransformNormalizedGhostOverlap"]},
        "canonical_stabilizer": {"Q": "a^2-5ab+b^2", "L": [list(row) for row in L], "A_equals_L_cubed": [list(row) for row in A], "A_mod_6": [list(row) for row in identity], "same_tuple_checks": same_tuple},
        "transport": {"root_of_unity": "xi_6=-exp(pi*i/6), xi_6^6=-1", "formula": "u_reduce(Lp)=xi_6^(-<Lp,reduce(Lp)>) u_p", "all_transport_scalars_are_signs": True, "records": transport_records},
        "corrected_reciprocal": {"formula": "u_p*u_reduce(-p)=(-1)^<q,p>, reduce(-p)=-p+6q", "records": reciprocal_records},
        "orbits": {"nonzero_L_orbit_count": len(orbits), "self_inverse_nonzero_L_orbits": [[list(point) for point in orbit] for orbit in self_inverse], "nonzero_inverse_orbit_pairs": [[[list(point) for point in left], [list(point) for point in right]] for left, right in inverse_pairs]},
        "countermodels": {"first_seed_u_(0,1)": "1", "second_seed_u_(0,1)": "2", "all_values_propagated_by_source_transport_and_corrected_reciprocity": True, "separating_observable": "u_(0,1)^2: 1 versus 4"},
        "summary": {"nonzero_characteristics_checked": 35, "transport_relations_checked": len(transport_records), "corrected_reciprocal_relations_checked": len(reciprocal_records), "nonzero_L_orbits": len(orbits), "self_inverse_nonzero_L_orbits": len(self_inverse), "nonzero_inverse_orbit_pairs": len(inverse_pairs), "free_multiplicative_rank_after_transport": len(inverse_pairs), "countermodels_checked": 2, "stabilizer_covariance_determines_u_01_square": False},
        "gate_outcome": {"same_tuple_stabilizer_transport": "PROVED_REDUCES_16_FREE_INVERSE_PAIRS_TO_6_ORBIT_PAIRS_BUT_DOES_NOT_FIX_U_01_SQUARE", "scope": "finite source covariance and quasiperiodicity only; modular-cocycle evaluation and analytic 2psi2/2phi1 continuation remain missing"},
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
