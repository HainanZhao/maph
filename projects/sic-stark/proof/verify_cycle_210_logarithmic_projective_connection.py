#!/usr/bin/env python3
"""Exact logarithmic projective-connection audit for Cycle 210/B047."""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
for path in (PROJECT_ROOT, PROJECT_ROOT / "scripts"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from proof.verify_cycle_206_projective_line_interface import packet_monomial
from dimension_six_stabilizer_ledger import A6, afk_phase_exponent_mod_48


DIMENSION = 6
BASEPOINTS = (Fraction(2), Fraction(3))


def exponent_connection() -> dict[str, object]:
    records = []
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            exponents = {packet_monomial(first, second, h)["t_exponent"] for h in range(DIMENSION)}
            assert exponents == {4 * second - 5 * first}
            exponent = exponents.pop()
            records.append({
                "characteristic": [first, second],
                "exponent": exponent,
                "connection_component": f"d-{exponent}*dlog(t)",
                "parallel_transport": f"(t1/t0)^({exponent})",
            })
    assert len(records) == DIMENSION * DIMENSION
    return {
        "epistemic_status": "PROVED",
        "connection": "nabla=d-diag(4*b-5*a)*dlog(t)",
        "source_domain_components": "0<t<1 and t>1",
        "channel_independent": True,
        "record_count": len(records),
        "records": records,
    }


def a6_multiplier_commutation() -> dict[str, object]:
    records = []
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            image = (
                (A6[0][0] * first + A6[0][1] * second) % DIMENSION,
                (A6[1][0] * first + A6[1][1] * second) % DIMENSION,
            )
            assert image == (first, second)
            exponent = 4 * second - 5 * first
            records.append({
                "characteristic": [first, second],
                "A6_image": list(image),
                "connection_exponent": exponent,
                "multiplier_zeta_48_exponent": afk_phase_exponent_mod_48(first, second),
                "commutation_reason": "Both A6 multiplier and exponent transport are diagonal at this fixed label.",
                "commutes": True,
            })
    assert len(records) == DIMENSION * DIMENSION
    assert all(record["commutes"] for record in records)
    return {
        "epistemic_status": "PROVED",
        "A6_mod_6": [[1, 0], [0, 1]],
        "record_count": len(records),
        "all_commute": True,
        "scope": "This is source transport covariance only, not a C198 or AFK amplitude identity.",
        "records": records,
    }


def basepoint_change_obstruction() -> dict[str, object]:
    t0, u0 = BASEPOINTS
    assert t0 > 1 and u0 > 1 and t0 != u0
    ratio = u0 / t0
    base_exponent, shifted_exponent = 0, 4
    base_entry = ratio**base_exponent
    shifted_entry = ratio**shifted_exponent
    assert base_entry == 1
    assert shifted_entry == Fraction(81, 16)
    assert base_entry != shifted_entry
    return {
        "epistemic_status": "PROVED",
        "same_component_basepoints": {"t0": str(t0), "u0": str(u0), "component": "t>1"},
        "basepoint_change": "diag((u0/t0)^(4*b-5*a))",
        "labels": {"base": [0, 0], "shifted": [0, 1]},
        "entries": {"base": str(base_entry), "shifted": str(shifted_entry)},
        "projectively_scalar": False,
        "conclusion": "The exponent-forced transport has no basepoint-free canonical projective normalization from its source data alone.",
    }


def run() -> dict[str, object]:
    connection = exponent_connection()
    symmetry = a6_multiplier_commutation()
    obstruction = basepoint_change_obstruction()
    assert connection["record_count"] == 36
    assert symmetry["all_commute"]
    assert not obstruction["projectively_scalar"]
    return {
        "schema": "sic-stark-cycle-210-logarithmic-projective-connection-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "The Cycle-206 exponents force the stated diagonal logarithmic projective connection; its relative transport commutes with the all-label A6/multiplier action, but its basepoint change is not projectively scalar. This proves no basepoint-free canonical source-to-C198 comparison from these data alone. It does not exclude a separately source-authorized base datum, non-diagonal connection, target-side theorem, AFK identity, fusion, Stark, or TCC statement.",
        "exponent_connection": connection,
        "a6_multiplier_commutation": symmetry,
        "basepoint_change_obstruction": obstruction,
        "gate_outcome": {
            "source_logarithmic_projective_connection": "PROVED_A6_MULTIPLIER_COMPATIBLE",
            "basepoint_free_c198_comparison": "OBSTRUCTED_FOR_DECLARED_SOURCE_ONLY_NORMALIZATION",
            "remaining_design_problem": "Derive a separately source-authorized canonical base datum or test a non-diagonal connection without target fitting.",
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    print(text, end="") if args.output is None else args.output.write_text(text, encoding="utf-8")
