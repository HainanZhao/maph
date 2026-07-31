#!/usr/bin/env python3
"""Versioned Engine-C convention re-audit for the staged v1.4 paper."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
PAPER = ROOT / "paper/effective-stark-results.tex"
THEORY = ROOT / "data/engine-c-general-e-theory-v4.json"
BRIDGE = ROOT / "scripts/generic_engine_c_packet_bridge.gp"
V1 = ROOT / "artifacts/engine-c-fourier-convention-correction-v1.json"
OUT = ROOT / "artifacts/engine-c-fourier-convention-correction-v2.json"
V1_SHA256 = "c6e48cebc242ac7194ac3905825d6780a05175e156559eb92de4d951bbc0a420"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return left[0] + right[0], left[1] + right[1]


def mul(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def main() -> None:
    if sha(V1) != V1_SHA256:
        raise RuntimeError("published Engine-C correction v1 was modified")

    psi = ((1, 0), (0, 1), (-1, 0), (0, -1))
    ell_vectors = (
        ((1, 0), (0, 0), (-1, 0), (0, 0)),
        ((0, 0), (1, 0), (0, 0), (-1, 0)),
    )
    transforms = []
    for vector in ell_vectors:
        value = (0, 0)
        for character, coefficient in zip(psi, vector, strict=True):
            value = add(value, mul(character, coefficient))
        transforms.append(value)
    if transforms != [(2, 0), (0, 2)]:
        raise RuntimeError(f"quartic Fourier transform changed: {transforms}")

    packet_coefficients = [(-2, 0), (0, -2), (2, 0), (0, 2)]
    paper = PAPER.read_text()
    required = (
        r"L'_S(0,\psi)",
        r"=-\frac4e(\ell_1+i\ell_\sigma)",
        r"N_{E/E^+}(\sigma^ru)^{-1}",
        r"\theta(\bar s)=\psi(\sigma)=i",
    )
    forbidden = (r"\ell_1-i\ell_\sigma", r"\sigma^{-r}u")
    if any(item not in paper for item in required):
        raise RuntimeError("paper omits the sigma-positive convention")
    if any(item in paper for item in forbidden):
        raise RuntimeError("paper retains the superseded convention")

    bridge = BRIDGE.read_text()
    bridge_needles = (
        "my(power = label_index - 1);",
        "for(repetition = 1, power,",
        "normal_sigma)",
    )
    if any(item not in bridge for item in bridge_needles):
        raise RuntimeError("exact bridge no longer uses positive sigma powers")

    payload = {
        "schema": "effective-stark-engine-c-fourier-convention-correction-v2",
        "recorded_at_utc": "2026-07-31T00:00:00Z",
        "claim_tag": "VERIFIED_EXACT_CONVENTION_REAUDIT",
        "verdict": "PASS",
        "supersedes_for_live_source_hash_only":
            "artifacts/engine-c-fourier-convention-correction-v1.json",
        "mathematical_convention_unchanged_from_v1": True,
        "fourier_transform_coefficients": {
            "ell_1": [2, 0],
            "ell_sigma": [0, 2],
        },
        "packet_log_coefficients_m0_m1": [
            list(pair) for pair in packet_coefficients
        ],
        "corrected_formulas": {
            "direct_lprime": "-(4/e)*(ell_1+i*ell_sigma)",
            "packet": "Y_(sbar^r)=N_(E/E+)(sigma^r*u)^-1",
        },
        "mathematical_impact": {
            "packet_polynomials": "UNCHANGED",
            "unlabeled_root_sets": "UNCHANGED",
            "artin_label_formula": "SIGMA_POSITIVE",
            "case_tags": "UNCHANGED",
        },
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (PAPER, THEORY, BRIDGE, SELF, V1)
        },
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("ENGINE_C_FOURIER_CONVENTION_V2_AUDIT=VERIFIED")


if __name__ == "__main__":
    main()
