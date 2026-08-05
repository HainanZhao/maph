#!/usr/bin/env python3
"""Exact independent check of the Cycle-5 difference-set obstruction."""

from __future__ import annotations

import json


def prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    return factors


def least_primitive_root(prime: int) -> int:
    factors = prime_factors(prime - 1)
    for candidate in range(2, prime):
        if all(pow(candidate, (prime - 1) // factor, prime) != 1 for factor in factors):
            return candidate
    raise AssertionError("primitive root not found")


def main() -> None:
    dimension, prime = 13, 199
    group_order = (prime - 1) // 2
    primitive_root = least_primitive_root(prime)
    bad: list[int] = []
    residue = 1
    for exponent in range(group_order):
        signed_residue = min(residue, prime - residue)
        if (dimension + 1) * signed_residue < prime:
            bad.append(exponent)
        residue = residue * primitive_root % prime
    differences = sorted({(left - right) % group_order for left in bad for right in bad})
    assert differences == list(range(group_order))
    print(
        json.dumps(
            {
                "status": "PASS",
                "epistemic_status": "PROVED",
                "dimension": dimension,
                "prime": prime,
                "primitive_root": primitive_root,
                "group_order": group_order,
                "bad_exponents": bad,
                "bad_set_size": len(bad),
                "difference_set_size": len(differences),
                "incompatibility_edge_count": 0,
                "conclusion": "B-B=H_199, so the Cycle-5 incompatibility graph is empty for every state.",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
