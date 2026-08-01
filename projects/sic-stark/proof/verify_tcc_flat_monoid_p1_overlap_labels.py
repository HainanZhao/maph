#!/usr/bin/env python3
"""Independent audit of the frozen d=12,f=3 AFK characteristic label map."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MONOID = ROOT / "discovery" / "tcc-flat-monoid-p1-overlap-adapter-v1.json"
LABELS = ROOT / "discovery" / "tcc-flat-monoid-p1-overlap-labels-v1.json"


def action(p: tuple[int, int]) -> tuple[int, int]:
    # L=[[0,1],[-1,11]], the positive-trace stabilizer of <1,-11,1>.
    return p[1] % 12, (11 * p[1] - p[0]) % 12


def main() -> None:
    monoid = json.loads(MONOID.read_text())["case"]
    labels = json.loads(LABELS.read_text())
    point_label = {tuple(row["p"]): row for row in labels["characteristic_labels"]}
    if len(point_label) != 144:
        raise AssertionError("characteristic population changed")
    locator = {
        tuple(element): index
        for index, orbit in enumerate(monoid["elements"])
        for element in orbit
    }
    if len(locator) != 288:
        raise AssertionError("monoid residue/sign population changed")
    visited: set[tuple[int, int]] = set()
    orbit_count = 0
    labels_seen: set[int] = set()
    for p1 in range(12):
        for p2 in range(12):
            p = (p1, p2)
            row = point_label[p]
            expected_residue = ((-p1 - 14 * p2) % 12, p2, 1)
            if tuple(row["residue_sign"]) != expected_residue:
                raise AssertionError("residue formula changed")
            if row["monoid_element"] != locator[expected_residue]:
                raise AssertionError("monoid lookup changed")
            if p in visited:
                continue
            orbit_count += 1
            q = p
            orbit_labels = set()
            while q not in visited:
                visited.add(q)
                orbit_labels.add(point_label[q]["monoid_element"])
                q = action(q)
            if q != p or len(orbit_labels) != 1:
                raise AssertionError("stabilizer orbit label failure")
            labels_seen |= orbit_labels
    if len(visited) != 144 or orbit_count != 50 or labels_seen != set(range(50)):
        raise AssertionError("bijection cardinalities changed")
    if point_label[(0, 0)]["monoid_element"] != 0:
        raise AssertionError("zero label changed")
    print("TCC_FLAT_MONOID_P1_OVERLAP_LABELS_AUDIT=PASS")
    print("D12_CHARACTERISTIC_ORBITS=50")
    print("D12_LABEL_MAP_BIJECTIVE=1")


if __name__ == "__main__":
    main()
