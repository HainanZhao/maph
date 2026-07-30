#!/usr/bin/env python3
"""Measure exact safe exponents for the frozen theorem-value pilot."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "data" / "theorem-value-exponent-pilot-v1.json"
GP_SCRIPT = ROOT / "scripts" / "compute_imaginary_divisor_exponent.gp"
OUTPUT = ROOT / "artifacts" / "theorem-value-exponent-pilot-v1.json"
TRANSCRIPT = (
    ROOT / "artifacts" / "theorem-value-exponent-pilot-v1.transcript"
)


def scalar(lines: list[str], key: str) -> str:
    prefix = f"{key}="
    values = [line[len(prefix):] for line in lines if line.startswith(prefix)]
    if len(values) != 1:
        raise RuntimeError(f"expected one {key}, got {len(values)}")
    return values[0]


def main() -> None:
    freeze = json.loads(FREEZE.read_text())
    records = []
    TRANSCRIPT.write_text("")
    for index, route in enumerate(freeze["routes"], start=1):
        hnf = route["conductor_hnf"]
        label = route.get("route_label", "selected")
        prelude = (
            f'CASE_ID="{route["case_id"]}";\n'
            f'ROUTE_LABEL="{label}";\n'
            f'BASE_A={route["base_a"]};BASE_B={route["base_b"]};\n'
            f'H11={hnf[0][0]};H12={hnf[0][1]};'
            f'H21={hnf[1][0]};H22={hnf[1][1]};\n'
        )
        completed = subprocess.run(
            ["gp", "-q"],
            input=(prelude + GP_SCRIPT.read_text()).encode(),
            check=True,
            capture_output=True,
            cwd=ROOT,
        )
        text = completed.stdout.decode()
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        measured_count = int(scalar(lines, "SHINTANI_DIVISOR_COUNT"))
        if measured_count != route["divisor_count"]:
            raise RuntimeError(
                f"{route['case_id']} {label}: frozen divisor count "
                f"{route['divisor_count']} != measured {measured_count}"
            )
        record = dict(route)
        record.update({
            "route_label": label,
            "base_discriminant": int(
                scalar(lines, "BASE_DISCRIMINANT")
            ),
            "base_class_number": int(
                scalar(lines, "BASE_CLASS_NUMBER")
            ),
            "base_roots_of_unity": int(
                scalar(lines, "BASE_ROOTS_OF_UNITY")
            ),
            "full_ray_order": int(scalar(lines, "FULL_RAY_ORDER")),
            "safe_exponent": int(
                scalar(lines, "SHINTANI_SAFE_EXPONENT")
            ),
        })
        records.append(record)
        with TRANSCRIPT.open("a") as stream:
            stream.write(
                f"===== {index}/{len(freeze['routes'])} "
                f"{route['case_id']} {label} =====\n{text}\n"
            )
        print(
            f"{route['case_id']} {label} "
            f"safe_exponent={record['safe_exponent']}"
        )

    payload = {
        "schema": "effective-stark-theorem-value-exponent-results-v1",
        "claim_tag": "VERIFIED",
        "freeze_sha256": hashlib.sha256(FREEZE.read_bytes()).hexdigest(),
        "gp_script_sha256":
            hashlib.sha256(GP_SCRIPT.read_bytes()).hexdigest(),
        "record_count": len(records),
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"OUTPUT={OUTPUT}")


if __name__ == "__main__":
    main()
