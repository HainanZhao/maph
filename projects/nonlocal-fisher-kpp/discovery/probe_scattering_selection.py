#!/usr/bin/env python3
"""Quarantined zero-energy scattering diagnostic for Cycle 2.

Requires scipy 1.14.1. The runtime records the resolved NumPy version.
Outputs OBSERVED data only. A converged fixed point of this diagnostic does
not predict front spacing: the pulled front probes the energy -1 ballistic
transmission problem, not this zero-energy scattering length.
"""

from __future__ import annotations

import argparse
import json
import math

import numpy as np
import scipy
from scipy.integrate import cumulative_trapezoid, solve_ivp
from scipy.optimize import root


def initial_guess(x: np.ndarray, length: float) -> np.ndarray:
    if length <= 2.0:
        q = length / 12.0
        v = length / 24.0 / np.cosh(np.minimum(q * x, 350.0)) ** 2
    else:
        inside = x < length / 2.0
        v = np.where(inside, math.pi / length * np.cos(math.pi * x / length), 0.0)
        # Add a small smooth tail and avoid a zero iterate.
        tail = math.pi / length * np.exp(-(x - length / 2.0))
        v = np.where(inside, v, tail)
    return np.maximum(v, 1e-12)


def solve_profile(length: float, tolerance: float, points: int) -> tuple[np.ndarray, np.ndarray, dict[str, float]]:
    xmax = max(30.0, 60.0 / length)
    x = np.linspace(0.0, xmax, points)
    spacing = x[1] - x[0]

    def primitive_weights(endpoint: float) -> np.ndarray:
        """Exact integral weights for the piecewise-linear interpolant on [0,s]."""
        endpoint = min(max(endpoint, 0.0), xmax)
        weights = np.zeros(points)
        if endpoint == 0.0:
            return weights
        cell = min(int(endpoint / spacing), points - 2)
        if cell >= 1:
            weights[0] = spacing / 2.0
            weights[1:cell] = spacing
            weights[cell] = spacing / 2.0
        offset = endpoint - x[cell]
        theta = offset / spacing
        weights[cell] += offset * (1.0 - theta / 2.0)
        weights[cell + 1] += offset * theta / 2.0
        return weights

    half_mass_weights = primitive_weights(xmax)
    mass_weights = 2.0 * half_mass_weights
    local_matrix = np.zeros((points, points))
    for i, center in enumerate(x):
        lower = center - length
        upper = center + length
        if lower >= 0.0:
            local_matrix[i] = primitive_weights(upper) - primitive_weights(lower)
        else:
            local_matrix[i] = primitive_weights(upper) + primitive_weights(-lower)

    def residual(v: np.ndarray) -> np.ndarray:
        out = np.zeros_like(v)
        mass = float(mass_weights @ v)
        local = local_matrix @ v
        out[0] = (-3.0 * v[0] + 4.0 * v[1] - v[2]) / (2.0 * spacing)
        out[-1] = v[-1]
        out[1:-1] = (v[:-2] - 2.0 * v[1:-1] + v[2:]) / spacing**2
        out[1:-1] += v[1:-1] * (1.0 - mass + 0.5 * local[1:-1])
        return out

    def jacobian(v: np.ndarray) -> np.ndarray:
        jac = np.zeros((points, points))
        mass = float(mass_weights @ v)
        local = local_matrix @ v
        jac[0, 0] = -3.0 / (2.0 * spacing)
        jac[0, 1] = 2.0 / spacing
        jac[0, 2] = -1.0 / (2.0 * spacing)
        jac[-1, -1] = 1.0
        for i in range(1, points - 1):
            jac[i, i - 1] += 1.0 / spacing**2
            jac[i, i] += -2.0 / spacing**2 + 1.0 - mass + 0.5 * local[i]
            jac[i, i + 1] += 1.0 / spacing**2
            jac[i, :] += v[i] * (-mass_weights + 0.5 * local_matrix[i, :])
        return jac

    result = root(
        residual,
        initial_guess(x, length),
        jac=jacobian,
        method="hybr",
        options={"xtol": tolerance, "maxfev": 4000},
    )
    if not result.success:
        raise RuntimeError(f"L={length}: {result.message}; norm={np.linalg.norm(result.fun)}")
    v = result.x
    if np.min(v) < -1e-7 or np.max(v) < 1e-6:
        raise RuntimeError(f"L={length}: nonpositive or trivial profile")
    v = np.maximum(v, 0.0)
    mass = float(mass_weights @ v)
    local = local_matrix @ v
    q_value = float(mass_weights @ (v * local))
    identity_residual = q_value - 2.0 * mass * (mass - 1.0)
    return x, v, {
        "mass": mass,
        "q": q_value,
        "mass_identity_residual": identity_residual,
        "xmax": xmax,
        "nodes": points,
        "equation_residual_norm": float(np.linalg.norm(residual(v), ord=np.inf)),
    }


def scattering_length(x: np.ndarray, v: np.ndarray) -> tuple[float, dict[str, float]]:
    xmax = float(x[-1])
    cumulative = np.concatenate(([0.0], cumulative_trapezoid(v, x)))
    half_mass = float(cumulative[-1])

    def primitive(point: float) -> float:
        return float(np.interp(min(abs(point), xmax), x, cumulative))

    def potential(point: float) -> float:
        if point >= 0.0:
            return 0.5 * (half_mass - primitive(point))
        return 0.5 * (half_mass + primitive(point))

    kappa = math.sqrt(max(potential(-xmax), 1e-15))
    scale = math.exp(-min(kappa * xmax, 300.0))

    def ode(_point: float, state: np.ndarray) -> np.ndarray:
        return np.array((state[1], potential(_point) * state[0]))

    result = solve_ivp(
        ode,
        (-xmax, xmax),
        np.array((scale, kappa * scale)),
        rtol=2e-10,
        atol=1e-12 * max(scale, 1e-30),
        max_step=0.03,
    )
    if not result.success:
        raise RuntimeError(result.message)
    psi, slope = result.y[:, -1]
    if slope <= 0.0:
        raise RuntimeError("nonpositive scattering slope")
    intercept = psi - xmax * slope
    intercept_over_slope = intercept / slope
    extrapolated_zero = -intercept_over_slope
    return float(extrapolated_zero), {
        "psi_right": float(psi),
        "slope_right": float(slope),
        "potential_left": potential(-xmax),
        "potential_right": potential(xmax),
        "intercept_over_slope": float(intercept_over_slope),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lengths", nargs="+", type=float, default=[0.5, 1, 2, 4, 8])
    parser.add_argument("--tolerance", type=float, default=2e-6)
    parser.add_argument("--points", type=int, default=700)
    args = parser.parse_args()
    rows = []
    for length in args.lengths:
        x, v, profile = solve_profile(length, args.tolerance, args.points)
        zero, scattering = scattering_length(x, v)
        rows.append({
            "L": length,
            "extrapolated_zero": zero,
            "fixed_point_residual": zero - length,
            "profile": profile,
            "scattering": scattering,
        })
    print(json.dumps({
        "status": "OBSERVED",
        "claim_boundary": (
            "Zero-energy diagnostic only; a root is not a Fisher-KPP "
            "front-selection result because the ballistic front probes "
            "exponential weight one."
        ),
        "numpy": np.__version__,
        "scipy": scipy.__version__,
        "points": args.points,
        "rows": rows,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
