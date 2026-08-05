#!/usr/bin/env python3
"""Verify the two exact C68 chord no-go witnesses against the source orbit polynomial."""

from __future__ import annotations

import argparse
import csv
import json
from fractions import Fraction
from pathlib import Path


def load_orbit(path: Path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def orbit_value(rows, e, t, c, r2, u, s2):
    total = Fraction()
    for row in rows:
        coefficient = Fraction(int(row["numerator"]), int(row["denominator"]))
        total += (
            coefficient
            * e ** int(row["e"]) * t ** int(row["t"]) * c ** int(row["c"])
            * r2 ** int(row["r2"]) * u ** int(row["u"]) * s2 ** int(row["s2"])
        )
    return total


def polynomial_value(path: Path, point):
    total = Fraction()
    with path.open(newline="") as handle:
        rows = csv.reader(handle, delimiter="\t")
        next(rows)
        for row in rows:
            exponent = tuple(map(int, row[:5]))
            coefficient = Fraction(int(row[5]), int(row[6]))
            term = coefficient
            for value, power in zip(point, exponent, strict=True):
                term *= value**power
            total += term
    return total


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("orbit", type=Path)
    parser.add_argument("probe", type=Path)
    parser.add_argument("chord_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    rows = load_orbit(args.orbit)
    probe = json.loads(args.probe.read_text())
    checked = {}
    for regime in ("low", "high"):
        point = tuple(Fraction(value) for value in probe["charts"][regime]["rational_point"])
        x, y, z, v, lam = point
        Z = z / 2 if regime == "low" else (1 + z) / 2
        e = x
        t = (1 - x) * y / 3
        c = (1 - x) * (1 - y) / 2
        r2 = 6 * t**2 * Z**2
        s2 = c**2 * v
        u_plus = 2 * t**3 * Z**3
        u_minus = -u_plus if regime == "low" else t**3 * (3 * Z**2 - 1)
        u_value = (1 - lam) * u_minus + lam * u_plus
        p_minus = orbit_value(rows, e, t, c, r2, u_minus, s2)
        p_value = orbit_value(rows, e, t, c, r2, u_value, s2)
        p_plus = orbit_value(rows, e, t, c, r2, u_plus, s2)
        chord = (1 - lam) * p_minus + lam * p_plus
        difference = p_value - chord
        remainder = polynomial_value(args.chord_dir / f"chord-{regime}.tsv", point)
        assert difference == lam * (1 - lam) * remainder
        assert p_minus > 0 and p_value > 0 and p_plus > 0 and chord > 0
        assert difference < 0 and remainder < 0
        checked[regime] = {
            "endpoint_minus_sign": 1,
            "interior_sign": 1,
            "endpoint_plus_sign": 1,
            "chord_sign": 1,
            "difference_sign": -1,
            "remainder_sign": -1,
            "floating_values": {
                "endpoint_minus": float(p_minus),
                "interior": float(p_value),
                "endpoint_plus": float(p_plus),
                "chord": float(chord),
                "remainder": float(remainder),
            },
            "exact_remainder": {
                "numerator": remainder.numerator,
                "denominator": remainder.denominator,
            },
        }
    payload = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "charts": checked,
        "conclusion": "Global u-chord dominance is false in both endpoint regimes.",
        "claim_boundary": "The witnesses have positive deficit and refute only concavity/chord certificate families, not fixed-S3 comparison.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
