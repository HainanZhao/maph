#!/usr/bin/env python3
"""Deterministic discovery search for H11 weighted first-lift duals."""

from __future__ import annotations

import argparse
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
K, P, C, Q = 3, 11, 4, 44
ITERATIONS = 20_000
SCALE = 1 << 20


def mask(speed: int) -> int:
    return sum(
        1 << time
        for time in range(Q)
        if (K + 1) * min((time * speed) % Q, Q - ((time * speed) % Q)) < Q
    )


def dot(weights: list[float], bits: int) -> float:
    return sum(weights[index] for index in range(Q) if bits >> index & 1)


def l1_improper(base: tuple[int, ...], masks: list[int]) -> bool:
    return masks[base[0]] | masks[base[1]] | masks[base[2]] == (1 << P) - 1


def certificate_margin(integer_weights: list[int], options: list[list[int]]) -> tuple[int, int]:
    total = sum(integer_weights)
    best = 0
    for choices in options:
        best += max(sum(integer_weights[t] for t in range(Q) if bits >> t & 1) for bits in choices)
    return total, best


def optimize(options: list[list[int]]) -> tuple[list[int], float, int, int]:
    weights = [1.0 / Q] * Q
    best_weights = weights[:]
    best_value = float("inf")
    for step in range(ITERATIONS):
        choices = [max(group, key=lambda bits: dot(weights, bits)) for group in options]
        value = sum(dot(weights, bits) for bits in choices)
        if value < best_value:
            best_value, best_weights = value, weights[:]
        eta = 0.7 / math.sqrt(step + 1)
        next_weights = []
        for time in range(Q):
            gradient = sum((bits >> time) & 1 for bits in choices)
            next_weights.append(weights[time] * math.exp(-eta * gradient))
        normalizer = sum(next_weights)
        weights = [value / normalizer for value in next_weights]
    integer = [max(0, round(value * SCALE)) for value in best_weights]
    total, best = certificate_margin(integer, options)
    return integer, best_value, total, best


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count-only", action="store_true")
    args = parser.parse_args()
    base_masks = [sum(
        1 << time
        for time in range(P)
        if (K + 1) * min((time * speed) % P, P - ((time * speed) % P)) < P
    ) for speed in range(P)]
    lifted_masks = [mask(speed) for speed in range(Q)]
    output = ROOT / "discovery/out/cycle9-h11-dual-discovery.txt"
    rows: list[str] = []
    improper_bases = 0
    accepted = 0
    for x in range(1, P):
        for y in range(1, P):
            for z in range(1, P):
                base = (x, y, z)
                if not l1_improper(base, base_masks):
                    continue
                improper_bases += 1
                if args.count_only:
                    continue
                options = [[lifted_masks[value + P * digit] for digit in range(C)] for value in base]
                integer, floating_value, total, best = optimize(options)
                status = "CERTIFICATE" if best < total else "NO_CERTIFICATE"
                accepted += status == "CERTIFICATE"
                rows.append("{} {} {} {} {:.12f} {} {} {}".format(*base, status, floating_value, total, best, ",".join(map(str, integer))))
    if not args.count_only:
        output.write_text("\n".join(rows) + "\n")
    print(f"raw_bases={(P-1)**K} l1_improper={improper_bases} certificates={accepted}")


if __name__ == "__main__":
    main()
