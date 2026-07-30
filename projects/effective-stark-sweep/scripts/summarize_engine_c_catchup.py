#!/usr/bin/env python3
"""Seal the 252-row complete-C catch-up result."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/engine-c-catchup-252-v1.json"
OUTPUT = ROOT / "artifacts/engine-c-catchup-summary-v1.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    if source["status"] != "COMPLETE":
        raise RuntimeError("C catch-up is incomplete")
    expected_cases = {
        "C_ELIGIBLE": 153,
        "HAS_TOOL_BLOCK": 1,
        "MIXED_PASS_FAIL": 3,
        "NO_PACKET_PASSES": 95,
    }
    expected_packets = {
        "GEOMETRY_PASS": 203,
        "LINEAR_REINDUCTION_BASE_COUNT_FAIL": 8,
        "NORMAL_CLOSURE_GROUP_NOT_16_13": 1,
        "NORMAL_CLOSURE_ORDER_NE_16": 102,
        "TOOL_BLOCKED": 1,
    }
    if source["case_taxonomy"] != expected_cases:
        raise RuntimeError("C catch-up case taxonomy changed")
    if source["packet_taxonomy"] != expected_packets:
        raise RuntimeError("C catch-up packet taxonomy changed")
    payload = {
        "schema": "effective-stark-engine-c-catchup-summary-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_COMPLETE_C_CATCHUP",
        "predicate_provenance": "GENUINE",
        "catchup_case_count": 252,
        "case_taxonomy": expected_cases,
        "packet_taxonomy": expected_packets,
        "updated_c_accounting": {
            "previous_certified_c_eligible": 728,
            "new_certified_c_eligible": 153,
            "total_certified_c_eligible": 881,
            "tool_blocked_not_counted_as_negative": 1,
        },
        "completeness_statement": (
            "All 252 queued rows reached the complete-C gate. Exactly "
            "881 rows are certified C-eligible across old and catch-up "
            "populations; one additional row remains explicitly "
            "TOOL_BLOCKED and is not a mathematical negative."
        ),
        "source_hashes": {
            str(SOURCE.relative_to(ROOT)): sha(SOURCE),
            "scripts/summarize_engine_c_catchup.py": sha(Path(__file__)),
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
