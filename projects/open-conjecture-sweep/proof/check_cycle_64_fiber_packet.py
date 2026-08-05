#!/usr/bin/env python3
"""Audit C64's exact uniform fiber-resultant reduction."""

from __future__ import annotations

import csv
import itertools
import json
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery" / "out" / "cycle64-fiber-minimization"


def load(name: str):
    return json.loads((OUT / name).read_text(encoding="utf-8"))


def direct_projection_controls() -> int:
    checked = 0
    for original in itertools.product(range(3), repeat=6):
        if sum(original) == 0:
            continue
        total = Fraction(sum(original))
        e, q1, q2, q3, v1, v2 = (Fraction(value, total) for value in original)
        t = (q1 + q2 + q3) / 3
        c = (v1 + v2) / 2
        x, y, z = q1 - t, q2 - t, q3 - t
        r2 = x*x + y*y + z*z
        u = x*y*z
        s2 = ((v1-v2)/2) ** 2
        assert e + 3*t + 2*c == 1
        assert 0 <= r2 <= 6*t*t
        assert 0 <= s2 <= c*c
        assert 54*u*u <= r2**3
        assert u >= t*r2/2 - t**3
        checked += 1
    return checked


def audit() -> dict[str, object]:
    anchors = [load(f"anchor-a{index}.json") for index in (1, 2, 3)]
    for index, anchor in enumerate(anchors, 1):
        assert anchor["status"] == "PASS"
        assert anchor["anchor"] == f"a{index}"
        assert anchor["derivatives"]["gcd_is_unit"] is True
        assert anchor["resultant"]["degree_u"] == 26
        assert anchor["resultant"]["terms"] == 27
        assert anchor["resultant"]["feasible_u_root_intervals"] == 0
        assert all(interval["outside_feasible_u_interval"]
                   for interval in anchor["resultant"]["isolating_intervals"])
        with (OUT / f"anchor-a{index}-resultant.tsv").open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        assert [int(row["u_exponent"]) for row in rows] == list(range(27))
    assert anchors[0]["fiber_polynomial"]["preserves_global_degrees"] is False
    assert anchors[1]["fiber_polynomial"]["preserves_global_degrees"] is False
    assert anchors[2]["fiber_polynomial"]["preserves_global_degrees"] is True

    leading = load("resultant-leading-coefficient.json")
    bound = load("resultant-bound.json")
    assert leading["status"] == "PASS"
    assert leading["maximum_u_degree"] == 26
    assert leading["maximum_weight_matchings"] == 27
    assert leading["top_coefficient_terms"] == 1
    assert leading["top_coefficient_monomials"] == [{
        "coefficient": "-152066696928339427279920998154715326750000000000",
        "exponents": [0, 0, 0, 0],
    }]
    assert leading["degree_drop_anchor_scale_check"] == 270
    assert bound["status"] == "PASS"
    assert bound["generic_resultant_u_degree_upper_bound"] == 26
    assert bound["exceptional_locus"].startswith("EMPTY")

    boundaries = [load(f"boundary-{name}.json")
                  for name in ("t_zero", "c_zero", "r_zero", "r_max")]
    assert all(row["status"] == "PASS" for row in boundaries)
    assert all(row["positive_coefficients"] and row["negative_coefficients"] for row in boundaries)

    return {
        "status": "PASS",
        "exact_reduction": {
            "epistemic_status": "PROVED",
            "projection_controls": direct_projection_controls(),
            "sylvester_size": 12,
            "resultant_u_degree": 26,
            "top_coefficient_nonzero_constant": True,
            "maximum_projected_u_values": 26,
            "maximum_isolated_pairs": 156,
            "anchor_fibers_without_interior_critical_u": 3,
        },
        "boundary_factorizations": {
            "epistemic_status": "OBSERVED",
            "named_outer_boundaries": 4,
            "all_mixed_coefficients": True,
        },
        "claim_boundary": "Uniform finite-per-fiber classification of S3 minima; branches still vary over a three-dimensional outer continuum, and no sign, S3 Zhao, universal Zhao, or Sidorenko conclusion follows.",
    }


def main() -> int:
    result = audit()
    (OUT / "packet-audit.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
