"""Regression checks for C86's all-inclusion Hall boundary."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def output() -> dict:
    return json.loads(subprocess.check_output([sys.executable, str(ROOT / "proof/check_cycle86_frankl_all_inclusion_hall.py")], text=True))


def test_c86_four_point_control_and_source_falsifier() -> None:
    result = output()
    assert result["status"] == "PASS"
    assert result["family_masks"] == 65536
    assert result["retained_dimension_three"] == 2034
    assert result["all_optimal_hall_failures"] == 0
    assert result["verifier_disagreements"] == 0
    controls = result["source_controls"]
    assert controls["example_319"]["optimal_1_hall_witness"] == [[0, 2, 4, 6], [3, 5, 7]]
    assert controls["example_320"]["all_inclusion_matching"] == [False] * 5
    assert all(witness is not None for witness in controls["example_320"]["hall_witnesses"])
    assert len(controls["example_320"]["immediate_cover_failures"]) == 5
