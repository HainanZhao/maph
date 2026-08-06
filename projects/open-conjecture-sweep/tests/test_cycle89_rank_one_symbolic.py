"""Regression test for C89's independent formula replay."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def test_c89_rank_one_symbolic_replay() -> None:
    result = json.loads(subprocess.check_output(
        [sys.executable, str(ROOT / "proof/check_cycle89_rank_one_symbolic_replay.py")], text=True
    ))
    assert result["status"] == "COEFFICIENTWISE_REPLAY_PASS"
    assert result["ordered_edge_pairs"] == 210
    assert [row["mismatch_count"] for row in result["controls"]] == [0, 0]
