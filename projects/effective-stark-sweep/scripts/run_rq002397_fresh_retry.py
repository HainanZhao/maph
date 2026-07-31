#!/usr/bin/env python3
"""Cycle-094 controlled fresh-process retry of a PARI 2.15.4 crash."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "scripts/screen_engine_c_geometry.gp"
PREREG = ROOT / "docs/cycle-094-fresh-process-segfault-retry.md"
OUTPUT = ROOT / "artifacts/rq002397-fresh-segfault-retry-v1.json"
CAP_SECONDS = 1_200

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("versioned output already exists")
    prelude = ('CASE_ID="RQ-002397";D_VALUE=65;'
               'H11=8;H12=0;H21=0;H22=8;PACKET_FILTER=2;\n')
    started = datetime.now(timezone.utc)
    clock = time.monotonic()
    try:
        result = subprocess.run(
            ["gp", "-q"], input=prelude + SCREEN.read_text(), text=True,
            capture_output=True, cwd=ROOT, timeout=CAP_SECONDS, check=False,
        )
        status = "COMPLETED" if result.returncode == 0 else "GP_NONZERO_EXIT"
        stdout, stderr, code = result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired as error:
        status, code = "CAP_EXPIRED_NO_VERDICT", None
        stdout = error.stdout.decode(errors="replace") if isinstance(error.stdout, bytes) else (error.stdout or "")
        stderr = error.stderr.decode(errors="replace") if isinstance(error.stderr, bytes) else (error.stderr or "")
    payload = {
        "schema": "effective-stark-rq002397-fresh-segfault-retry-v1",
        "claim_tag": "OBSERVED_COMPUTE_STATUS",
        "case_id": "RQ-002397", "packet_index": 2,
        "method": "unchanged PARI/GP 2.15.4 exact geometry screen in a fresh process",
        "cap_seconds": CAP_SECONDS, "started_at_utc": started.isoformat(),
        "wall_seconds": time.monotonic() - clock, "status": status,
        "returncode": code, "stdout": stdout, "stderr": stderr,
        "source_hashes": {
            "scripts/screen_engine_c_geometry.gp": sha256(SCREEN),
            "docs/cycle-094-fresh-process-segfault-retry.md": sha256(PREREG),
            "scripts/run_rq002397_fresh_retry.py": sha256(Path(__file__)),
        },
        "mathematical_verdict": None,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"RQ002397_FRESH_RETRY={status}", flush=True)

if __name__ == "__main__":
    main()
