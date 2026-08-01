#!/usr/bin/env python3
"""Enumerate AFK (d,r) skeletons, without a ray-support verdict.

This is discovery-only.  It records the finite tuple/conductor skeleton
needed for a successor to the invalid maximal-order Phase-1 scan.  It never
constructs a ray group or labels a tuple eligible.
"""

from __future__ import annotations

from collections import Counter
from hashlib import sha256
import json
from math import isqrt
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIMIT = 1024
OUTPUT = ROOT / "discovery" / "tcc-sweep-afk-tuple-skeleton-d1024-v1.json"


def squarefree_part(value: int) -> int:
    result = 1
    divisor = 2
    while divisor * divisor <= value:
        exponent = 0
        while value % divisor == 0:
            value //= divisor
            exponent += 1
        if exponent % 2:
            result *= divisor
        divisor += 1 if divisor == 2 else 2
    return result * value


def fundamental_discriminant(squarefree: int) -> int:
    return squarefree if squarefree % 4 == 1 else 4 * squarefree


def divisors(value: int) -> list[int]:
    small: list[int] = []
    large: list[int] = []
    for divisor in range(1, isqrt(value) + 1):
        if value % divisor == 0:
            small.append(divisor)
            if divisor * divisor != value:
                large.append(value // divisor)
    return small + list(reversed(large))


def main() -> None:
    records: list[dict[str, object]] = []
    for dimension in range(4, LIMIT + 1):
        numerator = dimension * dimension - 1
        for rank in range(1, dimension // 2):
            denominator = rank * (dimension - rank)
            if numerator % denominator:
                continue
            n = numerator // denominator
            if n <= 4:
                continue
            field_radicand = squarefree_part(n * (n - 4))
            discriminant = fundamental_discriminant(field_radicand)
            # AFK gives epsilon^j + epsilon^-j = d_j-1 = n-2 and
            # f_j=(epsilon^j-epsilon^-j)/sqrt(Delta_0), hence this square.
            f_square = n * (n - 4) // discriminant
            f_j = isqrt(f_square)
            if f_j * f_j != f_square:
                raise AssertionError((dimension, rank, n, discriminant, f_square))
            conductors = divisors(f_j)
            records.append(
                {
                    "d": dimension,
                    "r": rank,
                    "n": n,
                    "field_radicand": field_radicand,
                    "fundamental_discriminant": discriminant,
                    "f_j": f_j,
                    "allowed_form_conductors": conductors,
                }
            )
    canonical = [record for record in records if record["r"] == 1]
    noncanonical = [record for record in records if record["r"] != 1]
    result = {
        "schema": "tcc-sweep-afk-tuple-skeleton-v1",
        "claim_tag": "OBSERVED",
        "scope": "AFK pair/triple and allowed-conductor skeleton for d<=1024; no form-class or ray-support enumeration",
        "derivation": "AFK admissibility nr(d-r)=d^2-1, d_j+1=n, and f_j^2*Delta_0=n(n-4)",
        "dimension_limit": LIMIT,
        "record_count": len(records),
        "canonical_rank_one_count": len(canonical),
        "noncanonical_rank_count": len(noncanonical),
        "distinct_fundamental_discriminant_count": len({record["fundamental_discriminant"] for record in records}),
        "max_allowed_conductor": max(record["f_j"] for record in records),
        "conductor_stratum_count": sum(len(record["allowed_form_conductors"]) for record in records),
        "records_by_dimension": dict(sorted(Counter(record["d"] for record in records).items())),
        "records": records,
    }
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    result["self_sha256_excluding_hash"] = sha256(serialized.encode()).hexdigest()
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("TCC_SWEEP_AFK_TUPLE_SKELETON=PASS")


if __name__ == "__main__":
    main()
