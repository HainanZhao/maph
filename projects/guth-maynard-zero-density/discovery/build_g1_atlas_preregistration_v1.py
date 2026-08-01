#!/usr/bin/env python3
"""Seal/check the Cycle-3 G1 atlas preregistration before discovery."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import sys
from typing import Any

import mpmath


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/cycle-3-g1-atlas-preregistration-v1.md"
OUTPUT = ROOT / "artifacts/cycle-3-g1-atlas-preregistration-v1.json"
SOURCE_TEX = ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex"
SOURCE_TAR = ROOT / "artifacts/sources/arxiv-2405.20552v2.tar"
SOURCE_TEX_SHA = "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"
SOURCE_TAR_SHA = "9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def ceil_q(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def s_grid() -> list[Fraction]:
    return [Fraction(7, 10) + Fraction(i, 100) for i in range(11)]


def n_grid() -> list[Fraction]:
    return [Fraction(3, 4) + Fraction(j, 60) for j in range(16)]


def v_grid() -> list[Fraction]:
    return s_grid()


def w_grid() -> list[Fraction]:
    return [Fraction(1, 2), Fraction(7, 12), Fraction(2, 3), Fraction(3, 4)]


def transfer_rows() -> list[dict[str, Any]]:
    rows = []
    for s in s_grid():
        ell = Fraction(10, 1) / (6 + 10 * s)
        upper = Fraction(15, 1) / (6 + 10 * s)
        alpha = Fraction(15, 1) * (1 - s) / ((3 + 5 * s) * (Fraction(18, 5) - 4 * s))
        n0s = {Fraction(j, 100) for j in range(2, 51)} | {Fraction(5, 13), ell / 2}
        for n0 in sorted(n0s):
            small = n0 <= ell / 2
            k = ceil_q(ell / n0) if small else 2
            value = k * n0
            assert 1 <= k <= 77 and value >= ell
            endpoint = "ASYMPTOTIC_ENDPOINT_ONLY" if n0 == Fraction(1, 2) else "EXACT_POWER_SCALE"
            if endpoint == "EXACT_POWER_SCALE":
                assert value <= upper
            rows.append({
                "s": q(s), "n0": q(n0), "k": k, "q": q(value),
                "ell": q(ell), "u": q(upper), "alpha": q(alpha),
                "provenance": endpoint,
                "branch": "q<=alpha" if value <= alpha else "q>alpha",
            })
    assert any(row == {
        "s": "7/10", "n0": "5/13", "k": 2, "q": "10/13",
        "ell": "10/13", "u": "15/13", "alpha": "45/52",
        "provenance": "EXACT_POWER_SCALE", "branch": "q<=alpha",
    } for row in rows)
    return rows


def primary_spine() -> list[dict[str, str]]:
    rows = []
    for s in (Fraction(7, 10), Fraction(3, 4), Fraction(4, 5)):
        nearby = sorted({value for value in (s - Fraction(1, 100), s, s + Fraction(1, 100)) if Fraction(7, 10) <= value <= Fraction(4, 5)})
        for n in (Fraction(4, 5), Fraction(5, 6)):
            for v in nearby:
                for w in (Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)):
                    rows.append({"s": q(s), "n": q(n), "v": q(v), "w": q(w)})
    assert len(rows) == 42 and len({tuple(row.values()) for row in rows}) == 42
    return rows


def certificate() -> dict[str, Any]:
    assert sha256(SOURCE_TEX) == SOURCE_TEX_SHA
    assert sha256(SOURCE_TAR) == SOURCE_TAR_SHA
    assert platform.python_implementation() == "CPython" and platform.python_version() == "3.12.3"
    assert mpmath.__version__ == "1.2.1"
    local_count = len(s_grid()) * len(n_grid()) * len(v_grid()) * len(w_grid())
    pairs = [
        ["C0-flat", "W0-sidon"], ["C0-flat", "W1-uniform"], ["C0-flat", "W3-AP"],
        ["C1-tent", "W1-uniform"], ["C1-tent", "W3-AP"], ["C2-two-tent", "W2-jitter"],
        ["C2-two-tent", "W4-four-block"], ["C3-root-chirp", "W0-sidon"],
        ["C3-root-chirp", "W5-rational"], ["C4-rademacher", "W0-sidon"],
        ["C4-rademacher", "W1-uniform"], ["C4-rademacher", "W2-jitter"],
        ["C5-point-aligned", "W3-AP"], ["C5-point-aligned", "W5-rational"],
    ]
    spine = primary_spine()
    assert len(spine) * len(pairs) == 588
    return {
        "artifact_id": "cycle-3-g1-atlas-preregistration-v1",
        "epistemic_status": "CONJECTURED",
        "claim_boundary": "Frozen finite discovery design only. It authorizes the specified G1 atlas but proves no theorem, extremizer, improvement, or saturation result.",
        "frozen_before_discovery": True,
        "document": {"path": "docs/cycle-3-g1-atlas-preregistration-v1.md", "sha256": sha256(DOC)},
        "sources": {
            "gm_tex": {"path": str(SOURCE_TEX.relative_to(ROOT)), "sha256": SOURCE_TEX_SHA, "locators": ["68--94", "1785--1820", "2307--2364", "2398"]},
            "gm_tar": {"path": str(SOURCE_TAR.relative_to(ROOT)), "sha256": SOURCE_TAR_SHA},
        },
        "runtime": {"implementation": "CPython", "python": "3.12.3", "mpmath": "1.2.1", "precisions_bits": [256, 384]},
        "local_grid": {"s": [q(x) for x in s_grid()], "n": [q(x) for x in n_grid()], "v": [q(x) for x in v_grid()], "w": [q(x) for x in w_grid()], "expected_rows": local_count},
        "formulas": {
            "large_values": {"A1": "2*n*(1-v)", "A2": "n*(18/5-4*v)", "A3": "1+n*(12/5-4*v)", "G": "max(A1,A2,A3)"},
            "classical": {"C1": "2*n*(1-v)", "C2": "1+n*(1-2*v)", "C3": "1+n*(4-6*v)", "C": "max(C1,min(C2,C3))", "Delta_LV": "C-G"},
            "energy_diagonal_only": {"eligibility": "v=s", "E1": "w+n*(4-4*s)", "E2": "21*w/8+1/4+n*(1-2*s)", "E3": "3*w+n*(1-2*s)"},
            "transfer": {"ell": "10/(6+10*s)", "u": "15/(6+10*s)", "alpha": "15*(1-s)/((3+5*s)*(18/5-4*s))", "B": "15*(1-s)/(3+5*s)"},
        },
        "transfer_rows": transfer_rows(),
        "mandatory_anchors": {"local": {"s": "7/10", "n": "5/6", "v": "7/10", "w": "2/3", "energy_terms": ["5/3", "5/3", "5/3"]}, "transfer": {"s": "7/10", "n0": "5/13", "k": 2, "q": "10/13"}},
        "screen": {"spine": spine, "pairs": pairs, "scale_U": 4096, "expected_rows": 588},
        "families": {"coefficients": ["C0-flat", "C1-tent", "C2-two-tent", "C3-root-chirp", "C4-rademacher", "C5-point-aligned"], "sets": ["W0-sidon", "W1-uniform", "W2-jitter", "W3-AP", "W4-four-block", "W5-rational"], "definitions_source": "the frozen document"},
        "rng": {"algorithm": "SplitMix64 unsigned wraparound", "seed": "0x47554d41594e4731", "coefficient_xor": "0x434f454646000001", "set_xor": "0x57414c5545000001"},
        "retention": {"rho_value_min": "-1/400", "rho_energy_min": "-1/400", "precision_disagreement_max": "1/1600", "maximum_per_regime_coefficient": 2, "maximum_total": 36, "validation_scales_U": [32768, 262144], "maximum_validation_rows": 72, "exact_cube_increments": ["1/300", "1/180", "1/300"]},
        "resources": {"seconds_per_finite_row": 180, "max_rss_bytes": 2147483648, "aggregate_cpu_hours": 128, "maximum_finite_rows": 660, "worst_case_hours_at_row_cap": 33},
        "failed_row_rule": "Every scheduled infeasible, invalid, resource, precision, nonfinite, or replay failure is retained once with its distinct code and no parameter-changing retry.",
        "replay": {"script_sha256": sha256(Path(__file__)), "write_command": "python3 projects/guth-maynard-zero-density/discovery/build_g1_atlas_preregistration_v1.py --write", "check_command": "python3 projects/guth-maynard-zero-density/discovery/build_g1_atlas_preregistration_v1.py --check"},
    }


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = render(certificate())
    if args.write:
        OUTPUT.write_text(payload)
    elif not OUTPUT.is_file() or OUTPUT.read_text() != payload:
        raise SystemExit("G1 preregistration artifact mismatch")
    else:
        print(json.dumps({"artifact": OUTPUT.name, "frozen": True, "verified": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
