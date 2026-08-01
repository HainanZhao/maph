#!/usr/bin/env python3
"""Audit the fixed-full-ray-label shortcut for the exploratory D12 lead.

This is a discovery containment check, not an AFK bridge.  For the
principal D12 form the Kopp-side positive element is
    gamma = q beta - p_tilde,  beta = 4 + 3 y,  y^2-y-3=0.
Its norm is p_tilde^2-11*p_tilde*q+q^2.  A ray class at modulus (12)
can label (gamma) only when that ideal is coprime to (12).  The audit
therefore falsifies the tempting, but invalid, one-fixed-modulus table
before any discrete-log computation is used.
"""

from __future__ import annotations

from hashlib import sha256
import json
from math import gcd
from pathlib import Path
import platform
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "discovery" / "tcc-sweep-d12-fixed-ray-shortcut-audit-v1.json"
D = 12


def positive_lift(p: int, q: int) -> int:
    """First p-12k for which q*beta' - (p-12k) is positive.

    The sign is decided by an integer-square comparison, never a float.
    """
    ptilde = p
    while True:
        left = 11 * q - 2 * ptilde
        # q*beta' - ptilde > 0 iff left > 3q sqrt(13).
        if left > 0 and left * left > 117 * q * q:
            return ptilde
        ptilde -= D


def norm(ptilde: int, q: int) -> int:
    return ptilde * ptilde - 11 * ptilde * q + q * q


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    records = []
    for p in range(D):
        for q in range(D):
            if (p, q) == (0, 0):
                continue
            ptilde = positive_lift(p, q)
            value = norm(ptilde, q)
            records.append({
                "characteristic": [p, q],
                "positive_lift": ptilde,
                "norm_q_beta_minus_ptilde": value,
                "gcd_norm_level": gcd(value, D),
                "coprime_to_finite_modulus": gcd(value, D) == 1,
            })
    noncoprime = [row for row in records if not row["coprime_to_finite_modulus"]]
    payload = {
        "schema": "tcc-sweep-d12-fixed-ray-shortcut-audit-v1",
        "claim_tag": "OBSERVED",
        "claim_boundary": (
            "Exact arithmetic audit of only the fixed-full-ray label shortcut. "
            "It neither computes lowered ray labels nor identifies an AFK packet "
            "or proves any TCC assertion."
        ),
        "candidate": {
            "d": 12,
            "r": 1,
            "field": "Q(sqrt(13))",
            "form": "<1,-3,-1>",
            "form_conductor": 1,
            "beta": "4+3y, y^2-y-3=0",
            "one_place_modulus": "(12) infinity_2",
        },
        "exact_derivation": {
            "conjugate_bound": "0 < (11-3 sqrt(13))/2 < 1",
            "positive_lift_rule": "first p-12k satisfying (11q-2p_tilde)^2>117q^2 and 11q-2p_tilde>0",
            "norm_formula": "Norm(q beta-p_tilde)=p_tilde^2-11 p_tilde q+q^2",
            "ray_condition": "A ray-class label at finite modulus (12) requires gcd(Norm(gamma),12)=1.",
        },
        "nonzero_characteristic_count": len(records),
        "full_modulus_coprime_count": len(records) - len(noncoprime),
        "full_modulus_noncoprime_count": len(noncoprime),
        "conclusion": (
            "The all-characteristic D12 bridge cannot use one fixed (12) ray group; "
            "the noncoprime rows require a characteristic-dependent conductor-lowering "
            "derivation before any ray-label comparison."
        ),
        "records": records,
        "replay": {
            "command": "python3 discovery/audit_tcc_sweep_d12_fixed_ray_shortcut.py",
            "python_version": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "source_hashes": {"audit_script": digest(Path(__file__))},
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    assert len(records) == 143
    assert len(noncoprime) > 0
    print("TCC_SWEEP_D12_FIXED_RAY_SHORTCUT_AUDIT=PASS")


if __name__ == "__main__":
    main()
