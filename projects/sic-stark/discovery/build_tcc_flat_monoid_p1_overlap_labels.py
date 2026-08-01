#!/usr/bin/env python3
"""Derive all d=12,f=3 AFK Upsilon labels in the frozen flat monoid."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import time


ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "data" / "tcc-flat-monoid-p1-preregistration-v3-labels.json"
MONOID = ROOT / "discovery" / "tcc-flat-monoid-p1-overlap-adapter-v1.json"
OUT = ROOT / "discovery" / "tcc-flat-monoid-p1-overlap-labels-v1.json"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def stabilizer_action(point: tuple[int, int]) -> tuple[int, int]:
    p1, p2 = point
    # [[0,1],[-1,11]] acts on column characteristics modulo 12.
    return p2 % 12, (-p1 + 11 * p2) % 12


def main() -> None:
    started = time.monotonic()
    prereg = json.loads(PREREG.read_text())
    monoid = json.loads(MONOID.read_text())["case"]
    elements = monoid["elements"]
    locator = {
        tuple(point): index
        for index, orbit in enumerate(elements)
        for point in orbit
    }
    if len(elements) != 50 or len(locator) != 288:
        raise AssertionError("frozen monoid artifact changed")
    if 11 * 11 - 4 != 117:
        raise AssertionError("form discriminant failure")
    if stabilizer_action((0, 1)) != (1, 11):
        raise AssertionError("stabilizer convention failure")
    seen: set[tuple[int, int]] = set()
    orbit_records = []
    point_records = []
    for p1 in range(12):
        for p2 in range(12):
            point = (p1, p2)
            if point in seen:
                continue
            orbit = []
            current = point
            while current not in orbit:
                orbit.append(current)
                current = stabilizer_action(current)
            if current != point:
                raise AssertionError("stabilizer action did not close at start")
            seen.update(orbit)
            labels = []
            for q1, q2 in orbit:
                # beta=-14+theta_3.  A totally-positive lift changes only
                # by 12 O_3, hence has this residue and positive infinity_2 sign.
                residue_sign = ((-q1 - 14 * q2) % 12, q2 % 12, 1)
                labels.append(locator[residue_sign])
                point_records.append(
                    {
                        "p": [q1, q2],
                        "residue_sign": list(residue_sign),
                        "monoid_element": locator[residue_sign],
                    }
                )
            if len(set(labels)) != 1:
                raise AssertionError(("nonconstant Upsilon label", orbit, labels))
            orbit_records.append(
                {
                    "representative": list(point),
                    "orbit": [list(value) for value in orbit],
                    "monoid_element": labels[0],
                }
            )
    point_records.sort(key=lambda row: tuple(row["p"]))
    orbit_records.sort(key=lambda row: tuple(row["representative"]))
    if len(seen) != 144 or len(orbit_records) != 50:
        raise AssertionError("characteristic orbit count failure")
    labels = [row["monoid_element"] for row in orbit_records]
    if sorted(labels) != list(range(50)):
        raise AssertionError("orbit-to-monoid map is not bijective")
    zero = next(row for row in point_records if row["p"] == [0, 0])
    if zero["monoid_element"] != 0:
        raise AssertionError("zero characteristic label changed")
    payload = {
        "schema": "tcc-flat-monoid-p1-overlap-labels-v1",
        "claim_tag": "PROVED_FINITE_LABEL_MAP",
        "scope": (
            "All characteristics for the frozen d=12,f=3 form Q=<1,-11,1>. "
            "No partial-zeta value, packet, support, or TCC claim."
        ),
        "preregistration_sha256": digest(PREREG),
        "monoid_artifact_sha256": digest(MONOID),
        "form": prereg["form"],
        "stabilizer_orbits": orbit_records,
        "characteristic_labels": point_records,
        "checks": {
            "characteristic_count": 144,
            "stabilizer_orbit_count": 50,
            "orbit_to_monoid_bijective": True,
            "zero_characteristic_monoid_element": 0,
        },
        "wall_seconds": round(time.monotonic() - started, 6),
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("TCC_FLAT_MONOID_P1_OVERLAP_LABELS=PASS")
    print("D12_CHARACTERISTIC_ORBITS=50")
    print("D12_LABEL_MAP_BIJECTIVE=1")


if __name__ == "__main__":
    main()
