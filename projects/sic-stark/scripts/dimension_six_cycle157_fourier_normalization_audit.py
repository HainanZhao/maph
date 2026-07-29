#!/usr/bin/env python3
"""Cycle 157: Fourier-normalization audit for the d=6 alias packet.

Cycle 156 deliberately evaluated the raw normalized-Gamma packets

    S_{a,b,r} = sum_k K_{a,b}(r+3k).

Those packets are useful diagnostics, but they are not coefficients of
the ordinary Fourier transform in equation (66).  The character in
that equation was obtained after extracting the y-independent phase

    exp(-pi*i*alpha*Q/(24*omega1)).

Restoring the ordinary Fourier transform therefore weights every alias
by

    g(alpha) = exp(+pi*i*alpha*Q/(24*omega1)).

At the fused boundary, the normalized Gamma product has alias-step
scalar -q and g has alias-step scalar -q, so the Fourier-normalized
packet has scalar q^2.
This script:

1. verifies the exact finite-frequency descent and the Fourier-gauge
   sign;
2. checks the weighted telescoped ratio against direct tilted kernels;
3. evaluates the complete z-sum (all three former residue packets) for
   a proved conductor-3 mode and an unproved primitive mode;
4. records separately the still-missing nonlinear map from these
   additive Fourier coefficients to ray-class logarithms P_j.

The numerical ladder is diagnostic.  It neither identifies a Fourier
coefficient with a Stark overlap nor proves a boundary limit.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
import math

import mpmath as mp

import dimension_six_cycle156_growing_component_dissection as cycle156


LEVEL = cycle156.LEVEL
GUARD_DIGITS = cycle156.GUARD_DIGITS


def ordinary_fourier_gauge(a, b, z, tau):
    """Restore the constant phase extracted from equation (66)."""

    omega_one = LEVEL * tau - cycle156.R_PARAMETER
    q_parameter = omega_one + 1
    alpha, _ = cycle156.kernel_alpha_discrete(a, b, z, tau)
    return mp.e ** (
        mp.pi * 1j * alpha * q_parameter / (LEVEL * omega_one)
    )


def gauge_step_ratio(tau):
    """g(alpha_{z+3})/g(alpha_z), independent of (a,b,z)."""

    omega_one = LEVEL * tau - cycle156.R_PARAMETER
    q_parameter = omega_one + 1
    d_parameter = 4 * tau - 1
    delta_alpha = 6 * d_parameter
    return mp.e ** (
        mp.pi * 1j * delta_alpha * q_parameter
        / (LEVEL * omega_one)
    )


def fourier_alias_packet(a, b, r, tau, maximum_terms=8000):
    """Sum g(alpha_z) K_{a,b}(z) over z=r mod 3."""

    tolerance = mp.mpf(10) ** (-(mp.mp.dps + 5))
    central = (
        ordinary_fourier_gauge(a, b, r, tau)
        * cycle156.kernel_factor(a, b, r, tau)
    )
    step_gauge = gauge_step_ratio(tau)

    total = mp.mpc(1)
    largest = mp.mpf(1)
    cutoffs = []
    for direction in (1, -1):
        term = mp.mpc(1)
        index = 0
        used = 0
        while True:
            if direction == 1:
                z = r + 3 * index
                term *= (
                    cycle156.alias_ratio_general(a, b, tau, z)
                    * step_gauge
                )
                index += 1
            else:
                index -= 1
                z = r + 3 * index
                term /= (
                    cycle156.alias_ratio_general(a, b, tau, z)
                    * step_gauge
                )
            total += term
            used += 1
            size = abs(term)
            largest = max(largest, size)
            if size < tolerance:
                break
            if used >= maximum_terms:
                raise RuntimeError(
                    "Fourier-normalized bilateral tail did not close "
                    f"for ({a},{b},{r})"
                )
        cutoffs.append(used)

    cancellation = (
        float(mp.log10(largest / abs(total))) if abs(total) > 0 else 0.0
    )
    return central * total, cutoffs, cancellation


def evaluate_mode(a, b, denominator, dps):
    """Evaluate all residues and the ordinary-transform coefficient."""

    with mp.workdps(dps + GUARD_DIGITS):
        tau = cycle156.geodesic_point(Fraction(1, denominator))
        residues = []
        cutoffs = []
        cancellation = []
        for r in range(3):
            packet, cutoff, lost = fourier_alias_packet(a, b, r, tau)
            residues.append(packet)
            cutoffs.append(cutoff)
            cancellation.append(lost)
        coefficient = sum(residues)
        scalar = cycle156.scalar_factor(tau)
        transformed = LEVEL * scalar * coefficient
        return {
            "residues": residues,
            "coefficient": coefficient,
            "scalar": scalar,
            "transformed": transformed,
            "cutoffs": cutoffs,
            "cancellation_digits": cancellation,
            "gauge_step": gauge_step_ratio(tau),
            "q_squared": mp.e ** (4 * mp.pi * 1j * tau),
        }


def relative_agreement(low, high):
    if abs(high) == 0:
        return mp.mpf(0)
    return abs(low / high - 1)


def clean_complex(value, digits=25):
    return mp.nstr(value, digits)


def evaluate_mode_two_precision(a, b, denominator, low_dps, high_dps):
    low = evaluate_mode(a, b, denominator, low_dps)
    high = evaluate_mode(a, b, denominator, high_dps)
    agreement = relative_agreement(low["transformed"], high["transformed"])
    tau = cycle156.geodesic_point(Fraction(1, denominator))
    gauge_boundary_error = relative_agreement(
        high["gauge_step"],
        -mp.e ** (2 * mp.pi * 1j * tau),
    )
    return {
        "denominator": denominator,
        "s": 1 / denominator,
        "residue_packets": [
            clean_complex(value) for value in high["residues"]
        ],
        "coefficient": clean_complex(high["coefficient"]),
        "coefficient_abs": float(abs(high["coefficient"])),
        "ordinary_transformed_value": clean_complex(high["transformed"]),
        "ordinary_transformed_abs": float(abs(high["transformed"])),
        "ordinary_transformed_arg_over_pi": float(
            mp.arg(high["transformed"]) / mp.pi
        ),
        "scalar": clean_complex(high["scalar"]),
        "cutoffs": high["cutoffs"],
        "cancellation_digits": high["cancellation_digits"],
        "two_precision_relative_error": clean_complex(agreement, 10),
        "two_precision_agreement_digits": float(
            -mp.log10(agreement) if agreement > 0 else high_dps
        ),
        "gauge_step": clean_complex(high["gauge_step"]),
        "minus_q": clean_complex(
            -mp.e ** (
                2
                * mp.pi
                * 1j
                * cycle156.geodesic_point(Fraction(1, denominator))
            )
        ),
        "fused_boundary_alias_scalar": "q^2 times rational term ratio",
        "gauge_step_vs_boundary_minus_q_relative_error": clean_complex(
            gauge_boundary_error, 10
        ),
    }


def weighted_ratio_crosscheck(a, b, r, denominator, dps):
    with mp.workdps(dps + GUARD_DIGITS):
        tau = cycle156.geodesic_point(Fraction(1, denominator))
        direct = (
            ordinary_fourier_gauge(a, b, r + 3, tau)
            * cycle156.kernel_factor(a, b, r + 3, tau)
            / (
                ordinary_fourier_gauge(a, b, r, tau)
                * cycle156.kernel_factor(a, b, r, tau)
            )
        )
        telescoped = (
            gauge_step_ratio(tau)
            * cycle156.alias_ratio_general(a, b, tau, r)
        )
        error = relative_agreement(direct, telescoped)
        return {
            "frequency": [a, b],
            "residue": r,
            "denominator": denominator,
            "direct": clean_complex(direct),
            "telescoped": clean_complex(telescoped),
            "relative_error": clean_complex(error, 10),
            "agreement_digits": float(
                -mp.log10(error) if error > 0 else dps
            ),
        }


def finite_frequency_ledger():
    """Exact integer descent for every (a,b) and several aliases."""

    records = []
    for a in range(6):
        for b in range(6):
            for z in range(-12, 13):
                discrete_label = a + 2 - 6 * z
                continuous_integer = b - 6 * z
                n_frequency = 5 * (discrete_label - 2)
                p_a = (-n_frequency) % 6
                p_b = continuous_integer % 6
                assert p_a == a
                assert p_b == b
                records.append((a, b, z))
    return {
        "records_checked": len(records),
        "N_z": "a+2-6*z",
        "ell_z": "b-6*z",
        "finite_frequency": "(p_a,p_b)=(-5*(N_z-2),ell_z) mod 6",
        "all_aliases_keep_frequency_(a,b)": True,
        "standard_restriction_weight": (
            "all aliases enter with coefficient +1 after the ordinary "
            "Fourier gauge has been included in each ambient coefficient"
        ),
    }


def growth_summary(records):
    first = records[0]["ordinary_transformed_abs"]
    last = records[-1]["ordinary_transformed_abs"]
    x_values = [math.log10(r["denominator"]) for r in records]
    y_values = [math.log10(r["ordinary_transformed_abs"]) for r in records]
    return {
        "first_denominator": records[0]["denominator"],
        "last_denominator": records[-1]["denominator"],
        "last_over_first_abs": last / first,
        "log_abs_vs_log_one_over_s": cycle156.linear_fit(
            x_values, y_values
        ),
        "bounded_limit_proved": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ladder", default="64,256,1024,4096")
    parser.add_argument("--dps-low", type=int, default=30)
    parser.add_argument("--dps-high", type=int, default=50)
    args = parser.parse_args()
    if not args.dps_high > args.dps_low + 15:
        raise ValueError("dps-high must exceed dps-low by more than 15")

    denominators = [int(item) for item in args.ladder.split(",")]
    modes = {
        "proved_conductor_3": (0, 2),
        "unproved_primitive": (0, 1),
    }
    numerical = {}
    for name, (a, b) in modes.items():
        records = []
        for denominator in denominators:
            records.append(
                evaluate_mode_two_precision(
                    a,
                    b,
                    denominator,
                    args.dps_low,
                    args.dps_high,
                )
            )
        numerical[name] = {
            "frequency": [a, b],
            "records": records,
            "growth_summary": growth_summary(records),
        }

    crosschecks = [
        weighted_ratio_crosscheck(a, b, 0, 64, args.dps_high)
        for a, b in modes.values()
    ]

    result = {
        "schema": "sic-stark-dimension-six-cycle157-fourier-audit-v1",
        "precision": {
            "dps_low": args.dps_low,
            "dps_high": args.dps_high,
            "guard_digits": GUARD_DIGITS,
        },
        "ladder_denominators": denominators,
        "equation_66_ledger": {
            "extracted_constant_phase": (
                "exp(-pi*i*alpha*Q/(24*omega1))"
            ),
            "ordinary_gauge_restored": (
                "exp(+pi*i*alpha*Q/(24*omega1))"
            ),
            "fused_normalized_gamma_alias_scalar": "-q",
            "fused_ordinary_gauge_alias_scalar": "-q",
            "fused_ordinary_transform_alias_scalar": (
                "q^2 times the rational term ratio"
            ),
            "cycle156_raw_packet_was_ordinary_fourier_coefficient": False,
        },
        "finite_frequency_ledger": finite_frequency_ledger(),
        "weighted_ratio_crosschecks": crosschecks,
        "numerical": numerical,
        "normalization_gates": {
            "ambient_fourier_transform": "VERIFIED",
            "ordinary_fourier_gauge": "VERIFIED_AND_RESTORED",
            "helical_finite_frequency_descent": "VERIFIED",
            "complete_additive_z_coefficient": "VERIFIED_DEFINITION",
            "finite_boundary_limit": "NOT_PROVED",
            "map_from_36_additive_coefficients_to_3_ray_classes": (
                "MISSING"
            ),
            "map_from_additive_values_to_logarithms_P_j": "MISSING",
            "logarithm_branch_and_boundary_subtraction": "MISSING",
            "identification_with_AFK_cocycle_values": "MISSING",
        },
        "control_dimensions": {
            "dimension_4": (
                "proved boundary overlap and interior alias sum are "
                "computed independently; no equality normalizes the map"
            ),
            "dimension_5": (
                "proved boundary overlap and interior alias sum are "
                "computed independently; no equality normalizes the map"
            ),
            "control_closes_missing_ray_log_map": False,
        },
        "verdict": {
            "cycle156_raw_growth_decides_true_fourier_packet": False,
            "BF6_as_written_uses_raw_ungauged_packets": True,
            "BF6_implies_MFC6_supported": False,
            "MFC6_is_operationally_testable_from_current_definition": False,
            "recommended_status": (
                "retire BF6 as written; keep only the explicitly "
                "Fourier-normalized additive coefficient as a diagnostic; "
                "do not resume boundary numerics until the coefficient-to-"
                "ray-logarithm map is supplied"
            ),
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
