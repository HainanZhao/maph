#!/usr/bin/env python3
"""Independent replay of Cycle 30 via full gcd strata and signature bytes."""
from __future__ import annotations

from collections import Counter
import csv
import itertools
import json
import math
import multiprocessing
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRIMARY = ROOT / "discovery/out/cycle30-crt-synchronization/result.json"
OUTPUT = ROOT / "discovery/out/cycle30-crt-synchronization/independent-replay.json"


def mask(k: int, q: int, speed: int) -> int:
    return sum(1 << time for time in range(q) if (k + 1) * min(speed * time % q, (-speed * time) % q) < q)


def full_stratum_masks(k: int, q: int, gcds: set[int]) -> list[int]:
    return sorted({mask(k, q, speed) for speed in range(q) if math.gcd(speed, q) in gcds})


def signature_atoms(q: int, masks: list[int]) -> list[list[int]]:
    classes: dict[bytes, list[int]] = {}
    for time in range(q - 1, -1, -1):
        signature = bytes((value >> time) & 1 for value in reversed(masks))
        classes.setdefault(signature, []).append(time)
    return sorted((sorted(points) for points in classes.values()), key=lambda points: points[0])


def base4() -> tuple[int, ...]:
    lines = (ROOT / "discovery/out/cycle8-p199-strata.txt").read_text().splitlines()
    return tuple(map(int, lines[4].split()))


def req(pair: tuple[int, int]) -> dict[int, bool]:
    left, right = pair
    return {coordinate: (coordinate not in (left, right)) for coordinate in range(right + 1)}


def allowed(base: tuple[int, ...]) -> tuple[tuple[int, ...], ...]:
    pairs = list(itertools.combinations(range(13), 2))
    two, seven = req(pairs[1]), req(pairs[0])
    rows = []
    for coordinate, residue in enumerate(base):
        digits = []
        for digit in range(14):
            speed = (residue + 199 * digit) % 14
            if coordinate in two and ((speed % 2 == 0) != two[coordinate]):
                continue
            if coordinate in seven and ((speed % 7 == 0) != seven[coordinate]):
                continue
            digits.append(digit)
        rows.append(tuple(digits))
    return tuple(rows)


def h11() -> dict[str, object]:
    speed_rows = tuple(speed for speed in range(1, 44) if speed % 11)
    gcds = {math.gcd(speed, 44) for speed in speed_rows}
    generators = full_stratum_masks(3, 44, gcds)
    atoms = signature_atoms(44, generators)
    full44, full11 = (1 << 44) - 1, (1 << 11) - 1
    masks44 = [mask(3, 44, speed) for speed in range(44)]
    masks11 = [mask(3, 11, speed) for speed in range(11)]
    raw = quotient = admissible_count = 0
    parity = Counter()
    retained = set()
    for base in itertools.product(range(1, 11), repeat=3):
        improper = masks11[base[0]] | masks11[base[1]] | masks11[base[2]] == full11
        for digits in itertools.product(range(4), repeat=3):
            speeds = tuple(base[index] + 11 * digits[index] for index in range(3))
            union = masks44[speeds[0]] | masks44[speeds[1]] | masks44[speeds[2]]
            direct = union == full44
            atom_result = all(any((masks44[speed] >> points[0]) & 1 for speed in speeds) for points in atoms)
            if direct != atom_result:
                raise AssertionError("independent H11 quotient")
            raw += direct
            quotient += atom_result
            admissible = all(math.gcd(4, *(speed for index, speed in enumerate(speeds) if index != omitted)) == 1 for omitted in range(3))
            if admissible:
                admissible_count += 1
                even = [index for index, speed in enumerate(speeds) if speed % 2 == 0]
                parity["none_even" if not even else f"coordinate_{even[0]}_even"] += 1
            if improper and admissible and direct:
                retained.add(base)
    return {
        "generated_mask_count": len(generators),
        "atom_count": len(atoms),
        "atom_size_counts": {str(size): count for size, count in sorted(Counter(map(len, atoms)).items())},
        "assignments": 64000,
        "raw_full_covers": raw,
        "quotient_full_covers": quotient,
        "gcd_admissible_assignments": admissible_count,
        "parity_signature_counts": dict(sorted(parity.items())),
        "retained_improper_bases": len(retained),
    }


def p199() -> dict[str, object]:
    with (ROOT / "discovery/out/cycle25-quadratic-crt/results.tsv").open(newline="", encoding="utf-8") as handle:
        rows = [row for row in csv.DictReader(handle, delimiter="\t") if (int(row["base_index"]), int(row["leaf_ordinal"]), row["status"]) == (4, 78, "UNRESOLVED")]
    if len(rows) != 1:
        raise AssertionError("independent p199 target")
    base = base4()
    digit_rows = allowed(base)
    speed_rows = tuple(sorted({base[i] + 199 * digit for i in range(13) for digit in digit_rows[i]}))
    gcds = {math.gcd(speed, 2786) for speed in speed_rows}
    generators = full_stratum_masks(13, 2786, gcds)
    atoms = signature_atoms(2786, generators)
    for value in generators:
        for time in range(2786):
            if ((value >> time) & 1) != ((value >> (-time % 2786)) & 1):
                raise AssertionError("negation invariance")
    negation_orbits = {min(time, -time % 2786) for time in range(2786)}
    merged_negation_orbits = [points for points in atoms if len({min(time, -time % 2786) for time in points}) > 1]
    masks = [[mask(13, 2786, base[i] + 199 * digit) for digit in range(14)] for i in range(13)]
    baseline = tuple(row[0] for row in digit_rows)
    controls = {baseline}
    for coordinate, digits in enumerate(digit_rows):
        for digit in digits:
            candidate = list(baseline)
            candidate[coordinate] = digit
            controls.add(tuple(candidate))
    covers = 0
    for digits in controls:
        selected = [masks[i][digit] for i, digit in enumerate(digits)]
        direct = 0
        for value in selected:
            direct |= value
        raw = direct == (1 << 2786) - 1
        quotient = all(any((value >> points[0]) & 1 for value in selected) for points in atoms)
        if raw != quotient:
            raise AssertionError("independent p199 quotient")
        covers += raw
    return {
        "allowed_speed_count": len(speed_rows),
        "gcd_strata": sorted(gcds),
        "generated_mask_count": len(generators),
        "atom_count": len(atoms),
        "atom_size_counts": {str(size): count for size, count in sorted(Counter(map(len, atoms)).items())},
        "negation_orbit_count": len(negation_orbits),
        "beyond_negation_atom_reduction": len(negation_orbits) - len(atoms),
        "merged_negation_orbit_atoms": merged_negation_orbits,
        "control_tuple_count": len(controls),
        "control_full_cover_count": covers,
    }


def main() -> None:
    with multiprocessing.Pool(2) as pool:
        h11_result, p199_result = pool.map(run_case, ("h11", "p199"))
    primary = json.loads(PRIMARY.read_text(encoding="utf-8"))
    if h11_result["atom_count"] != primary["h11"]["algebra"]["atom_count"] or h11_result["generated_mask_count"] != primary["h11"]["algebra"]["generated_mask_count"]:
        raise AssertionError("independent H11 algebra")
    for key in ("raw_full_covers", "quotient_full_covers", "gcd_admissible_assignments", "parity_signature_counts", "retained_improper_bases"):
        if h11_result[key] != primary["h11"][key]:
            raise AssertionError(f"independent H11 {key}")
    for key in ("allowed_speed_count", "control_tuple_count", "control_full_cover_count"):
        if p199_result[key] != primary["p199"][key]:
            raise AssertionError(f"independent p199 {key}")
    for key in ("generated_mask_count", "atom_count", "atom_size_counts"):
        if p199_result[key] != primary["p199"]["algebra"][key]:
            raise AssertionError(f"independent p199 algebra {key}")
    result = {"status": "PASS", "epistemic_status": "OBSERVED", "h11": h11_result, "p199": p199_result}
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUTPUT)
    print(json.dumps({"status": "PASS", "h11_atoms": h11_result["atom_count"], "p199_atoms": p199_result["atom_count"], "beyond_negation_reduction": p199_result["beyond_negation_atom_reduction"]}, sort_keys=True))


def run_case(name: str) -> dict[str, object]:
    return h11() if name == "h11" else p199()


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
