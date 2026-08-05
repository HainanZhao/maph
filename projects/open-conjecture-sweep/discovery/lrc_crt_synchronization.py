#!/usr/bin/env python3
"""Cycle 30 exact gcd-stratified mask-transport algebra prototype."""
from __future__ import annotations

from collections import Counter, deque
import csv
import itertools
import json
import math
import multiprocessing
import os
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle30-crt-synchronization"
MASK_CAP = 12000
REFINEMENT_CAP = 50_000_000


def bad_mask(k: int, q: int, speed: int) -> int:
    value = 0
    for point in range(q):
        residue = speed * point % q
        if (k + 1) * min(residue, q - residue) < q:
            value |= 1 << point
    return value


def units(q: int) -> tuple[int, ...]:
    return tuple(value for value in range(1, q) if math.gcd(value, q) == 1)


def least_multiplier(canonical: int, speed: int, q: int, unit_rows: tuple[int, ...]) -> int:
    for unit in unit_rows:
        if unit * canonical % q == speed % q:
            return unit
    raise AssertionError("unit associates missing")


def subgroup(q: int, generators: tuple[int, ...]) -> tuple[int, ...]:
    seen = {1}
    queue = deque([1])
    while queue:
        left = queue.popleft()
        for right in generators:
            value = left * right % q
            if value not in seen:
                if math.gcd(value, q) != 1:
                    raise AssertionError("nonunit subgroup element")
                seen.add(value)
                queue.append(value)
    return tuple(sorted(seen))


def transported_mask(mask: int, multiplier: int, q: int) -> int:
    result = 0
    for point in range(q):
        if mask & (1 << (multiplier * point % q)):
            result |= 1 << point
    return result


def stratum_orbit(job: tuple[int, int, int, tuple[int, ...]]) -> dict[str, object]:
    k, q, gcd_value, speed_rows = job
    unit_rows = units(q)
    canonical = min(speed_rows)
    multipliers = tuple(least_multiplier(canonical, speed, q, unit_rows) for speed in speed_rows)
    group = subgroup(q, multipliers)
    canonical_mask = bad_mask(k, q, canonical)
    orbit = {}
    for multiplier in group:
        transported = transported_mask(canonical_mask, multiplier, q)
        direct = bad_mask(k, q, multiplier * canonical % q)
        if transported != direct:
            raise AssertionError("transport equality")
        orbit.setdefault(transported, multiplier)
    for speed, multiplier in zip(speed_rows, multipliers, strict=True):
        if transported_mask(canonical_mask, multiplier, q) != bad_mask(k, q, speed):
            raise AssertionError("allowed speed transport")
    return {
        "gcd": gcd_value,
        "canonical_speed": canonical,
        "allowed_speeds": list(speed_rows),
        "least_multipliers": list(multipliers),
        "generated_subgroup_size": len(group),
        "distinct_orbit_masks": len(orbit),
        "orbit_masks": sorted(orbit),
    }


def transport_algebra(k: int, q: int, speed_rows: tuple[int, ...]) -> tuple[dict[str, object], list[int]]:
    strata = []
    for gcd_value in sorted({math.gcd(speed, q) for speed in speed_rows}):
        rows = tuple(sorted({speed % q for speed in speed_rows if math.gcd(speed, q) == gcd_value}))
        strata.append((k, q, gcd_value, rows))
    with multiprocessing.Pool(min(3, len(strata))) as pool:
        outcomes = pool.map(stratum_orbit, strata, chunksize=1)
    generated = sorted({mask for row in outcomes for mask in row.pop("orbit_masks")})
    if len(generated) > MASK_CAP:
        raise RuntimeError("generated mask cap")
    full = (1 << q) - 1
    atoms = [full]
    checks = 0
    for mask in generated:
        complement = full ^ mask
        refined = []
        for atom in atoms:
            checks += 1
            if checks > REFINEMENT_CAP:
                raise RuntimeError("signature refinement cap")
            inside = atom & mask
            outside = atom & complement
            if inside:
                refined.append(inside)
            if outside:
                refined.append(outside)
        atoms = refined
        if len(atoms) == q:
            break
    atoms.sort(key=lambda atom: (atom & -atom).bit_length() - 1)
    if sum(atom.bit_count() for atom in atoms) != q:
        raise AssertionError("atom partition cardinality")
    union = 0
    for atom in atoms:
        if union & atom:
            raise AssertionError("atom overlap")
        union |= atom
    if union != full:
        raise AssertionError("atom partition coverage")
    for speed in speed_rows:
        mask = bad_mask(k, q, speed)
        rebuilt = 0
        for atom in atoms:
            intersection = atom & mask
            if intersection not in (0, atom):
                raise AssertionError("allowed mask splits atom")
            if intersection:
                rebuilt |= atom
        if rebuilt != mask:
            raise AssertionError("allowed mask atom union")
    return {
        "q": q,
        "gcd_strata": outcomes,
        "generated_mask_count": len(generated),
        "signature_refinements": checks,
        "atom_count": len(atoms),
        "atom_size_counts": {str(size): count for size, count in sorted(Counter(atom.bit_count() for atom in atoms).items())},
        "status": "COMPLETE",
    }, atoms


def atom_cover(atoms: list[int], masks: tuple[int, ...]) -> bool:
    union = 0
    for mask in masks:
        union |= mask
    return all(atom & union == atom for atom in atoms)


def h11_shard(job: tuple[int, int, list[int]]) -> tuple[int, int, int, int, Counter[str]]:
    start, stop, atoms = job
    low = [bad_mask(3, 11, speed) for speed in range(11)]
    high = [bad_mask(3, 44, speed) for speed in range(44)]
    low_full, high_full = (1 << 11) - 1, (1 << 44) - 1
    assignments = raw_covers = quotient_covers = admissible_count = 0
    retained = set()
    parity = Counter()
    bases = list(itertools.product(range(1, 11), repeat=3))
    for base in bases[start:stop]:
        base_union = low[base[0]] | low[base[1]] | low[base[2]]
        for digits in itertools.product(range(4), repeat=3):
            assignments += 1
            speeds = tuple(base[index] + 11 * digits[index] for index in range(3))
            selected = tuple(high[speed] for speed in speeds)
            direct = (selected[0] | selected[1] | selected[2]) == high_full
            quotient = atom_cover(atoms, selected)
            if direct != quotient:
                raise AssertionError("H11 direct/atom quotient")
            raw_covers += direct
            quotient_covers += quotient
            admissible = all(math.gcd(4, *(speed for index, speed in enumerate(speeds) if index != omitted)) == 1 for omitted in range(3))
            even = tuple(index for index, speed in enumerate(speeds) if speed % 2 == 0)
            if admissible != (len(even) <= 1):
                raise AssertionError("H11 parity")
            if admissible:
                admissible_count += 1
                parity["none_even" if not even else f"coordinate_{even[0]}_even"] += 1
            if base_union == low_full and admissible and direct:
                retained.add(base)
    return assignments, raw_covers, quotient_covers, admissible_count, parity | Counter({f"retained::{base}": 1 for base in retained})


def h11() -> dict[str, object]:
    speed_rows = tuple(speed for speed in range(1, 44) if speed % 11)
    algebra, atoms = transport_algebra(3, 44, speed_rows)
    jobs = [(0, 334, atoms), (334, 667, atoms), (667, 1000, atoms)]
    with multiprocessing.Pool(3) as pool:
        rows = pool.map(h11_shard, jobs, chunksize=1)
    parity = Counter()
    retained = set()
    for row in rows:
        for key, value in row[4].items():
            if key.startswith("retained::"):
                retained.add(key)
            else:
                parity[key] += value
    result = {
        "algebra": algebra,
        "lifted_assignments": sum(row[0] for row in rows),
        "raw_full_covers": sum(row[1] for row in rows),
        "quotient_full_covers": sum(row[2] for row in rows),
        "gcd_admissible_assignments": sum(row[3] for row in rows),
        "parity_signature_counts": dict(sorted(parity.items())),
        "retained_improper_bases": len(retained),
    }
    expected = (64000, 720, 720, 32000, 0)
    observed = (result["lifted_assignments"], result["raw_full_covers"], result["quotient_full_covers"], result["gcd_admissible_assignments"], result["retained_improper_bases"])
    if observed != expected or set(parity.values()) != {8000} or len(parity) != 4:
        raise AssertionError(f"H11 frozen counts: {observed}")
    return result


def p199_base() -> tuple[int, ...]:
    rows = [tuple(map(int, line.split())) for line in (ROOT / "discovery/out/cycle8-p199-strata.txt").read_text().splitlines() if line]
    return rows[4]


def pair_requirements(pair: tuple[int, int]) -> dict[int, bool]:
    left, right = pair
    value = {coordinate: True for coordinate in range(left)}
    value[left] = False
    value.update({coordinate: True for coordinate in range(left + 1, right)})
    value[right] = False
    return value


def p199_allowed(base: tuple[int, ...], leaf: int) -> tuple[tuple[int, ...], ...]:
    pairs = [(left, right) for left in range(13) for right in range(left + 1, 13)]
    req2 = pair_requirements(pairs[leaf // 78])
    req7 = pair_requirements(pairs[leaf % 78])
    result = []
    for coordinate in range(13):
        digits = []
        for digit in range(14):
            speed_mod_c = (base[coordinate] + 199 * digit) % 14
            if coordinate in req2 and ((speed_mod_c % 2 == 0) != req2[coordinate]):
                continue
            if coordinate in req7 and ((speed_mod_c % 7 == 0) != req7[coordinate]):
                continue
            digits.append(digit)
        result.append(tuple(digits))
    return tuple(result)


def cnf_masks() -> list[list[int]]:
    path = ROOT / "discovery/out/cycle11-certified-sat/p199/004.cnf"
    lines = [line for line in path.read_text().splitlines() if line and not line.startswith("c")]
    clauses = [tuple(map(int, line.split()[:-1])) for line in lines[1:]]
    time_clauses = clauses[1196:1196 + 2786]
    if len(time_clauses) != 2786:
        raise AssertionError("p199 CNF time clauses")
    result = [[0 for _digit in range(14)] for _coordinate in range(13)]
    for point, clause in enumerate(time_clauses):
        for literal in clause:
            variable = literal - 1
            result[variable // 14][variable % 14] |= 1 << point
    return result


def p199() -> dict[str, object]:
    with (ROOT / "discovery/out/cycle25-quadratic-crt/results.tsv").open(newline="", encoding="utf-8") as handle:
        matches = [row for row in csv.DictReader(handle, delimiter="\t") if (int(row["base_index"]), int(row["leaf_ordinal"]), row["status"]) == (4, 78, "UNRESOLVED")]
    if len(matches) != 1:
        raise AssertionError("p199 target")
    base = p199_base()
    allowed = p199_allowed(base, 78)
    speed_rows = tuple(sorted({base[coordinate] + 199 * digit for coordinate in range(13) for digit in allowed[coordinate]}))
    algebra, atoms = transport_algebra(13, 2786, speed_rows)
    frozen_masks = cnf_masks()
    formula_masks = [[bad_mask(13, 2786, base[coordinate] + 199 * digit) for digit in range(14)] for coordinate in range(13)]
    for coordinate in range(13):
        for digit in allowed[coordinate]:
            if formula_masks[coordinate][digit] != frozen_masks[coordinate][digit]:
                raise AssertionError("p199 formula/CNF mask")
    baseline = tuple(digits[0] for digits in allowed)
    controls = {baseline}
    for coordinate, digits in enumerate(allowed):
        for digit in digits:
            row = list(baseline)
            row[coordinate] = digit
            controls.add(tuple(row))
    if len(controls) > 183:
        raise AssertionError("p199 control tuple cap")
    cover_rows = []
    for digits in sorted(controls):
        selected = tuple(formula_masks[coordinate][digit] for coordinate, digit in enumerate(digits))
        direct_union = 0
        for mask in selected:
            direct_union |= mask
        direct = direct_union == (1 << 2786) - 1
        quotient = atom_cover(atoms, selected)
        if direct != quotient:
            raise AssertionError("p199 direct/atom quotient")
        cover_rows.append({"digits": list(digits), "direct_full_cover": direct, "quotient_full_cover": quotient})
    algebra["strategic_threshold"] = 1393
    algebra["strategic_outcome"] = "ADVANCE" if algebra["atom_count"] <= 1393 else "CONTAINED"
    return {
        "base_index": 4,
        "leaf_ordinal": 78,
        "times": 2786,
        "allowed_digit_counts": [len(row) for row in allowed],
        "allowed_speed_count": len(speed_rows),
        "algebra": algebra,
        "control_tuple_count": len(cover_rows),
        "control_full_cover_count": sum(row["direct_full_cover"] for row in cover_rows),
        "control_rows": cover_rows,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    result = {"epistemic_status": "OBSERVED", "h11": h11(), "p199": p199()}
    result["status"] = "PASS"
    result["wall_seconds"] = time.monotonic() - started
    temporary = OUT / "result.json.tmp"
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUT / "result.json")
    summary = (
        f"status=PASS h11_atoms={result['h11']['algebra']['atom_count']} "
        f"h11_rows={result['h11']['lifted_assignments']} "
        f"p199_atoms={result['p199']['algebra']['atom_count']} "
        f"p199_outcome={result['p199']['algebra']['strategic_outcome']} "
        f"wall_seconds={result['wall_seconds']:.6f}"
    )
    (OUT / "summary.txt").write_text(summary + "\n", encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
