#!/usr/bin/env python3
"""Audit the exhaustive hash-chained Q-stratum packet corpus."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "artifacts" / "census-q-packets-v1"
MANIFEST = CORPUS / "manifest.json"
HEIGHTS = ROOT / "artifacts" / "census-packet-height-calibration-v1.json"
EULER = ROOT / "artifacts" / "engine-a-euler-degeneracy-v1.json"
ANCHOR = ROOT / "artifacts" / "rq000245-packet-synthesis-v1.json"
PREREGISTRATION = (
    ROOT / "data" / "census-paper-preregistration-amendment-v5.json"
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text())
    heights = json.loads(HEIGHTS.read_text())
    euler = json.loads(EULER.read_text())
    anchor = json.loads(ANCHOR.read_text())
    preregistration = json.loads(PREREGISTRATION.read_text())
    if manifest["status"] != "PASS_EXHAUSTIVE_Q_PACKET_SYNTHESIS":
        raise RuntimeError("corpus manifest is not PASS")
    if manifest["population"] != {
        "attempted_rows": 1560,
        "failed_case_ids": [],
        "failed_rows": 0,
        "passed_rows": 1560,
    }:
        raise RuntimeError("corpus population changed")
    if sha256(HEIGHTS) != preregistration["calibration"]["sha256"]:
        raise RuntimeError("height calibration hash changed")

    height_by_id = {row["case_id"]: row for row in heights["records"]}
    euler_by_id = {row["case_id"]: row for row in euler["records"]}
    paths = sorted((CORPUS / "rows").glob("rq-*.json"))
    if len(paths) != 1560:
        raise RuntimeError(f"expected 1560 row files, got {len(paths)}")

    previous_hash = "0" * 64
    rows = []
    for path in paths:
        raw = path.read_bytes()
        row = json.loads(raw)
        expected_filename = f"{row['case_id'].lower()}.json"
        if path.name != expected_filename:
            raise RuntimeError(f"filename mismatch: {path}")
        if row["chain_previous_sha256"] != previous_hash:
            raise RuntimeError(f"hash-chain mismatch at {row['case_id']}")
        if (
            row["status"] != "PASS_EXACT_PACKET_POLYNOMIAL"
            or row["claim_tag"] != "PROVED"
        ):
            raise RuntimeError(f"non-PASS row: {row['case_id']}")
        if row["independence_wall"] != {
            "analytic_packet_target_opened": False,
            "height_calibration_used_for_factor_selection": False,
        }:
            raise RuntimeError(
                f"independence wall changed: {row['case_id']}"
            )
        gates = row["exact_gates"]
        required_true = (
            "base_bnfcertify",
            "packet_factor_reciprocal",
            "packet_factor_squarefree",
            "packet_factor_irreducible_over_K",
            "packet_factor_positive_root_sign_pattern",
        )
        if not all(gates[key] is True for key in required_true):
            raise RuntimeError(f"exact gate failed: {row['case_id']}")
        if gates["coefficient_coordinate_decimal_digits"] > 256:
            raise RuntimeError(f"digit cap failed: {row['case_id']}")
        calibrated = height_by_id[row["case_id"]]
        if (
            row["effective_artin_image_size"]
            != calibrated["effective_artin_image_size"]
            or row["packet_factor_degree_over_K"]
            != calibrated["effective_artin_image_size"]
        ):
            raise RuntimeError(
                f"Artin orbit mismatch: {row['case_id']}"
            )
        previous_hash = sha256_bytes(raw)
        rows.append(row)

    if previous_hash != manifest["chain"]["final_sha256"]:
        raise RuntimeError("final hash-chain root changed")
    if [row["case_id"] for row in rows] != sorted(height_by_id):
        raise RuntimeError("stable Q ordering changed")

    degree_counts = collections.Counter(
        row["packet_factor_degree_over_K"] for row in rows
    )
    denominator_counts = collections.Counter(
        row["common_denominator"] for row in rows
    )
    all_zero_rows = [
        row for row in rows if row["packet_factor_over_K"] == "x - 1"
    ]
    if dict(sorted(degree_counts.items())) != {
        1: 346,
        2: 930,
        4: 242,
        8: 42,
    }:
        raise RuntimeError(f"packet degree distribution changed: {degree_counts}")
    if dict(sorted(denominator_counts.items())) != {1: 1491, 2: 69}:
        raise RuntimeError(
            f"denominator distribution changed: {denominator_counts}"
        )
    if len(all_zero_rows) != 346:
        raise RuntimeError("all-zero X-1 count changed")
    for row in all_zero_rows:
        source = euler_by_id[row["case_id"]]
        if (
            source["zero_euler_characters"]
            != source["supported_quadratic_characters"]
        ):
            raise RuntimeError(
                f"X-1 row lacks all-zero evidence: {row['case_id']}"
            )

    rq000245 = next(row for row in rows if row["case_id"] == "RQ-000245")
    if (
        rq000245["packet_factor_over_K"]
        != anchor["exact_data"]["packet_factor_over_K"]
        or rq000245["absolute_packet_resultant"]
        != anchor["exact_data"]["packet_absolute_polynomial"]
    ):
        raise RuntimeError("RQ-000245 corpus row differs from anchor")

    maximum_digits = max(
        row["exact_gates"]["coefficient_coordinate_decimal_digits"]
        for row in rows
    )
    maximum_digit_cases = [
        row["case_id"]
        for row in rows
        if row["exact_gates"]["coefficient_coordinate_decimal_digits"]
        == maximum_digits
    ]
    result = {
        "schema": "effective-stark-census-q-packet-audit-v1",
        "status": "PASS_EXHAUSTIVE_Q_PACKET_CORPUS_AUDIT",
        "claim_tags": {
            "finite_q_corpus_packet_polynomials": "PROVED",
            "height_predictor_distribution": "OBSERVED",
        },
        "population": {
            "rows": len(rows),
            "supported_quadratic_character_occurrences": 2232,
            "effective_character_occurrences": sum(
                row["effective_character_count"]
                for row in heights["records"]
            ),
            "all_zero_X_minus_1_rows": len(all_zero_rows),
        },
        "exact_distributions": {
            "packet_degree_over_K": {
                str(key): value for key, value in sorted(degree_counts.items())
            },
            "common_denominator": {
                str(key): value
                for key, value in sorted(denominator_counts.items())
            },
            "maximum_coefficient_coordinate_decimal_digits": maximum_digits,
            "maximum_digit_case_ids": maximum_digit_cases,
            "frozen_digit_cap": 256,
        },
        "chain": {
            "row_count": len(rows),
            "final_sha256": previous_hash,
            "verified": True,
        },
        "anchor_reconciliation": {
            "case_id": "RQ-000245",
            "packet_factor_equal": True,
            "absolute_polynomial_equal": True,
        },
        "runtime": manifest["runtime"],
        "source_hashes": {
            "manifest_sha256": sha256(MANIFEST),
            "height_calibration_sha256": sha256(HEIGHTS),
            "euler_audit_sha256": sha256(EULER),
            "rq000245_anchor_sha256": sha256(ANCHOR),
            "preregistration_sha256": sha256(PREREGISTRATION),
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
