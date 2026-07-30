#!/usr/bin/env python3
"""Run the ten remaining exact B/C packet-alignment checks."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "artifacts/dual-engine-alignment-queue-v1.json"
SCRIPT = ROOT / "scripts/screen_dual_packet_alignment.gp"
OUTPUT = ROOT / "artifacts/remaining-dual-alignments-v1.json"
TRANSCRIPT = ROOT / "artifacts/remaining-dual-alignments-v1.transcript"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scalar(text: str, key: str) -> str:
    values = re.findall(rf"^{re.escape(key)}=(.*)$", text, re.MULTILINE)
    if len(values) != 1:
        raise RuntimeError(f"expected one {key}, got {len(values)}")
    return values[0]


def main():
    queue = json.loads(QUEUE.read_text())
    records = [
        record for record in queue["records"]
        if record["case_id"] != "RQ-000458"
    ]
    if len(records) != 10:
        raise RuntimeError("remaining overlap count changed")
    script = SCRIPT.read_text()
    outputs = []
    transcripts = []
    for index, record in enumerate(records, start=1):
        hnf = record["finite_ideal_hnf"]
        packet_index = record["c_passing_packet_indices"][0]
        prelude = (
            f'CASE_ID="{record["case_id"]}";D_VALUE={record["d"]};'
            f'H11={hnf[0][0]};H12={hnf[0][1]};'
            f'H21={hnf[1][0]};H22={hnf[1][1]};'
            f'C_PACKET_INDEX={packet_index};\n'
        )
        completed = subprocess.run(
            ["gp", "-q"],
            input=prelude + script,
            text=True,
            capture_output=True,
            cwd=ROOT,
            timeout=600,
        )
        text = completed.stdout
        if "DUAL_PACKET_ALIGNMENT_VERIFIED=1" not in text:
            raise RuntimeError(
                f"{record['case_id']} failed:\n{text}\n{completed.stderr}"
            )
        outputs.append({
            "case_id": record["case_id"],
            "c_packet_index": packet_index,
            "same_modulus": scalar(text, "SAME_MODULUS") == "1",
            "same_ray_classes":
                scalar(text, "SAME_RAY_CLASSES") == "1",
            "same_character_pair":
                scalar(text, "SAME_CHARACTER_PAIR") == "1",
            "identical_relative_packet_polynomial": (
                scalar(
                    text, "IDENTICAL_RELATIVE_PACKET_POLYNOMIAL"
                ) == "1"
            ),
            "identical_absolute_packet_polynomial": (
                scalar(
                    text, "IDENTICAL_ABSOLUTE_PACKET_POLYNOMIAL"
                ) == "1"
            ),
            "c_character": scalar(text, "C_CHARACTER"),
            "c_inverse_character":
                scalar(text, "C_INVERSE_CHARACTER"),
            "kernel_hnf": scalar(text, "C_KERNEL_HNF"),
            "relative_packet_polynomial":
                scalar(text, "C_PACKET_RELATIVE_POLYNOMIAL"),
            "state": "ALIGNED_NOT_DUAL_PROVED",
        })
        transcripts.append(
            f"===== {index}/10 {record['case_id']} =====\n{text}"
        )
    TRANSCRIPT.write_text("\n".join(transcripts))
    payload = {
        "schema": "effective-stark-remaining-dual-alignments-v1",
        "claim_tag": "VERIFIED_ALIGNMENT_ONLY",
        "candidate_count": len(outputs),
        "aligned_count": sum(
            all(
                record[key]
                for key in (
                    "same_modulus",
                    "same_ray_classes",
                    "same_character_pair",
                    "identical_relative_packet_polynomial",
                    "identical_absolute_packet_polynomial",
                )
            )
            for record in outputs
        ),
        "promotion_boundary": (
            "Exact alignment is not DUAL_PROVED. Each case still needs "
            "independent Engine-B and Engine-C W3 certificates."
        ),
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (QUEUE, SCRIPT)
        },
        "records": outputs,
    }
    if payload["aligned_count"] != 10:
        raise RuntimeError("not all remaining candidates aligned")
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "candidate_count": payload["candidate_count"],
        "aligned_count": payload["aligned_count"],
        "state": "ALIGNMENT_ONLY_NO_DUAL_PROOF",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
