#!/usr/bin/env python3
"""Prepare the deterministic 128-table Cycle-015 hygiene pilot."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.crt import choose_moduli
from src.scaled_integer import error_numerator_bound


VECTOR = ROOT / "data" / "cycle-015-synthetic-vector-32.16"
SCHEDULE = ROOT / "data" / "primes-schedule-v1.json"
OUTPUT = ROOT / "data" / "cycle-015-pilot-spec.json"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    schedule = json.loads(SCHEDULE.read_text())
    primes = [int(row["p"]) for row in schedule["primes"][:3738]]
    source_hash = digest(VECTOR)
    required: dict[int, int] = {}
    for power in (1, 2, 3):
        weights = [
            Fraction(1, index**power)
            for index in range(1, 17)
        ]
        bound = error_numerator_bound(32, weights)
        required[power] = len(choose_moduli(primes, bound))

    tables = []
    for index in range(128):
        power = index % 3 + 1
        tables.append(
            {
                "table_id": f"pilot-{index:03d}",
                "source_id": "cycle-015-project-synthetic",
                "source_citation": (
                    "Certified-QMC project-authored odd-residue "
                    "hygiene vector"
                ),
                "source_path": str(VECTOR.relative_to(ROOT)),
                "source_snapshot_sha256": source_hash,
                "source_file_sha256": source_hash,
                "N": 32,
                "dimension": 16,
                "weight_power": power,
                "work_prime_count": required[power],
            }
        )
    payload = {
        "schema": "certified-qmc-chunked-production-spec-v1",
        "run_id": "cycle-015-pilot-v1",
        "frozen_at_utc": "2026-07-29T07:29:16Z",
        "prefix_block_size": 512,
        "prime_schedule": "data/primes-schedule-v1.json",
        "prime_schedule_manifest": (
            "certificates/cycle-014-prime-schedule-manifest.json"
        ),
        "preregistrations": [
            "data/cycle-015-preregistration-v2.json",
            "data/workstream-b-production-freeze.json",
            "data/workstream-b-streaming-pilot-preregistration-v2.json"
        ],
        "tables": tables,
        "boundary": (
            "Project-authored synthetic data for resume and verifier "
            "hygiene only; it is not a production merit table."
        ),
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "sha256": digest(OUTPUT),
                "work_prime_counts": required,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
