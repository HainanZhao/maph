"""Frozen conventions for the bounded actual-log CRR spectral probe v1.

This is a discovery-only finite analogue.  It uses literal ``n**(i*t)``
phases, literal reduced Farey labels, and literal plateau-ray multiplicities,
but v=2 is far below the asymptotic Farey-geometry regime.  Nothing here is a
continuous CRR witness predicate.
"""
from __future__ import annotations

from math import ceil, exp, floor, gcd
from typing import Iterable

import numpy as np


V_PARAMETER = 2
H = V_PARAMETER**12
L = V_PARAMETER**10
R = V_PARAMETER**8
Q = V_PARAMETER**4
CENTRAL_VALUE = V_PARAMETER**7
RAW_FAREY_AMPLITUDE = V_PARAMETER**6
MINIMUM_SEPARATION = 2
MACROCELLS = 16
POINTS_PER_MACROCELL = R // MACROCELLS
THETA_NODES = (-3.0, 0.0, 3.0)
FAREY_POWER_ITERATIONS = 32
MINIMUM_VALUE_ITERATIONS = 16
JOINT_OUTER_ITERATIONS = 2
EPSILON = 2.0**-40
RESOURCE_WALL_SECONDS = 600
RESOURCE_RSS_BYTES = 1 << 30


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def ceiling_division(numerator: int, denominator: int) -> int:
    require(denominator > 0, "positive denominator required")
    return -((-numerator) // denominator)


def smooth_eta(values: np.ndarray) -> np.ndarray:
    result = np.zeros_like(values, dtype=np.float64)
    mask = values > 0.0
    result[mask] = np.exp(-1.0 / values[mask])
    return result


def smooth_step(values: np.ndarray) -> np.ndarray:
    numerator = smooth_eta(values)
    denominator = numerator + smooth_eta(1.0 - values)
    return np.divide(numerator, denominator, out=np.zeros_like(numerator), where=denominator > 0.0)


def coefficient_indices_and_weight() -> tuple[np.ndarray, np.ndarray]:
    """Return the literal integer support and frozen CRR smooth weights."""
    indices = np.arange(L + 1, 2 * L, dtype=np.float64)
    scaled = indices / float(L)
    weight = smooth_step(5.0 * (scaled - 1.0)) * smooth_step(5.0 * (2.0 - scaled))
    require(indices.size == L - 1, "integer support count mismatch")
    require(np.all(weight > 0.0) and np.all(weight <= 1.0), "smooth weight range mismatch")
    return indices, weight


def farey_pairs() -> tuple[tuple[int, int], ...]:
    """Return the literal reduced Q-by-Q CRR Farey shell at v=2."""
    result: list[tuple[int, int]] = []
    for r in range(Q, 2 * Q):
        for s in range(Q, 2 * Q):
            if gcd(r, s) == 1 and 4 * r >= 3 * s and 4 * r <= 5 * s:
                result.append((r, s))
    result.sort()
    require(result, "actual Farey shell is empty")
    return tuple(result)


def ray_count(r: int, s: int) -> int:
    """Count the exact plateau ray K_(r,s) used in the cross-Gram identity."""
    lower = max(ceiling_division(6 * L, 5 * r), ceiling_division(6 * L, 5 * s))
    upper = min((9 * L) // (5 * r), (9 * L) // (5 * s))
    count = max(0, upper - lower + 1)
    require(count > 0, "frozen plateau ray is unexpectedly empty")
    return count


def phase(values: np.ndarray) -> np.ndarray:
    """Coordinatewise capped phase; zero coordinates remain zero."""
    magnitude = np.abs(values)
    return np.divide(values, magnitude, out=np.zeros_like(values), where=magnitude > 0.0)


def measurement_matrix(times: Iterable[int] | np.ndarray, indices: np.ndarray, weight: np.ndarray) -> np.ndarray:
    times_array = np.asarray(tuple(times) if not isinstance(times, np.ndarray) else times, dtype=np.float64)
    return np.exp(1j * np.outer(times_array, np.log(indices))) * weight[None, :]


def farey_feature_matrix(times: np.ndarray) -> tuple[np.ndarray, tuple[tuple[int, int, float, int], ...]]:
    """Build U with ||1_W^* U||^2 equal to the discrete Farey-ray score."""
    labels: list[tuple[int, int, float, int]] = []
    columns: list[np.ndarray] = []
    for r, s in farey_pairs():
        count = ray_count(r, s)
        for theta in THETA_NODES:
            x = (r / s) * exp(theta / H)
            labels.append((r, s, theta, count))
            columns.append(np.sqrt(float(count)) * np.exp(1j * times.astype(np.float64) * np.log(x)))
    matrix = np.column_stack(columns)
    require(matrix.shape[0] == H and matrix.shape[1] == len(labels), "Farey feature shape mismatch")
    return matrix, tuple(labels)


def normalized_power(apply, dimension: int, iterations: int) -> np.ndarray:
    """Deterministic positive-semidefinite power iteration with fixed start."""
    vector = np.ones(dimension, dtype=np.complex128)
    vector /= np.linalg.norm(vector)
    for _ in range(iterations):
        vector = apply(vector)
        norm = np.linalg.norm(vector)
        require(np.isfinite(norm) and norm > 0.0, "power iteration collapsed")
        vector /= norm
    pivot = int(np.argmax(np.abs(vector)))
    if abs(vector[pivot]) > 0.0:
        vector *= np.exp(-1j * np.angle(vector[pivot]))
    return vector


def select_stratified(score: np.ndarray) -> np.ndarray:
    """Take literal score leaders in every macrocell, with the frozen gap."""
    require(score.shape == (H,), "selection score shape mismatch")
    selected: list[int] = []
    width = H // MACROCELLS
    require(width * MACROCELLS == H, "macrocell partition mismatch")
    for cell in range(MACROCELLS):
        start, stop = cell * width, (cell + 1) * width
        candidates = list(range(start, stop))
        candidates.sort(key=lambda t: (-float(score[t]), t))
        chosen = 0
        for t in candidates:
            if all(abs(t - other) >= MINIMUM_SEPARATION for other in selected):
                selected.append(t)
                chosen += 1
                if chosen == POINTS_PER_MACROCELL:
                    break
        require(chosen == POINTS_PER_MACROCELL, "stratified selector could not fill a macrocell")
    result = np.asarray(sorted(selected), dtype=np.int64)
    require(result.size == R, "stratified cardinality mismatch")
    require(np.min(np.diff(result)) >= MINIMUM_SEPARATION, "stratified spacing mismatch")
    return result


def tolerance_one_energy(times: np.ndarray) -> int:
    """Compute the CRR ordered tolerance-one additive energy exactly."""
    require(times.ndim == 1 and times.size == R, "energy expects a central-cardinality set")
    pair_sums = (times[:, None] + times[None, :]).ravel()
    counts = np.bincount(pair_sums, minlength=2 * H + 1).astype(object)
    total = 0
    for index, count in enumerate(counts):
        if count:
            total += int(count) * int(count)
            if index:
                total += int(count) * int(counts[index - 1])
            if index + 1 < counts.size:
                total += int(count) * int(counts[index + 1])
    return total


def exact_rows() -> dict[str, object]:
    indices, weight = coefficient_indices_and_weight()
    pairs = farey_pairs()
    ray_counts = [ray_count(r, s) for r, s in pairs]
    require(H == Q**3 and L == Q * V_PARAMETER**6 and R == Q**2, "frozen-scale relation mismatch")
    require(POINTS_PER_MACROCELL * MACROCELLS == R, "stratified count mismatch")
    return {
        "v": V_PARAMETER,
        "H": H,
        "L": L,
        "R": R,
        "Q": Q,
        "central_value": CENTRAL_VALUE,
        "raw_farey_amplitude": RAW_FAREY_AMPLITUDE,
        "smooth_support_count": int(indices.size),
        "smooth_weight_minimum": float(np.min(weight)),
        "smooth_weight_maximum": float(np.max(weight)),
        "farey_pair_count": len(pairs),
        "ray_count_minimum": min(ray_counts),
        "ray_count_maximum": max(ray_counts),
        "theta_nodes": list(THETA_NODES),
        "minimum_separation": MINIMUM_SEPARATION,
        "macrocells": MACROCELLS,
        "points_per_macrocell": POINTS_PER_MACROCELL,
        "energy_center_R4_over_H": R**4 // H,
    }
