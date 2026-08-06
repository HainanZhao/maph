"""Regression checks for the C84 composite-modulus boundary."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def output(path: str) -> dict:
    return json.loads(subprocess.check_output([sys.executable, str(ROOT / path)], text=True))


def test_c84_composite_target_box_has_named_obstruction() -> None:
    exhaustive = output("proof/check_cycle84_composite_prop41.py")
    witness = output("proof/check_cycle84_composite_witness.py")
    assert exhaustive["status"] == witness["status"] == "PASS"
    assert exhaustive["fiber_vectors"] == 8191
    assert exhaustive["failing_vectors"] == 4824
    assert exhaustive["first_failure"]["vector"] == list(witness["vector"])
    assert len(witness["r_rows"]) == 6
