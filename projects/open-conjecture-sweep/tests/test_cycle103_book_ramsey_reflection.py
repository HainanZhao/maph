from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_q7_reflection_gate_has_a_replayable_independent_no_hit(tmp_path: Path) -> None:
    result = tmp_path / "result.json"
    subprocess.run([sys.executable, "proof/cycle103_book_ramsey_reflection.py", "--output", str(result)], cwd=ROOT, check=True)
    checked = subprocess.check_output([sys.executable, "proof/check_cycle103_book_ramsey_reflection.py", str(result)], cwd=ROOT, text=True)
    payload = json.loads(result.read_text())
    assert payload["logical_assignments"] == 1 << 25
    assert len(payload["row_sum_masks"]) == 222
    assert payload["seidel_checked_assignments"] == 14_208
    assert payload["q7_hits"] == []
    assert json.loads(checked) == {"logical_assignments": 1 << 25, "q7_hits": [], "row_sum_masks": 222, "seidel_checked_assignments": 14_208}
