#!/usr/bin/env python3
"""Search the preregistered expanded range for four-support degeneracy."""

from __future__ import annotations

import hashlib
import json
import subprocess
import time
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ENUMERATOR = ROOT / "scripts/enumerate_frozen_ideals.gp"
SCREEN = ROOT / "discovery/search_q_four_support_all_zero.gp"
PREREG = ROOT / "docs/cycle-128-q-four-support-falsification-amendment-v1.md"
OUT = ROOT / "discovery/q-four-support-counterexample-search-v2.json"
WALL_CAP_SECONDS = 1200


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matrix(text: str) -> tuple[int, int, int, int]:
    values = tuple(int(value) for value in text.split(","))
    if len(values) != 4:
        raise RuntimeError(f"invalid matrix: {text}")
    return values


def scalar(output: str, key: str) -> str:
    prefix = f"{key}="
    values = [
        line[len(prefix) :].strip()
        for line in output.splitlines()
        if line.startswith(prefix)
    ]
    if len(values) != 1:
        raise RuntimeError(f"expected one {key}, got {values}")
    return values[0]


def enumerate_cases() -> list[dict]:
    program = "D_MIN=2;D_MAX=500;NORM_MAX=300;\n" + ENUMERATOR.read_text()
    completed = subprocess.run(
        ["gp", "-q"],
        input=program,
        text=True,
        capture_output=True,
        cwd=ROOT,
        timeout=300,
        check=False,
    )
    fatal = "\n".join(
        line for line in completed.stderr.splitlines() if "Warning:" not in line
    )
    if completed.returncode or "***" in fatal:
        raise RuntimeError(completed.stdout + completed.stderr)
    representatives: dict[tuple[int, tuple[int, ...]], dict] = {}
    for line in completed.stdout.splitlines():
        parts = line.split("|")
        if parts[0] != "IDEAL":
            continue
        d = int(parts[1])
        norm = int(parts[2])
        if norm <= 100:
            continue
        ideal = matrix(parts[3])
        conjugate = matrix(parts[4])
        canonical = min(ideal, conjugate)
        representatives.setdefault(
            (d, canonical),
            {
                "base_radicand": d,
                "finite_norm": norm,
                "finite_ideal_hnf": [
                    [canonical[0], canonical[1]],
                    [canonical[2], canonical[3]],
                ],
            },
        )
    return sorted(
        representatives.values(),
        key=lambda row: (
            row["base_radicand"],
            row["finite_norm"],
            row["finite_ideal_hnf"],
        ),
    )


def main() -> None:
    started = time.monotonic()
    cases = enumerate_cases()
    screen_source = SCREEN.read_text()
    histogram: Counter[int] = Counter()
    processed = 0
    four_support_rows = 0
    counterexample = None
    terminal = "COMPLETE_NO_COUNTEREXAMPLE"

    for index, case in enumerate(cases, start=1):
        if time.monotonic() - started >= WALL_CAP_SECONDS:
            terminal = "PARTIAL_WALL_CAP_NO_COUNTEREXAMPLE"
            break
        hnf = case["finite_ideal_hnf"]
        case_id = (
            f"XQ-D{case['base_radicand']:03d}-N{case['finite_norm']:03d}-"
            f"{hnf[0][0]}-{hnf[0][1]}-{hnf[1][0]}-{hnf[1][1]}"
        )
        prelude = (
            f'CASE_ID="{case_id}";D_VALUE={case["base_radicand"]};'
            f"H11={hnf[0][0]};H12={hnf[0][1]};"
            f"H21={hnf[1][0]};H22={hnf[1][1]};\n"
        )
        remaining = max(1, int(WALL_CAP_SECONDS - (time.monotonic() - started)))
        completed = subprocess.run(
            ["gp", "-q"],
            input=prelude + screen_source,
            text=True,
            capture_output=True,
            cwd=ROOT,
            timeout=min(60, remaining),
            check=False,
        )
        fatal = "\n".join(
            line for line in completed.stderr.splitlines() if "Warning:" not in line
        )
        if (
            completed.returncode
            or "***" in fatal
            or "Q_FOUR_SUPPORT_COUNTEREXAMPLE_SCREEN_VERIFIED=1"
            not in completed.stdout
        ):
            raise RuntimeError(
                f"{case_id} failed\n{completed.stdout}{completed.stderr}"
            )
        support = int(scalar(completed.stdout, "SUPPORTED_CHARACTER_COUNT"))
        histogram[support] += 1
        processed += 1
        if support == 4:
            four_support_rows += 1
        if int(scalar(completed.stdout, "FOUR_SUPPORT_ALL_ZERO")):
            counterexample = {
                **case,
                "case_id": case_id,
                "support_count": support,
                "zero_euler_character_count": int(
                    scalar(completed.stdout, "ZERO_EULER_CHARACTER_COUNT")
                ),
                "exact_stdout": completed.stdout,
            }
            terminal = "COUNTEREXAMPLE_FOUND"
            break
        if index % 1000 == 0:
            print(f"{index}/{len(cases)}", flush=True)

    payload = {
        "schema": "effective-stark-q-four-support-counterexample-search-v2",
        "supersedes": "discovery/q-four-support-counterexample-search-v1.json",
        "status": terminal,
        "claim_tag": "OBSERVED",
        "range": {
            "D_min": 2,
            "D_max": 500,
            "finite_norm_min": 101,
            "finite_norm_max": 300,
            "ordering": "base radicand, finite norm, canonical HNF",
        },
        "enumerated_selected_moduli": len(cases),
        "processed_selected_moduli": processed,
        "support_count_histogram_completed_prefix": dict(sorted(histogram.items())),
        "four_support_rows_screened": four_support_rows,
        "counterexample": counterexample,
        "runtime_wall_seconds": time.monotonic() - started,
        "resource_cap_wall_seconds": WALL_CAP_SECONDS,
        "source_hashes": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (ENUMERATOR, SCREEN, PREREG, Path(__file__))
        },
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"Q_FOUR_SUPPORT_SEARCH_STATUS={terminal}")
    print(f"Q_FOUR_SUPPORT_ROWS_SCREENED={four_support_rows}")
    if counterexample:
        print(f"Q_FOUR_SUPPORT_COUNTEREXAMPLE={counterexample['case_id']}")


if __name__ == "__main__":
    main()
