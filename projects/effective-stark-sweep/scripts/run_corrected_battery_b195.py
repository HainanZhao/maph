#!/usr/bin/env python3
"""Freshly re-screen every previously passing Engine-B case.

This is the invalidation repair required after discovery of the
NO_ABELIAN_IMAGINARY_BASE false-pass mode.  It deliberately starts a fresh
PARI process for every case and compares the new deciding data with the
banked corrected-screen record.  A rolling JSON checkpoint makes a VPS
interruption resumable without converting partial work into a verdict.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts" / "engine-b-two-route-analysis-v1.json"
GP_SCRIPT = ROOT / "scripts" / "screen_engine_b_two_route.gp"
DEFAULT_OUTPUT = ROOT / "artifacts" / "corrected-battery-b195-v1.json"
DEFAULT_TRANSCRIPT = (
    ROOT / "artifacts" / "corrected-battery-b195-v1.transcript"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalized(value: str) -> str:
    return "".join(value.split())


def one_value(lines: list[str], key: str) -> str:
    prefix = f"{key}="
    values = [line[len(prefix):] for line in lines if line.startswith(prefix)]
    if len(values) != 1:
        raise RuntimeError(f"expected one {key}, got {len(values)}")
    return values[0]


def checkpoint(
    output: Path,
    records: list[dict[str, Any]],
    expected_count: int,
    source_hash: str,
    screen_hash: str,
    status: str,
) -> None:
    passed = sum(record["passed"] for record in records)
    payload = {
        "schema": "effective-stark-corrected-battery-b195-v1",
        "claim_tag": (
            "VERIFIED_W2_SCREEN"
            if status == "COMPLETE" and passed == expected_count
            else "INCOMPLETE"
        ),
        "status": status,
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_analysis_sha256": source_hash,
        "corrected_screen_sha256": screen_hash,
        "expected_case_count": expected_count,
        "completed_case_count": len(records),
        "passed_case_count": passed,
        "records": records,
        "verdict": (
            "CORRECTED_BATTERY_195_OF_195_PASSED"
            if status == "COMPLETE" and passed == expected_count
            else "NO_VERDICT_PARTIAL_RESCREEN"
        ),
    }
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timeout", type=int, default=3600)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--transcript", type=Path, default=DEFAULT_TRANSCRIPT
    )
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    source_hash = sha256(SOURCE)
    screen_hash = sha256(GP_SCRIPT)
    analysis = json.loads(SOURCE.read_text(encoding="utf-8"))
    selected = [
        record
        for record in analysis["records"]
        if record["classification"] == "TWO_ROUTE_PASS"
    ]
    selected.sort(key=lambda record: record["case_id"])
    if len(selected) != 195:
        raise RuntimeError(
            f"frozen corrected-pass population changed: {len(selected)} != 195"
        )

    records: list[dict[str, Any]] = []
    if args.resume and args.output.exists():
        prior = json.loads(args.output.read_text(encoding="utf-8"))
        if prior["source_analysis_sha256"] != source_hash:
            raise RuntimeError("resume source hash mismatch")
        if prior["corrected_screen_sha256"] != screen_hash:
            raise RuntimeError("resume screen hash mismatch")
        records = prior["records"]
    elif args.output.exists() or args.transcript.exists():
        raise RuntimeError(
            "output exists; use --resume or choose versioned output paths"
        )

    completed_ids = {record["case_id"] for record in records}
    mode = "a" if records else "w"
    args.transcript.parent.mkdir(parents=True, exist_ok=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.transcript.open(mode, encoding="utf-8") as transcript:
        for index, expected in enumerate(selected, start=1):
            if expected["case_id"] in completed_ids:
                continue
            hnf = expected["finite_ideal_hnf"]
            prelude = (
                f'CASE_ID="{expected["case_id"]}";\n'
                f'D_VALUE={expected["d"]};\n'
                f"H11={hnf[0][0]};H12={hnf[0][1]};"
                f"H21={hnf[1][0]};H22={hnf[1][1]};\n"
            )
            try:
                completed = subprocess.run(
                    ["gp", "-q"],
                    input=(prelude + GP_SCRIPT.read_text()).encode(),
                    capture_output=True,
                    cwd=ROOT,
                    timeout=args.timeout,
                    check=False,
                )
            except subprocess.TimeoutExpired as error:
                text = (error.stdout or b"").decode(errors="replace")
                failure = "TIMEOUT"
                returncode = None
            else:
                text = (
                    completed.stdout + completed.stderr
                ).decode(errors="replace")
                failure = (
                    None
                    if completed.returncode == 0
                    else f"GP_EXIT_{completed.returncode}"
                )
                returncode = completed.returncode

            actual: dict[str, Any] = {}
            checks: dict[str, bool] = {}
            if failure is None:
                try:
                    lines = [
                        line.strip()
                        for line in text.splitlines()
                        if line.strip()
                    ]
                    actual = {
                        "route1_abelian_imaginary_base_count": int(
                            one_value(
                                lines,
                                "ROUTE1_ABELIAN_IMAGINARY_BASE_COUNT",
                            )
                        ),
                        "two_route_ray_subfield_match_count": int(
                            one_value(
                                lines,
                                "TWO_ROUTE_RAY_SUBFIELD_MATCH_COUNT",
                            )
                        ),
                        "abelian_imaginary_bases": one_value(
                            lines, "ROUTE1_ABELIAN_IMAGINARY_BASES"
                        ),
                        "normal_closure_absolute_field": one_value(
                            lines, "NORMAL_CLOSURE_ABSOLUTE_FIELD"
                        ),
                        "complete": int(
                            one_value(
                                lines,
                                "ENGINE_B_TWO_ROUTE_SCREEN_COMPLETE",
                            )
                        ),
                    }
                    checks = {
                        "nonempty_abelian_imaginary_base": (
                            actual[
                                "route1_abelian_imaginary_base_count"
                            ]
                            > 0
                        ),
                        "nonempty_route_two_match": (
                            actual[
                                "two_route_ray_subfield_match_count"
                            ]
                            > 0
                        ),
                        "base_count_matches_banked": (
                            actual[
                                "route1_abelian_imaginary_base_count"
                            ]
                            == expected[
                                "route1_abelian_imaginary_base_count"
                            ]
                        ),
                        "match_count_matches_banked": (
                            actual[
                                "two_route_ray_subfield_match_count"
                            ]
                            == expected[
                                "two_route_ray_subfield_match_count"
                            ]
                        ),
                        "bases_match_banked": normalized(
                            actual["abelian_imaginary_bases"]
                        )
                        == normalized(expected["abelian_imaginary_bases"]),
                        "normal_closure_matches_banked": normalized(
                            actual["normal_closure_absolute_field"]
                        )
                        == normalized(
                            expected["normal_closure_absolute_field"]
                        ),
                        "screen_completed": actual["complete"] == 1,
                    }
                except (KeyError, RuntimeError, ValueError) as error:
                    failure = f"PARSE_ERROR:{error}"

            passed = failure is None and all(checks.values())
            record = {
                "case_id": expected["case_id"],
                "d": expected["d"],
                "finite_norm": expected["finite_norm"],
                "finite_ideal_hnf": hnf,
                "returncode": returncode,
                "failure": failure,
                "checks": checks,
                "actual": actual,
                "passed": passed,
                "output_sha256": hashlib.sha256(
                    text.encode()
                ).hexdigest(),
            }
            records.append(record)
            transcript.write(
                f"===== {index}/195 {expected['case_id']} "
                f"PASSED={int(passed)} =====\n{text}\n"
            )
            transcript.flush()
            checkpoint(
                args.output,
                records,
                195,
                source_hash,
                screen_hash,
                "RUNNING" if passed else "HALTED_ON_MISMATCH",
            )
            print(
                f"CORRECTED_B_RESCREEN={index}/195 "
                f"CASE={expected['case_id']} PASSED={int(passed)}",
                flush=True,
            )
            if not passed:
                print("CORRECTED_BATTERY_MISMATCH_HALT=1", flush=True)
                return 1

    checkpoint(
        args.output,
        records,
        195,
        source_hash,
        screen_hash,
        "COMPLETE",
    )
    print("CORRECTED_BATTERY_195_OF_195_PASSED=1")
    print(f"TRANSCRIPT_SHA256={sha256(args.transcript)}")
    print(f"OUTPUT_SHA256={sha256(args.output)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
