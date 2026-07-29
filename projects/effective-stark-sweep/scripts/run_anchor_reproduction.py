#!/usr/bin/env python3
"""Replay the seven frozen Paper-I/II Effective-Stark anchor bundles."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from datetime import datetime, timezone
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = PROJECT_ROOT.parents[1]
SIC_ROOT = WORKSPACE_ROOT / "projects" / "sic-stark"
MANIFEST = PROJECT_ROOT / "data" / "anchor-battery-v1.json"
DEFAULT_OUTPUT = PROJECT_ROOT / "artifacts" / "anchor-reproduction-v1.json"
TRANSCRIPT_DIR = PROJECT_ROOT / "artifacts" / "anchor-transcripts"


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def expand_argv(argv: list[str]) -> list[str]:
    python = SIC_ROOT / ".venv" / "bin" / "python"
    return [str(python) if item == "{PYTHON}" else item for item in argv]


def verify_source(manifest: dict[str, Any]) -> dict[str, str]:
    source = manifest["source"]
    frozen_commit = source["sic_stark_commit"]

    def frozen_blob(path: str) -> bytes:
        return subprocess.run(
            ["git", "show", f"{frozen_commit}:{path}"],
            cwd=WORKSPACE_ROOT,
            check=True,
            capture_output=True,
        ).stdout

    actual = {
        "paper_I_sha256": sha256_bytes(
            frozen_blob(
                "projects/sic-stark/paper/"
                "sic-stark-dimensions-four-five.tex"
            )
        ),
        "paper_II_sha256": sha256_bytes(
            frozen_blob(
                "projects/sic-stark/paper/"
                "sic-stark-dimensions-seven-eight.tex"
            )
        ),
    }
    for key, digest in actual.items():
        if digest != source[key]:
            raise RuntimeError(
                f"source mismatch for {key}: expected {source[key]}, got {digest}"
            )
    tree = subprocess.run(
        [
            "git",
            "rev-parse",
            f"{frozen_commit}:projects/sic-stark",
        ],
        cwd=WORKSPACE_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if tree != source["sic_stark_tree"]:
        raise RuntimeError(
            "Frozen SIC--Stark subtree mismatch: "
            f"expected {source['sic_stark_tree']}, got {tree}"
        )
    return {**actual, "sic_stark_tree": tree}


def run_step(step: dict[str, Any], timeout: int) -> dict[str, Any]:
    argv = expand_argv(step["argv"])
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(SIC_ROOT / "scripts")
    started = time.monotonic()
    completed = subprocess.run(
        argv,
        cwd=SIC_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    elapsed = time.monotonic() - started
    combined = completed.stdout + completed.stderr
    missing = [
        marker
        for marker in step["required_markers"]
        if marker not in combined
    ]
    passed = completed.returncode == 0 and not missing
    return {
        "argv": argv,
        "elapsed_seconds": round(elapsed, 6),
        "missing_markers": missing,
        "output": combined,
        "output_sha256": sha256_bytes(combined.encode("utf-8")),
        "passed": passed,
        "required_markers": step["required_markers"],
        "returncode": completed.returncode,
    }


def write_transcript(anchor_id: str, steps: list[dict[str, Any]]) -> Path:
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)
    path = TRANSCRIPT_DIR / f"{anchor_id}.txt"
    pieces = []
    for index, step in enumerate(steps, start=1):
        pieces.append(
            f"STEP={index}\n"
            f"ARGV={json.dumps(step['argv'])}\n"
            f"RETURNCODE={step['returncode']}\n"
            f"PASSED={int(step['passed'])}\n"
            f"OUTPUT_SHA256={step['output_sha256']}\n"
            "OUTPUT_BEGIN\n"
            f"{step['output']}"
            "OUTPUT_END\n"
        )
    path.write_text("".join(pieces), encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--anchor", action="append", default=[])
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout", type=int, default=3600)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    manifest = load_manifest()
    anchors = manifest["anchors"]
    selected_ids = set(args.anchor)
    full_gate = not selected_ids
    if selected_ids:
        known = {anchor["id"] for anchor in anchors}
        unknown = selected_ids - known
        if unknown:
            parser.error(f"unknown anchors: {sorted(unknown)}")
        anchors = [
            anchor for anchor in anchors if anchor["id"] in selected_ids
        ]

    if args.list:
        for anchor in anchors:
            print(f"{anchor['id']} engine={anchor['engine']} "
                  f"scope={anchor['historical_scope']}")
        return 0

    source = verify_source(manifest)
    if args.dry_run:
        for anchor in anchors:
            for step in anchor["commands"]:
                print(anchor["id"], json.dumps(expand_argv(step["argv"])))
        print(f"DRY_RUN_ANCHOR_COUNT={len(anchors)}")
        print("SOURCE_FREEZE_VERIFIED=1")
        return 0

    records = []
    all_passed = True
    for anchor in anchors:
        print(f"RUNNING_ANCHOR={anchor['id']}", flush=True)
        steps = []
        for step in anchor["commands"]:
            result = run_step(step, args.timeout)
            steps.append(result)
            print(
                f"STEP_RESULT={anchor['id']} "
                f"returncode={result['returncode']} "
                f"missing={len(result['missing_markers'])} "
                f"passed={int(result['passed'])}",
                flush=True,
            )
            if not result["passed"]:
                all_passed = False
                break
        transcript = write_transcript(anchor["id"], steps)
        records.append(
            {
                "anchor_id": anchor["id"],
                "engine": anchor["engine"],
                "passed": all(step["passed"] for step in steps)
                and len(steps) == len(anchor["commands"]),
                "step_count": len(steps),
                "transcript": str(transcript.relative_to(PROJECT_ROOT)),
                "transcript_sha256": sha256_file(transcript),
                "steps": [
                    {
                        key: value
                        for key, value in step.items()
                        if key != "output"
                    }
                    for step in steps
                ],
            }
        )
        if not all_passed:
            print("ANCHOR_MISMATCH_HALT=1", flush=True)
            break

    selected_passed = all_passed and len(records) == len(anchors)
    output = {
        "claim_tag": "VERIFIED" if all_passed else "FAILED_GATE",
        "completed_anchor_count": sum(record["passed"] for record in records),
        "expected_anchor_count": manifest["expected_anchor_count"],
        "gate_scope": "FULL_7_ANCHOR_GATE" if full_gate else "SELECTED_REPLAY",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "records": records,
        "schema": "effective-stark-anchor-reproduction-v1",
        "source": source,
        "verdict": (
            "ANCHOR_GATE_PASSED"
            if selected_passed and full_gate
            else "SELECTED_ANCHORS_PASSED"
            if selected_passed
            else "ANCHOR_GATE_FAILED"
        ),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"RESULT={args.output}")
    return 0 if selected_passed else 1


if __name__ == "__main__":
    sys.exit(main())
