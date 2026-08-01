#!/usr/bin/env python3
"""Exact AFK/Kopp multiplier comparison for the exploratory D12 tuple.

This finite ledger checks the phase-square identity independently from the
ray-label ledger.  It is not a signed reconstruction or a TCC proof.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "discovery" / "tcc-sweep-d12-multiplier-ledger-v1.json"
D = 12
# Q=<1,-3,-1>; L_z=[[10,3],[3,1]], and A_t=L_z^3.
A = (1189, 360, 360, 109)


def mod_one(value: Fraction) -> Fraction:
    return value % 1


def dedekind_sum(a: int, c: int) -> Fraction:
    if c <= 0:
        raise ValueError(c)
    total = Fraction(0)
    for n in range(1, c):
        total += (Fraction(n, c) - Fraction(1, 2)) * (
            Fraction((n * a) % c, c) - Fraction(1, 2)
        )
    return total


def rademacher(a: int, c: int, d: int) -> Fraction:
    # AFK/Kopp convention for c>0.
    return Fraction(a + d, c) - 3 - 12 * dedekind_sum(a, c)


def positive_lift(p: int, q: int) -> int:
    ptilde = p
    while True:
        left = 11 * q - 2 * ptilde
        if left > 0 and left * left > 117 * q * q:
            return ptilde
        ptilde -= D


def theta_exponent(ptilde: int, q: int) -> Fraction:
    a, b, c, d = A
    r1, r2 = Fraction(ptilde, D), Fraction(q, D)
    return Fraction(1, 2) * (
        (c - d + 1) * r1 + (-a + b + 1) * r2 - c * d * r1 * r1
        + 2 * (a - 1) * d * r1 * r2 - (a - 2) * b * r2 * r2
    )


def quadratic_form(p: int, q: int) -> int:
    return p * p - 3 * p * q - q * q


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    a, b, c, d = A
    if a * d - b * c != 1 or (a % D, b % D, c % D, d % D) != (1, 0, 0, 1):
        raise AssertionError(A)
    psi = rademacher(a, c, d)
    if psi != 0:
        raise AssertionError(psi)
    records = []
    for p in range(D):
        for q in range(D):
            if (p, q) == (0, 0):
                continue
            ptilde = positive_lift(p, q)
            qvalue = quadratic_form(p, q)
            theta = mod_one(theta_exponent(ptilde, q))
            # AFK Theorem thm:phaserelation specializes xi_12^2=omega_12.
            afk_phase_square = mod_one(-Fraction(qvalue, 4))
            kopp_multiplier = mod_one(-psi / 12 - theta)
            if theta != mod_one(Fraction(qvalue, 4)):
                raise AssertionError((p, q, ptilde, theta, qvalue))
            if kopp_multiplier != afk_phase_square:
                raise AssertionError((p, q, kopp_multiplier, afk_phase_square))
            records.append({
                "characteristic": [p, q],
                "positive_lift": ptilde,
                "quadratic_form": qvalue,
                "theta_character_exponent_mod_1": str(theta),
                "afk_phase_square_exponent_mod_1": str(afk_phase_square),
                "kopp_multiplier_exponent_mod_1": str(kopp_multiplier),
                "match": True,
            })
    if len(records) != 143:
        raise AssertionError(len(records))
    payload = {
        "schema": "tcc-sweep-d12-multiplier-ledger-v1",
        "claim_tag": "EXPLORATORY",
        "claim_boundary": (
            "Exact all-characteristic multiplier comparison for the D12 "
            "conductor-one lead only. It neither identifies each AFK value with "
            "a lowered ray label nor proves a sign table, reconstruction, minors, or TCC."
        ),
        "candidate": {"d": 12, "r": 1, "form": "<1,-3,-1>", "form_conductor": 1},
        "stabilizer": {"L_z": [[10, 3], [3, 1]], "A_t": [[a, b], [c, d]], "rademacher_invariant": str(psi)},
        "formulae": {
            "theta_character": "Kopp arXiv:2411.06763, thm:thetamod",
            "phase_relation": "AFK arXiv:2501.03970v2, thm:phaserelation",
            "specialization": "theta exponent=Q(p,q)/4; phase-square exponent=-Q(p,q)/4 mod 1",
        },
        "nonzero_characteristic_count": len(records),
        "all_multiplier_comparisons_match": all(row["match"] for row in records),
        "records": records,
        "replay": {"command": "python3 discovery/audit_tcc_sweep_d12_multiplier_ledger.py", "python_version": sys.version.split()[0]},
        "source_hashes": {"audit_script": digest(Path(__file__))},
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("TCC_SWEEP_D12_MULTIPLIER_LEDGER=PASS")


if __name__ == "__main__":
    main()
