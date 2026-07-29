#!/usr/bin/env python3
"""Cycle 156: proved growing-component dissection inside d=6.

Among the 30 one-sided-growing alias modes, the modulus-three orbit
points (0,2) and (2,0) are NOT Fresnel and have PROVED boundary values
through the conductor-lowered quadratic component (conductor 3, chi_3).
The lower-stratum certificate (scripts/dimension_six_lower_stratum.gp)
proves exp(Z'(0,I)) = nu_{0,2}^2 = Y, where Y is the positive root of
x^4 - x^3 - 3x^2 - x + 1, so nu_{0,2} = sqrt(Y) is the proved overlap
table entry.

This script dissects that proved component:

1. Identify (a,b) of a conductor-lowered growing mode and keep its
   proved overlap sqrt(Y) as an arithmetic reference.  No unsupported
   equality between one raw alias residue and sqrt(Y) is assumed.
2. Compute S_{a,b,r}(gamma(s)) down a geometric s-ladder using the
   tilted sinh-integral route (well-conditioned, unlike the factorized
   q-Pochhammer continuation) and the bilateral alias ratio.
3. Return-ladder dissection: iterate the geodesic by A_6 and measure
   convergence of the raw fixed-label kernel.  The exact multiplier
   psi^2(A_6)=-1 belongs to the transported Kopp/AFK cocycle and is not
   incorrectly imposed on this untransported kernel value.
4. Compare the proved mode (0,2) against one primitive unproved growing
   mode (0,1) at the same s-ladder.
5. Extend the proved r=0 packet to a deeper reduced-precision ladder and
   recombine r=0,1,2 at sparse points, testing whether either the
   individual packet or the three-residue sum stays bounded.

All computation is floating-point mpmath with two-precision agreement
as the conditioning diagnostic.
"""

from __future__ import annotations

from fractions import Fraction
import json
import math

import mpmath as mp


# ---------------------------------------------------------------------
# Constants and geometry
# ---------------------------------------------------------------------

DIMENSION = 6
LEVEL = 24
P_PARAMETER = -115
R_PARAMETER = 5
TRACE = 5
DISCRIMINANT = 21
CENTER = Fraction(5, 2)
REFLECTED_TOTAL = 4
GUARD_DIGITS = 15


def beta_endpoint():
    """Attracting endpoint, recomputed at the active mp precision."""

    return (
        mp.mpf(TRACE) + mp.sqrt(mp.mpf(TRACE ** 2 - 4))
    ) / 2


def a6_contraction():
    """Exact geodesic contraction beta^(-6), at active precision."""

    return beta_endpoint() ** (-6)


def geodesic_point(s):
    """gamma(s) on the A_6 axis; s=0 gives beta."""

    radius = mp.sqrt(mp.mpf(DISCRIMINANT)) / 2
    center = mp.mpf(CENTER.numerator) / CENTER.denominator
    if isinstance(s, Fraction):
        s = mp.mpf(s.numerator) / s.denominator
    else:
        s = mp.mpf(s)
    if s == 0:
        return mp.mpc(center + radius)
    denominator = 1 + s ** 2
    return mp.mpc(
        center + radius * (1 - s ** 2) / denominator,
        radius * 2 * s / denominator,
    )


def mobius_a6(tau):
    """A_6 * tau = (115*tau - 24) / (24*tau - 5)."""

    return (115 * tau - 24) / (24 * tau - 5)


# ---------------------------------------------------------------------
# Bernoulli B_22 and sinh-integral log gamma2
# (adapted from dimension_six_tilted_integral_rehearsal.py)
# ---------------------------------------------------------------------


def bernoulli_b22(z, omega_one, omega_two=1):
    return (
        z ** 2 / (omega_one * omega_two)
        - z * (omega_one + omega_two) / (omega_one * omega_two)
        + (omega_one ** 2 + 3 * omega_one * omega_two + omega_two ** 2)
        / (6 * omega_one * omega_two)
    )


def log_gamma2_strip(z, omega_one):
    """log gamma2(z; omega_one, 1) for 0 < Re z < Re(omega_one)+1."""

    q_period = omega_one + 1
    linear = q_period - 2 * z

    def regularized(t):
        return (
            mp.sinh(linear * t / 2)
            / (2 * t * mp.sinh(omega_one * t / 2) * mp.sinh(t / 2))
            - linear / (omega_one * t ** 2)
        )

    def plain(t):
        return mp.sinh(linear * t / 2) / (
            2 * t * mp.sinh(omega_one * t / 2) * mp.sinh(t / 2)
        )

    margin = min(mp.re(z), mp.re(q_period - z))
    if not margin > 0:
        raise ValueError("argument left the fundamental strip")
    cutoff = (mp.mp.dps + 10) * mp.log(10) / margin
    delta = mp.mpf("1e-4")

    order = 8 + mp.mp.dps // 5

    def h_coefficients(a):
        return [
            a ** (2 * n) / (mp.mpf(4) ** n * mp.factorial(2 * n + 1))
            for n in range(order)
        ]

    numerator = h_coefficients(linear)
    first = h_coefficients(omega_one)
    second = h_coefficients(mp.mpf(1))
    denominator = [
        sum(first[i] * second[n - i] for i in range(n + 1))
        for n in range(order)
    ]
    inverse = [mp.mpc(0)] * order
    inverse[0] = 1 / denominator[0]
    for n in range(1, order):
        inverse[n] = (
            -sum(
                denominator[i] * inverse[n - i]
                for i in range(1, n + 1)
            )
            / denominator[0]
        )
    ratio_series = [
        sum(numerator[i] * inverse[n - i] for i in range(n + 1))
        for n in range(order)
    ]
    series_part = sum(
        (linear / omega_one)
        * ratio_series[n + 1]
        * delta ** (2 * n + 1)
        / (2 * n + 1)
        for n in range(order - 1)
    )

    near = mp.quad(
        regularized,
        [delta, mp.mpf("0.01"), mp.mpf("0.1"), 1],
    )
    far_points = [mp.mpf(1)]
    node = mp.mpf(10)
    while node < cutoff:
        far_points.append(node)
        node *= 10
    far_points.append(cutoff)
    far = mp.quad(plain, far_points)
    return series_part + near + far - linear / omega_one


def gamma_standard_tilted(z, omega_one):
    """Standard Faddeev gamma_2 via sinh-integral, with shifts."""

    z = mp.mpc(z)
    shifted = z
    prefactor = mp.mpc(1)
    while mp.re(shifted) < 1:
        prefactor /= 2 * mp.sin(mp.pi * shifted / omega_one)
        shifted += 1
    while mp.re(shifted) > mp.re(omega_one):
        shifted -= 1
        prefactor *= 2 * mp.sin(mp.pi * shifted / omega_one)
    return prefactor * mp.e ** (
        mp.pi * 1j * bernoulli_b22(z, omega_one) / 2
        + log_gamma2_strip(shifted, omega_one)
    )


def gamma_lens_tilted(mu, discrete, omega_one):
    """24-factor lens gamma via S--S equation (15), tilted route."""

    result = mp.mpc(1)
    for gamma_index in range(LEVEL):
        delta_index = (
            P_PARAMETER * gamma_index - P_PARAMETER * discrete
        ) % LEVEL
        result *= gamma_standard_tilted(
            (mu + omega_one * delta_index + gamma_index) / LEVEL,
            omega_one,
        )
    return result


# ---------------------------------------------------------------------
# General-(a,b,r) kernel and alias packet
# ---------------------------------------------------------------------


def kernel_alpha_discrete(a, b, z, tau):
    """Return (alpha, discrete) for K_{a,b}(z; tau)."""

    d_parameter = 4 * tau - 1
    alpha = d_parameter * (4 * b - 5 * a) / 3 + 2 * d_parameter * z
    discrete = a + 2 - 6 * z
    return alpha, discrete


def kernel_factor(a, b, z, tau):
    """K_{a,b}(z; tau) = G_tau(alpha, N) * G_tau(-alpha, 4-N) via tilted route."""

    omega_one = LEVEL * tau - R_PARAMETER
    alpha, discrete = kernel_alpha_discrete(a, b, z, tau)
    first = gamma_lens_tilted(alpha, discrete, omega_one)
    second = gamma_lens_tilted(
        -alpha, REFLECTED_TOTAL - discrete, omega_one
    )
    return first * second


def scalar_factor(tau):
    """Gamma_M(Q, 0; tau) via tilted route."""

    omega_one = LEVEL * tau - R_PARAMETER
    return gamma_lens_tilted(mp.mpc(omega_one + 1), 0, omega_one)


def alias_ratio_general(a, b, tau, z):
    """K_{a,b}(z+3; tau) / K_{a,b}(z; tau) from q-Pochhammer telescoping."""

    omega_one = LEVEL * tau - R_PARAMETER
    q_lens = mp.e ** (2j * mp.pi * tau)
    q_lens_tilde = mp.e ** (2j * mp.pi * mobius_a6(tau))

    alpha, discrete = kernel_alpha_discrete(a, b, z, tau)

    def variables(mu, label):
        x_value = mp.e ** (2j * mp.pi * (mu + label) / LEVEL)
        a_value = q_lens_tilde * mp.e ** (
            2j
            * mp.pi
            * (mu - P_PARAMETER * label * omega_one)
            / (LEVEL * omega_one)
        )
        return x_value, a_value

    x_first, a_first = variables(alpha, discrete)
    x_second, a_second = variables(
        -alpha, REFLECTED_TOTAL - discrete
    )
    return (
        (1 - x_first) / (1 - a_first)
        * (1 - a_second / q_lens_tilde)
        / (1 - x_second / q_lens)
    )


def alias_packet(a, b, r, tau, maximum_terms=8000):
    """S_{a,b,r}(s) = sum_k K_{a,b}(r+3k; tau).

    Returns (packet, central_kernel, cutoffs, cancellation_digits,
    largest_term_abs).
    """

    tolerance = mp.mpf(10) ** (-(mp.mp.dps + 5))
    central = kernel_factor(a, b, r, tau)

    total = mp.mpc(1)  # normalized at k=0
    largest = mp.mpf(1)
    cutoffs = []

    for direction in (1, -1):
        term = mp.mpc(1)
        index = 0
        used = 0
        while True:
            if direction == 1:
                z = r + 3 * index
                term *= alias_ratio_general(a, b, tau, z)
                index += 1
            else:
                index -= 1
                z = r + 3 * index
                term /= alias_ratio_general(a, b, tau, z)
            total += term
            used += 1
            size = abs(term)
            if size > largest:
                largest = size
            if size < tolerance:
                break
            if used >= maximum_terms:
                raise RuntimeError(
                    f"bilateral alias tail did not close for "
                    f"({a},{b},{r}) at "
                    f"|tau-beta|={float(abs(tau - beta_endpoint())):.4e}"
                )
        cutoffs.append(used)

    cancellation = float(mp.log10(largest / abs(total))) if abs(total) > 0 else 0.0
    packet = central * total
    return packet, central, cutoffs, cancellation, largest


# ---------------------------------------------------------------------
# Proved boundary value from lower stratum certificate
# ---------------------------------------------------------------------


def proved_lower_unit_y():
    """Positive root Y of x^4 - x^3 - 3x^2 - x + 1.

    From scripts/dimension_six_lower_stratum.gp:
      Y + Y^{-1} = beta - 2
      Y = ((beta-2) + sqrt((beta-2)^2 - 4)) / 2
    """

    b_minus_2 = beta_endpoint() - 2
    discriminant = b_minus_2 ** 2 - 4
    return (b_minus_2 + mp.sqrt(discriminant)) / 2


def proved_overlap_value():
    """nu_{0,2} = sqrt(Y), the proved overlap table entry."""

    return mp.sqrt(proved_lower_unit_y())


def proved_regulator():
    """log(beta) * log(Y), the certified Stark regulator."""

    return mp.log(beta_endpoint()) * mp.log(proved_lower_unit_y())


# ---------------------------------------------------------------------
# Component classification
# ---------------------------------------------------------------------


def centered_lift(value):
    return (value + 3) % 6 - 3


def component_kind(a, b):
    coeff = centered_lift(4 * b - 5 * a)
    if coeff == 0:
        return "FRESNEL"
    return "GROWING"


def modulus_three_orbit():
    """Zauner orbit of (0,2): {(0,2), (2,0), (4,4)}."""

    result = []
    current = (0, 2)
    while current not in result:
        result.append(current)
        first, second = current
        current = ((5 * first + second) % 6, (-first) % 6)
    return result


# ---------------------------------------------------------------------
# Linear fit
# ---------------------------------------------------------------------


def linear_fit(x_values, y_values):
    count = len(x_values)
    if count < 2:
        return {"slope": 0, "intercept": 0, "r_squared": 1.0}
    x_mean = sum(x_values) / count
    y_mean = sum(y_values) / count
    covariance = sum(
        (x - x_mean) * (y - y_mean) for x, y in zip(x_values, y_values)
    )
    variance = sum((x - x_mean) ** 2 for x in x_values)
    slope = covariance / variance if variance != 0 else 0
    intercept = y_mean - slope * x_mean
    residual = sum(
        (y - (slope * x + intercept)) ** 2
        for x, y in zip(x_values, y_values)
    )
    total = sum((y - y_mean) ** 2 for y in y_values)
    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "r_squared": float(1 - residual / total) if total != 0 else 1.0,
    }


# ---------------------------------------------------------------------
# Main dissection
# ---------------------------------------------------------------------


def evaluate_packet(a, b, r, s, dps):
    """Compute S_{a,b,r}(gamma(s)) at given precision."""

    with mp.workdps(dps + GUARD_DIGITS):
        tau = geodesic_point(s)
        packet, central, cutoffs, cancellation, largest = alias_packet(
            a, b, r, tau
        )
        return {
            "packet": packet,
            "central_kernel": central,
            "cutoffs": cutoffs,
            "cancellation_digits": cancellation,
            "largest_term_abs": largest,
            "tau": tau,
        }


def evaluate_packet_two_precision(a, b, r, s, dps_low, dps_high):
    """Compute at two precisions and measure agreement."""

    low = evaluate_packet(a, b, r, s, dps_low)
    high = evaluate_packet(a, b, r, s, dps_high)

    def rel_diff(lo, hi):
        if abs(hi) == 0:
            return mp.mpf(0)
        return abs(lo / hi - 1)

    packet_rel = rel_diff(low["packet"], high["packet"])
    kernel_rel = rel_diff(low["central_kernel"], high["central_kernel"])

    def digits_lost(rel):
        if rel == 0:
            return 0.0
        return max(0.0, dps_low - float(-mp.log10(rel)))

    return {
        "s": float(s),
        "packet": high["packet"],
        "central_kernel": high["central_kernel"],
        "cutoffs": high["cutoffs"],
        "cancellation_digits": high["cancellation_digits"],
        "packet_digits_lost": digits_lost(packet_rel),
        "kernel_digits_lost": digits_lost(kernel_rel),
        "packet_agreement_digits": float(
            -mp.log10(packet_rel) if packet_rel > 0 else dps_high
        ),
    }


def alias_ratio_direct_crosscheck(a, b, r, s, dps):
    """Check the telescoped K(z+3)/K(z) ratio against direct kernels."""

    with mp.workdps(dps + GUARD_DIGITS):
        tau = geodesic_point(s)
        direct = (
            kernel_factor(a, b, r + 3, tau)
            / kernel_factor(a, b, r, tau)
        )
        telescoped = alias_ratio_general(a, b, tau, r)
        relative = abs(direct / telescoped - 1)
        agreement = (
            float(-mp.log10(relative)) if relative > 0 else float(dps)
        )
        return {
            "frequency": [a, b],
            "r": r,
            "s": str(s),
            "direct_ratio": mp.nstr(direct, 25),
            "telescoped_ratio": mp.nstr(telescoped, 25),
            "relative_error": mp.nstr(relative, 8),
            "agreement_digits": agreement,
        }


def dissection_ladder(a, b, r, s_values, dps_low, dps_high):
    """Evaluate S_{a,b,r} at a ladder of s values."""

    records = []
    for s in s_values:
        rec = evaluate_packet_two_precision(
            a, b, r, s, dps_low, dps_high
        )
        s_float = float(s)
        rec["one_over_s"] = 1 / s_float
        records.append(rec)
    return records


def evaluate_kernel_only(a, b, r, s, dps):
    """Compute K_{a,b}(r; gamma(s)) and scalar at given precision.

    No alias summation — just the central kernel factor and scalar.
    Used for A_6 deep points where the full alias sum would need
    millions of terms.
    """

    with mp.workdps(dps + GUARD_DIGITS):
        tau = geodesic_point(s)
        kernel = kernel_factor(a, b, r, tau)
        scalar = scalar_factor(tau)
        tilted = LEVEL * kernel * scalar
        return {
            "s": float(s),
            "kernel": kernel,
            "scalar": scalar,
            "tilted_value": tilted,
            "tau": tau,
        }


def evaluate_kernel_only_two_precision(a, b, r, s, dps_low, dps_high):
    """Kernel at two precisions for conditioning diagnostic."""

    low = evaluate_kernel_only(a, b, r, s, dps_low)
    high = evaluate_kernel_only(a, b, r, s, dps_high)

    def digits_lost(lo, hi):
        if abs(hi) == 0:
            return 0.0
        rel = abs(lo / hi - 1)
        if rel == 0:
            return 0.0
        return max(0.0, dps_low - float(-mp.log10(rel)))

    return {
        "s": float(s),
        "kernel": high["kernel"],
        "scalar": high["scalar"],
        "tilted_value": high["tilted_value"],
        "kernel_digits_lost": digits_lost(low["kernel"], high["kernel"]),
        "scalar_digits_lost": digits_lost(low["scalar"], high["scalar"]),
        "tilted_digits_lost": digits_lost(
            low["tilted_value"], high["tilted_value"]
        ),
    }


def a6_kernel_ladder(a, b, r, s0, steps, dps_low, dps_high):
    """Kernel at A_6 geodesic ladder: s_k = s0 * beta^{-6k}.

    Each step applies the A_6 return map to tau.  These are raw
    fixed-label kernel values, before the automorphy normalization that
    carries the exact Kopp/AFK multiplier psi^2(A_6)=-1.
    """

    with mp.workdps(dps_high + GUARD_DIGITS):
        s0_mp = mp.mpf(s0) if isinstance(s0, (int, float)) else s0

    records = []
    for step in range(steps + 1):
        with mp.workdps(dps_high + GUARD_DIGITS):
            s = s0_mp * a6_contraction() ** step
        rec = evaluate_kernel_only_two_precision(
            a, b, r, s, dps_low, dps_high
        )
        rec["step"] = step
        rec["s_exact"] = mp.nstr(s, 15)
        records.append(rec)
    return records


def a6_return_ladder_analysis(
    kernel_records,
    boundary_kernel,
    boundary_tilted,
):
    """Analyze raw-kernel convergence along the A_6 return ladder.

    For each consecutive pair (k, k+1):
    - ratio = K(s_{k+1}) / K(s_k)
    - increment = K(s_{k+1}) - K(s_k)
    - distance to the directly evaluated boundary kernel.

    No multiplier prediction is attached to the raw ratio.  The
    verified -1 is an automorphy multiplier of the transported cocycle,
    not of K(a,b,r;tau) with its labels and normalization held fixed.
    """

    rows = []
    kernels = [r["kernel"] for r in kernel_records]
    scalars = [r["scalar"] for r in kernel_records]
    tilted = [r["tilted_value"] for r in kernel_records]

    for i in range(len(kernel_records)):
        row = {
            "step": kernel_records[i]["step"],
            "s": kernel_records[i]["s"],
            "kernel_abs": float(abs(kernels[i])),
            "kernel_arg_over_pi": float(
                mp.arg(kernels[i]) / mp.pi
            ) if abs(kernels[i]) > 0 else 0,
            "scalar_abs": float(abs(scalars[i])),
            "tilted_abs": float(abs(tilted[i])),
            "tilted_arg_over_pi": float(
                mp.arg(tilted[i]) / mp.pi
            ) if abs(tilted[i]) > 0 else 0,
            "kernel_distance_to_boundary": float(
                abs(kernels[i] - boundary_kernel)
            ),
            "tilted_distance_to_boundary": float(
                abs(tilted[i] - boundary_tilted)
            ),
            "kernel_digits_lost": kernel_records[i]["kernel_digits_lost"],
            "tilted_digits_lost": kernel_records[i]["tilted_digits_lost"],
        }
        if i > 0:
            ratio = kernels[i] / kernels[i - 1]
            increment = kernels[i] - kernels[i - 1]
            row["kernel_ratio_abs"] = float(abs(ratio))
            row["kernel_ratio_arg_over_pi"] = float(
                mp.arg(ratio) / mp.pi
            ) if abs(ratio) > 0 else 0
            row["kernel_increment_abs"] = float(abs(increment))
            row["kernel_increment_arg_over_pi"] = float(
                mp.arg(increment) / mp.pi
            ) if abs(increment) > 0 else 0

            t_ratio = tilted[i] / tilted[i - 1]
            t_increment = tilted[i] - tilted[i - 1]
            row["tilted_ratio_abs"] = float(abs(t_ratio))
            row["tilted_ratio_arg_over_pi"] = float(
                mp.arg(t_ratio) / mp.pi
            ) if abs(t_ratio) > 0 else 0
            row["tilted_increment_abs"] = float(abs(t_increment))

        if i > 1:
            increment_current = kernels[i] - kernels[i - 1]
            increment_previous = kernels[i - 1] - kernels[i - 2]
            row["kernel_increment_contraction_ratio"] = float(
                abs(increment_current) / abs(increment_previous)
            ) if abs(increment_previous) > 0 else 0

            t_increment_current = tilted[i] - tilted[i - 1]
            t_increment_previous = tilted[i - 1] - tilted[i - 2]
            row["tilted_increment_contraction_ratio"] = float(
                abs(t_increment_current) / abs(t_increment_previous)
            ) if abs(t_increment_previous) > 0 else 0

        rows.append(row)

    return rows


def boundary_evaluation(a, b, r, dps):
    """Evaluate kernel, scalar, and packet at the boundary tau=beta."""

    with mp.workdps(dps + GUARD_DIGITS):
        tau = mp.mpc(beta_endpoint())
        omega_one = LEVEL * tau - R_PARAMETER

        alpha, discrete = kernel_alpha_discrete(a, b, r, tau)
        kernel = gamma_lens_tilted(alpha, discrete, omega_one)
        kernel_conj = gamma_lens_tilted(
            -alpha, REFLECTED_TOTAL - discrete, omega_one
        )
        kernel_product = kernel * kernel_conj
        scalar = gamma_lens_tilted(
            mp.mpc(omega_one + 1), 0, omega_one
        )

        return {
            "tau_beta": mp.nstr(tau, 20),
            "omega_one": mp.nstr(omega_one, 20),
            "alpha_boundary": mp.nstr(alpha, 20),
            "discrete_boundary": int(discrete),
            "kernel_first": kernel,
            "kernel_second": kernel_conj,
            "kernel_product": kernel_product,
            "scalar": scalar,
            "tilted_value": LEVEL * kernel_product * scalar,
        }


def packet_convergence_analysis(records, boundary_packet):
    """Analyze packet convergence on an ordinary decreasing-s ladder.

    The input points are not separated by an A_6 period.  Per-period
    Return-map diagnostics belong exclusively to
    ``a6_return_ladder_analysis``.
    For consecutive ordinary ladder points this routine records:

    - increment = S(s_{k+1}) - S(s_k)
    - ratio = S(s_{k+1}) / S(s_k)
    - distance to boundary = |S(s_k) - S^{fus}|
    """

    rows = []
    packets = [rec["packet"] for rec in records]
    s_vals = [rec["s"] for rec in records]

    for i in range(len(records)):
        dist = abs(packets[i] - boundary_packet)
        row = {
            "s": s_vals[i],
            "log10_s": math.log10(s_vals[i]) if s_vals[i] > 0 else 0,
            "packet_abs": float(abs(packets[i])),
            "packet_arg_over_pi": float(
                mp.arg(packets[i]) / mp.pi
            ) if abs(packets[i]) > 0 else 0,
            "distance_to_boundary": float(dist),
            "log10_distance": float(mp.log10(dist)) if dist > 0 else -999,
        }
        if i > 0:
            increment = packets[i] - packets[i - 1]
            ratio = (
                packets[i] / packets[i - 1]
                if abs(packets[i - 1]) > 0
                else mp.mpc(0)
            )
            row["increment_abs"] = float(abs(increment))
            row["increment_arg_over_pi"] = float(
                mp.arg(increment) / mp.pi
            ) if abs(increment) > 0 else 0
            row["ratio_abs"] = float(abs(ratio))
            row["ratio_arg_over_pi"] = float(
                mp.arg(ratio) / mp.pi
            ) if abs(ratio) > 0 else 0
        rows.append(row)

    # Fit distance to boundary vs s
    log_s = [r["log10_s"] for r in rows if r["distance_to_boundary"] > 0]
    log_dist = [r["log10_distance"] for r in rows if r["distance_to_boundary"] > 0]
    rate_fit = linear_fit(log_s, log_dist) if len(log_s) >= 2 else None

    ratios = [r.get("ratio_abs") for r in rows if "ratio_abs" in r]
    ratio_args = [
        r.get("ratio_arg_over_pi") for r in rows if "ratio_arg_over_pi" in r
    ]

    return {
        "records": rows,
        "distance_rate_fit_log10dist_vs_log10s": rate_fit,
        "mean_ratio_abs": sum(ratios) / len(ratios) if ratios else 0,
        "mean_ratio_arg_over_pi": sum(ratio_args) / len(ratio_args)
        if ratio_args
        else 0,
    }


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--dps-low", type=int, default=50)
    parser.add_argument("--dps-high", type=int, default=80)
    parser.add_argument(
        "--ladder",
        default="8,16,24,32,48,64",
        help="Denominators for s=1/n ladder",
    )
    parser.add_argument(
        "--a6-steps", type=int, default=2,
        help="Number of A_6 geodesic recursion deep points",
    )
    parser.add_argument(
        "--deep-ladder",
        default="128,256,512,1024,2048,4096",
        help="Reduced-precision denominators for the proved r=0 sweep",
    )
    parser.add_argument("--deep-dps-low", type=int, default=30)
    parser.add_argument("--deep-dps-high", type=int, default=50)
    parser.add_argument(
        "--residue-ladder",
        default="64,256,1024,4096",
        help="Denominators for recombining proved r=0,1,2 packets",
    )
    args = parser.parse_args()

    dps_low, dps_high = args.dps_low, args.dps_high
    if not dps_high > dps_low + 15:
        raise ValueError("dps-high must exceed dps-low by more than 15")
    deep_dps_low = args.deep_dps_low
    deep_dps_high = args.deep_dps_high
    if not deep_dps_high > deep_dps_low + 15:
        raise ValueError(
            "deep-dps-high must exceed deep-dps-low by more than 15"
        )

    # ---- Proved boundary value ----
    with mp.workdps(dps_high + GUARD_DIGITS):
        y_val = proved_lower_unit_y()
        overlap_val = proved_overlap_value()
        regulator = proved_regulator()
        contraction_text = mp.nstr(a6_contraction(), 30)

    # ---- Identification chain ----
    mod3_orbit = modulus_three_orbit()
    proved_modes = [
        (a, b) for a, b in mod3_orbit if component_kind(a, b) == "GROWING"
    ]
    # The Fresnel stratum audit shows (0,2) and (2,0) are the growing
    # intersection with the modulus-three orbit; (4,4) is Fresnel in
    # output space for both shifts.
    proved_mode = (0, 2)
    unproved_mode = (0, 1)

    # Verify classification
    assert component_kind(*proved_mode) == "GROWING"
    assert component_kind(*unproved_mode) == "GROWING"
    assert centered_lift(4 * 2 - 5 * 0) != 0  # (0,2) is growing
    assert centered_lift(4 * 1 - 5 * 0) != 0  # (0,1) is growing
    assert proved_mode in mod3_orbit
    assert unproved_mode not in mod3_orbit

    # ---- Tractable full-packet s-ladder ----
    base_ladder = [
        Fraction(1, int(n)) for n in args.ladder.split(",")
    ]

    import sys
    # ---- Compute for proved mode (0,2) ----
    print("Computing proved mode (0,2)...", file=sys.stderr, flush=True)
    proved_records = []
    for s in base_ladder:
        s_val = float(s) if isinstance(s, Fraction) else float(s)
        print(f"  s={s_val:.6e}...", file=sys.stderr, flush=True)
        rec = evaluate_packet_two_precision(
            proved_mode[0], proved_mode[1], 0, s, dps_low, dps_high
        )
        rec["one_over_s"] = 1 / s_val
        proved_records.append(rec)

    # ---- Compute for unproved mode (0,1) ----
    print("Computing unproved mode (0,1)...", file=sys.stderr, flush=True)
    unproved_records = []
    for s in base_ladder:
        s_val = float(s) if isinstance(s, Fraction) else float(s)
        print(f"  s={s_val:.6e}...", file=sys.stderr, flush=True)
        rec = evaluate_packet_two_precision(
            unproved_mode[0], unproved_mode[1], 0, s, dps_low, dps_high
        )
        rec["one_over_s"] = 1 / s_val
        unproved_records.append(rec)

    # ---- Boundary evaluations ----
    print("Computing boundary values...", file=sys.stderr, flush=True)
    with mp.workdps(dps_high + GUARD_DIGITS):
        proved_boundary = boundary_evaluation(
            proved_mode[0], proved_mode[1], 0, dps_high
        )
        unproved_boundary = boundary_evaluation(
            unproved_mode[0], unproved_mode[1], 0, dps_high
        )

        # Proved overlap reference.  A single raw alias residue is not
        # identified with this value by the existing bridge.
        proved_target = overlap_val

        # Retain the old WIP comparison as a falsifiable diagnostic,
        # explicitly not as a normalization identity.
        last_proved_packet = proved_records[-1]["packet"]

    # ---- A_6 raw-kernel return ladder ----
    # The A_6 geodesic ladder s_k = s0 * beta^{-6k} gives one A_6 period
    # per step.  The kernel-only evaluation avoids the alias-sum term
    # count explosion at tiny s.
    print("Computing A_6 kernel ladders...", file=sys.stderr, flush=True)
    a6_s0 = Fraction(1, 8)
    a6_kernel_steps = args.a6_steps if args.a6_steps > 0 else 2
    proved_a6 = a6_kernel_ladder(
        proved_mode[0], proved_mode[1], 0,
        a6_s0, a6_kernel_steps, dps_low, dps_high,
    )
    unproved_a6 = a6_kernel_ladder(
        unproved_mode[0], unproved_mode[1], 0,
        a6_s0, a6_kernel_steps, dps_low, dps_high,
    )

    with mp.workdps(dps_high + GUARD_DIGITS):
        proved_a6_analysis = a6_return_ladder_analysis(
            proved_a6,
            proved_boundary["kernel_product"],
            proved_boundary["tilted_value"],
        )
        unproved_a6_analysis = a6_return_ladder_analysis(
            unproved_a6,
            unproved_boundary["kernel_product"],
            unproved_boundary["tilted_value"],
        )

        # ---- Convergence dissection (ordinary packet ladder) ----
        proved_dissection = packet_convergence_analysis(
            proved_records, proved_target
        )
        unproved_proxy_boundary = unproved_records[-1]["packet"]
        unproved_dissection = packet_convergence_analysis(
            unproved_records, unproved_proxy_boundary
        )

    # ---- Deep proved r=0 packet sweep at reduced precision ----
    deep_denominators = [
        int(n) for n in args.deep_ladder.split(",")
    ]
    print(
        "Computing deep proved r=0 packet sweep...",
        file=sys.stderr,
        flush=True,
    )
    proved_deep_records = []
    for denominator in deep_denominators:
        print(
            f"  s=1/{denominator}...",
            file=sys.stderr,
            flush=True,
        )
        rec = evaluate_packet_two_precision(
            proved_mode[0],
            proved_mode[1],
            0,
            Fraction(1, denominator),
            deep_dps_low,
            deep_dps_high,
        )
        rec["one_over_s"] = float(denominator)
        proved_deep_records.append(rec)

    # ---- Sparse recombination of all three helical residues ----
    residue_denominators = [
        int(n) for n in args.residue_ladder.split(",")
    ]
    r0_by_denominator = {
        int(round(rec["one_over_s"])): rec["packet"]
        for rec in proved_records + proved_deep_records
    }
    missing_r0 = [
        n for n in residue_denominators if n not in r0_by_denominator
    ]
    if missing_r0:
        raise ValueError(
            "residue-ladder denominators must occur in the primary or "
            f"deep ladder; missing {missing_r0}"
        )

    print(
        "Computing proved three-residue recombination...",
        file=sys.stderr,
        flush=True,
    )
    proved_residue_recombination = []
    for denominator in residue_denominators:
        residue_packets = [r0_by_denominator[denominator]]
        residue_records = []
        for residue in (1, 2):
            print(
                f"  s=1/{denominator}, r={residue}...",
                file=sys.stderr,
                flush=True,
            )
            rec = evaluate_packet_two_precision(
                proved_mode[0],
                proved_mode[1],
                residue,
                Fraction(1, denominator),
                deep_dps_low,
                deep_dps_high,
            )
            residue_packets.append(rec["packet"])
            residue_records.append(rec)
        with mp.workdps(deep_dps_high + GUARD_DIGITS):
            combined = sum(residue_packets)
            proved_residue_recombination.append(
                {
                    "denominator": denominator,
                    "s": 1 / denominator,
                    "residue_packets": [
                        mp.nstr(value, 25) for value in residue_packets
                    ],
                    "combined_packet": mp.nstr(combined, 25),
                    "combined_abs": float(abs(combined)),
                    "combined_arg_over_pi": float(
                        mp.arg(combined) / mp.pi
                    ),
                    "combined_over_sqrt_y": mp.nstr(
                        combined / proved_target, 25
                    ),
                    "r1_r2_packet_digits_lost": [
                        rec["packet_digits_lost"]
                        for rec in residue_records
                    ],
                }
            )

    print(
        "Crosschecking telescoped alias ratios...",
        file=sys.stderr,
        flush=True,
    )
    alias_ratio_crosschecks = [
        alias_ratio_direct_crosscheck(
            a, b, 0, Fraction(1, 8), 35
        )
        for a, b in (proved_mode, unproved_mode)
    ]

    with mp.workdps(deep_dps_high + GUARD_DIGITS):
        r0_growth_records = [proved_records[-1]] + proved_deep_records
        r0_growth_fit = linear_fit(
            [
                math.log10(rec["one_over_s"])
                for rec in r0_growth_records
            ],
            [
                float(mp.log10(abs(rec["packet"])))
                for rec in r0_growth_records
            ],
        )
        last_deep_packet = proved_deep_records[-1]["packet"]
        last_deep_ratio_to_overlap = last_deep_packet / proved_target
        last_deep_target_distance = abs(
            last_deep_packet - proved_target
        )

    # ---- Assemble result ----
    def clean_record(rec):
        return {
            "s": rec["s"],
            "one_over_s": rec["one_over_s"],
            "packet": mp.nstr(rec["packet"], 25),
            "packet_abs": float(abs(rec["packet"])),
            "packet_arg_over_pi": float(
                mp.arg(rec["packet"]) / mp.pi
            ) if abs(rec["packet"]) > 0 else 0,
            "central_kernel": mp.nstr(rec["central_kernel"], 25),
            "cutoffs": rec["cutoffs"],
            "cancellation_digits": rec["cancellation_digits"],
            "packet_digits_lost": rec["packet_digits_lost"],
            "kernel_digits_lost": rec["kernel_digits_lost"],
            "packet_agreement_digits": rec["packet_agreement_digits"],
        }

    result = {
        "schema": "sic-stark-dimension-six-cycle156-growing-component-v3",
        "methodology": {
            "packet_ladder": (
                "Full bilateral alias packets on the tractable ordinary "
                "s=1/n ladder."
            ),
            "a6_return_ladder": (
                "Raw fixed-label central kernels at "
                "s_k=(1/8)*beta^(-6k); no alias summation."
            ),
            "multiplier_scope": (
                "psi^2(A6)=-1 is exact for the transported Kopp/AFK "
                "cocycle. It is not imposed on the raw fixed-label "
                "kernel ratios reported here."
            ),
            "arithmetic_reference_scope": (
                "sqrt(Y) is the proved conductor-three overlap. The "
                "existing bridge does not identify one raw helical "
                "residue packet with sqrt(Y); comparisons are diagnostic."
            ),
            "deep_packet_sweep": (
                "Proved-mode r=0 packets at reduced 30/50 precision "
                "through s=1/4096."
            ),
            "residue_recombination": (
                "Raw proved-mode r=0,1,2 packets summed at four sparse "
                "points; no additional Fourier gauge is inserted."
            ),
        },
        "identification": {
            "proved_mode": {
                "frequency": list(proved_mode),
                "kind": component_kind(*proved_mode),
                "conductor": 3,
                "characteristic": "modulus-three orbit point, "
                                  "conductor-lowered quadratic (chi_3)",
                "modulus_three_orbit": [list(p) for p in mod3_orbit],
                "proved_overlap_reference": mp.nstr(proved_target, 30),
                "raw_residue_packet_equals_overlap_assumed": False,
                "proved_unit_y": mp.nstr(y_val, 30),
                "proved_unit_y_polynomial": "x^4-x^3-3x^2-x+1",
                "proved_regulator": mp.nstr(regulator, 30),
                "identification_chain": [
                    "scripts/dimension_six_fresnel_stratum_audit.py: "
                    "(0,2) is in the proved modulus-three orbit and is "
                    "growing (4*2-5*0=8, centered_lift=2 != 0)",
                    "scripts/dimension_six_lower_stratum.gp: "
                    "exp(Z'(0,I)) = nu_{0,2}^2 = Y, Y root of "
                    "x^4-x^3-3x^2-x+1, regulator log(beta)*log(Y)",
                    "scripts/dimension_six_conductor_obstruction.gp: "
                    "chi_3 descends to conductor 3; chi_1, chi_5 are "
                    "killed by conductor lowering",
                    "scripts/dimension_six_grade2_equivalence.py: "
                    "Grade-2 equivalence through proved quadratic "
                    "component, C_6 Fourier inversion, multiplier ledger",
                ],
            },
            "unproved_mode": {
                "frequency": list(unproved_mode),
                "kind": component_kind(*unproved_mode),
                "conductor": 6,
                "characteristic": "primitive, not conductor-lowered; "
                                  "requires chi_1 (MFC_6 open)",
            },
            "fresnel_condition": "4*b-5*a == 0 mod 6",
            "modulus_three_orbit_growing": [
                list(p) for p in proved_modes
            ],
        },
        "proved_mode_raw_kernel_boundary": {
            "kernel_first": mp.nstr(
                proved_boundary["kernel_first"], 25
            ),
            "kernel_second": mp.nstr(
                proved_boundary["kernel_second"], 25
            ),
            "kernel_product": mp.nstr(
                proved_boundary["kernel_product"], 25
            ),
            "scalar": mp.nstr(proved_boundary["scalar"], 25),
            "tilted_value": mp.nstr(
                proved_boundary["tilted_value"], 25
            ),
            "alpha_boundary": proved_boundary["alpha_boundary"],
            "discrete_boundary": proved_boundary["discrete_boundary"],
        },
        "unproved_mode_raw_kernel_boundary": {
            "kernel_first": mp.nstr(
                unproved_boundary["kernel_first"], 25
            ),
            "kernel_second": mp.nstr(
                unproved_boundary["kernel_second"], 25
            ),
            "kernel_product": mp.nstr(
                unproved_boundary["kernel_product"], 25
            ),
            "scalar": mp.nstr(unproved_boundary["scalar"], 25),
            "tilted_value": mp.nstr(
                unproved_boundary["tilted_value"], 25
            ),
        },
        "proved_mode_records": [
            clean_record(r) for r in proved_records
        ],
        "unproved_mode_records": [
            clean_record(r) for r in unproved_records
        ],
        "proved_mode_overlap_reference_analysis": proved_dissection,
        "unproved_mode_last_point_proxy_analysis": unproved_dissection,
        "proved_mode_deep_r0_records": [
            clean_record(r) for r in proved_deep_records
        ],
        "proved_mode_deep_r0_log_abs_vs_log_one_over_s": r0_growth_fit,
        "proved_mode_three_residue_recombination": (
            proved_residue_recombination
        ),
        "alias_ratio_direct_crosschecks": alias_ratio_crosschecks,
        "a6_raw_kernel_return_ladder": {
            "contraction_beta_inv6": contraction_text,
            "s0": str(a6_s0),
            "steps": a6_kernel_steps,
            "proved_mode_analysis": proved_a6_analysis,
            "unproved_mode_analysis": unproved_a6_analysis,
        },
        "proved_overlap_reference_check": {
            "comparison_is_not_an_asserted_identity": True,
            "last_primary_packet": mp.nstr(last_proved_packet, 25),
            "last_deep_packet": mp.nstr(last_deep_packet, 25),
            "proved_overlap_reference": mp.nstr(proved_target, 25),
            "last_deep_packet_over_overlap": mp.nstr(
                last_deep_ratio_to_overlap, 25
            ),
            "last_deep_ratio_abs": float(
                abs(last_deep_ratio_to_overlap)
            ),
            "ratio_arg_over_pi": float(
                mp.arg(last_deep_ratio_to_overlap) / mp.pi
            ) if abs(last_deep_ratio_to_overlap) > 0 else 0,
            "last_deep_distance_to_overlap": float(
                last_deep_target_distance
            ),
        },
        "precision": {
            "primary_dps_low": dps_low,
            "primary_dps_high": dps_high,
            "deep_dps_low": deep_dps_low,
            "deep_dps_high": deep_dps_high,
        },
        "packet_ladder": [str(s) for s in base_ladder],
        "deep_packet_ladder": deep_denominators,
        "residue_recombination_ladder": residue_denominators,
        "a6_contraction": contraction_text,
    }

    # ---- Determine verdict ----
    last_unproved = unproved_records[-1]

    proved_well_conditioned = all(
        rec["packet_digits_lost"] < 10
        for rec in proved_records + proved_deep_records
    )
    unproved_well_conditioned = last_unproved["packet_digits_lost"] < 10

    r0_growth_factor = (
        proved_deep_records[-1]["packet"]
        / proved_records[-1]["packet"]
    )
    recombination_growth_factor = (
        proved_residue_recombination[-1]["combined_abs"]
        / proved_residue_recombination[0]["combined_abs"]
    )
    proved_boundary_last = proved_a6_analysis[-1]
    unproved_boundary_last = unproved_a6_analysis[-1]

    result["verdict"] = {
        "proved_mode_well_conditioned": proved_well_conditioned,
        "unproved_mode_well_conditioned": unproved_well_conditioned,
        "alias_ratio_crosschecks_pass": all(
            rec["agreement_digits"] > 30
            for rec in alias_ratio_crosschecks
        ),
        "proved_r0_abs_growth_1_over_64_to_1_over_4096": float(
            abs(r0_growth_factor)
        ),
        "proved_r0_growth_power_fit": r0_growth_fit,
        "three_residue_abs_growth_1_over_64_to_1_over_4096": (
            recombination_growth_factor
        ),
        "proved_raw_kernel_last_boundary_distance": (
            proved_boundary_last["kernel_distance_to_boundary"]
        ),
        "unproved_raw_kernel_last_boundary_distance": (
            unproved_boundary_last["kernel_distance_to_boundary"]
        ),
        "raw_a6_kernel_multiplier_claimed": False,
        "single_raw_residue_equals_sqrt_y_claimed": False,
        "componentwise_BF6_numerical_status": (
            "ADVERSE_NO_BOUNDED_CONVERGENCE_OBSERVED"
        ),
        "cycle155_scope_correction": (
            "The stable tilted central integral does not by itself "
            "control spectral periodization."
        ),
        "finite_numerics_are_not_a_nonexistence_proof": True,
    }

    print(json.dumps(result, indent=2, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
