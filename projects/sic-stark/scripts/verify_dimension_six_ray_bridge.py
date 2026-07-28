#!/usr/bin/env python3
"""Audit every primitive d=6 characteristic against Kopp's ray packet."""

from __future__ import annotations

import ast
import math
from pathlib import Path
import re
import subprocess

from explore_dimension_six import principal_overlap


ROOT = Path(__file__).resolve().parents[1]
CHARACTERISTIC = re.compile(
    r"^CHAR_(\d+)_(\d+) .* COPRIME=1 LOG=(\d+)$"
)
RAY_LOGS = re.compile(
    r"^FOURIER_INVERTED_DIFFERENCED_RAY_LOGS=(\[.*\])$"
)


def run_gp(script: str) -> str:
    return subprocess.run(
        ["gp", "-q", str(ROOT / "scripts" / script)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def main() -> None:
    class_by_characteristic = {}
    for line in run_gp("dimension_six_ray_recon.gp").splitlines():
        match = CHARACTERISTIC.match(line)
        if match:
            first, second, ray_log = map(int, match.groups())
            class_by_characteristic[(first, second)] = ray_log

    ray_logs = None
    for line in run_gp("dimension_six_primitive_fourier_audit.gp").splitlines():
        match = RAY_LOGS.match(line)
        if match:
            ray_logs = [float(value) for value in ast.literal_eval(match.group(1))]
            break
    if ray_logs is None:
        raise AssertionError("ray logarithm packet was not printed")

    residuals = {}
    for characteristic, ray_log in class_by_characteristic.items():
        actual = 2 * math.log(abs(principal_overlap(*characteristic)))
        residuals[characteristic] = actual - ray_logs[ray_log]

    worst = max(residuals, key=lambda item: abs(residuals[item]))
    print(f"primitive characteristics checked = {len(residuals)}")
    print(f"worst characteristic = {worst}")
    print(f"maximum log-square residual = {abs(residuals[worst]):.3e}")
    if len(residuals) != 18 or abs(residuals[worst]) > 2e-8:
        raise AssertionError("dimension-six ray bridge audit failed")


if __name__ == "__main__":
    main()
