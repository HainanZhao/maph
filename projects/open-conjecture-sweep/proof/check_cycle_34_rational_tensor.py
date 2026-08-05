#!/usr/bin/env python3
"""Audit Cycle 34's exact rational degree-zero obstruction."""
from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle34-rational-tensor"
ASSIGNMENT_HASH = "de06f7bea5bf1673f5a31d2febcac3e130fd67f5bf1ed6112e237b76a0cf5f84"


def audit() -> dict[str, object]:
    primary = json.loads((OUT / "result.json").read_text(encoding="utf-8"))
    independent = json.loads((OUT / "independent-replay.json").read_text(encoding="utf-8"))
    assert primary["status"] == independent["status"] == "PASS"
    assert primary["assignment_hash"] == independent["assignment_hash"] == ASSIGNMENT_HASH
    assert (primary["assignments"], primary["predicate_columns"]) == (4243, 1394)
    skeleton = primary["gf5_skeleton"]
    assert (skeleton["rank"], skeleton["contradiction_size"], skeleton["contradiction_row"]) == (1228, 985, 1228)
    assert len(skeleton["basis_rows"]) == len(set(skeleton["basis_rows"])) == 1228
    assert len(skeleton["pivot_columns"]) == len(set(skeleton["pivot_columns"])) == 1228
    assert primary["exact_solves"] == 1 and primary["augmentations"] == []

    outcome = primary["outcome"]
    assert outcome["status"] == "PROVED_RATIONAL_INCONSISTENCY"
    assert (outcome["target_row"], outcome["basis_rank"], outcome["height_bits"]) == (1228, 1228, 2807)
    terms = outcome["certificate_terms"]
    assert len(terms) == 1229
    rows = [int(term["row_index"]) for term in terms]
    coefficients = [int(term["coefficient"]) for term in terms]
    assert len(set(rows)) == 1229 and rows[-1] == 1228
    assert set(rows[:-1]) == set(skeleton["basis_rows"])
    divisor = 0
    for coefficient in coefficients:
        divisor = math.gcd(divisor, abs(coefficient))
    assert divisor == 1 and coefficients[0] > 0
    assert str(sum(coefficients)) == outcome["certificate_rhs"]
    assert sum(coefficients) != 0

    assert independent["epistemic_status"] == "PROVED"
    assert (independent["assignments"], independent["predicate_columns"], independent["certificate_terms"]) == (4243, 1394, 1229)
    assert independent["primitive_gcd"] == 1
    assert independent["integer_predicate_sum"] == "ZERO"
    assert independent["integer_rhs_nonzero"] is True
    assert independent["integer_rhs"] == outcome["certificate_rhs"]
    assert independent["max_coefficient_height_bits"] == 2807
    assert independent["audit_prime"] == 2147483647
    assert independent["audit_prime_predicate_sum"] == "ZERO"
    return {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "claim_boundary": "degree-zero rational span, p199 base 4 / leaf 78 direct uncovered predicates only",
        "assignment_hash": ASSIGNMENT_HASH,
        "evaluation_rows": 4243,
        "predicate_columns": 1394,
        "certificate_terms": 1229,
        "certificate_height_bits": 2807,
        "integer_left_null": True,
        "integer_rhs_nonzero": True,
        "rational_degree_zero_identity": False,
        "independent_direct_set_replay": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
