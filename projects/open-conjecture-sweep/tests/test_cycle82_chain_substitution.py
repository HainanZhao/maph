"""Regression checks for the frozen C82 inverse-realization certificate."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def output(path: str) -> dict:
    return json.loads(subprocess.check_output([sys.executable, str(ROOT / path)], text=True))


def test_c82_independent_routes_agree() -> None:
    dynamic = output("proof/check_cycle82_chain_substitution.py")
    direct = output("proof/check_cycle82_direct_enumeration.py")
    for result in (dynamic, direct):
        assert result["status"] == "PASS"
        assert result["vertices"] == 15
        assert result["extensions"] == 571_725
        assert not result["full_has_4_cycle"]
        assert not result["restricted_has_4_cycle"]
    assert direct["transitive_closure_added_relations"] == 3
