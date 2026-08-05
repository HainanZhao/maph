#!/usr/bin/env python3
"""Exact algebra check for C77's endpoint-interpolation target relation."""

import json
import sympy as sp


q, t, a, b, c = sp.symbols("q t a b c")
q_of_t = (1 + t) / 2
partial_sums = (0, a, a + b, a + b + c)


def main():
    checks = []
    for s in partial_sums:
        target_q = q + (1 - q) * s
        endpoint_mix = (1 - t) * (sp.Rational(1, 2) + sp.Rational(1, 2) * s) + t
        checks.append(sp.simplify(target_q.subs(q, q_of_t) - endpoint_mix) == 0)
    assert all(checks)
    assert sp.simplify(q_of_t - (1 - q_of_t)) == t
    print(json.dumps({"status": "PASS", "epistemic_status": "PROVED",
                      "ky_fan_target_rows": 4,
                      "endpoint_interpolation_identities": len(checks)},
                     sort_keys=True))


if __name__ == "__main__":
    main()
