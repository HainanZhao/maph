#!/usr/bin/env python3
"""Independent data audit for C61's exact flat-stratum computation."""
from __future__ import annotations

import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.check_cycle_61_flat_stratum import (
    FLAT_BASES,
    SIGN,
    STANDARD_AXIS,
    deficit_taylor,
)
from proof.check_cycle_61_transverse import audit as transverse_audit

OUT = ROOT / "discovery/out/cycle61-flat-stratum/flat-stratum-summary.json"
OLD = ROOT / "discovery/out/cycle55-zhao-deficit/polynomials.tsv"


def c55_quartic() -> dict[tuple[tuple[int, int, int], tuple[int, ...]], int]:
    rows: dict[tuple[tuple[int, int, int], tuple[int, ...]], int] = {}
    with OLD.open() as source:
        for row in csv.DictReader(source, delimiter="\t"):
            base = tuple(map(int, row["base"].split(",")))
            direction = tuple(map(int, row["direction"].split(",")))
            if base in FLAT_BASES and direction in (STANDARD_AXIS, SIGN):
                rows[(base, direction)] = int(row["deficit_coefficients"].split(",")[4])
    return rows


def audit() -> dict[str, object]:
    transverse = transverse_audit()
    payload = json.loads(OUT.read_text())
    assert payload["status"] == "PASS" and payload["epistemic_status"] == "PROVED"
    old = c55_quartic()
    assert len(old) == 8
    for base in FLAT_BASES:
        key = "".join(map(str, base))
        actual = payload["bases"][key]
        axis = deficit_taylor(base, STANDARD_AXIS)
        sign = deficit_taylor(base, SIGN)
        assert actual["axis_taylor"] == axis
        assert actual["sign_taylor"] == sign
        assert axis[4] == old[(base, STANDARD_AXIS)]
        assert sign[4] == old[(base, SIGN)]
        coeff = actual["quartic_invariant_coefficients"]
        cert = actual["strict_positivity_certificate"]
        assert coeff["D"] == "0" and all(cert.values())
    return {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "bases": ["".join(map(str, b)) for b in FLAT_BASES],
        "c55_independent_axis_and_sign_checks": 8,
        "transverse_factor_audit": transverse["factors"],
        "claim_boundary": payload["claim_boundary"],
    }


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
