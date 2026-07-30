#!/usr/bin/env python3
"""Audit zero imprimitive Euler products over all 1,560 Engine-A rows."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "artifacts/w1-full-census-v1.json"
QUEUE = ROOT / "artifacts/engine-a-queue-analysis-v1.json"
GP = ROOT / "scripts/screen_engine_a_euler_degeneracy.gp"
OUT = ROOT / "artifacts/engine-a-euler-degeneracy-v1.json"
TRANSCRIPT = ROOT / "artifacts/engine-a-euler-degeneracy-v1.transcript"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scalar(text: str, key: str) -> int:
    prefix = f"{key}="
    values = [
        int(line[len(prefix):])
        for line in text.splitlines()
        if line.startswith(prefix)
    ]
    if len(values) != 1:
        raise RuntimeError(f"expected one {key}, got {values}")
    return values[0]


def main() -> None:
    census = json.loads(CENSUS.read_text())
    by_id = {row["case_id"]: row for row in census["records"]}
    queue = json.loads(QUEUE.read_text())
    selected = [by_id[case_id] for case_id in queue["quadratic_case_ids"]]
    gp_source = GP.read_text()
    records = []
    transcripts = []

    for index, row in enumerate(selected, start=1):
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
            check=False,
        )
        if (
            completed.returncode
            or "ENGINE_A_EULER_AUDIT_VERIFIED=1" not in completed.stdout
        ):
            raise RuntimeError(
                f"{row['case_id']} failed\n"
                f"{completed.stdout}{completed.stderr}"
            )
        supported = scalar(
            completed.stdout, "SUPPORTED_QUADRATIC_CHARACTER_COUNT"
        )
        if supported != row["support_count"]:
            raise RuntimeError(f"{row['case_id']}: support count changed")
        records.append(
            {
                "case_id": row["case_id"],
                "supported_quadratic_characters": supported,
                "zero_euler_characters": scalar(
                    completed.stdout, "ZERO_EULER_CHARACTER_COUNT"
                ),
                "removed_primes": scalar(
                    completed.stdout, "REMOVED_PRIME_COUNT"
                ),
            }
        )
        transcripts.append(
            f"===== {index}/{len(selected)} {row['case_id']} =====\n"
            f"{completed.stdout}"
        )
        if index % 100 == 0 or index == len(selected):
            print(f"{index}/{len(selected)}", flush=True)

    TRANSCRIPT.write_text("\n".join(transcripts))
    payload = {
        "schema": "effective-stark-engine-a-euler-degeneracy-v1",
        "claim_tag": "VERIFIED_EXACT_EULER_DEGENERACY_AUDIT",
        "case_count": len(records),
        "supported_quadratic_character_count": sum(
            row["supported_quadratic_characters"] for row in records
        ),
        "characters_with_zero_euler_product": sum(
            row["zero_euler_characters"] for row in records
        ),
        "cases_with_zero_euler_product": sum(
            row["zero_euler_characters"] > 0 for row in records
        ),
        "cases_with_all_supported_euler_products_zero": sum(
            row["zero_euler_characters"]
            == row["supported_quadratic_characters"]
            for row in records
        ),
        "removed_prime_count": sum(
            row["removed_primes"] for row in records
        ),
        "records": records,
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (CENSUS, QUEUE, GP)
        },
        "transcript": {
            "path": str(TRANSCRIPT.relative_to(ROOT)),
            "sha256": sha(TRANSCRIPT),
        },
        "verdict": "VERIFIED",
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(
        "ENGINE_A_ZERO_EULER_CHARACTERS="
        f"{payload['characters_with_zero_euler_product']}"
    )
    print(
        "ENGINE_A_ZERO_EULER_CASES="
        f"{payload['cases_with_zero_euler_product']}"
    )
    print("ENGINE_A_EULER_DEGENERACY_AUDIT=VERIFIED")


if __name__ == "__main__":
    main()
