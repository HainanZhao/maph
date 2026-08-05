#!/usr/bin/env python3
"""Exact certificate for Cycle 41's first canonical chain-filling failure."""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import itertools
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_ownership_functional as c38
import lrc_signed_ownership_moments as c40
from lrc_multiplied_fill_probe import oriented_transport

OUT = ROOT / "discovery/out/cycle41-multiplied-ideal/first-exact-obstruction.json"
TYPES = (4, 64, 73)


def eliminate(rows, rhs):
    basis = {}
    for source, (coefficients, value) in enumerate(zip(rows, rhs)):
        row = {index: Fraction(coefficient) for index, coefficient in coefficients.items() if coefficient}
        target = Fraction(value)
        combination = {source: Fraction(1)}
        while row:
            pivot = min(row)
            if pivot not in basis:
                scale = row[pivot]
                row = {index: coefficient / scale for index, coefficient in row.items()}
                target /= scale
                combination = {index: coefficient / scale for index, coefficient in combination.items()}
                basis[pivot] = (row, target, combination)
                break
            base_row, base_target, base_combination = basis[pivot]
            factor = row[pivot]
            for index, coefficient in base_row.items():
                row[index] = row.get(index, Fraction(0)) - factor * coefficient
                if not row[index]:
                    del row[index]
            target -= factor * base_target
            for index, coefficient in base_combination.items():
                combination[index] = combination.get(index, Fraction(0)) - factor * coefficient
                if not combination[index]:
                    del combination[index]
        else:
            if target:
                return basis, combination, target
    return basis, None, Fraction(0)


def primitive_integers(values):
    denominator = math.lcm(*(value.denominator for value in values))
    integers = [value.numerator * (denominator // value.denominator) for value in values]
    divisor = math.gcd(*(abs(value) for value in integers if value))
    integers = [value // divisor for value in integers]
    if next(value for value in integers if value) < 0:
        integers = [-value for value in integers]
    return integers


def main():
    c38.prepare()
    complete_types = sorted({row[0] for root in c38._TYPE_ROWS for rows in root.values() for row in rows})
    type_id = {value: index for index, value in enumerate(complete_types)}
    masks = [sum(1 << coordinate for coordinate, signature in enumerate(value) if signature) for value in complete_types]
    c40._TYPE_ID = type_id
    c40._TYPE_MASKS = masks
    prior = json.loads((ROOT / "discovery/out/cycle40-signed-moments/result.json").read_text(encoding="utf-8"))
    marginals = [{int(owner): Fraction(int(numerator), int(denominator)) for owner, numerator, denominator in values} for values in prior["singleton_marginals_by_complete_type"]]
    original = defaultdict(int)
    combined = defaultdict(int)
    for coordinate in range(13):
        result = c40.coordinate_classes(coordinate)
        for pair in result["rank_two_pairs"]:
            original[tuple(pair)] |= 1 << coordinate
            combined[tuple(pair)] |= 1 << coordinate
        for pair in result["induced_pair_deletions"]:
            combined[tuple(pair)] |= 1 << coordinate

    s, t, u = TYPES
    pair_types = ((s, t), (s, u), (t, u))
    pair_moments = [oriented_transport(left, right, combined, marginals, masks) for left, right in pair_types]
    row_keys = []
    rhs = []
    for pair_index, (left, right) in enumerate(pair_types):
        for i in range(13):
            if not masks[left] & (1 << i):
                continue
            for j in range(13):
                if masks[right] & (1 << j):
                    row_keys.append((pair_index, i, j))
                    rhs.append(pair_moments[pair_index].get((i, j), Fraction(0)))
    row_id = {key: index for index, key in enumerate(row_keys)}
    rows = [dict() for _ in row_keys]
    cells = []
    deleted = [original.get(tuple(sorted(pair)), 0) for pair in pair_types]
    for i, j, k in itertools.product(range(13), repeat=3):
        if not (masks[s] & (1 << i) and masks[t] & (1 << j) and masks[u] & (1 << k)):
            continue
        if (i == j and deleted[0] & (1 << i)) or (i == k and deleted[1] & (1 << i)) or (j == k and deleted[2] & (1 << j)):
            continue
        column = len(cells)
        cells.append((i, j, k))
        for key in ((0, i, j), (1, i, k), (2, j, k)):
            rows[row_id[key]][column] = 1

    basis, combination, contradiction = eliminate(rows, rhs)
    if combination is None:
        raise AssertionError("interface unexpectedly fillable")
    full_basis, _unused_combination, _unused_target = eliminate(rows, [Fraction(0)] * len(rows))
    indices = sorted(combination)
    integer_values = primitive_integers([combination[index] for index in indices])
    certificate = dict(zip(indices, integer_values))
    for column in range(len(cells)):
        if sum(certificate.get(row, 0) * rows[row].get(column, 0) for row in range(len(rows))):
            raise AssertionError("certificate does not annihilate a cell")
    right_side = sum(Fraction(certificate.get(row, 0)) * rhs[row] for row in range(len(rows)))
    if not right_side:
        raise AssertionError("zero certificate right side")
    payload = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "outcome": "CANONICAL_CYCLE40_PAIR_TRANSPORT_NOT_FILLABLE",
        "types": list(TYPES),
        "owner_masks": [masks[index] for index in TYPES],
        "original_deleted_diagonals": deleted,
        "combined_pair_deleted_diagonals": [combined.get(tuple(sorted(pair)), 0) for pair in pair_types],
        "pair_equations": len(rows),
        "allowed_triple_cells": len(cells),
        "matrix_rank": len(full_basis),
        "certificate_nonzero_rows": len(certificate),
        "certificate_maximum_coefficient_bits": max(abs(value).bit_length() for value in certificate.values()),
        "certificate_right_side": [right_side.numerator, right_side.denominator],
        "certificate": [{"pair": list(pair_types[row_keys[index][0]]), "owners": list(row_keys[index][1:]), "coefficient": coefficient} for index, coefficient in sorted(certificate.items())],
        "claim_boundary": "This exact left-null certificate refutes only the canonical Cycle 40 pair-transport filling on one type triple. Pair transports are variables in the general Cycle 41 system, so general degree-three infeasibility is not proved.",
    }
    temporary = OUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT)
    print(json.dumps({key: payload[key] for key in ("status", "outcome", "pair_equations", "allowed_triple_cells", "matrix_rank", "certificate_nonzero_rows", "certificate_right_side")}, sort_keys=True))


if __name__ == "__main__":
    main()
