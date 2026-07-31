#!/usr/bin/env python3
"""Apply the dominant-embedding gauge to all five phase controls."""

from __future__ import annotations

from decimal import Decimal
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    first = json.loads(
        (
            ROOT
            / "artifacts"
            / "roblot-rq000129-constructor-sealed-v2.json"
        ).read_text()
    )
    remaining = json.loads(
        (
            ROOT
            / "artifacts"
            / "remaining-roblot-constructors-sealed-v1.json"
        ).read_text()
    )
    phase = json.loads(
        (ROOT / "artifacts" / "all-five-phase-gates-v1.json").read_text()
    )
    logs = {
        "RQ-000129": [
            Decimal(value)
            for value in first["numerical_data"]["log_orbit"]
        ]
    }
    # For the four remaining cases, the two independent logarithms are
    # exactly the coefficient's real and imaginary parts and the orbit
    # is (a,b,-a,-b).
    for row in remaining["cases"]:
        coefficient = row["coefficient"]
        a = Decimal(coefficient["real"])
        b = Decimal(coefficient["imag"])
        logs[row["case_id"]] = [a, b, -a, -b]
    q = {
        row["case_id"]: row["defect_quarter_turn"]
        for row in phase["cases"]
    }
    for case_id in sorted(logs):
        orbit = logs[case_id]
        maximum = max(orbit)
        indices = [i for i, value in enumerate(orbit) if value == maximum]
        if len(indices) != 1:
            raise RuntimeError(f"{case_id}: dominant gauge is degenerate")
        j = indices[0]
        canonical = (q[case_id] + j) % 4
        print(
            f"{case_id}|DOMINANT_INDEX={j}"
            f"|RAW_Q={q[case_id]}|DOMINANT_Q={canonical}"
        )
    print("DOMINANT_GAUGE=PASS")


if __name__ == "__main__":
    main()
