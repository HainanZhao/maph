#!/usr/bin/env python3
"""Independent witness replay for Cycle 38's rooted-span obstruction."""
from __future__ import annotations

import itertools
import json
import math
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_coupled_incidence as coupled
import lrc_pair_choice as direct
import lrc_width_four_stage_a as width4

SOURCE = ROOT / "discovery/out/cycle38-ownership-functional/result.json"
OUTPUT = ROOT / "discovery/out/cycle38-ownership-functional/independent-replay.json"


def main() -> None:
    started = time.monotonic()
    result = json.loads(SOURCE.read_text(encoding="utf-8"))
    c37 = json.loads((ROOT / "artifacts/cycle-37-b037-lrc-degree-two-product-v1.json").read_text(encoding="utf-8"))
    normals = tuple(tuple(map(int, row)) for row in c37["breakthrough"]["local_normals_by_allowed_option_offset"])
    base = coupled.read_bases()[4]
    allowed = tuple(tuple(row) for row in direct.allowed_digits(base, 78))
    coverage = width4.raw_coverage(direct.CNFS[4])
    if [sum(row) for row in normals] != [1] * 13 or coverage.shape != (2786, 13, 14):
        raise AssertionError("frozen interface")
    supports = tuple(tuple((option, weight) for option, weight in enumerate(normal) if weight) for normal in normals)
    support_size = math.prod(len(row) for row in supports)
    assignments = tuple(itertools.product(*supports))
    if len(assignments) != support_size or support_size != int(result["interface"]["nonzero_support_assignments"]):
        raise AssertionError("signed support")

    witnesses = []
    diagonal = []
    for root_row in result["roots"]:
        root = int(root_row["root"])
        witness = root_row["first_nonzero"]
        if witness is None or int(witness["rank"]) != 2:
            raise AssertionError("rank-two root witness")
        points = tuple(map(int, witness["representative_times"]))
        signatures = []
        for point in points:
            signature = sum(1 << offset for offset, digit in enumerate(allowed[root]) if coverage[point, root, digit])
            signatures.append(signature)
        if signatures != list(map(int, witness["signatures"])) or signatures[0] & signatures[1]:
            raise AssertionError("raw blocker signatures")
        if not signatures[0] or not signatures[1]:
            raise AssertionError("rank-two minimality")

        order = tuple(range(root, 13)) + tuple(range(root))
        moment = 0
        for assignment in assignments:
            option_offsets = tuple(row[0] for row in assignment)
            weight = math.prod(row[1] for row in assignment)
            owners = []
            for point in points:
                owner = root
                for coordinate in order:
                    digit = allowed[coordinate][option_offsets[coordinate]]
                    if coverage[point, coordinate, digit]:
                        owner = coordinate
                        break
                owners.append(owner)
            if owners == [root, root]:
                moment += weight
            if len(owners) != 2 or any(not 0 <= owner < 13 for owner in owners):
                raise AssertionError("total ownership")
        if moment != int(witness["moment"]) or moment == 0:
            raise AssertionError("direct root moment")
        diagonal.append(moment)
        witnesses.append({"root": root, "times": list(points), "signatures": signatures, "moment": moment})

    if len(diagonal) != 13 or math.prod(diagonal) == 0:
        raise AssertionError("root-diagonal rank")
    common = math.lcm(*(abs(value) for value in diagonal))
    blocker_row_multipliers = [-common // value for value in diagonal]
    mass_row_multiplier = common
    if any(blocker_row_multipliers[index] * diagonal[index] + mass_row_multiplier != 0 for index in range(13)):
        raise AssertionError("integer left-null certificate")
    if mass_row_multiplier == 0:
        raise AssertionError("nonzero augmented right side")
    replay = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "signed_support_assignments": support_size,
        "root_witnesses": witnesses,
        "root_diagonal_rank": 13,
        "mass_one_span_extension_exists": False,
        "reason": "each independently checked blocker row forces its rooted coefficient to zero, contradicting coefficient sum one",
        "augmented_system_left_null_certificate": {
            "blocker_row_multipliers": blocker_row_multipliers,
            "mass_row_multiplier": mass_row_multiplier,
            "left_product_with_coefficient_matrix": [0] * 13,
            "left_product_with_right_hand_side": mass_row_multiplier,
        },
        "wall_seconds": time.monotonic() - started,
    }
    temporary = OUTPUT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(replay, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(OUTPUT)
    print(json.dumps({"status": "PASS", "roots": len(witnesses), "support": support_size, "wall_seconds": replay["wall_seconds"]}, sort_keys=True))


if __name__ == "__main__":
    main()
