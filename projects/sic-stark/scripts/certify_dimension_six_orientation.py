#!/usr/bin/env python3
"""Rigorous analytic orientation certificate for the d=6 primitive packet.

For the ray generator used by the exact class-field certificate, the
characteristics (3,5) and (3,4) represent ray logs 1 and 2.  Their
differenced partial-zeta derivatives are twice the logarithms of the
absolute principal overlaps.  Arb enclosures proving both logarithms
positive therefore give

    Im L'_S(0, chi_1) = sqrt(3)/2 * (Z'_1 + Z'_2) > 0.

This certificate is analytic: it uses only the convention-matched
double-sine integral and the exact characteristic-to-ray labels, not the
conjectural algebraic identification with z and w.
"""

from __future__ import annotations

import argparse
from fractions import Fraction

from flint import arb, ctx

from certify_dimension_five_double_sine import overlap_log


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=30)
    parser.add_argument("--tolerance", default="1e-7")
    arguments = parser.parse_args()
    tolerance = Fraction(arguments.tolerance)
    if tolerance <= 0:
        raise ValueError("tolerance must be positive")

    ctx.dps = arguments.digits
    ctx.cap = 6
    beta = (5 + arb(21).sqrt()) / 2

    # Exact labels from dimension_six_ray_recon.gp:
    #   (3,5) -> g^1 and (3,4) -> g^2.
    ray_characteristics = ((1, 3, 5), (2, 3, 4))
    ray_derivatives: dict[int, arb] = {}
    for ray_log, first, second in ray_characteristics:
        logarithm, panels = overlap_log(
            first,
            second,
            beta,
            tolerance,
            dimension=6,
        )
        derivative = 2 * logarithm
        ray_derivatives[ray_log] = derivative
        print(
            f"RAY_LOG_{ray_log}_CHARACTERISTIC=({first},{second}) "
            f"LOG_ABS_OVERLAP={logarithm} "
            f"DIFFERENCED_ZETA_DERIVATIVE={derivative} "
            f"PANELS={panels}"
        )
        print(f"RAY_LOG_{ray_log}_POSITIVE={derivative > 0}")
        if not derivative > 0:
            raise RuntimeError(
                f"failed to certify positivity for ray log {ray_log}"
            )

    imaginary_part = (
        arb(3).sqrt()
        * (ray_derivatives[1] + ray_derivatives[2])
        / 2
    )
    print(f"PRIMITIVE_IMAGINARY_PART={imaginary_part}")
    print(f"PRIMITIVE_IMAGINARY_PART_POSITIVE={imaginary_part > 0}")
    if not imaginary_part > 0:
        raise RuntimeError("failed to certify primitive orientation")


if __name__ == "__main__":
    main()
