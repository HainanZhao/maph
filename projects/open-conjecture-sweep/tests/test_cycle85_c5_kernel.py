"""Regression checks for C85's exact C5 triple-kernel boundary."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]


def output(path: str) -> dict:
    return json.loads(subprocess.check_output([sys.executable, str(ROOT / path)], text=True))


def test_c85_packet_routes_and_cp_expansion() -> None:
    kernel = output("proof/check_cycle85_c5_kernel.py")
    direct = output("proof/check_cycle85_direct_bigraphon.py")
    expansion = output("proof/check_cycle85_cp_expansion.py")
    assert kernel == direct
    assert kernel["status"] == "PASS"
    assert kernel["packet_rows"] == 729
    assert kernel["negative_rows"] == 0
    assert kernel["zero_rows"] == 81
    assert kernel["minimum_positive_defect"] == "7381/14281868906496"
    assert expansion["status"] == "PASS"
    assert expansion["expanded_terms"] == 8771
    assert expansion["total_degree"] == 35
    assert expansion["uv_total_degree"] == 15
    assert expansion["expanded_sha256"] == "5cd3cc7d244ae83ce8c55fa335ee4806038570b76d71da016496ed4c52fd2397"
