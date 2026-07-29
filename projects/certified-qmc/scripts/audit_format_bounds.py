#!/usr/bin/env python3
"""Checkpoint exact formatting cells without reading external merit data."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.format_bound import formatting_bound


OUTPUT = ROOT / "certificates" / "workstream-b-format-bound-preflight.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    cases = [
        ("1.2345", 5),
        ("1.2345e-3", 5),
        ("0.0001234", 4),
        ("-12.30", 4),
        ("0.0000", None),
        ("1200", 2),
    ]
    results = [
        formatting_bound(lexeme, significant_digits=digits).as_dict()
        for lexeme, digits in cases
    ]
    inventory = json.loads(
        (ROOT / "data" / "workstream-b-table-inventory.json").read_text()
    )
    certificate = {
        "schema": "certified-qmc/workstream-b-format-bound-preflight/v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_EXACT_FORMAT_CELLS",
        "assumption": "round-to-nearest on the observed decimal grid",
        "cases": results,
        "source": {
            "path": "src/format_bound.py",
            "sha256": sha256(ROOT / "src" / "format_bound.py"),
        },
        "current_frozen_set": {
            "table_count": inventory["counts"]["frozen_tables"],
            "merit_column_count": inventory["counts"][
                "frozen_tables_with_merit_columns"
            ],
            "format_bounds_required": 0,
        },
        "boundary": (
            "These are synthetic exact formatting cells. No external merit "
            "lexeme was read or compared."
        ),
    }
    OUTPUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(OUTPUT)


if __name__ == "__main__":
    main()
