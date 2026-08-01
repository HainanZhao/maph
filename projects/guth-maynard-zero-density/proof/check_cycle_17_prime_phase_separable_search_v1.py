#!/usr/bin/env python3
"""Integrity and semantic checks for the immutable Cycle 17 discovery result."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "artifacts/cycle-17-prime-phase-separable-search-v1.json"
SEARCH = ROOT / "discovery/search_cycle_17_prime_phase_separable.py"
PREREG = ROOT / "docs/cycle-17-prime-phase-separable-search-preregistration-v1.md"
EXPECTED = {
    RESULT: "8ce4a5592b1ce895b62c659b4568e10992f84f92574db9f2b3f799d1189b89f6",
    SEARCH: "13d194106631511d69fe71ec28aad7f4ca1ca583763a863d2aa214e292372dfc",
    PREREG: "e6b46f7dd33f19fd606289a38860a6731b00813ad5bcad823c2ae8c91fbe666f",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate() -> dict[str, object]:
    for path, expected in EXPECTED.items():
        require(path.is_file(), f"missing Cycle 17 input: {path.name}")
        require(sha256(path) == expected, f"Cycle 17 hash mismatch: {path.name}")
    payload = json.loads(RESULT.read_text(encoding="utf-8"))
    require(payload["artifact_id"] == "cycle-17-prime-phase-separable-search-v1", "artifact id mismatch")
    require(payload["epistemic_status"] == "OBSERVED", "epistemic status mismatch")
    require(payload["status"] == "BASELINE_APPROACHED", "registered outcome mismatch")
    require(len(payload["optimized_rows"]) == 80, "optimized-row count mismatch")
    require(len(payload["deterministic_rows"]) == 35, "deterministic-row count mismatch")
    require(all(row["accepted_monotone"] for row in payload["optimized_rows"]), "nonmonotone optimization row")
    best = payload["best_row"]
    require(best["m"] == 16 and best["family"] == "alternating", "best-family mismatch")
    require(best["count"] == 67, "best-count mismatch")
    require(best["count_exponent"] >= 1.5, "baseline marker not reached")
    larger = {}
    for m in (32, 48, 64):
        rows = [row for row in payload["optimized_rows"] + payload["deterministic_rows"] if row["m"] == m]
        row = max(rows, key=lambda value: (value["count_exponent"], value["count"]))
        require(row["count_exponent"] < 36 / 25, f"unexpected larger-size target crossing: m={m}")
        larger[str(m)] = {"count": row["count"], "count_exponent": row["count_exponent"]}
    return {"status": payload["status"], "best": best, "larger_size_best": larger}


if __name__ == "__main__":
    print(json.dumps(validate(), indent=2, sort_keys=True))
