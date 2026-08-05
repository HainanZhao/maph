#!/usr/bin/env python3
"""Controls for Cycle 50's actual-mask coupled-discharge selector."""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import itertools
import json
from pathlib import Path

from lrc_cube_rewrite import normalized_cube, pair_marginals
from lrc_deletion_aware_packet import admissible_triple_packet, contract
from lrc_relative_diagonal import PAIRS, cell_allowed

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle50-deletion-aware-packet"
C49 = ROOT / "discovery/out/cycle49-relative-diagonal"


def parse(rows):
    return {tuple(cell): Fraction(num, den) for cell, num, den in rows}


def exhaustive_controls():
    checks = 0
    for size in (5, 6):
        owners = tuple(range(size))
        for w in owners:
            supports = (owners, owners, owners)
            options = tuple(owner for owner in owners if owner != w)
            for alternatives in itertools.product(options, repeat=3):
                cube = normalized_cube((w, w, w), alternatives)
                for flags in itertools.product((0, 1), repeat=4):
                    pair_deleted = {pair: (1 << w if flags[index] else 0) for index, pair in enumerate(PAIRS)}
                    triple_deleted = 1 << w if flags[3] else 0
                    state = defaultdict(Fraction, cube)
                    selected = admissible_triple_packet(state, (w, w, w), supports, pair_deleted, triple_deleted)
                    # The candidate itself is a zero-marginal coupled defect and must discharge.
                    assert selected is not None
                    chosen, selected_cube = selected
                    scale = state[(w, w, w)] / selected_cube[(w, w, w)]
                    for cell, value in selected_cube.items():
                        assert cell_allowed(cell, pair_deleted, triple_deleted) or state[cell] - scale * value == 0
                    assert all(not values for values in pair_marginals(selected_cube).values())
                    checks += 1
    return checks


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    exhaustive = exhaustive_controls()
    full = json.loads((C49 / "full-audit.json").read_text())
    first = full["first_failure"]
    inventory = json.loads((C49 / "inventory.json").read_text())
    rows = {row["index"]: row for row in inventory["types"]}
    supports = tuple(tuple(owner for owner in range(13) if rows[value]["support_mask"] & (1 << owner)) for value in first["types"])
    pair_deleted = {(left, right): deleted for left, right, deleted in first["pair_deleted"]}
    source = parse(first["mobius"])
    positive = contract(source, supports, pair_deleted, first["triple_deleted"])
    assert positive["status"] == "CONTRACTED"
    triple_steps = [step for step in positive["steps"] if step[0] == "TRIPLE_DELETION_AWARE"]
    assert triple_steps and triple_steps[0][2] == (10, 10, 12)
    assert all(not cell_allowed(cell, pair_deleted, first["triple_deleted"]) for cell in ((9, 9, 9), (9, 10, 9), (10, 9, 9)))

    negative_supports = ((0,), (0,), (0, 1))
    negative = {(0, 0, 0): Fraction(1), (0, 0, 1): Fraction(-1)}
    negative_deleted = {(0, 1): 1, (0, 2): 0, (1, 2): 0}
    blocked = contract(negative, negative_supports, negative_deleted, 0)
    assert blocked["status"] == "NO_ADMISSIBLE_PACKET"

    result = {
        "status": "PASS", "epistemic_status": "PROVED", "stage": "DELETION_AWARE_PACKET_CONTROLS",
        "exhaustive_actual_mask_checks": exhaustive,
        "repeated_alternative_positive": {"types": first["types"], "alternatives": list(triple_steps[0][2]), "status": positive["status"]},
        "negative_no_admissible_packet": {"status": blocked["status"], "supports": [list(values) for values in negative_supports]},
        "claim_boundary": "Controls prove only the selector algebra and declared positive/negative states; they do not classify the full p199 domain.",
    }
    (OUT / "controls.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
