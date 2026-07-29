#!/usr/bin/env python3
"""Independent crosscheck of the tilted-integral evaluator against the
factorized q-Pochhammer continuation, implemented purely in mpmath.

The factorized route computes the same lens gamma as a product of
``level`` standard factors, each a ratio of q-Pochhammer symbols.
The tilted route computes the same standard factor as
``exp(pi*i*B22/2) * gamma2(sinh-integral)``.  They must agree at
interior points where both converge.
"""

from __future__ import annotations

from fractions import Fraction
import sys

import mpmath as mp

sys.path.insert(0, ".")
from dimension_six_tilted_integral_rehearsal import (
    PARAMETERS,
    gamma_standard_tilted,
    geodesic_point,
    primitive_alpha,
    tilted_components,
    beta_endpoint,
)


def q_pochhammer_inf(a, q, tol=None):
    """(a; q)_inf = prod_{n=0}^inf (1 - a*q^n)."""
    if tol is None:
        tol = mp.mpf(10) ** (-(mp.mp.dps + 5))
    product = mp.mpc(1)
    n = 0
    while True:
        factor = 1 - a * q**n
        product *= factor
        if abs(a * q**n) < tol:
            break
        n += 1
        if n > 200000:
            raise RuntimeError("q-Pochhammer did not converge")
    return product


def gamma_standard_factorized(z, omega_one):
    """Factorized standard factor via q-Pochhammer."""
    q = mp.e ** (2j * mp.pi * omega_one)
    q_tilde = mp.e ** (-2j * mp.pi / omega_one)
    return q_pochhammer_inf(
        q_tilde * mp.e ** (2j * mp.pi * z / omega_one), q_tilde
    ) / q_pochhammer_inf(mp.e ** (2j * mp.pi * z), q)


def gamma_lens_factorized_mp(mu, discrete, omega_one, dimension):
    """Factorized lens gamma in mpmath."""
    par = PARAMETERS[dimension]
    level, p_parameter = par["level"], par["p"]
    result = mp.mpc(1)
    for gamma_index in range(level):
        delta_index = (
            p_parameter * gamma_index
            - p_parameter * discrete
        ) % level
        z = (mu + omega_one * delta_index + gamma_index) / level
        result *= gamma_standard_factorized(z, omega_one)
    return result


def crosscheck(dimension, s, dps=40):
    """Compare tilted vs factorized kernel at an interior point."""
    with mp.workdps(dps + 10):
        tau = geodesic_point(dimension, s)
        par = PARAMETERS[dimension]
        omega_one = par["level"] * tau - par["r"]
        alpha = primitive_alpha(dimension, tau)

        # Tilted route
        tilted_kernel = gamma_standard_tilted_factor(
            alpha, par["discrete"], omega_one, dimension
        ) * gamma_standard_tilted_factor(
            -alpha,
            par["reflected_total"] - par["discrete"],
            omega_one,
            dimension,
        )

        # Factorized route
        factored_kernel = gamma_lens_factorized_mp(
            alpha, par["discrete"], omega_one, dimension
        ) * gamma_lens_factorized_mp(
            -alpha,
            par["reflected_total"] - par["discrete"],
            omega_one,
            dimension,
        )

        relative = abs(tilted_kernel / factored_kernel - 1)
        agreement = float(-mp.log10(relative)) if relative > 0 else dps
        print(f"  d={dimension}  s={float(s):.6f}  "
              f"agreement = {agreement:.1f} digits  "
              f"relative = {mp.nstr(relative, 4)}")
        return agreement


def gamma_standard_tilted_factor(mu, discrete, omega_one, dimension):
    """Tilted lens gamma (re-export for clarity)."""
    par = PARAMETERS[dimension]
    level, p_parameter = par["level"], par["p"]
    result = mp.mpc(1)
    for gamma_index in range(level):
        delta_index = (
            p_parameter * gamma_index
            - p_parameter * discrete
        ) % level
        result *= gamma_standard_tilted(
            (mu + omega_one * delta_index + gamma_index) / level,
            omega_one,
        )
    return result


def main():
    print("Crosscheck: tilted (sinh-integral) vs factorized (q-Pochhammer)")
    print("=" * 60)
    ok = True
    for dim, s_vals, dps in [
        (6, [Fraction(1, 4), Fraction(1, 8), Fraction(1, 16)], 35),
        (4, [Fraction(1, 8), Fraction(1, 16), Fraction(1, 32)], 35),
    ]:
        for s in s_vals:
            agree = crosscheck(dim, s, dps)
            if agree < dps - 10:
                ok = False
    print("=" * 60)
    if ok:
        print("CROSSCHECK_PASSED")
    else:
        print("CROSSCHECK_FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
