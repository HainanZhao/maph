#!/usr/bin/env python3
"""Verify the compact engine oracle, optionally against table datasets."""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

from src.certificate import canonical_sha256
from src.chunked_table import file_sha256
from src.shadow_decision import candidate_score_fraction


DEFAULT_ORACLE = ROOT / "certificates" / "engine-oracle-set-v1.json"


def load_self_hashed(path: Path, field: str) -> dict:
    value = json.loads(path.read_text())
    supplied = value.pop(field)
    if canonical_sha256(value) != supplied:
        raise ValueError(f"{path.name} self-hash mismatch")
    value[field] = supplied
    return value


def verify_entry_hashes(oracle: dict) -> None:
    for entry in oracle["table_merits"]:
        supplied = entry.pop("entry_sha256")
        expected = canonical_sha256(entry)
        entry["entry_sha256"] = supplied
        if supplied != expected:
            raise ValueError("oracle table-entry self-hash mismatch")
    for case in oracle["adversarial_decision_cases"]:
        supplied = case.pop("case_sha256")
        expected = canonical_sha256(case)
        case["case_sha256"] = supplied
        if supplied != expected:
            raise ValueError("oracle adversarial-case self-hash mismatch")


def verify_adversarial(case: dict) -> None:
    weights = [Fraction(value) for value in case["weights"]]
    left = candidate_score_fraction(
        int(case["N"]),
        case["prefix"],
        weights,
        int(case["candidates"][0]),
    )
    right = candidate_score_fraction(
        int(case["N"]),
        case["prefix"],
        weights,
        int(case["candidates"][1]),
    )
    comparison = (left > right) - (left < right)
    expected = {
        "left_score_numerator": str(left.numerator),
        "left_score_denominator": str(left.denominator),
        "right_score_numerator": str(right.numerator),
        "right_score_denominator": str(right.denominator),
        "comparison": comparison,
        "exact_equality": comparison == 0,
    }
    for key, value in expected.items():
        if case[key] != value:
            raise ArithmeticError(
                f"adversarial oracle mismatch: {case['case_id']} {key}"
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--oracle", type=Path, default=DEFAULT_ORACLE)
    parser.add_argument("--fidelity", type=Path)
    parser.add_argument("--usability", type=Path)
    args = parser.parse_args()
    if (args.fidelity is None) != (args.usability is None):
        raise ValueError(
            "--fidelity and --usability must be supplied together"
        )
    oracle_path = args.oracle.resolve()
    oracle = load_self_hashed(oracle_path, "oracle_sha256")
    if (
        oracle["claim_tag"] != "VERIFIED"
        or oracle["counts"]["total"] != 298
        or len(oracle["table_merits"]) != 290
        or len(oracle["adversarial_decision_cases"]) != 8
    ):
        raise ValueError("oracle count/tag contract failed")
    prereg = ROOT / oracle["selection_preregistration"]["path"]
    if (
        file_sha256(prereg)
        != oracle["selection_preregistration"]["file_sha256"]
    ):
        raise ValueError("oracle selection preregistration mismatch")
    verify_entry_hashes(oracle)
    for case in oracle["adversarial_decision_cases"]:
        verify_adversarial(case)

    full_replay = args.fidelity is not None
    if full_replay:
        with tempfile.TemporaryDirectory(
            prefix="certified-qmc-oracle-replay-"
        ) as directory:
            rebuilt = Path(directory) / "oracle.json"
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "build_engine_oracle_set.py"),
                    "--fidelity",
                    str(args.fidelity.resolve()),
                    "--usability",
                    str(args.usability.resolve()),
                    "--output",
                    str(rebuilt),
                    "--recorded-at-utc",
                    oracle["recorded_at_utc"],
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            if rebuilt.read_bytes() != oracle_path.read_bytes():
                raise ArithmeticError(
                    "full engine-oracle replay is not byte-identical"
                )
    result = {
        "status": "VERIFIED",
        "claim_tag": (
            "VERIFIED_FULL_ORACLE_REPLAY"
            if full_replay
            else "VERIFIED_ORACLE_STRUCTURE_AND_ADVERSARIAL_CASES"
        ),
        "oracle_sha256": oracle["oracle_sha256"],
        "file_sha256": sha256(oracle_path.read_bytes()).hexdigest(),
        "table_entry_hashes_verified": 290,
        "adversarial_cases_exactly_recomputed": 8,
        "table_datasets_replayed": full_replay,
        "boundary": (
            "Without both datasets, table-merit values are authenticated "
            "but not arithmetically reconstructed in this invocation."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
