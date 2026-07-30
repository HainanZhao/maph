#!/usr/bin/env python3
"""Dedicated corrected two-route W2 replay for RQ-002057."""

from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "scripts" / "screen_engine_b_two_route.gp"
OUTPUT = ROOT / "artifacts" / "rq57-norm27-w2-two-route-v1.transcript"
PRELUDE = (
    'CASE_ID="RQ-002057";\n'
    "D_VALUE=57;\n"
    "H11=9;H12=3;H21=0;H22=3;\n"
)
MARKERS = [
    "ROUTE1_ABELIAN_IMAGINARY_BASE_COUNT=2",
    "TWO_ROUTE_RAY_SUBFIELD_MATCH_COUNT=2",
    "ENGINE_B_TWO_ROUTE_SCREEN_COMPLETE=1",
]


def main() -> int:
    if OUTPUT.exists():
        raise RuntimeError("versioned W2 transcript already exists")
    completed = subprocess.run(
        ["gp", "-q"],
        input=(PRELUDE + SCREEN.read_text()).encode(),
        capture_output=True,
        cwd=ROOT,
        timeout=3600,
        check=False,
    )
    text = (completed.stdout + completed.stderr).decode(errors="replace")
    OUTPUT.write_text(text, encoding="utf-8")
    missing = [marker for marker in MARKERS if marker not in text]
    passed = completed.returncode == 0 and not missing
    print(f"RQ57_W2_TWO_ROUTE_PASSED={int(passed)}")
    print(f"MISSING_MARKERS={missing}")
    print(f"TRANSCRIPT_SHA256={hashlib.sha256(OUTPUT.read_bytes()).hexdigest()}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
