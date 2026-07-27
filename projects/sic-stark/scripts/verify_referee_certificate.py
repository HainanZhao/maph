#!/usr/bin/env python3
"""Verify every dimension-four minor certificate by rational arithmetic."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE = ROOT / "certificates" / "dimension-four-certificate.json"
ZERO = (Fraction(0),) * 4


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def mul(a, b):
    out = [Fraction(0)] * 4
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            common = i & j
            scale = (2 if common & 1 else 1) * (5 if common & 2 else 1)
            out[i ^ j] += scale * x * y
    return tuple(out)


def cadd(a, b):
    return add(a[0], b[0]), add(a[1], b[1])


def cneg(a):
    return neg(a[0]), neg(a[1])


def cmul(a, b):
    return add(mul(a[0], b[0]), neg(mul(a[1], b[1]))), add(
        mul(a[0], b[1]), mul(a[1], b[0])
    )


def decode(value):
    return tuple(Fraction(x) for x in value["real"]), tuple(
        Fraction(x) for x in value["imaginary"]
    )


def polynomial(encoded):
    return {int(power): decode(value) for power, value in encoded.items()}


def padd(a, b):
    out = dict(a)
    for power, coefficient in b.items():
        out[power] = cadd(out.get(power, (ZERO, ZERO)), coefficient)
        if out[power] == (ZERO, ZERO):
            del out[power]
    return out


def pmul(a, b):
    out = {}
    for i, x in a.items():
        for j, y in b.items():
            out = padd(out, {i + j: cmul(x, y)})
    return out


def main():
    data = json.loads(CERTIFICATE.read_text())
    section = data["minor_factorization"]
    assert section["coefficient_basis"] == ["1", "sqrt(2)", "sqrt(5)", "sqrt(10)"]
    records = section["minor_certificates"]
    assert len(records) == section["all_minor_count"] == 36

    one = ((Fraction(1), 0, 0, 0), ZERO)
    t = ((0, Fraction(1, 2), 0, Fraction(1, 2)), ZERO)
    relation = {2: one, 1: cneg(t), 0: one}

    seen = set()
    for record in records:
        key = tuple(record["rows"]), tuple(record["columns"])
        assert key not in seen
        seen.add(key)
        assert record["division_remainder"] == {}
        minor = polynomial(record["laurent_minor"])
        shifted_minor = {power + 2: coefficient for power, coefficient in minor.items()}
        quotient = polynomial(record["quotient_after_multiplication_by_x_squared"])
        assert shifted_minor == pmul(relation, quotient), key

    print(f"verified {len(records)} exact minor identities from {CERTIFICATE}")


if __name__ == "__main__":
    main()
