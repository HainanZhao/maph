#!/usr/bin/env python3
"""Frozen derivative-resolved simple-root profiler; discovery only."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from math import gcd
from pathlib import Path

import mpmath as mp

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "discovery/cycle-118-simple-root-profiler-v1.json"


def profile_D(D: int) -> dict[str, object]:
    Q = round(D ** (5 / 9))
    K = round(D ** (16 / 15))
    x = 2 * mp.pi / D
    threshold = mp.mpf(1) / K
    counts = Counter()
    examples = {}
    retained = simple = 0
    for a in range(-D, D + 1):
        if a == 0:
            continue
        ea = mp.exp(a * x)
        for b in range(-D, D + 1):
            if b == 0:
                continue
            eb = mp.exp(b * x)
            M = max(abs(a), abs(b))
            for B in range(1, Q + 1):
                for C in range(1, Q + 1):
                    target = B * ea + C * eb
                    A = int(mp.nint(target))
                    if A <= 0:
                        continue
                    delta = abs(A - target)
                    if delta > threshold:
                        continue
                    retained += 1
                    eta = abs(B * a * ea + C * b * eb)
                    S2 = B * a * a + C * b * b
                    Lx = S2 * mp.exp(mp.mpf("1.5") * M * x)
                    newton = max(4 * delta / x, 2 * mp.sqrt(Lx * delta))
                    if eta < newton:
                        continue
                    simple += 1
                    J0, J1 = A - B - C, B * a + C * b
                    signature = (
                        "J0_ZERO" if J0 == 0 else "J0_NONZERO",
                        "J1_ZERO" if J1 == 0 else "J1_NONZERO",
                        "OPPOSITE" if a * b < 0 else "SAME",
                    )
                    key = "/".join(signature)
                    counts[key] += 1
                    if key not in examples:
                        examples[key] = {
                            "A": A, "B": B, "C": C, "a": a, "b": b,
                            "J0": J0, "J1": J1, "gcd_modes": gcd(abs(a), abs(b)),
                            "delta": mp.nstr(delta, 20), "eta": mp.nstr(eta, 20),
                        }
    return {
        "D": D, "Q": Q, "K": K, "retained": retained, "simple": simple,
        "signatures": dict(sorted(counts.items())), "examples": examples,
    }


def run() -> dict[str, object]:
    mp.mp.dps = 80
    return {
        "epistemic_status": "OBSERVED", "proof_role": "none",
        "mpmath_version": mp.__version__, "decimal_precision": 80,
        "rows": [profile_D(D) for D in (24, 36, 48)],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    encoded = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.write:
        if OUTPUT.exists():
            raise SystemExit("refusing to overwrite discovery output")
        OUTPUT.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
