#!/usr/bin/env python3
"""Exact two-route packet bridges for the first three e=6 fields."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
CONFIG = ROOT / "data/engine-c-e6-tranche-01-packet-bridge-v1.json"
ORBIT_CERT = ROOT / "artifacts/engine-c-e6-tranche-01-unit-orbits-v1.json"
GENERIC_RUNNER = ROOT / "scripts/run_engine_c_packet_bridge.py"
GP_SOURCE = ROOT / "scripts/generic_engine_c_packet_bridge.gp"
OUTPUT = ROOT / "artifacts/engine-c-e6-tranche-01-packet-bridge-v1.json"
TRANSCRIPT = ROOT / "artifacts/engine-c-e6-tranche-01-packet-bridge-v1.transcript"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_generic():
    spec = importlib.util.spec_from_file_location(
        "generic_packet_bridge", GENERIC_RUNNER
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("packet-bridge import failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    generic = load_generic()
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    orbit_cert = json.loads(ORBIT_CERT.read_text(encoding="utf-8"))
    certified = {
        (row["case_id"], row["route_id"]): {
            tuple(value) for value in row["isolated_integral_orbit"]
        }
        for row in orbit_cert["records"]
    }
    source = GP_SOURCE.read_text(encoding="utf-8")
    records = []
    transcripts = []
    polynomial_sets: dict[tuple[str, str], set[str]] = {}
    for record in config["records"]:
        key = (record["case_id"], record["route_id"])
        coordinate = tuple(
            int(item)
            for item in record["candidate_coordinates"]
            .strip("[]")
            .split(",")
        )
        if coordinate not in certified[key]:
            raise RuntimeError(f"{key}: coordinate not certified")
        prelude = "\n".join(
            [
                f'CASE_ID="{record["case_id"]}";',
                f'ROUTE_ID="{record["route_id"]}";',
                "CHARACTER_FIELD_POLYNOMIAL="
                f'{record["character_field_polynomial"]};',
                "REAL_SELECTOR_FIELD_POLYNOMIAL="
                f'{record["real_selector_field_polynomial"]};',
                f'CANDIDATE_COORDINATES={record["candidate_coordinates"]};',
                f'SEPARATOR_PRIME={record["separator_prime"]};',
            ]
        )
        completed = subprocess.run(
            ["gp", "-q"],
            input=prelude + "\n" + source,
            text=True,
            capture_output=True,
            cwd=ROOT,
            timeout=600,
            check=False,
        )
        if (
            completed.returncode != 0
            or "GENERIC_ENGINE_C_PACKET_BRIDGE_VERIFIED=1"
            not in completed.stdout
        ):
            raise RuntimeError(
                f"{key} failed:\n{completed.stdout}\n{completed.stderr}"
            )
        text = completed.stdout
        count = int(
            generic.scalar(text, "DISTINCT_POSITIVE_NORM_POLYNOMIAL_COUNT")
        )
        polynomials = [
            generic.scalar(text, f"POSITIVE_NORM_POLYNOMIAL_{index}")
            for index in range(1, count + 1)
        ]
        polynomial_sets[key] = set(polynomials)
        fixed = [
            int(
                generic.scalar(
                    text, f"ARTIN_LABEL_{index}_CONJUGATION_FIXED"
                )
            )
            == 1
            for index in range(4)
        ]
        if not all(fixed):
            raise RuntimeError(f"{key}: Artin norm not conjugation-fixed")
        records.append(
            {
                **record,
                "candidate_minpoly": generic.scalar(
                    text, "CANDIDATE_MINPOLY"
                ),
                "candidate_norm": generic.scalar(text, "CANDIDATE_NORM"),
                "normal_closure_degree": int(
                    generic.scalar(text, "NORMAL_CLOSURE_DEGREE")
                ),
                "positive_norm_polynomials": polynomials,
                "artin_labeled_packet_polynomial": generic.scalar(
                    text, "ARTIN_LABELED_PACKET_POLYNOMIAL"
                ),
                "artin_labeled_packet_polynomial_coefficients":
                    generic.rational_polynomial(
                        text, "ARTIN_LABELED_PACKET"
                    ),
                "artin_norms_conjugation_fixed": fixed,
                "normal_field_polynomial_coefficients":
                    generic.rational_polynomial(text, "NORMAL_FIELD"),
                "complex_conjugation_coefficients":
                    generic.rational_polynomial(
                        text, "COMPLEX_CONJUGATION"
                    ),
                "artin_norm_coefficients": [
                    generic.rational_polynomial(
                        text, f"ARTIN_NORM_{index}"
                    )
                    for index in range(4)
                ],
            }
        )
        transcripts.append(
            f"===== {record['case_id']} {record['route_id']} =====\n{text}"
        )
    common_by_case = {}
    for case_id in sorted({row["case_id"] for row in config["records"]}):
        keys = [
            (row["case_id"], row["route_id"])
            for row in config["records"]
            if row["case_id"] == case_id
        ]
        common = polynomial_sets[keys[0]] & polynomial_sets[keys[1]]
        if not common:
            raise RuntimeError(f"{case_id}: no identical two-route packet")
        common_by_case[case_id] = sorted(common)
    TRANSCRIPT.write_text("\n".join(transcripts), encoding="utf-8")
    payload = {
        "schema": "effective-stark-engine-c-e6-tranche-01-packet-bridge-v1",
        "claim_tag": "VERIFIED_EXACT_TWO_ROUTE_PACKET_BRIDGES",
        "field_count": 3,
        "route_count": 6,
        "identical_two_route_packet_polynomials": common_by_case,
        "records": records,
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (
                CONFIG,
                ORBIT_CERT,
                GENERIC_RUNNER,
                GP_SOURCE,
                SELF,
            )
        },
        "transcript": {
            "path": str(TRANSCRIPT.relative_to(ROOT)),
            "sha256": sha(TRANSCRIPT),
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("FIELD_COUNT=3")
    print("ROUTE_COUNT=6")
    print("ALL_TWO_ROUTE_PACKET_BRIDGES_VERIFIED=1")
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")


if __name__ == "__main__":
    main()
