"""Exact C92 common-witness control for intersection-closed families on [4]."""
from __future__ import annotations
import hashlib
import json

N = 4
SETS = range(1 << N)
FULL = (1 << N) - 1


def closed(mask: int) -> bool:
    rows = [a for a in SETS if mask >> a & 1]
    return all(mask >> (a & b) & 1 for a in rows for b in rows)


def retain(mask: int) -> bool:
    rows = [a for a in SETS if mask >> a & 1]
    return bool(mask & 1) and len(rows) >= 2 and all(any(a >> i & 1 for a in rows) for i in range(N)) and closed(mask)


def witnesses(mask: int, t: int) -> int:
    rows = [a for a in SETS if mask >> a & 1]
    weights = {a: (3 ** (N - a.bit_count()) if t == 3 else 1) for a in rows}
    total = sum(weights.values())
    return sum(1 << i for i in range(N) if 2 * sum(weights[a] for a in rows if not (a >> i & 1)) >= total)


def rows_from_masks(masks):
    return tuple((mask, witnesses(mask, 3), witnesses(mask, 1)) for mask in sorted(masks) if retain(mask))


def direct():
    return rows_from_masks(range(1 << 16))


def closure(seed: int) -> int:
    mask = seed
    while True:
        rows = [a for a in SETS if mask >> a & 1]
        expanded = mask
        for a in rows:
            for b in rows:
                expanded |= 1 << (a & b)
        if expanded == mask:
            return mask
        mask = expanded


def generated():
    return rows_from_masks({closure(seed) for seed in range(1 << 16)})


def digest(rows):
    return hashlib.sha256("".join(f"{m:04x}:{a:x}:{b:x}\n" for m, a, b in rows).encode()).hexdigest()


def payload():
    first, second = direct(), generated()
    assert first == second
    crossing = next((row for row in first if not (row[1] & row[2])), None)
    low_empty = next((row for row in first if not row[1]), None)
    uniform_empty = next((row for row in first if not row[2]), None)
    return {"status":"PASS", "epistemic_status":"PROVED", "family_masks":65536,
            "retained":len(first), "row_sha256":digest(first), "route_agreement":True,
            "crossing":crossing, "low_temperature_empty":low_empty,
            "uniform_empty":uniform_empty,
            "claim_boundary":"One n=4 full-universe control only; not Frankl or a temperature interpolation theorem."}


if __name__ == "__main__": print(json.dumps(payload(), sort_keys=True))
