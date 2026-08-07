#!/usr/bin/env python3
"""Exact boundary test for the k=r=4 Conjecture 5.4 reduction.

For every nondecreasing non-divisible quadruple in the requested box, set
``b = 1 + sum(a_i // 4)``, the largest value authorized by the conjectured
inequality.  Check both the direct product differences and the stronger
four-section dominance lemma used by the reduction.  All arithmetic is exact.
"""

from __future__ import annotations

import argparse
import itertools
import json

from goal_qanalog_k4r4_sweep import convolve_interval, multiply_q4_interval


def formal_quotient_prefix(a_coefficients: list[int], through: int) -> list[int]:
    """Return coefficients through ``through`` of A(q)/(1+q+q^2+q^3)."""
    quotient: list[int] = []
    for degree in range(through + 1):
        value = a_coefficients[degree] if degree < len(a_coefficients) else 0
        for offset in range(1, 4):
            if degree >= offset:
                value -= quotient[degree - offset]
        quotient.append(value)
    return quotient


def fail(kind: str, **payload: object) -> None:
    print(json.dumps({"status": "COUNTEREXAMPLE", "kind": kind, **payload}, sort_keys=True))
    raise SystemExit(1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=40)
    args = parser.parse_args()
    if args.limit < 3:
        raise SystemExit("--limit must be at least 3")

    allowed = [value for value in range(1, args.limit + 1) if value % 4]
    quadruples = 0
    boundary_differences = 0
    lemma_dominance_checks = 0
    lemma_positivity_checks = 0
    minimum_boundary: tuple[int, tuple[int, ...], int, int] | None = None
    minimum_dominance: tuple[int, tuple[int, ...], int, int] | None = None
    minimum_positivity: tuple[int, tuple[int, ...], int] | None = None

    for lengths in itertools.combinations_with_replacement(allowed, 4):
        quadruples += 1
        coefficients = [1]
        for length in lengths:
            coefficients = convolve_interval(coefficients, length)
        degree_a = sum(length - 1 for length in lengths)
        residues = [length % 4 for length in lengths]
        residual_degree = sum(residue - 1 for residue in residues)
        b = 1 + sum(length // 4 for length in lengths)
        product = multiply_q4_interval(coefficients, b)
        midpoint = (len(product) - 1) // 2
        lemma_through = degree_a - (residual_degree + 1) // 2
        quotient = formal_quotient_prefix(coefficients, max(midpoint, lemma_through))

        # This is the exact coefficient inequality needed at the largest
        # admissible b.  Independently reconstruct the product and require
        # agreement with the formal quotient identity before checking sign.
        for degree in range(midpoint + 1):
            prior = product[degree - 1] if degree else 0
            direct = product[degree] - prior
            reduced = quotient[degree]
            if degree >= 4 * b:
                reduced -= quotient[degree - 4 * b]
            if direct != reduced:
                fail(
                    "REDUCTION_MISMATCH",
                    a=lengths,
                    b=b,
                    degree=degree,
                    direct=direct,
                    reduced=reduced,
                )
            if direct < 0:
                fail("BOUNDARY_DIFFERENCE", a=lengths, b=b, degree=degree, value=direct)
            boundary_differences += 1
            candidate = (direct, lengths, b, degree)
            if minimum_boundary is None or candidate < minimum_boundary:
                minimum_boundary = candidate

        # Positivity clause of the stronger four-section lemma.
        for degree in range(lemma_through + 1):
            value = quotient[degree]
            if value < 0:
                fail("LEMMA_POSITIVITY", a=lengths, degree=degree, value=value)
            lemma_positivity_checks += 1
            candidate = (value, lengths, degree)
            if minimum_positivity is None or candidate < minimum_positivity:
                minimum_positivity = candidate

        # Dominance clause. For fixed residue and n, the permitted earlier m
        # form a prefix, so one prefix maximum checks every pair in O(D).
        dominance_bound = degree_a - 4
        for residue in range(4):
            indices = list(range(residue, len(quotient), 4))
            prefix_max: list[tuple[int, int]] = []
            best = (-10**100, -1)
            for index in indices:
                if quotient[index] > best[0]:
                    best = (quotient[index], index)
                prefix_max.append(best)
            for position, n in enumerate(indices):
                cutoff = min(n - 4, dominance_bound - n)
                if cutoff < residue:
                    continue
                earlier_position = min(position - 1, (cutoff - residue) // 4)
                if earlier_position < 0:
                    continue
                earlier_value, m = prefix_max[earlier_position]
                gap = quotient[n] - earlier_value
                if gap < 0:
                    fail(
                        "LEMMA_DOMINANCE",
                        a=lengths,
                        m=m,
                        n=n,
                        q_m=earlier_value,
                        q_n=quotient[n],
                    )
                lemma_dominance_checks += earlier_position + 1
                candidate = (gap, lengths, m, n)
                if minimum_dominance is None or candidate < minimum_dominance:
                    minimum_dominance = candidate

    assert minimum_boundary and minimum_dominance and minimum_positivity
    print(json.dumps({
        "boundary_coefficient_differences": boundary_differences,
        "lemma_dominance_pair_checks": lemma_dominance_checks,
        "lemma_positivity_coefficients": lemma_positivity_checks,
        "limit": args.limit,
        "minimum_boundary_difference": {
            "value": minimum_boundary[0],
            "a": minimum_boundary[1],
            "b": minimum_boundary[2],
            "degree": minimum_boundary[3],
        },
        "minimum_lemma_dominance_gap": {
            "value": minimum_dominance[0],
            "a": minimum_dominance[1],
            "m": minimum_dominance[2],
            "n": minimum_dominance[3],
        },
        "minimum_lemma_positivity": {
            "value": minimum_positivity[0],
            "a": minimum_positivity[1],
            "degree": minimum_positivity[2],
        },
        "quadruples": quadruples,
        "status": "NO_COUNTEREXAMPLE",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
