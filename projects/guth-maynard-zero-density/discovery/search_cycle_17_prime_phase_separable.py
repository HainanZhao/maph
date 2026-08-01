#!/usr/bin/env python3
"""Preregistered finite search for prime-phase rank-one large-value families."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import resource
import sys
import time

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-17-prime-phase-separable-search-v1.json"
M_VALUES = (16, 24, 32, 48, 64)
SEEDS = tuple(range(8))
ITERATIONS = 25
CHUNK = 8192


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sieve(limit: int) -> list[int]:
    flags = bytearray(b"\x01") * (limit + 1)
    flags[:2] = b"\x00\x00"
    for value in range(2, math.isqrt(limit) + 1):
        if flags[value]:
            flags[value * value : limit + 1 : value] = b"\x00" * (((limit - value * value) // value) + 1)
    return [index for index, flag in enumerate(flags) if flag]


def prime_block(m: int) -> tuple[int, np.ndarray]:
    x0 = math.ceil(4 * m * math.log(4 * m))
    values = [prime for prime in sieve(2 * x0) if prime >= x0]
    require(len(values) >= m, f"insufficient registered primes for m={m}")
    return x0, np.asarray(values[:m], dtype=np.float64)


def evaluate_all(log_primes: np.ndarray, h: int, coefficients: np.ndarray) -> np.ndarray:
    output = np.empty(h + 1, dtype=np.complex128)
    for start in range(0, h + 1, CHUNK):
        stop = min(h + 1, start + CHUNK)
        rows = np.arange(start, stop, dtype=np.float64)[:, None]
        output[start:stop] = np.exp(1j * rows * log_primes[None, :]) @ coefficients
    return output


def gradient_on_rows(log_primes: np.ndarray, rows: np.ndarray, values: np.ndarray) -> np.ndarray:
    phases = np.exp(1j * rows.astype(np.float64)[:, None] * log_primes[None, :])
    weights = np.abs(values) ** 2 * values
    return phases.conj().T @ weights


def coefficient_hash(coefficients: np.ndarray) -> str:
    payload = [[round(float(value.real), 15), round(float(value.imag), 15)] for value in coefficients]
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode("utf-8")).hexdigest()


def metrics(log_primes: np.ndarray, h: int, threshold: float, coefficients: np.ndarray, r_select: int) -> dict[str, object]:
    values = evaluate_all(log_primes, h, coefficients)
    magnitudes = np.abs(values)
    selected = np.argpartition(magnitudes, -r_select)[-r_select:]
    selected = selected[np.argsort(magnitudes[selected])[::-1]]
    count = int(np.count_nonzero(magnitudes >= threshold))
    p = 24.0 / 5.0
    top = selected[:10]
    return {
        "count": count,
        "count_exponent": math.log(max(count, 1)) / math.log(len(log_primes)),
        "selected_fourth_over_m2": float(np.sum(magnitudes[selected] ** 4) / (len(log_primes) ** 2)),
        "fractional_moment_ratio": float(np.sum(magnitudes**p) / ((h + 1) * len(log_primes) ** (p / 2))),
        "top_rows": [int(row) for row in top],
        "top_magnitudes": [float(magnitudes[row]) for row in top],
        "coefficient_hash": coefficient_hash(coefficients),
    }


def optimize(log_primes: np.ndarray, h: int, threshold: float, coefficients: np.ndarray, r_select: int) -> tuple[np.ndarray, list[float]]:
    history: list[float] = []
    current = coefficients.copy()
    for _ in range(ITERATIONS):
        values = evaluate_all(log_primes, h, current)
        magnitudes = np.abs(values)
        rows = np.argpartition(magnitudes, -r_select)[-r_select:]
        old_objective = float(np.sum(magnitudes[rows] ** 4))
        gradient = gradient_on_rows(log_primes, rows, values[rows])
        proposal = current.copy()
        nonzero = np.abs(gradient) > 0
        proposal[nonzero] = gradient[nonzero] / np.abs(gradient[nonzero])
        proposal_values = evaluate_all(log_primes, h, proposal)
        proposal_objective = float(np.sum(np.abs(proposal_values[rows]) ** 4))
        if proposal_objective + 1e-9 >= old_objective:
            current = proposal
            history.append(proposal_objective)
        else:
            history.append(old_objective)
    return current, history


def deterministic_families(log_primes: np.ndarray, h: int) -> dict[str, np.ndarray]:
    m = len(log_primes)
    index = np.arange(m, dtype=np.float64)
    result = {
        "all_ones": np.ones(m, dtype=np.complex128),
        "alternating": np.where(np.arange(m) % 2 == 0, 1.0, -1.0).astype(np.complex128),
        "quadratic_index": np.exp(2j * np.pi * index * index / max(m, 1)),
    }
    for label, row in (("align_0", 0), ("align_1_4", h // 4), ("align_1_2", h // 2), ("align_3_4", 3 * h // 4)):
        result[label] = np.exp(-1j * row * log_primes)
    return result


def run() -> dict[str, object]:
    started = time.perf_counter()
    rows: list[dict[str, object]] = []
    deterministic: list[dict[str, object]] = []
    for m in M_VALUES:
        x0, primes = prime_block(m)
        log_primes = np.log(primes)
        h = math.floor(m ** (12 / 5))
        threshold = m ** (7 / 10)
        r_select = min(h + 1, math.ceil(m ** (8 / 5)))
        for label, coefficients in deterministic_families(log_primes, h).items():
            deterministic.append({"m": m, "x0": x0, "H": h, "V": threshold, "R_select": r_select, "family": label, **metrics(log_primes, h, threshold, coefficients, r_select)})
        for seed in SEEDS:
            generator = np.random.Generator(np.random.PCG64(seed))
            random_coefficients = np.exp(2j * np.pi * generator.random(m))
            aligned_coefficients = np.exp(-1j * (h // 2) * np.log(primes))
            for initialization, coefficients in (("random", random_coefficients), ("aligned_half", aligned_coefficients)):
                optimized, history = optimize(log_primes, h, threshold, coefficients, r_select)
                rows.append({
                    "m": m,
                    "x0": x0,
                    "prime_min": int(primes[0]),
                    "prime_max": int(primes[-1]),
                    "H": h,
                    "V": threshold,
                    "R_select": r_select,
                    "seed": seed,
                    "initialization": initialization,
                    "iterations": ITERATIONS,
                    "objective_initial": history[0],
                    "objective_final": history[-1],
                    "accepted_monotone": all(right + 1e-9 >= left for left, right in zip(history, history[1:])),
                    **metrics(log_primes, h, threshold, optimized, r_select),
                })
    best = max(rows + deterministic, key=lambda row: (row["count_exponent"], row["count"]))
    best_exponent = float(best["count_exponent"])
    outcome = "BASELINE_APPROACHED" if best_exponent >= 1.5 else "TARGET_CROSSED" if best_exponent >= 36 / 25 else "NO_TARGET_CROSSING"
    elapsed = time.perf_counter() - started
    return {
        "artifact_id": "cycle-17-prime-phase-separable-search-v1",
        "epistemic_status": "OBSERVED",
        "status": outcome,
        "claim_boundary": "Finite complex128 alternating search only; no asymptotic theorem, certified enclosure, density gain, or universal negative.",
        "runtime": {"python": platform.python_version(), "implementation": platform.python_implementation(), "numpy": np.__version__, "optimization_level": sys.flags.optimize},
        "frozen_parameters": {"m_values": list(M_VALUES), "seeds": list(SEEDS), "iterations": ITERATIONS, "chunk": CHUNK, "rng": "PCG64"},
        "deterministic_rows": deterministic,
        "optimized_rows": rows,
        "best_row": best,
        "wall_seconds": elapsed,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }


def render(payload: dict[str, object]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", required=True)
    args = parser.parse_args()
    require(not OUTPUT.exists(), "refusing to overwrite Cycle 17 discovery artifact")
    payload = run()
    with OUTPUT.open("xb") as handle:
        handle.write(render(payload))
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"], "best_count_exponent": payload["best_row"]["count_exponent"], "wall_seconds": payload["wall_seconds"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
