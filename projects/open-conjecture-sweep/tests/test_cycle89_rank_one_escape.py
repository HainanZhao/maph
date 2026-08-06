"""Regression test for C89's exact rank-one tangent control."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def test_c89_rank_one_escape_control() -> None:
    result = json.loads(subprocess.check_output(
        [sys.executable, str(ROOT / "proof/check_cycle89_rank_one_escape.py")], text=True
    ))
    assert result["status"] == "PSD_CONTROL_PASS"
    assert result["edges"] == 15 and result["labelled_maps"] == 59049
    assert result["density"] == "1/4"
    assert result["deficit_at_base"] == "153275/8349416423424"
    assert result["tangent_dimension"] == 7
    assert result["negative_principal_minors"] == []
    check = result["line_checks"][0]
    assert check["linear"] == check["gradient"] == "0"
    assert check["quadratic_times_2"] == check["hessian"]
