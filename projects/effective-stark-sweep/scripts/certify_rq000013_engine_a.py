#!/usr/bin/env python3
"""Write or replay-check the exact Engine-A certificate for RQ-000013."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PY_SCRIPT = Path(__file__).resolve()
GP_SCRIPT = ROOT / "scripts" / "certify_rq000013_engine_a.gp"
SELECTION = ROOT / "data" / "census-paper-imprimitive-worked-case-selection-v1.json"
THEOREM = ROOT / "data" / "engine-a-uniform-theorem-v1.json"
EULER_AUDIT = ROOT / "artifacts" / "engine-a-euler-degeneracy-v1.json"
FIELD_CENSUS = ROOT / "artifacts" / "engine-a-field-census-v1.json"
OUTPUT = ROOT / "artifacts" / "rq000013-engine-a-imprimitive-certificate-v1.json"
TRANSCRIPT = ROOT / "artifacts" / "rq000013-engine-a-imprimitive-certificate-v1.transcript"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_gp() -> str:
    completed = subprocess.run(
        ["gp", "-fq", GP_SCRIPT.name],
        cwd=GP_SCRIPT.parent,
        check=True,
        capture_output=True,
        text=True,
    )
    if completed.stderr:
        raise RuntimeError(f"unexpected GP stderr:\n{completed.stderr}")
    return completed.stdout


def parse_transcript(text: str) -> dict[str, str]:
    records: dict[str, str] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if "=" not in line:
            raise RuntimeError(f"unparseable transcript line: {line}")
        key, value = line.split("=", 1)
        if key in records:
            raise RuntimeError(f"duplicate transcript key: {key}")
        records[key] = value
    if records.get("RQ000013_ENGINE_A_CERTIFIED") != "1":
        raise RuntimeError("GP certificate did not reach its completion marker")
    return records


def payload(text: str) -> dict:
    records = parse_transcript(text)
    return {
        "schema": "effective-stark-rq000013-engine-a-imprimitive-certificate-v1",
        "claim_tag": "PROVED_BY_UNIFORM_ENGINE_A_THEOREM_AND_EXACT_FINITE_CERTIFICATE",
        "case_id": "RQ-000013",
        "claim_boundary": {
            "proved": (
                "the Artin-labelled packet identity "
                "X_[0]=u^2 and X_[1]=u^(-2)"
            ),
            "certified_inputs": (
                "primitive conductor, Euler factor, class numbers, roots of "
                "unity, exact norm map, primitive norm kernel, relative "
                "index, orientation by rational root isolation, and Artin labels"
            ),
            "quarantined_cross_check": (
                "PARI bnrL1 point-value residual; not used in the proof"
            ),
        },
        "theorem_formula": (
            "L'_m(0,chi)=E_chi*(h_L/h_K)*(w_K/w_L)"
            "*(2/I_chi)*log|u_chi|"
        ),
        "exact_result": {
            "E_chi": 2,
            "h_K": 1,
            "h_L": 1,
            "w_K": 2,
            "w_L": 2,
            "I_chi": 2,
            "Lprime_log_coefficient": 2,
            "ray_group_order": 2,
            "fourier_coefficient": "2/|G|=1",
            "packet_power_identity": "X_[0]=u^2; X_[1]=u^(-2)",
            "oriented_unit_minpoly": "x^4 - 2*x^3 + x^2 - 2*x + 1",
            "oriented_unit_isolating_interval": ["9/5", "19/10"],
            "packet_unit_minpoly": "x^4 - 2*x^3 - 5*x^2 - 2*x + 1",
            "packet_unit_isolating_interval": ["7/2", "18/5"],
        },
        "replay": {
            "command": "python3 scripts/certify_rq000013_engine_a.py --check",
            "pari_version": records["PARI_VERSION"],
            "transcript": str(TRANSCRIPT.relative_to(ROOT)),
            "transcript_sha256": hashlib.sha256(text.encode()).hexdigest(),
            "completion_marker": records["RQ000013_ENGINE_A_CERTIFIED"],
        },
        "source_hashes": {
            str(PY_SCRIPT.relative_to(ROOT)): sha256(PY_SCRIPT),
            str(GP_SCRIPT.relative_to(ROOT)): sha256(GP_SCRIPT),
            str(SELECTION.relative_to(ROOT)): sha256(SELECTION),
            str(THEOREM.relative_to(ROOT)): sha256(THEOREM),
            str(EULER_AUDIT.relative_to(ROOT)): sha256(EULER_AUDIT),
            str(FIELD_CENSUS.relative_to(ROOT)): sha256(FIELD_CENSUS),
        },
        "exact_transcript_records": {
            key: value
            for key, value in records.items()
            if not key.startswith("QUARANTINED_")
        },
        "quarantined_numerical_cross_check": {
            "tag": "OBSERVED",
            "bnrL1_value": records["QUARANTINED_BNRL1_VALUE"],
            "formula_value": records["QUARANTINED_FORMULA_VALUE"],
            "residual": records["QUARANTINED_BNRL1_FORMULA_RESIDUAL"],
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()

    text = run_gp()
    current = payload(text)
    if args.write:
        TRANSCRIPT.write_text(text)
        OUTPUT.write_text(json.dumps(current, indent=2, sort_keys=True) + "\n")
        print(f"WROTE={OUTPUT.relative_to(ROOT)}")
        print(f"TRANSCRIPT_SHA256={current['replay']['transcript_sha256']}")
        return

    if not OUTPUT.exists() or not TRANSCRIPT.exists():
        raise RuntimeError("certificate artifacts are missing; run with --write")
    frozen = json.loads(OUTPUT.read_text())
    if current != frozen:
        raise RuntimeError("recomputed certificate differs from frozen JSON")
    if text != TRANSCRIPT.read_text():
        raise RuntimeError("recomputed transcript differs from frozen transcript")
    print("RQ000013_ENGINE_A_CERTIFICATE_REPLAY=PASS")


if __name__ == "__main__":
    main()
