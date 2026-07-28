#!/usr/bin/env python3
"""Compare the d=8 conductor-lowered zeta packet with cocycle values."""

from __future__ import annotations

import math
from pathlib import Path
import re
import subprocess

from explore_dimension_eight import principal_overlap


ROOT = Path(__file__).resolve().parents[1]
GP_SCRIPT = ROOT / "scripts" / "explore_dimension_eight_conductor_lowering.gp"
CHARACTERISTIC = re.compile(r"^CHARACTERISTIC=\[(\d+),(\d+)\]$")
PREDICTION = re.compile(r"^  PREDICTED_LOG_SQUARE=(.+)$")


def predicted_logs() -> dict[tuple[int, int], float]:
    process = subprocess.run(
        ["gp", "-q", str(GP_SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    result: dict[tuple[int, int], float] = {}
    current: tuple[int, int] | None = None
    for line in process.stdout.splitlines():
        characteristic_match = CHARACTERISTIC.match(line)
        if characteristic_match:
            current = tuple(map(int, characteristic_match.groups()))
            continue
        prediction_match = PREDICTION.match(line)
        if prediction_match:
            if current is None:
                raise AssertionError("prediction precedes characteristic")
            result[current] = float(prediction_match.group(1))
    return result


def main() -> None:
    predictions = predicted_logs()
    residuals = {}
    for characteristic, prediction in predictions.items():
        overlap = principal_overlap(*characteristic)
        actual = 2 * math.log(abs(overlap))
        residuals[characteristic] = actual - prediction

    worst = max(residuals, key=lambda item: abs(residuals[item]))
    print(f"primitive characteristics checked = {len(residuals)}")
    print(f"worst characteristic = {worst}")
    print(f"maximum log-square residual = {abs(residuals[worst]):.3e}")
    if len(residuals) != 48 or abs(residuals[worst]) > 2e-8:
        raise AssertionError("dimension-eight conductor-lowering audit failed")


if __name__ == "__main__":
    main()
