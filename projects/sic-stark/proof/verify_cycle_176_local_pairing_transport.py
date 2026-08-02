#!/usr/bin/env python3
"""All-row direct transport induced by the frozen local F3 pairing."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TORSOR = ROOT / "discovery/cycle-166-fibre-torsor-prototype-v1.json"
ANCHORS = {(3, 5): 2, (3, 4): 1}


def build_payload() -> dict[str, object]:
    torsor = json.loads(TORSOR.read_text())
    transport = {
        tuple(row["characteristic"]): (tuple(row["successor"]), row["transport_exponent_mod_6"])
        for row in torsor["multiplier_rows"]
    }
    section = {}
    for orbit in torsor["transport_orbits"]:
        for point, label in zip(orbit["orbit"], orbit["lift_labels"], strict=True):
            section[tuple(point)] = label
    if len(transport) != 36 or len(section) != 36:
        raise AssertionError("sealed all-row torsor data incomplete")
    rows = []
    for point in sorted(section):
        successor, d = transport[point]
        s = section[point]
        local_value = (2 * s) % 3  # B(s, 1)
        local_increment = (2 * d) % 3  # B(d, 1)
        if (local_value + local_increment) % 3 != (2 * section[successor]) % 3:
            raise AssertionError(("local covariance failure", point))
        rows.append({"characteristic": list(point), "successor": list(successor), "section_exponent_mod_6": s, "transport_exponent_mod_6": d, "local_pairing_value_mod_3": local_value, "local_transport_increment_mod_3": local_increment})
    if {point: (2 * section[point]) % 3 for point in ANCHORS} != ANCHORS:
        raise AssertionError("labelled local anchors changed")

    states_checked = 0
    for point in sorted(section):
        for fibre in range(3):
            state = (point, fibre)
            for _ in range(3):
                successor, d = transport[state[0]]
                state = (successor, (state[1] + 2 * d) % 3)
            if state != (point, fibre):
                raise AssertionError(("local third return failure", point, fibre, state))
            states_checked += 1
    return {
        "schema": "sic-stark-cycle-176-local-pairing-transport-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "This exact finite result composes the sealed multiplier-torsor section with the frozen local F3 pairing. It defines no additive coefficient operation, AFK interface, regulator equality, fusion theorem, or TCC identity.",
        "conventions": {"row_map": "F(x)=B(s(x),1)=2s(x) mod 3", "local_transport": "T_loc(x,r)=(Tx,r+2d(x))", "source": "Cycle-166 all-row C6 section and transport", "pairing": "Cycle-175 B(a,b)=2ab mod 3"},
        "summary": {"base_rows_checked": len(rows), "local_states_checked": states_checked, "all_row_covariances": True, "local_third_return": True, "orientation_anchors": {"3,5": 2, "3,4": 1}},
        "rows": rows,
        "gate_outcome": {"direct_local_pairing_transport": "SURVIVES_ALL_ROW_FINITE_TEST", "scope": "finite composition only; no additive coefficient-to-ray operation"},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(build_payload(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
