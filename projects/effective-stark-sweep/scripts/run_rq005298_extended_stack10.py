#!/usr/bin/env python3
"""Cycle-096 restart of RQ-005298 with a larger exact GP stack."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "scripts/screen_engine_c_geometry.gp"
AMENDMENT = ROOT / "docs/cycle-096-rq005298-memory-cap-amendment.md"
OUTPUT = ROOT / "artifacts/rq005298-extended-resolvent-stack10-v1.json"
CAP_SECONDS = 10_800
STACK_BYTES = 10_000_000_000

def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()

def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())

def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("versioned output already exists")
    original = SCREEN.read_text()
    screen = original.replace(
        "default(parisizemax, 4000000000);",
        f"default(parisizemax, {STACK_BYTES});",
        1,
    )
    if screen == original:
        raise RuntimeError("historical GP stack declaration not found")
    prelude = ('CASE_ID="RQ-005298";D_VALUE=130;'
               'H11=24;H12=8;H21=0;H22=4;PACKET_FILTER=4;\n')
    started = datetime.now(timezone.utc)
    clock = time.monotonic()
    try:
        result = subprocess.run(
            ["gp", "-q"], input=prelude + screen, text=True,
            capture_output=True, cwd=ROOT, timeout=CAP_SECONDS, check=False,
        )
        status = "COMPLETED" if result.returncode == 0 else "GP_NONZERO_EXIT"
        stdout, stderr, code = result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired as error:
        status, code = "CAP_EXPIRED_NO_VERDICT", None
        stdout = error.stdout.decode(errors="replace") if isinstance(error.stdout, bytes) else (error.stdout or "")
        stderr = error.stderr.decode(errors="replace") if isinstance(error.stderr, bytes) else (error.stderr or "")
    payload = {
        "schema": "effective-stark-rq005298-extended-resolvent-stack10-v1",
        "claim_tag": "OBSERVED_COMPUTE_STATUS", "case_id": "RQ-005298",
        "packet_index": 4, "cap_seconds": CAP_SECONDS,
        "stack_bytes": STACK_BYTES, "started_at_utc": started.isoformat(),
        "wall_seconds": time.monotonic() - clock, "status": status,
        "returncode": code, "stdout": stdout, "stderr": stderr,
        "source_hashes": {
            "scripts/screen_engine_c_geometry.gp": sha256(SCREEN),
            "in_memory_stack10_geometry_source": sha256_bytes(screen.encode()),
            "docs/cycle-096-rq005298-memory-cap-amendment.md": sha256(AMENDMENT),
            "scripts/run_rq005298_extended_stack10.py": sha256(Path(__file__)),
        }, "mathematical_verdict": None,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"RQ005298_STACK10={status}", flush=True)

if __name__ == "__main__":
    main()
