#!/usr/bin/env python3
"""Audit the logical and chart coverage of the C68 secant certificate."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import sympy


PRIMARY = {
    f"{regime}-{side}-{dominant}-dominant"
    for regime in ("low", "high")
    for side in ("below", "above")
    for dominant in ("distance", "second_scale", "cycle")
}
SECONDARY = {
    f"tangent-{side}-{dominant}-dominant"
    for side in ("below", "above")
    for dominant in ("ratio_distance", "primary_rho", "cycle_relative")
}
PRIMARY_SECONDARY_SOURCE = "high-below-second_scale-dominant"
PRIMARY_SUBDIVIDED = "high-below-cycle-dominant"


def read(path: Path) -> dict:
    return json.loads(path.read_text())


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("c67_artifact", type=Path)
    parser.add_argument("source_polynomial", type=Path)
    parser.add_argument("secant_summary", type=Path)
    parser.add_argument("factor_report", type=Path)
    parser.add_argument("primary_blowup", type=Path)
    parser.add_argument("primary_root", type=Path)
    parser.add_argument("primary_subdivision", type=Path)
    parser.add_argument("secondary_blowup", type=Path)
    parser.add_argument("secondary_root", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    c67 = read(args.c67_artifact)
    require(c67["status"] == "SEALED" and c67["epistemic_status"] == "PROVED", "C67 not proved")
    require(c67["audit"]["endpoint_families"] == 4, "C67 endpoint coverage changed")
    require("cycle_equal.tsv" in c67["audit"]["evidence_hashes"], "C67 cycle-equal evidence missing")

    degrees = set()
    with args.source_polynomial.open(newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            degrees.add(sum(int(row[name]) for name in ("a0", "a1", "a2", "a5", "a3", "a4")))
    require(degrees == {15}, "direct source is not homogeneous of degree 15")

    secant = read(args.secant_summary)
    require(secant["coefficientwise_identity"] == "P=P|s2=0+s2*G", "secant identity missing")
    require(secant["status"] == "PASS" and secant["epistemic_status"] == "PROVED", "secant failed")

    factors = read(args.factor_report)
    require(set(factors["charts"]) == {"secant-low", "secant-high"}, "factor charts changed")
    for chart in factors["charts"].values():
        require(chart["factors"] == {"1-x": 1}, "unexpected removed secant factor")

    primary = read(args.primary_blowup)
    require(set(primary["charts"]) == PRIMARY, "primary chart set is not exhaustive")
    for chart in primary["charts"].values():
        require(chart["removed_radial_factor"] == "rho^1", "unexpected primary radial order")
        if chart["source_regime"] == "low":
            require(chart["clearing_factor"] == "(3-y)^12", "low clearing factor changed")
        else:
            require(chart["clearing_factor"] == "3^12", "high clearing factor changed")

    primary_root = read(args.primary_root)
    require(set(primary_root["charts"]) == PRIMARY, "root sign chart set changed")
    root_open = {name for name, chart in primary_root["charts"].items() if not chart["complete"]}
    require(root_open == {PRIMARY_SUBDIVIDED, PRIMARY_SECONDARY_SOURCE}, "unexpected root residual")
    primary_subdivision = read(args.primary_subdivision)
    require(primary_subdivision["charts"][PRIMARY_SUBDIVIDED]["complete"] is True, "subdivision chart open")

    secondary = read(args.secondary_blowup)
    require(set(secondary["charts"]) == SECONDARY, "secondary chart set is not exhaustive")
    require(secondary["source_chart"] == PRIMARY_SECONDARY_SOURCE + ".tsv", "secondary source mismatch")
    for chart in secondary["charts"].values():
        require(chart["removed_radial_factor"] == "eta^1", "unexpected secondary radial order")
        require(chart["clearing_factor"] == "3^12", "secondary clearing factor changed")
    secondary_root = read(args.secondary_root)
    require(set(secondary_root["charts"]) == SECONDARY, "secondary sign chart set changed")
    require(secondary_root["complete_cover"] is True, "secondary sign cover incomplete")

    # Exact side identities and endpoint coverage.
    x, y, s = sympy.symbols("x y s", real=True)
    q = 1 - y - 3 * x + x * y
    low_below = (1 - y) * (1 - s) / (3 - y)
    low_above = (1 - y + 2 * s) / (3 - y)
    require(sympy.simplify(q.subs(x, low_below) - s * (1 - y)) == 0, "low below q identity failed")
    require(sympy.simplify(q.subs(x, low_above) + 2 * s) == 0, "low above q identity failed")
    require(sympy.simplify(low_below.subs(s, 0) - low_above.subs(s, 0)) == 0, "q=0 omitted")
    require(sympy.simplify(low_below.subs(s, 1)) == 0, "low below endpoint failed")
    require(sympy.simplify(low_above.subs(s, 1)) == 1, "low above endpoint failed")
    high_below = (1 - s) / 3
    high_above = (1 + 2 * s) / 3
    require(high_below.subs(s, 0) == high_above.subs(s, 0) == sympy.Rational(1, 3), "x=1/3 omitted")
    require(high_below.subs(s, 1) == 0 and high_above.subs(s, 1) == 1, "high endpoints failed")
    tangent_below = 2 * (1 - s) / 3
    tangent_above = (2 + s) / 3
    require(tangent_below.subs(s, 0) == tangent_above.subs(s, 0) == sympy.Rational(2, 3), "a=2/3 omitted")
    require(tangent_below.subs(s, 1) == 0 and tangent_above.subs(s, 1) == 1, "tangent endpoints failed")

    payload = {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "direct_source_homogeneous_degree": 15,
        "boundary_bridge": {
            "identity": "P=P0+s2*G",
            "P0_coverage": "s2=0 iff the two cycle values agree; this is the complete C67 cycle_equal family",
            "secant_factor": "G=(1-x)*H",
            "x_equals_one": "c=s2=0 and the exact factor gives G=0",
        },
        "cube_coverage": {
            "normalization": "x=e, 3t=(1-x)y, 2c=(1-x)(1-y)",
            "transposition_radius": "0<=r2<=6t^2 gives Z in [0,1], split at Z=1/2",
            "u_fiber": "lambda interpolates the exact C64 lower and upper endpoints",
            "cycle_radius": "s2=c^2*v with v in [0,1]",
        },
        "primary_side_identities": {
            "low_below": "q=(1-y)*s",
            "low_above": "q=-2*s",
            "high_below_range": "x in [0,1/3]",
            "high_above_range": "x in [1/3,1]",
            "low_denominator_range": "3-y in [2,3]",
        },
        "dominant_scale_lemma": {
            "statement": "For every nonzero triple in [0,1]^3, choose rho=max; the two remaining ratios lie in [0,1]. The zero triple is the removed radial-factor origin.",
            "primary_applications": 12,
            "secondary_applications": 6,
        },
        "terminal_sign_charts": 18,
        "claim_boundary": "Logical coverage and dependency audit; coefficient construction and Bernstein arithmetic are checked by their separate replays.",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
