#!/usr/bin/env python3
"""Exact bounded search for the C98 degree-(4,3,6) ansatz.

The search is intentionally narrower than the Diophantine problem: it only
enumerates the frozen coefficient box and solves the leading equations in a
fixed order.  It never searches large integer triples directly.
"""
from __future__ import annotations

import argparse
import json
import math
import time
from pathlib import Path

B = 648
NODE_CAP = 100_000_000
WALL_CAP = 900.0


def coefficients(a, b, c, p, q, r, s, u, v):
    """Hard-coded coefficient route, ordered by powers t^12,...,t^0."""
    return [
        a**3 + p**2 * r + r**2,
        3 * a**2 * b + p**2 * s + 2 * p * q * r + 2 * r * s,
        3 * a**2 * c + 3 * a * b**2 + p**2 * u + 2 * p * q * s + q**2 * r + 2 * r * u + s**2,
        6 * a * b * c + b**3 + p**2 * v + 2 * p * q * u + q**2 * s + 2 * r * v + 2 * s * u,
        3 * a * c**2 + 3 * b**2 * c + 2 * p * q * v + q**2 * u + 2 * s * v + u**2,
        3 * b * c**2 + q**2 * v + 2 * u * v,
        c**3 + v**2 - 2,
    ]


def control_coefficients(a, b, c, p, q, r, s, u, v):
    """Published adjacent-equation control: z²+y²z+x³+x+1."""
    out = coefficients(a, b, c, p, q, r, s, u, v)
    # Replacing x^3-2 by x^3+x+1 adds x+3: t^4, t^2, and t^0.
    out[4] += a
    out[5] += b
    out[6] += c + 3
    return out


def bounded(value):
    return -B <= value <= B


def run():
    started = time.monotonic()
    nodes = 0
    roots = []
    hits = []
    cap = False
    # Leading t^12 equation is quadratic in r; enumerate its exact roots.
    for a in range(-B, B + 1):
        if a == 0:
            continue
        for p in range(1, B + 1):
            disc = p**4 - 4 * a**3
            if disc < 0:
                continue
            sq = math.isqrt(disc)
            if sq * sq != disc:
                continue
            for num in (-p**2 + sq, -p**2 - sq):
                if num % 2:
                    continue
                r = num // 2
                if r == 0 or not bounded(r):
                    continue
                roots.append((a, p, r))

    for a, p, r in roots:
        den = p**2 + 2 * r
        for q in range(-B, B + 1):
            for u in range(-B, B + 1):
                nodes += 1
                if nodes > NODE_CAP or time.monotonic() - started > WALL_CAP:
                    cap = True
                    break
                # The constant equation forces c=1 and v=±1 in the box.
                for c, v in ((1, -1), (1, 1)):
                    numer_b = -v * (q**2 + 2 * u)
                    if numer_b % 3:
                        continue
                    b = numer_b // 3
                    if not bounded(b):
                        continue
                    numer_s = v * a**2 * (q**2 + 2 * u) - 2 * p * q * r
                    if den == 0:
                        if numer_s != 0:
                            continue
                        s_values = range(-B, B + 1)
                    else:
                        if numer_s % den:
                            continue
                        s0 = numer_s // den
                        s_values = (s0,)
                    for s in s_values:
                        if not bounded(s):
                            continue
                        vals = (a, b, c, p, q, r, s, u, v)
                        if all(x == 0 for x in coefficients(*vals)):
                            hits.append({"coefficients": list(vals), "t_start": 10**13})
            if cap:
                break
        if cap:
            break

    control = [ -108, -24, -2, 36, 2, 648, 288, 50, 3 ]
    payload = {
        "cycle": 98,
        "box": B,
        "roots_t12": len(roots),
        "nodes": nodes,
        "status": "CAP" if cap else "EXHAUSTED",
        "hits": hits,
        "control_coefficients": control_coefficients(*control),
        "control_pass": all(x == 0 for x in control_coefficients(*control)),
        "wall_seconds": time.monotonic() - started,
    }
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    payload = run()
    text = json.dumps(payload, sort_keys=True, indent=2) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    if not payload["control_pass"]:
        raise SystemExit("published adjacent-family control failed")


if __name__ == "__main__":
    main()
