#!/usr/bin/env python3
"""Replay C103's engine and independent checker in a disposable directory."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"logical_assignments": 1 << 25, "q7_hits": [], "row_sum_masks": 222, "seidel_checked_assignments": 14_208}


def main() -> None:
    with tempfile.TemporaryDirectory() as temporary:
        result = Path(temporary) / "result.json"
        subprocess.run([sys.executable, "proof/cycle103_book_ramsey_reflection.py", "--output", str(result)], cwd=ROOT, check=True)
        checked = json.loads(subprocess.check_output([sys.executable, "proof/check_cycle103_book_ramsey_reflection.py", str(result)], cwd=ROOT, text=True))
        recorded = json.loads(result.read_text())
    assert recorded["logical_assignments"] == EXPECTED["logical_assignments"]
    assert len(recorded["row_sum_masks"]) == EXPECTED["row_sum_masks"]
    assert recorded["seidel_checked_assignments"] == EXPECTED["seidel_checked_assignments"]
    assert recorded["q7_hits"] == EXPECTED["q7_hits"]
    assert checked == EXPECTED
    print(json.dumps({"status": "PASS", **EXPECTED}, sort_keys=True))


if __name__ == "__main__":
    main()
