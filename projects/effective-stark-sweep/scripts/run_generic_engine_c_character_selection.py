#!/usr/bin/env python3
"""Run the generic exact Engine-C character selector on frozen cases."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
CONFIG = ROOT / "data/engine-c-character-selection-cases-v1.json"
GP_SOURCE = ROOT / "scripts/generic_engine_c_character_selection.gp"
OUTPUT = ROOT / "artifacts/engine-c-character-selection-v1.json"
TRANSCRIPT = ROOT / "artifacts/engine-c-character-selection-v1.transcript"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scalar(text: str, key: str) -> str:
    values = re.findall(
        rf"^{re.escape(key)}=(.*)$", text, flags=re.MULTILINE
    )
    if len(values) != 1:
        raise RuntimeError(f"{key}: expected one value, got {len(values)}")
    return values[0]


def run(record: dict, coefficient_limit: int, source: str) -> tuple[dict, str]:
    prelude = "\n".join(
        [
            f'CASE_ID="{record["case_id"]}";',
            f'ROUTE_ID="{record["route_id"]}";',
            f'REAL_BASE_POLYNOMIAL={record["real_base_polynomial"]};',
            f'REAL_FINITE_HNF={record["real_finite_hnf"]};',
            f'SOURCE_CHARACTER={record["source_character"]};',
            f'PACKET_FIELD_POLYNOMIAL={record["packet_field_polynomial"]};',
            f'CM_BASE_POLYNOMIAL={record["cm_base_polynomial"]};',
            (
                "CHARACTER_FIELD_POLYNOMIAL="
                f'{record["character_field_polynomial"]};'
            ),
            f"COEFFICIENT_LIMIT={coefficient_limit};",
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
    fatal_stderr = "\n".join(
        line
        for line in completed.stderr.splitlines()
        if "Warning:" not in line
    )
    if (
        completed.returncode != 0
        or "***" in fatal_stderr
        or "GENERIC_ENGINE_C_CHARACTER_SELECTION_VERIFIED=1"
        not in completed.stdout
    ):
        raise RuntimeError(
            f'{record["case_id"]}/{record["route_id"]} failed:\n'
            f"{completed.stdout}\n{completed.stderr}"
        )
    result = {
        "case_id": scalar(completed.stdout, "CASE_ID"),
        "route_id": scalar(completed.stdout, "ROUTE_ID"),
        "role": record["role"],
        "source_conductor": scalar(
            completed.stdout, "SOURCE_CONDUCTOR"
        ),
        "cm_base": scalar(completed.stdout, "CM_BASE"),
        "cm_base_roots_of_unity_w_k": int(
            scalar(completed.stdout, "CM_BASE_ROOTS_OF_UNITY_W_K")
        ),
        "character_field_polynomial": scalar(
            completed.stdout, "CHARACTER_FIELD_POLYNOMIAL"
        ),
        "character_field_class_number": int(
            scalar(completed.stdout, "CHARACTER_FIELD_CLASS_NUMBER")
        ),
        "character_field_roots_of_unity_e": int(
            scalar(
                completed.stdout,
                "CHARACTER_FIELD_ROOTS_OF_UNITY_E",
            )
        ),
        "canonical_relative_factor": scalar(
            completed.stdout, "CANONICAL_RELATIVE_FACTOR"
        ),
        "cm_conductor": scalar(completed.stdout, "CM_CONDUCTOR"),
        "cm_conductor_factorization": scalar(
            completed.stdout, "CM_CONDUCTOR_FACTORIZATION"
        ),
        "cm_ray_cyc": scalar(completed.stdout, "CM_RAY_CYC"),
        "cm_ray_subgroup_hnf": scalar(
            completed.stdout, "CM_RAY_SUBGROUP_HNF"
        ),
        "compatible_quartic_characters": scalar(
            completed.stdout, "COMPATIBLE_QUARTIC_CHARACTERS"
        ),
        "selected_cm_character": scalar(
            completed.stdout, "SELECTED_CM_CHARACTER"
        ),
        "inverse_cm_character": scalar(
            completed.stdout, "INVERSE_CM_CHARACTER"
        ),
        "exact_separator_index": int(
            scalar(completed.stdout, "EXACT_SEPARATOR_INDEX")
        ),
        "source_separator_coefficient": scalar(
            completed.stdout, "SOURCE_SEPARATOR_COEFFICIENT"
        ),
        "selected_separator_coefficient": scalar(
            completed.stdout, "SELECTED_SEPARATOR_COEFFICIENT"
        ),
        "inverse_separator_coefficient": scalar(
            completed.stdout, "INVERSE_SEPARATOR_COEFFICIENT"
        ),
        "distinct_finite_conductor_primes": int(
            scalar(
                completed.stdout,
                "DISTINCT_FINITE_CONDUCTOR_PRIMES",
            )
        ),
        "stark_s_size": int(
            scalar(completed.stdout, "STARK_S_SIZE")
        ),
        "global_unit_clause_applies": bool(
            int(
                scalar(
                    completed.stdout,
                    "GLOBAL_UNIT_CLAUSE_APPLIES",
                )
            )
        ),
        "claim_tag": scalar(completed.stdout, "CLAIM_TAG"),
    }
    expected = record["banked_selected_character"]
    if expected is not None and result["selected_cm_character"] != expected:
        raise RuntimeError(
            f"anchor mismatch: {result['selected_cm_character']} != {expected}"
        )
    return result, completed.stdout


def main() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    source = GP_SOURCE.read_text(encoding="utf-8")
    results = []
    transcripts = []
    for index, record in enumerate(config["records"], start=1):
        result, transcript = run(
            record, config["coefficient_limit"], source
        )
        results.append(result)
        transcripts.append(
            f"===== {index}/{len(config['records'])} "
            f"{record['case_id']} {record['route_id']} =====\n"
            f"{transcript}"
        )
    if any(not result["global_unit_clause_applies"] for result in results):
        raise RuntimeError("a frozen route failed the |S|>=3 scope gate")
    if any(result["exact_separator_index"] != 5 for result in results):
        raise RuntimeError("frozen separator index changed")

    TRANSCRIPT.write_text("\n".join(transcripts), encoding="utf-8")
    payload = {
        "schema": "effective-stark-engine-c-character-selection-v1",
        "claim_tag": "VERIFIED_EXACT_CHARACTER_SELECTION",
        "route_count": len(results),
        "anchor_replay_count": sum(
            result["role"] == "REGRESSION_ANCHOR"
            for result in results
        ),
        "new_case_route_count": sum(
            result["role"] == "NEW_CASE_ROUTE"
            for result in results
        ),
        "coefficient_limit": config["coefficient_limit"],
        "records": results,
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (CONFIG, GP_SOURCE, SELF)
        },
        "transcript": {
            "path": str(TRANSCRIPT.relative_to(ROOT)),
            "sha256": sha(TRANSCRIPT),
        },
        "promotion_boundary": (
            "Exact character selection alone does not identify a Stark "
            "unit or promote a real packet."
        ),
    }
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(serialized, encoding="utf-8")
    print(f"ROUTE_COUNT={len(results)}")
    print("ANCHOR_REPLAY=1")
    print("NEW_CASE_ROUTES=2")
    print(f"OUTPUT_SHA256={hashlib.sha256(serialized.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
