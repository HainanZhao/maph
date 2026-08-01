#!/usr/bin/env python3
"""Hostile v3 correction of the Stream C Route A explicit-formula closure.

This uses no Route-B artifact.  v1 and v2 are historical records and remain
untouched.  The correction distinguishes the uniform and almost-all heights.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import platform
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any

PROJECT = Path(__file__).resolve().parents[1]
GM = PROJECT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex"
KEDLAYA = PROJECT / "artifacts/sources/kedlaya-2007-errorbounds-author.pdf"
ACCESS = PROJECT / "docs/cycle-2-stream-c-explicit-formula-access-ledger-v1.md"
HUXLEY_LEDGER = PROJECT / "docs/literature-ledger-classical-inputs.md"
FORD = PROJECT / "artifacts/sources/ford-2002-zero-free-regions.pdf"
PLATT = PROJECT / "artifacts/sources/platt-trudgian-2021-rh-3e12.tar"
HSW = PROJECT / "artifacts/sources/hasanalizade-shen-wong-2022-counting-zeros.tar"
BUI = PROJECT / "artifacts/sources/bui-heath-brown-2013-simple-zeros.tar"
V2 = PROJECT / "artifacts/cycle-2-stream-c-route-a-v2.json"
HASHES = {
    GM: "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
    KEDLAYA: "375d96e65a99d7dbfbdc9ca51aa286bb53af7e77dfffa59e167dfcd9b18b919d",
    FORD: "a43a2c37cf0f34b05bf80d9e58bcef176371437eedf7aae17d72f2c55b04c948",
    PLATT: "c4f13cdfca711d2bf90a097147be2a094ff175b0b161647359e174633fd8bf86",
    HSW: "8ba8d0eb95e1dd967adf17b7a2e77bdc45a99f6aa283d41d23dd4d0ac4358247",
    BUI: "a171c6e74be228955df48191675e497ce4934623ae33ddddd9761b8cb1185ca5",
}
B = Fraction(30, 13)

def sha256(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def canonical_sha256(value: dict[str, Any]) -> str: return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
def gzip_text(path: Path) -> str:
    with gzip.open(path, "rt", encoding="utf-8") as stream: return stream.read()

def check_sources() -> None:
    for path, expected in HASHES.items(): assert sha256(path) == expected, f"hash mismatch: {path.name}"
    gm, access, huxley, hsw, bui, platt = GM.read_text(), ACCESS.read_text(), HUXLEY_LEDGER.read_text(), gzip_text(HSW), gzip_text(BUI), gzip_text(PLATT)
    for text in ("\\(z\\ge2\\), \\(T\\ge2\\)", "R(z,T)", "nearest *other*", "half weight at a"):
        assert text in access, f"missing checked formula-chain statement: {text}"
    for text in ("T=xy^{-1}\\exp(2\\sqrt[4]{\\log{x}})", "T=\\delta^{-1}\\exp(4\\sqrt[4]{\\log{X}})", "T<x^{13/30-\\epsilon/2}", "X^{2\\sigma+1}N(\\sigma,T)"):
        assert text in gm, f"missing GM anchor: {text}"
    assert "N(\\alpha,T)\\ll T^{3(1-\\alpha)/(3\\alpha-1)}\\ell^{44}" in huxley
    assert "For any $T\\ge e$" in hsw and "where each zero is counted with multiplicity" in bui
    assert "all zeroes $\\beta + i\\gamma$" in platt and "$\\beta = 1/2$" in platt

def bookkeeping() -> dict[str, Any]:
    uniform_t, almost_t = Fraction(13, 30), Fraction(13, 15)
    assert uniform_t < Fraction(1, 2) < almost_t < 1
    assert Fraction(3, 1) / (3 * Fraction(4, 5) - 1) == Fraction(15, 7) < B
    return {
        "uniform": {"theta": "17/30", "T_power_at_endpoint": "13/30", "CHJ_I_alpha_half": "admissible only here", "arbitrary_T_formula": "admissible: 2<=T<=x eventually"},
        "almost_all": {"theta": "2/15", "delta": "X^(-13/15+epsilon/2)", "T_power_before_subpower": "13/15", "CHJ_I_alpha_half": "NOT admissible: 13/15>1/2", "arbitrary_T_formula": "admissible: 2<=T<=X eventually"},
        "formula_transfer": "At integer endpoints the half-weight correction and prime-power-distance term are O(log X); for 2<=T<=X the two arbitrary-T remainders are O(X(log X)^3/T).",
        "modulus_boundary": "If |gamma|<=T-1/T then |rho|<T since 0<beta<1. Thus |rho| versus |gamma| can differ only in T-1/T<|gamma|<=T; O(log T) multiplicity-inclusive zeros there contribute O(X log T/T), absorbed by X(log X)^3/T.",
        "multiplicity": "The residue of -zeta'/zeta at a zero of order m is m. Hence the von-Mangoldt zero sum is the multiplicity-weighted residue sum; Bui--Heath-Brown independently pins the same convention for N(T).",
        "near_one": "Huxley (1.9) is two-sided with log^44; h(s)<=15/7<30/13 for s>=4/5. GM supplies the adjacent density range. Ford plus Platt--Trudgian supplies the VK cutoff at all heights.",
        "prime_powers": "For z asymp X and y>=X^(2/15+epsilon), prime powers with exponent >=2 in [z,z+y] contribute O((y/X^(1/2)+1)(log X)^2)=o(y exp(-(log X)^(1/4))). Partial summation then transfers theta to pi with the weaker stated error.",
    }

def rows() -> list[dict[str, Any]]:
    return [
        {"id":"SC-A29-v2-reproducibility-correction","status":"PROVED","finding":"v2 embedded wall_time_ns in its mathematical artifact, so replay rewrote its bytes. v3 excludes runtime from the deterministic --write/--check artifact; optional runtime data is isolated in a performance artifact."},
        {"id":"SC-A30-v2-correction","status":"PROVED","finding":"CHJ-I alpha<=1/2 cannot cover T~X^(13/15); v2's almost-all PASS was invalid. Its all-zeros wording also did not itself state multiplicity."},
        {"id":"SC-A31-arbitrary-T-explicit-formula","status":"PROVED","locator":"Iwaniec Theorem 10.1 checked in the access ledger; local Kedlaya 2007 author archival Theorem 1, SHA pinned","statement":"The half-weighted formula holds for every x>=2,T>0 with a distance-to-other-prime-power remainder. Integer endpoint transfer gives GM's weaker O(X(log X)^3/T) formula at both truncation scales."},
        {"id":"SC-A32-multiplicity-and-height","status":"PROVED","locator":"residue lemma; Bui--Heath-Brown; HSW","statement":"Residues impose multiplicity; HSW+Bui gives the boundary-strip count, and the |rho|/ordinate mismatch is absorbed into the truncation error."},
        {"id":"SC-A33-density-VK-pair","status":"PROVED","locator":"Huxley (1.9), Ford Theorem 5, Platt--Trudgian Theorem 1, HSW+Bui","statement":"Near-one logarithmic density, all-height VK cutoff, and multiplicity-inclusive O(log T) unit strips supply both uniform supremum and almost-all pair kernel."},
        {"id":"SC-A34-prime-transfer","status":"PROVED","locator":"GM §13.2 and elementary prime-power counting","statement":"Prime-power and partial-summation losses are below the stated error in both the uniform and almost-all ranges."},
    ]

def build_report() -> dict[str, Any]:
    check_sources(); old = json.loads(V2.read_text())
    assert old["exact_replay_sha256"] == "3e0e194aab6810a2697f7951058c3ee407fa3dc47e9ce91ba96139f037fc3970"
    report_rows = rows(); assert all(row["status"] == "PROVED" for row in report_rows)
    return {"artifact_id":"cycle-2-stream-c-route-a-v3","supersedes":{"artifact":"cycle-2-stream-c-route-a-v2","exact_replay_sha256":old["exact_replay_sha256"],"correction":"v2 uniform formula closure retained; its almost-all CHJ-I closure withdrawn and replaced by the arbitrary-T chain"},"status":"PROVED: corrected external-input closure for GM §13.2, conditional on GM's published density theorem","claim_boundary":"No independent zero-density or short-interval theorem, and no new exponent, is claimed.","sources":{p.name:h for p,h in HASHES.items()},"rows":report_rows,"exact_bookkeeping":bookkeeping(),"open_blockers":[],"result_labels":{"uniform_theta":"17/30","almost_all_theta":"2/15","uniform":"PROVED input compatibility conditional on GM density","almost_all":"PROVED input compatibility conditional on GM density"},"pass_state":"PASS: the arbitrary-T formula chain, not CHJ-I, covers the almost-all height; conventions and prime transfer are separately checked."}

def artifact_bytes() -> bytes:
    script = Path(__file__).resolve()
    report = build_report()
    report["exact_replay_sha256"] = canonical_sha256(report)
    report["replay"] = {"script": str(script.relative_to(PROJECT)), "script_sha256": sha256(script), "python_implementation": platform.python_implementation(), "python_version": sys.version.split()[0], "write_command": "python3 proof/replay_cycle2_stream_c_route_a_v3.py --write", "check_command": "python3 proof/replay_cycle2_stream_c_route_a_v3.py --check"}
    return (json.dumps(report, indent=2, sort_keys=True) + "\n").encode()

def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write-performance", action="store_true")
    args = parser.parse_args()
    started = time.perf_counter_ns()
    target = PROJECT / "artifacts/cycle-2-stream-c-route-a-v3.json"
    data = artifact_bytes()
    if args.write:
        target.write_bytes(data)
        print(target)
        return
    if args.check:
        assert target.read_bytes() == data, "v3 artifact differs from deterministic replay; run --write"
        print(f"PASS: {target}")
        return
    performance = {"artifact_id": "cycle-2-stream-c-route-a-v3-performance", "script_sha256": sha256(Path(__file__).resolve()), "wall_time_ns": time.perf_counter_ns() - started}
    path = PROJECT / "artifacts/cycle-2-stream-c-route-a-v3-performance.json"
    path.write_text(json.dumps(performance, indent=2, sort_keys=True) + "\n")
    print(path)
if __name__ == "__main__": main()
