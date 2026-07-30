#!/usr/bin/env python3
"""Run and cross-check the exact two-route Engine-C packet bridge."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
CONFIG = ROOT / "data/engine-c-packet-bridge-cases-v1.json"
ORBIT_CERT = ROOT / "artifacts/engine-c-unit-orbits-v1.json"
GP_SOURCE = ROOT / "scripts/generic_engine_c_packet_bridge.gp"
OUTPUT = ROOT / "artifacts/engine-c-packet-bridge-v1.json"
TRANSCRIPT = ROOT / "artifacts/engine-c-packet-bridge-v1.transcript"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scalar(text: str, key: str) -> str:
    found = re.findall(rf"^{re.escape(key)}=(.*)$", text, re.MULTILINE)
    if len(found) != 1:
        raise RuntimeError(f"{key}: got {len(found)} values")
    return found[0]

def rational_polynomial(text: str, label: str) -> list[list[int]]:
    degree = int(scalar(text, f"{label}_DEGREE"))
    answer = []
    for index in range(degree + 1):
        numerator, denominator = scalar(
            text, f"{label}_COEFF_{index}"
        ).split("/")
        answer.append([int(numerator), int(denominator)])
    return answer


def main() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    orbit_cert = json.loads(ORBIT_CERT.read_text(encoding="utf-8"))
    certified_orbits = {
        (row["case_id"], row["route_id"]): {
            tuple(item) for item in row["isolated_integral_orbit"]
        }
        for row in orbit_cert["records"]
    }
    source = GP_SOURCE.read_text(encoding="utf-8")
    records = []
    transcripts = []
    route_polynomial_sets: dict[tuple[str, str], set[str]] = {}
    for record in config["records"]:
        key = (record["case_id"], record["route_id"])
        coordinate = tuple(
            int(item)
            for item in record["candidate_coordinates"]
            .strip("[]")
            .split(",")
        )
        if coordinate not in certified_orbits.get(key, set()):
            raise RuntimeError(f"{key}: coordinate not in certified orbit")
        prelude = "\n".join(
            [
                f'CASE_ID="{record["case_id"]}";',
                f'ROUTE_ID="{record["route_id"]}";',
                (
                    "CHARACTER_FIELD_POLYNOMIAL="
                    f'{record["character_field_polynomial"]};'
                ),
                (
                    "REAL_SELECTOR_FIELD_POLYNOMIAL="
                    f'{record["real_selector_field_polynomial"]};'
                ),
                (
                    "CANDIDATE_COORDINATES="
                    f'{record["candidate_coordinates"]};'
                ),
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
            raise RuntimeError(completed.stdout + completed.stderr)
        count = int(
            scalar(
                completed.stdout,
                "DISTINCT_POSITIVE_NORM_POLYNOMIAL_COUNT",
            )
        )
        polynomials = [
            scalar(
                completed.stdout,
                f"POSITIVE_NORM_POLYNOMIAL_{index}",
            )
            for index in range(1, count + 1)
        ]
        route_polynomial_sets[key] = set(polynomials)
        records.append(
            {
                **record,
                "candidate_minpoly": scalar(
                    completed.stdout, "CANDIDATE_MINPOLY"
                ),
                "candidate_norm": scalar(
                    completed.stdout, "CANDIDATE_NORM"
                ),
                "normal_closure_degree": int(
                    scalar(completed.stdout, "NORMAL_CLOSURE_DEGREE")
                ),
                "real_conjugation_record_count": int(
                    scalar(
                        completed.stdout,
                        "REAL_CONJUGATION_RECORD_COUNT",
                    )
                ),
                "positive_norm_polynomials": polynomials,
                "artin_labeled_packet_polynomial": scalar(
                    completed.stdout,
                    "ARTIN_LABELED_PACKET_POLYNOMIAL",
                ),
                "artin_labeled_packet_polynomial_coefficients":
                    rational_polynomial(
                        completed.stdout, "ARTIN_LABELED_PACKET"
                    ),
                "normal_sigma_group_index": int(
                    scalar(
                        completed.stdout,
                        "NORMAL_SIGMA_GROUP_INDEX",
                    )
                ),
                "complex_conjugation_group_index": int(
                    scalar(
                        completed.stdout,
                        "COMPLEX_CONJUGATION_GROUP_INDEX",
                    )
                ),
                "artin_labeled_positive_norms": [
                    scalar(
                        completed.stdout,
                        f"ARTIN_LABEL_{index}_POSITIVE_NORM",
                    )
                    for index in range(4)
                ],
                "artin_norms_conjugation_fixed": [
                    int(
                        scalar(
                            completed.stdout,
                            f"ARTIN_LABEL_{index}_CONJUGATION_FIXED",
                        )
                    )
                    == 1
                    for index in range(4)
                ],
                "normal_field_polynomial_coefficients": rational_polynomial(
                    completed.stdout, "NORMAL_FIELD"
                ),
                "complex_conjugation_coefficients": rational_polynomial(
                    completed.stdout, "COMPLEX_CONJUGATION"
                ),
                "artin_norm_coefficients": [
                    rational_polynomial(
                        completed.stdout, f"ARTIN_NORM_{index}"
                    )
                    for index in range(4)
                ],
            }
        )
        transcripts.append(
            f"===== {record['case_id']} {record['route_id']} =====\n"
            f"{completed.stdout}"
        )
    common = (
        route_polynomial_sets[("RQ-001280", "Qsqrt(-10)")]
        & route_polynomial_sets[("RQ-001280", "Qsqrt(-14)")]
    )
    if not common:
        raise RuntimeError("independent routes have no identical norm packet")

    TRANSCRIPT.write_text("\n".join(transcripts), encoding="utf-8")
    payload = {
        "schema": "effective-stark-engine-c-packet-bridge-v1",
        "claim_tag": "VERIFIED_EXACT_TWO_ROUTE_PACKET_BRIDGE",
        "records": records,
        "identical_two_route_packet_polynomials": sorted(common),
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (CONFIG, ORBIT_CERT, GP_SOURCE, SELF)
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
    print(f"ROUTE_COUNT={len(records)}")
    print(f"COMMON_PACKET_POLYNOMIAL_COUNT={len(common)}")
    print("VERIFIED_EXACT_TWO_ROUTE_PACKET_BRIDGE=1")
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")


if __name__ == "__main__":
    main()
