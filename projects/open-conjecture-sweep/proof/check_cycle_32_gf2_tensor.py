#!/usr/bin/env python3
"""Audit Cycle 32's exact degree-zero GF(2) boundary."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle32-gf2-tensor"


def audit() -> dict[str, object]:
    primary = json.loads((OUT / "result.json").read_text(encoding="utf-8"))
    independent = json.loads((OUT / "independent-replay.json").read_text(encoding="utf-8"))
    assert primary["status"] == independent["status"] == "PASS"
    h11 = primary["h11"]
    assert h11["selected_base"] == [1, 1, 1]
    assert (h11["bases_scanned"], h11["assignments"], h11["predicate_columns"], h11["matrix_status"], h11["rank"]) == (1, 64, 23, "CONSISTENT", 8)
    assert (h11["coefficient_times"], h11["coefficient_weight"]) == ([12], 1)
    assert independent["h11"] == {"base": [1, 1, 1], "assignments": 64, "constant_uncovered_time": 12, "coefficient_weight": 1}
    p199 = primary["p199"]
    assert p199["status"] == "INCONSISTENT_EVALUATION_SUBSYSTEM"
    assert (p199["predicate_columns"], p199["initial_equations"], p199["equations"], p199["rounds"], p199["rank"], p199["tensor_verifier_nodes"], p199["contradiction_size"]) == (1394, 4243, 4243, 1, 1226, 0, 577)
    replay = independent["p199"]
    assert (replay["assignments"], replay["predicate_columns"], replay["contradiction_size"], replay["contradiction_xor"], replay["reverse_elimination_status"]) == (4243, 1394, 577, "constant_one", "INCONSISTENT")
    assert replay["reverse_elimination_rank_before_contradiction"] == 1228
    return {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "claim_boundary": "degree-zero GF(2), one H11 base and p199 base 4 / leaf 78 only",
        "h11_certificate_weight": 1,
        "p199_predicate_columns": 1394,
        "p199_contradiction_size": 577,
        "p199_degree_zero_identity": False,
        "independent_replay": "PASS",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
