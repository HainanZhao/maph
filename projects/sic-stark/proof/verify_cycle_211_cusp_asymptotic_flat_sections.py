#!/usr/bin/env python3
"""Exact cusp-section and nonselection audit for Cycle 211/B048."""
from __future__ import annotations

import argparse
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


def exponent_extrema() -> dict[str, object]:
    records = [
        {"characteristic": [first, second], "exponent": 4 * second - 5 * first}
        for first in range(DIMENSION)
        for second in range(DIMENSION)
    ]
    maximum = max(record["exponent"] for record in records)
    minimum = min(record["exponent"] for record in records)
    maximum_labels = [record["characteristic"] for record in records if record["exponent"] == maximum]
    minimum_labels = [record["characteristic"] for record in records if record["exponent"] == minimum]
    assert maximum == 20 and maximum_labels == [[0, 5]]
    assert minimum == -25 and minimum_labels == [[5, 0]]
    return {
        "epistemic_status": "PROVED",
        "record_count": len(records),
        "records": records,
        "maximum": {"exponent": maximum, "unique_label": maximum_labels[0]},
        "minimum": {"exponent": minimum, "unique_label": minimum_labels[0]},
    }


def cusp_sections() -> dict[str, object]:
    records = []
    for h in range(DIMENSION):
        infinity = packet_monomial(0, 5, h)
        zero = packet_monomial(5, 0, h)
        assert infinity["t_exponent"] == 20
        assert zero["t_exponent"] == -25
        records.append({
            "h_channel": h,
            "t_to_infinity_normalization": "t^(-20)*P(t)->e_(0,5)",
            "t_to_zero_normalization": f"t^(25)*P(t)->zeta_6^({zero['zeta_6_exponent_mod_6']})*e_(5,0)",
            "infinity_projective_line": "[e_(0,5)]",
            "zero_projective_line": "[e_(5,0)]",
        })
    assert len(records) == DIMENSION
    return {
        "epistemic_status": "PROVED",
        "record_count": len(records),
        "all_h_infinity_line": "[e_(0,5)]",
        "all_h_zero_line": "[e_(5,0)]",
        "records": records,
        "connection_interpretation": "Each line is the projective asymptotic of a horizontal t^(4*b-5*a) packet component.",
    }


def a6_preservation_audit() -> dict[str, object]:
    lines = ((0, 5), (5, 0))
    records = []
    for first, second in lines:
        image = (
            (A6[0][0] * first + A6[0][1] * second) % DIMENSION,
            (A6[1][0] * first + A6[1][1] * second) % DIMENSION,
        )
        assert image == (first, second)
        records.append({
            "line_label": [first, second],
            "A6_image": list(image),
            "multiplier_zeta_48_exponent": afk_phase_exponent_mod_48(first, second),
            "projectively_preserved": True,
        })
    return {
        "epistemic_status": "PROVED",
        "A6_mod_6": [[1, 0], [0, 1]],
        "records": records,
        "all_cusp_lines_projectively_preserved": True,
    }


def nonselection_audit() -> dict[str, object]:
    infinity_line, zero_line = "[e_(0,5)]", "[e_(5,0)]"
    assert infinity_line != zero_line
    return {
        "epistemic_status": "PROVED",
        "cusp_line_set": [infinity_line, zero_line],
        "distinct_projective_lines": True,
        "declared_source_rules": "exponent extrema, all-h packet phases, A6 label action, and diagonal multiplier ledger",
        "rule_outcome": "Both cusp lines are retained and projectively preserved; no declared rule selects one.",
        "selection_status": "OPEN_REQUIRES_ADDITIONAL_SOURCE_ORIENTATION_OR_BOUNDARY_THEOREM",
    }


def run() -> dict[str, object]:
    extrema = exponent_extrema()
    sections = cusp_sections()
    symmetry = a6_preservation_audit()
    nonselection = nonselection_audit()
    assert extrema["record_count"] == 36
    assert sections["record_count"] == 6
    assert symmetry["all_cusp_lines_projectively_preserved"]
    assert nonselection["distinct_projective_lines"]
    return {
        "schema": "sic-stark-cycle-211-cusp-asymptotic-flat-sections-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "The complete source packet has two exact all-h cusp projective sections, [e_(0,5)] and [e_(5,0)], and the declared A6/multiplier data preserve both distinct lines. Thus those declared data do not select a canonical cusp section. This does not rule out an additional source orientation or boundary theorem, non-diagonal boundary theory, C198 comparison, AFK identity, fusion, Stark, or TCC statement.",
        "exponent_extrema": extrema,
        "cusp_sections": sections,
        "a6_preservation_audit": symmetry,
        "nonselection_audit": nonselection,
        "gate_outcome": {
            "source_cusp_sections": "PROVED_TWO_DISTINCT_A6_MULTIPLIER_PRESERVED_LINES",
            "canonical_source_only_cusp_selection": "OPEN_REQUIRES_ADDITIONAL_SOURCE_THEOREM",
            "remaining_design_problem": "Derive a source-authorized orientation/boundary theorem, or test a non-diagonal boundary theory without C198 fitting.",
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    print(text, end="") if args.output is None else args.output.write_text(text, encoding="utf-8")
