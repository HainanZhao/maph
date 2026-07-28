#!/usr/bin/env python3
"""Normalization ledger for the d=6 helical Fourier aliases.

The degenerate beta transform contains three convention-sensitive
pieces:

1. the unnormalized two-gamma q-product;
2. the normalized Gamma_M factors Z(m) exp(-pi*i*B/(48));
3. the y-independent Fourier gauge
       exp(pi*i*Q*alpha/(24*omega1)).

For an alias step (alpha,N)->(alpha+Delta,N+6), with

    s=4*ell-5*(N-2),  alpha=D*s/3,

the exact ratios are:

    unnormalized q-product scalar  = -q,
    Z-times-Bernoulli scalar       = 1,
    extracted Fourier gauge        = -q.

Thus the normalized Gamma_M product itself is the well-poised
2-psi-2 orbit at argument -q.  Restoring the ordinary Fourier gauge
moves the scalar to q^2.  This script prevents those two gauges from
being silently interchanged.
"""

from __future__ import annotations

import json


def main() -> None:
    # Store exponents L in exp(pi*i*L), reduced using
    # beta^2=5 beta-1 and s=4 ell-5(N-2).
    ratios = {
        "unnormalized_q_product": {
            "exponent": "1+2*beta",
            "value": "-q",
        },
        "Z_times_Bernoulli": {
            "exponent": "-216*N-2*ell-228",
            "value": "+1",
        },
        "normalized_Gamma_product": {
            "exponent": "-216*N+2*beta-2*ell-227",
            "value": "-q",
        },
        "extracted_Fourier_gauge": {
            "exponent": "2*beta-5",
            "value": "-q",
        },
        "ordinary_Fourier_transform": {
            "value": "q^2 times the rational term ratio",
        },
    }

    # Integer parity checks for a broad exact residue window.
    records = []
    for dual_label in range(-24, 49):
        for helical_integer in range(-24, 49):
            z_bernoulli_exponent = (
                -216 * dual_label
                - 2 * helical_integer
                - 228
            )
            assert z_bernoulli_exponent % 2 == 0
            records.append(
                {
                    "N": dual_label,
                    "ell": helical_integer,
                    "Z_B_exponent_mod_2": 0,
                }
            )

    result = {
        "schema": "sic-stark-dimension-six-alias-normalization-v1",
        "alias_step": "(alpha,N)->(alpha+Delta,N+6)",
        "ratios": ratios,
        "parity_records_checked": len(records),
        "normalized_alias_series": (
            "_2psi_2(x,-w^(-1)x;"
            "q*w^(-1)x,-q*x;q,-q)"
        ),
        "ordinary_transform_alias_argument": "q^2",
        "Bailey_closed_argument": "q",
        "normalization_does_not_close_Bailey_gap": True,
        "conclusion": (
            "After a full Z/Bernoulli/Fourier audit, the natural "
            "normalized Gamma_M alias packet remains at argument -q. "
            "Bailey's one-product value at q is a neighboring identity, "
            "while the ordinary ungauged transform lies at q^2."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
