"""Regression checks for C83's exact local-method boundary."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def output(path: str) -> dict:
    return json.loads(subprocess.check_output([sys.executable, str(ROOT / path)], text=True))


def test_c83_exact_controls_and_defect_falsifier() -> None:
    tips = output("proof/check_cycle83_tip_fibers.py")
    conditional = output("proof/check_cycle83_interval_conditioning.py")
    words = output("proof/check_cycle83_word_pairing.py")
    defect = output("proof/check_cycle83_global_defect.py")
    assert tips["status"] == conditional["status"] == words["status"] == defect["status"] == "PASS"
    assert tips["c81"]["identities"] == 84 and tips["c82"]["identities"] == 78
    assert conditional["reversed_rows"] == 30
    assert words["c81_imbalanced_global_arrow_queries"] == 216
    assert defect["c81"]["inequality_failures"] == 18
    assert defect["c82"]["inequality_failures"] == 768
