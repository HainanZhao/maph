#!/usr/bin/env python3
"""Cycle-093, 10,800-second exact rerun of the deferred RQ-005298 kernel."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import time


ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "scripts/screen_engine_c_geometry.gp"
PREREGISTRATION = ROOT / "docs/cycle-093-quartic-completion-preregistration.md"
OUTPUT = ROOT / "artifacts/rq005298-extended-resolvent-v1.json"
CAP_SECONDS = 10_800


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("versioned output already exists")
    prelude = (
        'CASE_ID="RQ-005298";D_VALUE=130;'
        "H11=24;H12=8;H21=0;H22=4;PACKET_FILTER=4;\n"
    )
    started = datetime.now(timezone.utc)
    wall_start = time.monotonic()
    try:
        completed = subprocess.run(
            ["gp", "-q"], input=prelude + SCREEN.read_text(), text=True,
            capture_output=True, cwd=ROOT, timeout=CAP_SECONDS, check=False,
        )
        verdict = "COMPLETED" if completed.returncode == 0 else "GP_NONZERO_EXIT"
        stdout, stderr, returncode = (
            completed.stdout, completed.stderr, completed.returncode,
        )
    except subprocess.TimeoutExpired as error:
        verdict, returncode = "CAP_EXPIRED_NO_VERDICT", None
        stdout = error.stdout.decode(errors="replace") if isinstance(error.stdout, bytes) else (error.stdout or "")
        stderr = error.stderr.decode(errors="replace") if isinstance(error.stderr, bytes) else (error.stderr or "")
    payload = {
        "schema": "effective-stark-rq005298-extended-resolvent-v1",
        "claim_tag": "OBSERVED_COMPUTE_STATUS",
        "case_id": "RQ-005298",
        "packet_index": 4,
        "method": "unchanged PARI/GP 2.15.4 exact geometry screen",
        "cap_seconds": CAP_SECONDS,
        "started_at_utc": started.isoformat(),
        "wall_seconds": time.monotonic() - wall_start,
        "status": verdict,
        "returncode": returncode,
        "stdout": stdout,
        "stderr": stderr,
        "source_hashes": {
            "scripts/screen_engine_c_geometry.gp": sha256(SCREEN),
            "docs/cycle-093-quartic-completion-preregistration.md": sha256(PREREGISTRATION),
            "scripts/run_rq005298_extended.py": sha256(Path(__file__)),
        },
        "mathematical_verdict": None,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"RQ005298_EXTENDED_STATUS={verdict}", flush=True)


if __name__ == "__main__":
    main()
