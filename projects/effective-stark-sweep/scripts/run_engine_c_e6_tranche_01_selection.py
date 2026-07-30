#!/usr/bin/env python3
"""Run exact generic character selection on the first three e=6 fields."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
CONFIG = ROOT / "data/engine-c-e6-tranche-01-selection-v1.json"
GENERIC = ROOT / "scripts/run_generic_engine_c_character_selection.py"
GP_SOURCE = ROOT / "scripts/generic_engine_c_character_selection.gp"
OUTPUT = ROOT / "artifacts/engine-c-e6-tranche-01-selection-v1.json"
TRANSCRIPT = ROOT / "artifacts/engine-c-e6-tranche-01-selection-v1.transcript"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_generic():
    spec = importlib.util.spec_from_file_location("generic_selector", GENERIC)
    if spec is None or spec.loader is None:
        raise RuntimeError("generic selector import failed")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    source = GP_SOURCE.read_text(encoding="utf-8")
    generic = load_generic()
    records = []
    transcripts = []
    for index, record in enumerate(config["records"], start=1):
        result, transcript = generic.run(
            record, config["coefficient_limit"], source
        )
        if not result["relative_abelian_certified"]:
            raise RuntimeError(f"{record['case_id']}: nonabelian route")
        if result["character_field_roots_of_unity_e"] != 6:
            raise RuntimeError(f"{record['case_id']}: e != 6")
        if not result["global_unit_clause_applies"]:
            raise RuntimeError(f"{record['case_id']}: |S| < 3")
        records.append(result)
        transcripts.append(
            f"===== {index}/6 {record['case_id']} "
            f"{record['route_id']} =====\n{transcript}"
        )
    if len({row["case_id"] for row in records}) != 3:
        raise RuntimeError("field count changed")
    TRANSCRIPT.write_text("\n".join(transcripts), encoding="utf-8")
    payload = {
        "schema": "effective-stark-engine-c-e6-tranche-01-selection-v1",
        "claim_tag": "VERIFIED_EXACT_CHARACTER_SELECTION",
        "field_count": 3,
        "route_count": 6,
        "records": records,
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (CONFIG, GENERIC, GP_SOURCE, SELF)
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
    print("E6_SELECTION_VERIFIED=1")
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")


if __name__ == "__main__":
    main()
