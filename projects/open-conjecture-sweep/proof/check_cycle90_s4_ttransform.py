#!/usr/bin/env python3
"""Compile and compare C90's two independent exact contractions."""
from __future__ import annotations
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent

def run(source: str, binary: str) -> dict:
    subprocess.run(["g++", "-O3", "-std=c++20", str(ROOT / source), "-o", binary], check=True)
    return json.loads(subprocess.check_output([binary], text=True))

def main() -> None:
    direct = run("cycle90_s4_ttransform_direct.cpp", "/tmp/c90-direct-check")
    regular = run("cycle90_s4_ttransform_regular.cpp", "/tmp/c90-regular-check")
    assert direct["normalization_denominator"] == regular["normalization_denominator"] == "2641807540224"
    assert direct["coefficients"] == regular["coefficients"]
    expected = ["26975973670912","0","294060523520","0","41130106880","0","701834240","0","20876600","0","35536","0","-190","0","0","0"]
    assert direct["coefficients"] == expected
    print(json.dumps({"status":"COEFFICIENTWISE_ROUTE_AGREEMENT","epistemic_status":"PROVED","normalization_denominator":direct["normalization_denominator"],"coefficients":expected,"claim_boundary":"One frozen S4 transfer only; no all-background, all-S4, Zhao, or Sidorenko conclusion."},sort_keys=True))

if __name__ == "__main__": main()
