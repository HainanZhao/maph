#!/usr/bin/env python3
"""Bilateral 2-psi-2 structure of the d=6 helical alias sum.

Fix one of the three alias classes z mod 3.  Advancing once in that
class sends

    (alpha,N) -> (alpha+Delta,N+6)

and multiplies both q-product arguments by q=e^(2*pi*i*beta).  If
x=e^(2*pi*i*u_1), w=e^(2*pi*i/6), the unnormalized two-gamma product has
term ratio

    -q (1-x)(1+w^(-1)x)
       / ((1+qx)(1-qw^(-1)x)).

The root that could have depended on the TCC frequency is

    rho=i^(19N-s),  s=4ell-5(N-2),

but 19N-s=24N-4ell-10 is always 2 modulo 4.  Hence rho=-1 in every
frequency sector.

After an alternating alias weight (-1)^k, the orbit is exactly Bailey's
bilateral 2-psi-2 sum

  _2psi_2(x,-w^-1 x; q w^-1 x,-q x; q,q),

with Bailey parameter A=w^-1*x^2.  The denominator parameters are
Aq/x and Aq/(-w^-1*x), and Bailey's argument -Aq/(bc) is q.

AFK's even-dimensional quasiperiodicity proves that the primitive
quotient is antiperiodic under the helical wrap.  On the dual side this
shifts the character lattice by one half; it does not supply the
alternating alias weight below.  Bailey's product therefore remains a
nearby comparison identity, not yet the desired raw alias evaluation.
"""

from __future__ import annotations

import json


DIMENSION = 6


def orientation_exponent_mod_four(
    dual_label: int,
    helical_integer: int,
) -> int:
    raw_discrete_mode = 5 * (dual_label - 2)
    s_parameter = 4 * helical_integer - raw_discrete_mode
    return (19 * dual_label - s_parameter) % 4


def main() -> None:
    orientation_records = []
    for dual_label in range(24):
        for helical_integer in range(-12, 18):
            exponent = orientation_exponent_mod_four(
                dual_label,
                helical_integer,
            )
            assert exponent == 2
            orientation_records.append(
                {
                    "N": dual_label,
                    "ell": helical_integer,
                    "rho_exponent_mod_4": exponent,
                    "rho": "-1",
                }
            )

    # Parameter identities are recorded as monomials in q, w, x.
    # Let top parameters b=x, c=-w^-1*x and Bailey A=w^-1*x^2.
    # Then
    #
    #   A*q/b = q*w^-1*x,
    #   A*q/c = -q*x,
    #   -A*q/(b*c) = q.
    bailey_parameters = {
        "top_b": "x",
        "top_c": "-w^(-1)*x",
        "Bailey_A": "w^(-1)*x^2",
        "bottom_Aq_over_b": "q*w^(-1)*x",
        "bottom_Aq_over_c": "-q*x",
        "Bailey_argument_minus_Aq_over_bc": "q",
    }

    # Without the alternating weight, the argument is -q.  Multiplying
    # the k-th alias term by (-1)^k changes it to q.
    result = {
        "schema": "sic-stark-dimension-six-alias-hypergeometric-v1",
        "orientation_records_checked": len(orientation_records),
        "orientation_root_is_universally_minus_one": True,
        "unnormalized_orbit_ratio": (
            "-q*(1-x)*(1+w^(-1)*x)/"
            "((1+q*x)*(1-q*w^(-1)*x))"
        ),
        "raw_bilateral_series": (
            "_2psi_2(x,-w^(-1)x;"
            "q*w^(-1)x,-q*x;q,-q)"
        ),
        "alternating_weight": "(-1)^k",
        "weighted_bilateral_series": (
            "_2psi_2(x,-w^(-1)x;"
            "q*w^(-1)x,-q*x;q,q)"
        ),
        "bailey_parameters": bailey_parameters,
        "Bailey_parameter_match_exact": True,
        "radial_convergence_condition": "|q|<1",
        "unit_circle_value_requires_boundary_continuation": True,
        "AFK_wrap_supplies_alternating_weight_proved": False,
        "conclusion": (
            "Every primitive helical alias class is one dual-index "
            "sign away from Bailey's closed 2-psi-2 summation.  AFK "
            "wrap holonomy shifts the dual lattice instead of supplying "
            "that sign.  The remaining analytic gate is therefore the "
            "special well-poised 2-psi-2 value at argument -q, together "
            "with its modular boundary convention."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
