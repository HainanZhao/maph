#!/usr/bin/env python3
"""Apply the corrected Engine-B two-route predicate to B-routed anchors."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SCREEN = ROOT / "scripts" / "screen_engine_b_two_route.gp"
OUTPUT = ROOT / "artifacts" / "corrected-battery-anchor-b-v1.json"
TRANSCRIPT = (
    ROOT / "artifacts" / "corrected-battery-anchor-b-v1.transcript"
)

# The two dimension-seven form strata have the same ray datum but are replayed
# in separate fresh processes so the seven-anchor ledger remains explicit.
CASES = [
    ("B-d5-ray5", 3, [[5, 0], [0, 5]]),
    ("B-d7-disc8", 2, [[14, 0], [0, 14]]),
    ("B-d7-disc32", 2, [[14, 0], [0, 14]]),
]


def one_int(lines: list[str], key: str) -> int:
    prefix = f"{key}="
    values = [line[len(prefix):] for line in lines if line.startswith(prefix)]
    if len(values) != 1:
        raise RuntimeError(f"expected one {key}, got {len(values)}")
    return int(values[0])


def main() -> int:
    if OUTPUT.exists() or TRANSCRIPT.exists():
        raise RuntimeError("versioned corrected-anchor output already exists")
    records = []
    with TRANSCRIPT.open("w", encoding="utf-8") as transcript:
        for index, (case_id, d, hnf) in enumerate(CASES, start=1):
            prelude = (
                f'CASE_ID="{case_id}";\nD_VALUE={d};\n'
                f"H11={hnf[0][0]};H12={hnf[0][1]};"
                f"H21={hnf[1][0]};H22={hnf[1][1]};\n"
            )
            completed = subprocess.run(
                ["gp", "-q"],
                input=(prelude + SCREEN.read_text()).encode(),
                capture_output=True,
                cwd=ROOT,
                timeout=3600,
                check=False,
            )
            text = (completed.stdout + completed.stderr).decode(
                errors="replace"
            )
            lines = [
                line.strip() for line in text.splitlines() if line.strip()
            ]
            base_count = (
                one_int(lines, "ROUTE1_ABELIAN_IMAGINARY_BASE_COUNT")
                if completed.returncode == 0
                else 0
            )
            match_count = (
                one_int(lines, "TWO_ROUTE_RAY_SUBFIELD_MATCH_COUNT")
                if completed.returncode == 0
                else 0
            )
            complete = (
                one_int(lines, "ENGINE_B_TWO_ROUTE_SCREEN_COMPLETE")
                if completed.returncode == 0
                else 0
            )
            passed = (
                completed.returncode == 0
                and base_count > 0
                and match_count > 0
                and complete == 1
            )
            records.append(
                {
                    "anchor_id": case_id,
                    "d": d,
                    "finite_ideal_hnf": hnf,
                    "route1_abelian_imaginary_base_count": base_count,
                    "two_route_ray_subfield_match_count": match_count,
                    "passed": passed,
                    "returncode": completed.returncode,
                    "output_sha256": hashlib.sha256(
                        text.encode()
                    ).hexdigest(),
                }
            )
            transcript.write(
                f"===== {index}/3 {case_id} PASSED={int(passed)} "
                f"=====\n{text}\n"
            )
            transcript.flush()
            print(
                f"CORRECTED_ANCHOR_B={index}/3 CASE={case_id} "
                f"PASSED={int(passed)}",
                flush=True,
            )
            if not passed:
                break
    all_passed = len(records) == len(CASES) and all(
        record["passed"] for record in records
    )
    payload = {
        "schema": "effective-stark-corrected-anchor-b-v1",
        "claim_tag": "VERIFIED_W2_SCREEN" if all_passed else "FAILED_GATE",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "corrected_screen_sha256": hashlib.sha256(
            SCREEN.read_bytes()
        ).hexdigest(),
        "expected_anchor_count": len(CASES),
        "passed_anchor_count": sum(r["passed"] for r in records),
        "records": records,
        "transcript_sha256": hashlib.sha256(
            TRANSCRIPT.read_bytes()
        ).hexdigest(),
        "verdict": (
            "CORRECTED_B_ROUTED_ANCHORS_PASSED"
            if all_passed
            else "CORRECTED_B_ROUTED_ANCHOR_MISMATCH"
        ),
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
