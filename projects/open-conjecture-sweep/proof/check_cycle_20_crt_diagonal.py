#!/usr/bin/env python3
"""Independent exact audit of Cycle 20's CRT two-diagonal controls."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery" / "out" / "cycle20-crt-diagonal"
DOMAINS = ((11, 4), (47, 7), (199, 14))


def local_inverse(p: int, c: int) -> int:
    candidates = [value for value in range(c) if (p * value) % c == 1 % c]
    assert len(candidates) == 1
    return candidates[0]


def independent_counts(p: int, c: int) -> dict[str, int]:
    assert math.gcd(p, c) == 1
    q = p * c
    inv = local_inverse(p, c)
    counts = {
        "comparisons": 0,
        "direct_bad": 0,
        "crt_bad": 0,
        "mismatches": 0,
        "strict_boundary_rows": 0,
    }
    for s in range(q):
        sp, sc = divmod(s, p)[1], divmod(s, c)[1]
        for a in range(q):
            x = (a * s) % q
            xp = ((a % p) * sp) % p
            xc = ((a % c) * sc) % c
            j = ((xc - (xp % c)) * inv) % c
            direct = min(x, q - x) < p
            local = (j == 0) or (j == c - 1 and xp > 0)
            counts["comparisons"] += 1
            counts["direct_bad"] += int(direct)
            counts["crt_bad"] += int(local)
            counts["mismatches"] += int(direct != local)
            counts["strict_boundary_rows"] += int(j == c - 1 and xp == 0)
    return counts


def audit() -> dict[str, object]:
    rows: list[dict[str, int]] = []
    total = 0
    for p, c in DOMAINS:
        summary_path = OUT / f"p{p}-c{c}-summary.tsv"
        mismatch_path = OUT / f"p{p}-c{c}-mismatches.tsv"
        with summary_path.open(newline="", encoding="utf-8") as handle:
            raw_rows = list(csv.DictReader(handle, delimiter="\t"))
        assert len(raw_rows) == 1
        observed = {key: int(value) for key, value in raw_rows[0].items()}
        assert observed["p"] == p and observed["c"] == c
        assert observed["q"] == p * c
        assert observed["inverse"] == local_inverse(p, c)
        expected = independent_counts(p, c)
        for key, value in expected.items():
            assert observed[key] == value, (p, c, key, observed[key], value)
        with mismatch_path.open(encoding="utf-8") as handle:
            mismatch_lines = handle.read().splitlines()
        assert mismatch_lines == [
            "p\tc\ts\ta\tx\txp\txc\tj\tdirect_bad\tcrt_bad"
        ]
        assert expected["mismatches"] == 0
        total += expected["comparisons"]
        rows.append({"p": p, "c": c, **expected})

    assert total == 7_871_973
    canonical = json.dumps(rows, sort_keys=True, separators=(",", ":"))
    return {
        "status": "PASS",
        "claim_tag": "PROVED",
        "domains": rows,
        "total_comparisons": total,
        "canonical_summary_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "claim_boundary": (
            "The exact theorem factorizes one bad-time predicate; it does not "
            "factorize or close the global simultaneous-cover problem."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
