#!/usr/bin/env python3
"""Emit the complete phase-and-ray-label packet for dimension seven."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess

from dimension_seven_phase_audit import (
    ZETA_ORDER,
    form_value,
    phase_exponent,
    sign_exponent,
)
from explore_dimension_seven import principal_overlap


ROOT = Path(__file__).resolve().parents[1]
GP_SCRIPT = ROOT / "scripts" / "explore_dimension_seven_conductor_lowering.gp"
CHARACTERISTIC = re.compile(r"^CHARACTERISTIC=\[(\d+),(\d+)\]$")
FACTOR = re.compile(r"^  FACTOR_(\d+)_(\w+)=(.*)$")
PREDICTION = re.compile(r"^  PREDICTED_LOG_SQUARE=(.+)$")


def main() -> None:
    process = subprocess.run(
        ["gp", "-q", str(GP_SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    records: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    for line in process.stdout.splitlines():
        characteristic_match = CHARACTERISTIC.match(line)
        if characteristic_match:
            first, second = map(int, characteristic_match.groups())
            overlap = principal_overlap(first, second)
            sf_phase = phase_exponent(first, second)
            current = {
                "characteristic": [first, second],
                "form_value": form_value(first, second),
                "sf_phase_zeta56_exponent": sf_phase,
                "normalized_overlap_sign": 1 if overlap > 0 else -1,
                "raw_shin_zeta56_exponent": (
                    sign_exponent(overlap) - sf_phase
                )
                % ZETA_ORDER,
                "absolute_normalized_overlap": abs(overlap),
                "factors": [{}, {}],
            }
            records.append(current)
            continue
        factor_match = FACTOR.match(line)
        if factor_match:
            if current is None:
                raise AssertionError("factor precedes characteristic")
            factor_index = int(factor_match.group(1))
            key = factor_match.group(2).lower()
            factors = current["factors"]
            assert isinstance(factors, list)
            factor = factors[factor_index]
            assert isinstance(factor, dict)
            factor[key] = factor_match.group(3)
            continue
        prediction_match = PREDICTION.match(line)
        if prediction_match:
            if current is None:
                raise AssertionError("prediction precedes characteristic")
            current["predicted_log_square"] = float(
                prediction_match.group(1)
            )

    if len(records) != 48:
        raise AssertionError(f"expected 48 records, got {len(records)}")
    if any(
        len(record["factors"]) != 2
        or any(not factor for factor in record["factors"])
        for record in records
    ):
        raise AssertionError("incomplete conductor-lowered factor packet")

    output = {
        "schema": "sic-stark-dimension-seven-complete-packet-v1",
        "dimension": 7,
        "phase_root_order": 56,
        "characteristic_count": len(records),
        "lowered_factor_count": 2 * len(records),
        "records": records,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
