#!/usr/bin/env python3
"""Export exact deleted-prime features for the frozen quadratic stratum."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "artifacts/w1-full-census-v1.json"
QUEUE = ROOT / "artifacts/engine-a-queue-analysis-v1.json"
LABELS = ROOT / "artifacts/engine-a-euler-degeneracy-v1.json"
PREREG = ROOT / "docs/cycle-128-q-euler-degeneracy-pattern-preregistration.md"
GP = ROOT / "discovery/export_q_euler_local_features.gp"
OUT = ROOT / "discovery/q-euler-local-features-v1.json"
TRANSCRIPT = ROOT / "discovery/q-euler-local-features-v1.transcript"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scalar(output: str, key: str) -> str:
    prefix = f"{key}="
    values = [
        line[len(prefix) :].strip()
        for line in output.splitlines()
        if line.startswith(prefix)
    ]
    if len(values) != 1:
        raise RuntimeError(f"expected one {key}, got {values}")
    return values[0]


def integer(output: str, key: str) -> int:
    return int(scalar(output, key))


def vector(output: str, key: str) -> list[int]:
    text = scalar(output, key)
    if not text.startswith("[") or not text.endswith("]"):
        raise RuntimeError(f"invalid vector for {key}: {text}")
    inner = text[1:-1].strip()
    return [] if not inner else [int(item.strip()) for item in inner.split(",")]


def matrix(output: str, key: str) -> list[list[int]]:
    text = scalar(output, key)
    match = re.fullmatch(
        r"\[\s*(-?\d+)\s*,\s*(-?\d+)\s*;\s*"
        r"(-?\d+)\s*,\s*(-?\d+)\s*\]",
        text,
    )
    if not match:
        raise RuntimeError(f"invalid 2x2 matrix for {key}: {text}")
    a, b, c, d = (int(value) for value in match.groups())
    return [[a, b], [c, d]]


def main() -> None:
    census = json.loads(CENSUS.read_text())
    by_id = {row["case_id"]: row for row in census["records"]}
    queue = json.loads(QUEUE.read_text())
    labels = json.loads(LABELS.read_text())
    label_by_id = {row["case_id"]: row for row in labels["records"]}
    selected = [by_id[case_id] for case_id in queue["quadratic_case_ids"]]
    gp_source = GP.read_text()
    records: list[dict] = []
    transcripts: list[str] = []
    started = time.monotonic()

    for row_index, row in enumerate(selected, start=1):
        hnf = row["finite_ideal_hnf"]
        prelude = (
            f'CASE_ID="{row["case_id"]}";\n'
            f'D_VALUE={row["d"]};\n'
            f"H11={hnf[0][0]};H12={hnf[0][1]};"
            f"H21={hnf[1][0]};H22={hnf[1][1]};\n"
        )
        completed = subprocess.run(
            ["gp", "-q"],
            input=prelude + gp_source,
            text=True,
            capture_output=True,
            cwd=ROOT,
            timeout=60,
            check=False,
        )
        output = completed.stdout
        if (
            completed.returncode
            or "Q_EULER_LOCAL_FEATURE_EXPORT_VERIFIED=1" not in output
        ):
            raise RuntimeError(
                f"{row['case_id']} failed\n{output}{completed.stderr}"
            )

        support_count = integer(output, "SUPPORTED_CHARACTER_COUNT")
        characters = []
        for character_index in range(1, support_count + 1):
            prefix = f"CHARACTER_{character_index}"
            removed_count = integer(output, f"{prefix}_REMOVED_COUNT")
            deleted_primes = []
            for removed_index in range(1, removed_count + 1):
                local = f"{prefix}_REMOVED_{removed_index}"
                value = integer(output, f"{local}_PRIMITIVE_VALUE")
                deleted_primes.append(
                    {
                        "rational_prime": integer(
                            output, f"{local}_RATIONAL_PRIME"
                        ),
                        "ramification_index": integer(
                            output, f"{local}_RAMIFICATION_INDEX"
                        ),
                        "residue_degree": integer(
                            output, f"{local}_RESIDUE_DEGREE"
                        ),
                        "absolute_norm": integer(
                            output, f"{local}_ABSOLUTE_NORM"
                        ),
                        "modulus_exponent": integer(
                            output, f"{local}_MODULUS_EXPONENT"
                        ),
                        "primitive_character_value": value,
                        "split_in_character_field": value == 1,
                        "prime_hnf": matrix(output, f"{local}_PRIME_HNF"),
                    }
                )
            zero_euler = bool(integer(output, f"{prefix}_ZERO_EULER"))
            if zero_euler != any(
                prime["primitive_character_value"] == 1
                for prime in deleted_primes
            ):
                raise RuntimeError(
                    f"{row['case_id']} character {character_index}: "
                    "local zero criterion failed"
                )
            characters.append(
                {
                    "ray_character": vector(output, f"{prefix}_COORDS"),
                    "primitive_ray_cyc": vector(
                        output, f"{prefix}_PRIMITIVE_CYC"
                    ),
                    "primitive_character": vector(
                        output, f"{prefix}_PRIMITIVE_COORDS"
                    ),
                    "primitive_conductor_hnf": matrix(
                        output, f"{prefix}_PRIMITIVE_CONDUCTOR_HNF"
                    ),
                    "deleted_primes": deleted_primes,
                    "zero_euler": zero_euler,
                }
            )

        label = label_by_id[row["case_id"]]
        zero_count = integer(output, "ZERO_EULER_CHARACTER_COUNT")
        removed_count = integer(output, "REMOVED_PRIME_COUNT")
        if (
            support_count != label["supported_quadratic_characters"]
            or zero_count != label["zero_euler_characters"]
            or removed_count != label["removed_primes"]
        ):
            raise RuntimeError(f"{row['case_id']}: frozen v1 label mismatch")

        records.append(
            {
                "case_id": row["case_id"],
                "base_radicand": row["d"],
                "base_discriminant": row["field_discriminant"],
                "finite_norm": row["finite_norm"],
                "finite_ideal_hnf": hnf,
                "ray_cyc": vector(output, "RAY_CYC"),
                "sign_log": vector(output, "SIGN_LOG"),
                "support_count": support_count,
                "zero_euler_character_count": zero_count,
                "all_supported_euler_factors_zero": zero_count == support_count,
                "characters": characters,
            }
        )
        transcripts.append(
            f"===== {row_index}/{len(selected)} {row['case_id']} =====\n{output}"
        )
        if row_index % 100 == 0 or row_index == len(selected):
            print(f"{row_index}/{len(selected)}", flush=True)

    TRANSCRIPT.write_text("\n".join(transcripts))
    payload = {
        "schema": "effective-stark-q-euler-local-features-v1",
        "status": "EXPLORATORY_EXACT_FEATURE_EXPORT",
        "claim_tag": "OBSERVED",
        "population": {
            "rows": len(records),
            "supported_character_occurrences": sum(
                len(row["characters"]) for row in records
            ),
            "all_zero_rows": sum(
                row["all_supported_euler_factors_zero"] for row in records
            ),
        },
        "runtime_wall_seconds": time.monotonic() - started,
        "records": records,
        "source_hashes": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (CENSUS, QUEUE, LABELS, PREREG, GP)
        },
        "transcript": {
            "path": str(TRANSCRIPT.relative_to(ROOT)),
            "sha256": sha256(TRANSCRIPT),
        },
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"Q_EULER_LOCAL_FEATURE_ROWS={len(records)}")
    print("Q_EULER_LOCAL_FEATURE_EXPORT=PASS")


if __name__ == "__main__":
    main()
