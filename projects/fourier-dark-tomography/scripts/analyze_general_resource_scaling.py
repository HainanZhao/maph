#!/usr/bin/env python3
"""Ideal local resource scaling for the all-mode Fourier-cat construction.

The probes are conservatively divided by m-1, which gives spectral norm at
most one.  The formulas are for independent selected Poisson channels at the
nominal device.  They distinguish:

* algebraic rank;
* the local background-free Cramer--Rao trace;
* the trials needed merely to observe a target number of reference events;
* the background-dominated scaling.

They are not a hardware model: source success, transmission, detector
efficiency, distinguishability, and calibration uncertainty must multiply or
augment the stated probabilities.
"""

from __future__ import annotations

import argparse
import cmath
import math


def alpha_squared(modes: int, photons: int) -> float:
    if modes < 2 or photons <= 2 or photons % modes:
        raise ValueError("require m>=2, n>2, and n divisible by m")
    return photons * modes ** (1 - photons)


def cyclic_inverse_frobenius(
    modes: int, photons: int, charge: int
) -> float:
    """Squared Frobenius norm of ((n-1)I+P_c)^(-1)."""
    return sum(
        1
        / abs(
            photons
            - 1
            + cmath.exp(2j * math.pi * charge * index / modes)
        )
        ** 2
        for index in range(modes)
    )


def allocation_coefficients(
    modes: int, photons: int
) -> tuple[float, float]:
    """Trace coefficients A_R,A_T for the two probe-pair allocations."""
    common = sum(
        cyclic_inverse_frobenius(modes, photons, charge)
        for charge in range(1, (modes - 1) // 2 + 1)
    )
    real = common
    imaginary = common
    if modes % 2 == 0:
        edges = modes / 2
        real += edges / photons**2
        imaginary += edges / (photons - 2) ** 2
    return real, imaginary


def optimal_pair_allocation(
    modes: int, photons: int
) -> tuple[float, float]:
    """A-optimal fractions for the R and T sign pairs."""
    real, imaginary = allocation_coefficients(modes, photons)
    root_real, root_imaginary = math.sqrt(real), math.sqrt(imaginary)
    total = root_real + root_imaginary
    return root_real / total, root_imaginary / total


def cramer_rao_trace(
    modes: int, photons: int, total_trials: float
) -> float:
    """Minimum ideal local covariance trace under optimal pair allocation."""
    real, imaginary = allocation_coefficients(modes, photons)
    return (
        (math.sqrt(real) + math.sqrt(imaginary)) ** 2
        / (4 * total_trials * alpha_squared(modes, photons))
    )


def normalized_reference_probabilities(
    modes: int, photons: int, epsilon: float
) -> tuple[float, float]:
    """Leading R and worst-case T reference probabilities per outcome."""
    alpha2 = alpha_squared(modes, photons)
    scale = modes - 1
    real = epsilon**2 * alpha2 * (photons / scale) ** 2
    imaginary_gain = photons - 2 if modes % 2 == 0 else photons
    imaginary = (
        epsilon**2 * alpha2 * (imaginary_gain / scale) ** 2
    )
    return real, imaginary


def trials_for_reference_counts(
    modes: int,
    photons: int,
    epsilon: float,
    target_counts: float,
) -> float:
    """Total trials giving target expected counts in the weakest sign bin."""
    allocation = optimal_pair_allocation(modes, photons)
    probabilities = normalized_reference_probabilities(
        modes, photons, epsilon
    )
    # Each pair allocation is split equally between its positive and
    # negative settings.
    weakest_rate = min(
        pair_fraction * probability / 2
        for pair_fraction, probability in zip(allocation, probabilities)
    )
    return target_counts / weakest_rate


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epsilon", type=float, default=0.05)
    parser.add_argument("--target-counts", type=float, default=10.0)
    parser.add_argument(
        "--modes", type=int, nargs="+", default=[4, 6, 8, 10]
    )
    args = parser.parse_args()
    print(
        "m n alpha^2 p_ref_min w_R w_T "
        "N*avgCRLB N_for_target_counts"
    )
    for modes in args.modes:
        photons = 4 if modes == 2 else modes
        dimension = modes * (modes - 1)
        alpha2 = alpha_squared(modes, photons)
        probabilities = normalized_reference_probabilities(
            modes, photons, args.epsilon
        )
        allocation = optimal_pair_allocation(modes, photons)
        trace_coefficient = cramer_rao_trace(modes, photons, 1.0)
        trials = trials_for_reference_counts(
            modes, photons, args.epsilon, args.target_counts
        )
        print(
            f"{modes:2d} {photons:2d} {alpha2:.3e} "
            f"{min(probabilities):.3e} "
            f"{allocation[0]:.4f} {allocation[1]:.4f} "
            f"{trace_coefficient / dimension:.3e} {trials:.3e}"
        )


if __name__ == "__main__":
    main()
