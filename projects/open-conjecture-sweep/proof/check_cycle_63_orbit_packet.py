#!/usr/bin/env python3
"""Audit the exact and exploratory boundaries of the C63 packet."""

from __future__ import annotations

import csv
import itertools
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery" / "out" / "cycle63-orbit-minimizer"


def load_json(name: str):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def check_realizability_controls() -> int:
    rows = 0
    for original in itertools.product(range(3), repeat=6):
        e, q1, q2, q3, v1, v2 = map(Fraction, original)
        total = sum(original)
        if total == 0:
            continue
        e /= total
        q1 /= total; q2 /= total; q3 /= total
        v1 /= total; v2 /= total
        t = (q1 + q2 + q3) / 3
        x, y, z = q1 - t, q2 - t, q3 - t
        c = (v1 + v2) / 2
        s2 = ((v1 - v2) / 2) ** 2
        r2 = x*x + y*y + z*z
        u = x*y*z
        assert e + 3*t + 2*c == 1
        assert min(e, t, c, r2, s2) >= 0
        assert r2**3 / 2 - 27*u**2 >= 0
        assert 3*t*t - r2/2 >= 0
        assert t**3 - t*r2/2 + u >= 0
        assert c*c - s2 >= 0
        rows += 1
    return rows


def audit() -> dict[str, object]:
    orbit_summary = load_json("orbit-summary.json")
    orbit_audit = load_json("orbit-audit.json")
    elementary = load_json("elementary-summary.json")
    stationary = load_json("generic-stationary-summary.json")
    modular = load_json("modular-dimension-32003.json")

    assert orbit_summary["invariant_span_reconstruction"] == "PASS"
    assert orbit_summary["orbit_terms"] == 1640
    assert orbit_summary["orbit_weighted_degrees"] == [15]
    assert orbit_audit["status"] == "PASS"
    assert orbit_audit["exact_symmetry_maps_checked"] == 12
    assert orbit_audit["c62_derivative_identities"] == 2
    assert orbit_audit["orientation_coupling_terms"] == 0
    assert elementary["status"] == "PASS"
    assert elementary["terms"] == 1728
    assert elementary["weighted_degrees"] == [15]
    assert elementary["central_substitution"] == "IDENTICALLY_ZERO"
    assert stationary["status"] == "PASS"
    assert list(stationary["equations"]) == sorted(stationary["equations"])
    assert stationary["equations"]["normalization"] == 4
    assert modular["result"] == "WALL_CAP_BEFORE_BASIS"

    probes = []
    for seed in (630631, 630632, 630633):
        probe = load_json(f"schur-probe-{seed}.json")
        assert probe["seed"] == seed
        assert probe["samples"] == 100000
        assert probe["exact_candidates"] == 0
        assert probe["exact_reversal"] is False
        assert probe["minimum_trans_factor"] > 0
        assert probe["minimum_cycle_factor"] > 0
        probes.append(probe)

    with (OUT / "orbit-polynomial.tsv").open(newline="", encoding="utf-8") as handle:
        orbit_rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(orbit_rows) == 1640
    assert all(int(row["w"]) == 0 for row in orbit_rows)

    result = {
        "status": "PASS",
        "exact": {
            "epistemic_status": "PROVED",
            "orbit_terms": 1640,
            "elementary_terms": 1728,
            "enlarged_symmetry_maps": 12,
            "realizability_controls": check_realizability_controls(),
            "stationary_equations": 6,
        },
        "schur_probe": {
            "epistemic_status": "OBSERVED",
            "rows": sum(probe["samples"] for probe in probes),
            "exact_reversals": 0,
        },
        "generic_elimination": {
            "epistemic_status": "OBSERVED",
            "result": "WALL_CAP_BEFORE_BASIS",
            "seconds": 300,
        },
        "claim_boundary": "Exact S3 orbit, realizability, and stationary-equation reduction only; no positivity, zero-dimensionality, Zhao, or Sidorenko conclusion.",
    }
    return result


def main() -> int:
    subprocess.run([sys.executable, str(ROOT / "proof" / "check_cycle63_orbit_polynomial.py")],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    result = audit()
    (OUT / "packet-audit.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
