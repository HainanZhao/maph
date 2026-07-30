#!/usr/bin/env python3
"""Run the three exact negative anchors for the rejected Engine D."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/frozen-ideal-census-v1.json"
W1 = ROOT / "artifacts/w1-full-census-v1.json"
GP = ROOT / "scripts/screen_engine_d_anchor_rejection.gp"
OUTPUT = ROOT / "artifacts/engine-d-anchor-rejections-v1.json"
TRANSCRIPTS = ROOT / "artifacts/engine-d-anchor-rejections"
CASE_IDS = ("RQ-000018", "RQ-000032", "RQ-000274")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_value(value: str) -> object:
    value = value.strip()
    if value.lstrip("-").isdigit():
        return int(value)
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if inner and all(
            item.strip().lstrip("-").isdigit()
            for item in inner.split(",")
        ):
            return [int(item.strip()) for item in inner.split(",")]
    return value


def run_case(case: dict, w1: dict) -> dict:
    hnf = case["finite_ideal_hnf"]
    prefix = (
        f'CASE_ID="{case["case_id"]}";D_VALUE={case["D"]};'
        f"H11={hnf[0][0]};H12={hnf[0][1]};"
        f"H21={hnf[1][0]};H22={hnf[1][1]};\n"
    )
    completed = subprocess.run(
        ["gp", "-q"],
        input=prefix + GP.read_text(encoding="utf-8") + "\n",
        text=True,
        capture_output=True,
        cwd=ROOT,
        timeout=3600,
        check=False,
    )
    fatal = "\n".join(
        line
        for line in completed.stderr.splitlines()
        if "Warning:" not in line
    )
    if completed.returncode or "***" in fatal:
        raise RuntimeError(
            f"{case['case_id']} failed:\n"
            f"{completed.stdout}\n{completed.stderr}"
        )
    TRANSCRIPTS.mkdir(parents=True, exist_ok=True)
    transcript = TRANSCRIPTS / f"{case['case_id']}.txt"
    transcript.write_text(completed.stdout, encoding="utf-8")
    parsed = {}
    for line in completed.stdout.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            parsed[key.lower()] = parse_value(value)
    if parsed.get("anchor_rejection_complete") != 1:
        raise RuntimeError(f"incomplete anchor {case['case_id']}")
    if parsed.get("finite_modulus_galois_stable") != 0:
        raise RuntimeError(
            f"former negative control became stable: {case['case_id']}"
        )
    if parsed.get("absolute_abelian_interpretation_rejected") != 1:
        raise RuntimeError(
            f"absolute-abelian rejection failed: {case['case_id']}"
        )
    return {
        "case_id": case["case_id"],
        "d": case["D"],
        "finite_ideal_hnf": hnf,
        "finite_norm": case["finite_norm"],
        "support_orders": w1["support_orders"],
        "former_index_proxy": w1["shintani_index"],
        "former_commutator_proxy": w1["commutator_size"],
        "exact": parsed,
        "transcript": str(transcript.relative_to(ROOT)),
        "transcript_sha256": sha(transcript),
    }


def main() -> None:
    census = json.loads(SOURCE.read_text(encoding="utf-8"))
    cases = {case["case_id"]: case for case in census["cases"]}
    w1 = json.loads(W1.read_text(encoding="utf-8"))
    w1_by_id = {row["case_id"]: row for row in w1["records"]}
    records = [
        run_case(cases[case_id], w1_by_id[case_id])
        for case_id in CASE_IDS
    ]
    payload = {
        "schema": "effective-stark-engine-d-anchor-rejections-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_NEGATIVE_ANCHOR_BUNDLES",
        "conclusion": (
            "All three former controls have conjugation-unstable finite "
            "moduli. Their index/commutator proxy cannot certify an "
            "absolute-abelian one-place ray field."
        ),
        "records": records,
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (SOURCE, W1, GP, Path(__file__).resolve())
        },
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("NEGATIVE_ANCHORS=3/3")
    print(f"OUTPUT_SHA256={sha(OUTPUT)}")


if __name__ == "__main__":
    main()
