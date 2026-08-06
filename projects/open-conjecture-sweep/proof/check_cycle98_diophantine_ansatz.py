#!/usr/bin/env python3
"""Independent exact checker for the C98 ansatz replay."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def add(x, y):
    out = [0] * max(len(x), len(y))
    for i, v in enumerate(x):
        out[i] += v
    for i, v in enumerate(y):
        out[i] += v
    return out


def mul(x, y):
    out = [0] * (len(x) + len(y) - 1)
    for i, a in enumerate(x):
        for j, b in enumerate(y):
            out[i + j] += a * b
    return out


def scale(x, k):
    return [k * v for v in x]


def pow_poly(x, n):
    out = [1]
    for _ in range(n):
        out = mul(out, x)
    return out


def generic_coefficients(vals):
    a, b, c, p, q, r, s, u, v = vals
    t = [0, 1]
    x = add(add(scale(pow_poly(t, 4), a), scale(pow_poly(t, 2), b)), [c])
    y = add(scale(pow_poly(t, 3), p), scale(t, q))
    z = add(add(add(scale(pow_poly(t, 6), r), scale(pow_poly(t, 4), s)), scale(pow_poly(t, 2), u)), [v])
    poly = add(add(pow_poly(z, 2), mul(pow_poly(y, 2), z)), add(pow_poly(x, 3), [-2]))
    assert all(poly[d] == 0 for d in (1, 3, 5, 7, 9, 11) if d < len(poly))
    return [poly[d] if d < len(poly) else 0 for d in (12, 10, 8, 6, 4, 2, 0)]


def generic_adjacent_coefficients(vals):
    """Independent control route for z²+y²z+x³+x+1."""
    out = generic_coefficients(vals)
    a, b, c, *_ = vals
    out[4] += a
    out[5] += b
    out[6] += c + 3
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("replay", type=Path)
    args = parser.parse_args()
    data = json.loads(args.replay.read_text(encoding="utf-8"))
    assert data["cycle"] == 98
    assert data["box"] == 648
    assert data["status"] in {"EXHAUSTED", "CAP"}
    assert data["control_pass"] is True
    assert data["control_coefficients"] == [0] * 7
    control = [-108, -24, -2, 36, 2, 648, 288, 50, 3]
    assert generic_adjacent_coefficients(control) == [0] * 7
    for row in data["hits"]:
        vals = row["coefficients"]
        assert len(vals) == 9 and all(-648 <= x <= 648 for x in vals)
        assert vals[0] and vals[3] > 0 and vals[5]
        assert generic_coefficients(vals) == [0] * 7
    print(json.dumps({"status": "OK", "hits": len(data["hits"]), "replay_status": data["status"]}, sort_keys=True))


if __name__ == "__main__":
    main()
