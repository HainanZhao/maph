"""Regression test for C88's exact fractional-drop falsifier."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def test_c88_fractional_drop_falsifier() -> None:
    result = json.loads(subprocess.check_output(
        [sys.executable, str(ROOT / "proof/check_cycle88_fractional_drop.py")], text=True
    ))
    assert result["status"] == "FD_REFUTED"
    assert result["epistemic_status"] == "PROVED"
    assert result["unreconstructed"] == []
    assert result["layer_counts"] == [1, 31, 420, 2582, 5403, 6101]
    first = result["failures"][0]
    assert first["depth"] == 1
    assert first["residual_edges"] == list(range(1, 10))
    assert first["tau_star"] == "23/8" and first["k"] == 3
    assert first["drop_vertices"] == []
