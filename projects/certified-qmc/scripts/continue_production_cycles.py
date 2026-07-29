#!/usr/bin/env python3
"""Continue gated fidelity audit and Cycle-018 work after the live run."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / ".venv" / "bin" / "python"
FIDELITY = ROOT / "artifacts" / "fidelity-v2"
USABILITY = ROOT / "artifacts" / "usability-v1"
FIDELITY_AUDIT = (
    ROOT / "certificates" / "cycles-016-017-production-audit.json"
)
USABILITY_AUDIT = (
    ROOT / "certificates" / "cycle-018-usability-audit.json"
)
LOGICAL_INDEX = USABILITY / "logical-table-index.json"
ENGINE_ORACLE = (
    ROOT / "certificates" / "engine-oracle-set-v1.json"
)
STATE = ROOT / "artifacts" / "cycle-continuation-state.json"
MAX_STALE_SECONDS = 15 * 60


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def last_record(path: Path) -> dict | None:
    if not path.is_file() or path.stat().st_size == 0:
        return None
    with path.open("rb") as stream:
        stream.seek(0, 2)
        position = stream.tell() - 1
        while position >= 0:
            stream.seek(position)
            if stream.read(1) not in (b"\n", b"\r"):
                break
            position -= 1
        end = position + 1
        while position >= 0:
            stream.seek(position)
            if stream.read(1) == b"\n":
                position += 1
                break
            position -= 1
        start = max(position, 0)
        stream.seek(start)
        line = stream.read(end - start)
    return json.loads(line) if line else None


def record_state(stage: str, **extra: object) -> None:
    payload = {
        "schema": "certified-qmc-cycle-continuation-state-v1",
        "updated_at_utc": utc_now(),
        "stage": stage,
        **extra,
    }
    STATE.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )


def run(command: list[str]) -> None:
    completed = subprocess.run(command, cwd=ROOT)
    if completed.returncode != 0:
        record_state(
            "HALTED_SUBPROCESS_FAILURE",
            command=command,
            return_code=completed.returncode,
        )
        raise SystemExit(completed.returncode)


def wait_for_fidelity_seal() -> None:
    manifest = FIDELITY / "manifest.jsonl"
    telemetry = FIDELITY / "telemetry.jsonl"
    while True:
        final = last_record(manifest)
        if final and final.get("event") == "SEAL":
            record_state(
                "FIDELITY_SEALED",
                seal_line_sha256=final["line_sha256"],
            )
            return
        timing = last_record(telemetry)
        if timing and timing.get("event") == "PAUSE":
            record_state(
                "HALTED_FIDELITY_THROUGHPUT_PAUSE",
                telemetry_line_sha256=timing["line_sha256"],
            )
            raise SystemExit(76)
        if telemetry.is_file():
            age = time.time() - telemetry.stat().st_mtime
            if age > MAX_STALE_SECONDS:
                record_state(
                    "HALTED_FIDELITY_STALE",
                    telemetry_age_seconds=age,
                )
                raise SystemExit(74)
        record_state("WAITING_FOR_FIDELITY_SEAL")
        time.sleep(30)


def main() -> None:
    wait_for_fidelity_seal()
    record_state("AUDITING_FIDELITY")
    run(
        [
            str(PYTHON),
            "scripts/audit_fidelity_production.py",
            str(FIDELITY),
            str(FIDELITY_AUDIT),
            utc_now(),
        ]
    )

    record_state("RUNNING_USABILITY")
    run(
        [
            str(PYTHON),
            "scripts/run_chunked_production.py",
            "--spec",
            "data/cycle-018-usability-spec.json",
            "--output",
            str(USABILITY),
        ]
    )

    record_state("AUDITING_USABILITY")
    run(
        [
            str(PYTHON),
            "scripts/audit_usability_production.py",
            str(FIDELITY),
            str(USABILITY),
            str(LOGICAL_INDEX),
            str(USABILITY_AUDIT),
            utc_now(),
        ]
    )
    record_state("BUILDING_ENGINE_ORACLE")
    run(
        [
            str(PYTHON),
            "scripts/build_engine_oracle_set.py",
            "--fidelity",
            str(FIDELITY),
            "--usability",
            str(USABILITY),
            "--output",
            str(ENGINE_ORACLE),
            "--recorded-at-utc",
            utc_now(),
        ]
    )
    record_state(
        "CYCLE_018_DATA_GATE_PASSED",
        fidelity_audit=str(FIDELITY_AUDIT.relative_to(ROOT)),
        usability_audit=str(USABILITY_AUDIT.relative_to(ROOT)),
        logical_index=str(LOGICAL_INDEX.relative_to(ROOT)),
        engine_oracle=str(ENGINE_ORACLE.relative_to(ROOT)),
    )
    print(STATE)


if __name__ == "__main__":
    main()
