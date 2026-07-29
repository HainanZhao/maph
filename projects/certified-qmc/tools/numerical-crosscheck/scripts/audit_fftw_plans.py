#!/usr/bin/env python3
"""Freeze the FFTW_ESTIMATE plans used by the Workstream-B producer model."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TOOL_ROOT = ROOT / "tools" / "numerical-crosscheck"
SOURCE = TOOL_ROOT / "native" / "fftw_plan_audit.c"
BINARY = ROOT / "build" / "numerical-crosscheck" / "fftw_plan_audit"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def command_output(*args: str) -> str:
    return subprocess.check_output(args, text=True).strip()


def parse_transcript(text: str) -> tuple[dict[str, str], list[dict[str, object]]]:
    metadata: dict[str, str] = {}
    plans: list[dict[str, object]] = []
    for line in text.splitlines():
        fields = line.split("\t")
        if fields[0] == "META" and len(fields) == 3:
            metadata[fields[1]] = fields[2]
        elif fields[0] == "PLAN" and len(fields) == 8:
            plans.append(
                {
                    "direction": fields[1],
                    "length": int(fields[2]),
                    "adds": int(fields[3]),
                    "muls": int(fields[4]),
                    "fmas": int(fields[5]),
                    "cost": float(fields[6]),
                    "description": fields[7],
                }
            )
        else:
            raise ValueError(f"unrecognized transcript line: {line!r}")
    return metadata, plans


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--maximum-log2", type=int, default=18)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "certificates" / "workstream-b-fftw-plan-audit.json",
    )
    args = parser.parse_args()

    subprocess.run(["make", "-C", str(TOOL_ROOT), "all"], check=True)
    first = command_output(str(BINARY), str(args.maximum_log2))
    second = command_output(str(BINARY), str(args.maximum_log2))
    if first != second:
        raise RuntimeError("FFTW_ESTIMATE transcript was not deterministic")
    metadata, plans = parse_transcript(first)

    compiler = command_output(os.environ.get("CC", "cc"), "--version").splitlines()[0]
    package = command_output(
        "dpkg-query", "-W", "-f=${Version}", "libfftw3-dev"
    )
    certificate = {
        "schema": "certified-qmc/workstream-b-fftw-plan-audit/v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_PLAN_METADATA",
        "scope": {
            "producer": "LatNet Builder fast-CBC",
            "latnet_builder_commit": "39dd60fceb0c86a6124b701072d91f8e3aed73df",
            "maximum_log2": args.maximum_log2,
            "planner_flag": "FFTW_ESTIMATE",
            "rounding_mode_required": "FE_TONEAREST",
        },
        "environment": {
            "platform": platform.platform(),
            "compiler": compiler,
            "fftw_package_version": package,
            **metadata,
        },
        "artifacts": {
            "source": str(SOURCE.relative_to(ROOT)),
            "source_sha256": sha256(SOURCE),
            "binary": str(BINARY),
            "binary_sha256": sha256(BINARY),
            "transcript_sha256": hashlib.sha256(first.encode()).hexdigest(),
        },
        "plans": plans,
        "replay": {
            "command": (
                "python3 tools/numerical-crosscheck/scripts/"
                f"audit_fftw_plans.py "
                f"--maximum-log2 {args.maximum_log2}"
            ),
            "identical_consecutive_transcripts": True,
        },
        "boundary": (
            "The plan transcript and fftw_flops counts are verified metadata. "
            "They are inputs to, not themselves a proof of, a forward-error bound."
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(args.output)


if __name__ == "__main__":
    main()
