#!/usr/bin/env python3
"""Extract and deduplicate every nontrivial Engine-A quadratic field."""

from __future__ import annotations

import collections
import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "artifacts" / "w1-full-census-v1.json"
A_ANALYSIS = ROOT / "artifacts" / "engine-a-queue-analysis-v1.json"
GP_SCRIPT = ROOT / "scripts" / "screen_engine_a_fields.gp"
OUTPUT = ROOT / "artifacts" / "engine-a-field-census-v1.json"
TRANSCRIPT = ROOT / "artifacts" / "engine-a-field-census-v1.transcript"


def scalar(lines: list[str], key: str) -> str:
    prefix = f"{key}="
    values = [line[len(prefix):] for line in lines if line.startswith(prefix)]
    if len(values) != 1:
        raise RuntimeError(f"expected one {key}, got {len(values)}")
    return values[0]


def main() -> None:
    census = json.loads(CENSUS.read_text())
    by_id = {row["case_id"]: row for row in census["records"]}
    analysis = json.loads(A_ANALYSIS.read_text())
    selected = [by_id[case_id] for case_id in analysis["quadratic_case_ids"]]
    records = []
    TRANSCRIPT.write_text("")
    for index, row in enumerate(selected, start=1):
        hnf = row["finite_ideal_hnf"]
        prelude = (
            f'CASE_ID="{row["case_id"]}";\n'
            f'D_VALUE={row["d"]};\n'
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
        count = int(scalar(
            lines, "SUPPORTED_QUADRATIC_CHARACTER_COUNT"
        ))
        fields = [
            line.split("=", 1)[1]
            for line in lines
            if re.fullmatch(r"QUADRATIC_\d+_ABSOLUTE_FIELD=.*", line)
        ]
        if len(fields) != count:
            raise RuntimeError(
                f"{row['case_id']}: {count} characters but {len(fields)} fields"
            )
        records.append({
            "case_id": row["case_id"],
            "d": row["d"],
            "finite_norm": row["finite_norm"],
            "finite_ideal_hnf": hnf,
            "supported_quadratic_character_count": count,
            "absolute_fields": fields,
            "distinct_absolute_field_count": len(set(fields)),
        })
        with TRANSCRIPT.open("a") as stream:
            stream.write(
                f"===== {index}/{len(selected)} {row['case_id']} =====\n"
                f"{text}\n"
            )
        if index % 100 == 0 or index == len(selected):
            print(f"{index}/{len(selected)}", flush=True)

    multiplicity = collections.Counter(
        field for row in records for field in row["absolute_fields"]
    )
    payload = {
        "schema": "effective-stark-engine-a-field-census-v1",
        "claim_tag": "VERIFIED_EXACT_FIELD_EXTRACTION",
        "source_census_sha256": hashlib.sha256(CENSUS.read_bytes()).hexdigest(),
        "a_analysis_sha256":
            hashlib.sha256(A_ANALYSIS.read_bytes()).hexdigest(),
        "screen_sha256": hashlib.sha256(GP_SCRIPT.read_bytes()).hexdigest(),
        "case_count": len(records),
        "quadratic_packet_occurrence_count": sum(
            row["supported_quadratic_character_count"] for row in records
        ),
        "distinct_absolute_quartic_field_count": len(multiplicity),
        "deduplication_factor": sum(multiplicity.values()) / len(multiplicity),
        "largest_field_multiplicities": [
            {"polynomial": polynomial, "occurrence_count": count}
            for polynomial, count in multiplicity.most_common(30)
        ],
        "records": records,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "case_count": payload["case_count"],
        "quadratic_packet_occurrence_count":
            payload["quadratic_packet_occurrence_count"],
        "distinct_absolute_quartic_field_count":
            payload["distinct_absolute_quartic_field_count"],
        "deduplication_factor": payload["deduplication_factor"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
