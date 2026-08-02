#!/usr/bin/env python3
"""Profile low-multiplicity sampled-Mellin aliases on frozen grids."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from math import floor, gcd
import json
from pathlib import Path

import mpmath as mp


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "discovery/cycle-128-sampled-mellin-profiler-v1.json"
D_VALUES = (72, 108, 162)
XI_VALUES = (Fraction(16, 25), Fraction(7, 10), Fraction(23, 30))
RADII = (1, 4)


def convergents(value: mp.mpf, denominator_cap: int) -> set[tuple[int, int]]:
    result: set[tuple[int, int]] = set()
    x = value
    p_minus_two, p_minus_one = 0, 1
    q_minus_two, q_minus_one = 1, 0
    for _ in range(256):
        coefficient = int(mp.floor(x))
        p = coefficient * p_minus_one + p_minus_two
        q = coefficient * q_minus_one + q_minus_two
        if q > denominator_cap:
            break
        result.add((p, q))
        remainder = x - coefficient
        if remainder == 0:
            break
        p_minus_two, p_minus_one = p_minus_one, p
        q_minus_two, q_minus_one = q_minus_one, q
        x = 1 / remainder
    return result


def additive_energy(values: set[int]) -> int:
    sums = Counter(a + b for a in values for b in values)
    return sum(count * count for count in sums.values())


def difference_profile(values: set[int]) -> tuple[int, int, int]:
    if len(values) < 2:
        return 0, 0, 0
    differences = Counter(b - a for a in values for b in values if b > a)
    difference, edges = min(differences.items(), key=lambda item: (-item[1], item[0]))
    starts = [a for a in values if a - difference not in values]
    longest = 0
    for start in starts:
        length = 0
        current = start
        while current + difference in values:
            length += 1
            current += difference
        longest = max(longest, length)
    return difference, edges, longest


def profile_grid(D: int, xi: Fraction, radius: int) -> dict[str, object]:
    x_scale = mp.mpf(D) ** (mp.mpf(5) / 3)
    Q = int(mp.nint(mp.mpf(D) ** (mp.mpf(5) / 9)))
    K = int(mp.nint(x_scale ** (mp.mpf(xi.numerator) / xi.denominator)))
    mode_cap = floor(D * mp.log(2) / (2 * mp.pi))
    ray_rows: dict[int, dict[tuple[int, int], int]] = defaultdict(lambda: defaultdict(int))
    residual_cap = mp.mpf(radius) / K
    for a in range(-mode_cap, mode_cap + 1):
        if a == 0:
            continue
        target = mp.exp(2 * mp.pi * a / D)
        for n in range(Q, 2 * Q):
            center = n * target
            nearest = int(mp.nint(center))
            for n_prime in range(max(Q, nearest - 1), min(2 * Q, nearest + 2)):
                if abs(n_prime - center) <= residual_cap:
                    divisor = gcd(n, n_prime)
                    ray_rows[a][(n_prime // divisor, n // divisor)] += 1
    occupied = set(ray_rows)
    all_rays = [(a, label, multiplicity) for a, labels in ray_rows.items() for label, multiplicity in labels.items()]
    nonconvergent = 0
    multi_label_modes = 0
    for a, labels in ray_rows.items():
        target = mp.exp(2 * mp.pi * a / D)
        conv = convergents(target, 2 * Q)
        if len(labels) > 1:
            multi_label_modes += 1
        for label in labels:
            if label not in conv:
                nonconvergent += 1
    difference, popular_edges, longest_chain = difference_profile(occupied)
    threshold = float((mp.mpf(Q) ** 3 / K) ** (mp.mpf(1) / 4))
    return {
        "D": D,
        "xi": f"{xi.numerator}/{xi.denominator}",
        "Q": Q,
        "K": K,
        "radius": radius,
        "mode_cap": mode_cap,
        "volume_proxy": float(mp.mpf(D) * Q * radius / K),
        "target": Q,
        "total_hits": sum(multiplicity for _, _, multiplicity in all_rays),
        "occupied_modes": len(occupied),
        "ray_count": len(all_rays),
        "max_ray_multiplicity": max((multiplicity for _, _, multiplicity in all_rays), default=0),
        "multi_label_modes": multi_label_modes,
        "nonconvergent_rays": nonconvergent,
        "additive_energy": additive_energy(occupied),
        "popular_difference": difference,
        "popular_difference_edges": popular_edges,
        "longest_popular_chain": longest_chain,
        "cycle125_threshold": threshold,
        "rays_above_cycle125_threshold": sum(multiplicity > threshold for _, _, multiplicity in all_rays),
        "representative_rays": [
            {"a": a, "p": label[0], "q": label[1], "multiplicity": multiplicity}
            for a, label, multiplicity in sorted(all_rays, key=lambda row: (-row[2], row[0], row[1]))[:12]
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    mp.mp.dps = 80
    rows = [profile_grid(D, xi, radius) for D in D_VALUES for xi in XI_VALUES for radius in RADII]
    payload = {
        "artifact_id": "cycle-128-sampled-mellin-profiler-v1",
        "epistemic_status": "OBSERVED",
        "mpmath_version": mp.__version__,
        "decimal_digits": mp.mp.dps,
        "rng": None,
        "rows": rows,
    }
    encoded = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.write:
        if OUTPUT.exists():
            raise SystemExit("refusing to overwrite discovery output")
        OUTPUT.write_text(encoded, encoding="utf-8")
        print(json.dumps({"output": str(OUTPUT.relative_to(ROOT)), "rows": len(rows)}, sort_keys=True))
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
