#!/usr/bin/env python3
"""Certify the three class numbers used in the Q(sqrt(35)) discussion.

This is deliberately a tiny, independent PARI/GP replay.  It does not
share the Engine-C field-construction helpers: the paper's statement only
needs the class numbers of three explicitly presented quadratic fields.
"""

from __future__ import annotations

import hashlib
import json
import platform
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "q35-base-class-numbers-v1.json"
TRANSCRIPT = ROOT / "artifacts" / "q35-base-class-numbers-v1.transcript"

EXPECTED = {
    "real_base_Q_sqrt_35": {"polynomial": "x^2-35", "class_number": 2},
    "imaginary_base_Q_sqrt_minus_10": {
        "polynomial": "x^2+10",
        "class_number": 2,
    },
    "imaginary_base_Q_sqrt_minus_14": {
        "polynomial": "x^2+14",
        "class_number": 4,
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    gp = shutil.which("gp")
    if gp is None:
        raise SystemExit("PARI/GP executable 'gp' not found")

    keys = list(EXPECTED)
    commands = [
        f'print("{key}|",bnfinit({EXPECTED[key]["polynomial"]}).no)'
        for key in keys
    ]
    program = "\n".join(commands + ["quit"]) + "\n"
    proc = subprocess.run(
        [gp, "-q"],
        input=program,
        text=True,
        capture_output=True,
        check=False,
    )
    transcript_text = (
        f"$ {gp} -q\n"
        f"{program}"
        f"--- stdout ---\n{proc.stdout}"
        f"--- stderr ---\n{proc.stderr}"
        f"--- returncode ---\n{proc.returncode}\n"
    )
    TRANSCRIPT.write_text(transcript_text, encoding="utf-8")
    if proc.returncode != 0:
        raise SystemExit(f"PARI/GP failed; see {TRANSCRIPT}")

    observed: dict[str, int] = {}
    for line in proc.stdout.splitlines():
        if "|" not in line:
            continue
        key, value = line.strip().split("|", 1)
        observed[key] = int(value)

    expected_values = {key: row["class_number"] for key, row in EXPECTED.items()}
    if observed != expected_values:
        raise AssertionError(
            f"class-number mismatch: expected {expected_values}, observed {observed}"
        )

    gp_version = subprocess.run(
        [gp, "--version-short"],
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()
    record = {
        "schema": "effective-stark-q35-base-class-numbers-v1",
        "claim_tag": "VERIFIED_EXACT",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "case": {
            "real_base": "Q(sqrt(35))",
            "finite_modulus_norm": 32,
            "imaginary_bases": ["Q(sqrt(-10))", "Q(sqrt(-14))"],
        },
        "fields": {
            key: {
                **EXPECTED[key],
                "observed_class_number": observed[key],
                "method": "PARI bnfinit(polynomial).no",
            }
            for key in keys
        },
        "conclusion": (
            "The real base has class number 2, while the two imaginary "
            "bases have distinct class numbers 2 and 4."
        ),
        "software": {
            "pari_gp": gp_version,
            "python": platform.python_version(),
        },
        "transcript": {
            "path": str(TRANSCRIPT.relative_to(ROOT)),
            "sha256": sha256(TRANSCRIPT),
        },
    }
    OUT.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Q35_CLASS_NUMBER_CERTIFICATE=PASS output={OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
