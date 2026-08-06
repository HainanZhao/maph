"""Regression test for C87's private-region countermodel."""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def test_c87_minimal_absorption_countermodel() -> None:
    result = json.loads(subprocess.check_output([sys.executable, str(ROOT / "proof/check_cycle87_private_absorption.py")], text=True))
    assert result["status"] == "PASS" and result["solver_status"] == "SAT"
    assert result["lower_bound"]["minimum_no_absorption_points"] == 12
    assert result["candidate"]["private_regions"] == [[1], [2, 3], [4, 5], [6, 7], [8, 9], [10, 11]]
    assert result["candidate"]["absorbed_pairs"] == []
    assert result["candidate"]["minimum_component_cover"] == 3
