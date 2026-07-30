#!/usr/bin/env python3
"""Independently reconcile the frozen census universe and T/Q/H split."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def sha256(relative: str) -> str:
    return hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()


def mathematical_enumeration_payload(record: dict) -> dict:
    record = dict(record)
    record.pop("recorded_at_utc", None)
    return record


def rerun_enumeration() -> tuple[bool, str]:
    with tempfile.TemporaryDirectory(prefix="effective-stark-census-") as folder:
        output = Path(folder) / "rerun.json"
        subprocess.run(
            [
                "python3",
                str(ROOT / "scripts" / "enumerate_frozen_ideals.py"),
                "--d-min",
                "2",
                "--d-max",
                "200",
                "--norm-max",
                "100",
                "--output",
                str(output),
            ],
            cwd=ROOT,
            check=True,
        )
        rerun = json.loads(output.read_text(encoding="utf-8"))
        banked = load("artifacts/frozen-ideal-census-v1.json")
        identical = (
            mathematical_enumeration_payload(rerun)
            == mathematical_enumeration_payload(banked)
        )
        return identical, hashlib.sha256(output.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ARTIFACTS / "census-paper-layer0-reconciliation-v1.json",
    )
    parser.add_argument(
        "--skip-enumeration-rerun",
        action="store_true",
        help="Only for fast unit tests; publication audit must omit this flag.",
    )
    args = parser.parse_args()

    census = load("artifacts/frozen-ideal-census-v1.json")
    w1 = load("artifacts/w1-full-census-v1.json")
    v5 = load("artifacts/full-census-yield-declaration-v5.json")
    queue = load("artifacts/engine-a-queue-analysis-v1.json")
    euler = load("artifacts/engine-a-euler-degeneracy-v1.json")

    cases = census["cases"]
    rows = w1["records"]
    classifications = {
        row["case_id"]: row["verdict"]
        for row in v5["classification_records"]
    }
    if census["range"] != {
        "D_min": 2,
        "D_max": 200,
        "norm_max": 100,
        "archimedean_places_per_orbit": 1,
    }:
        raise RuntimeError("frozen range changed")
    if (
        census["field_count"] != 121
        or census["raw_ideal_count"] != 13939
        or census["deduplicated_case_count"] != 8200
        or not census["all_bnfcertify"]
    ):
        raise RuntimeError("enumeration summary changed")
    expected_ids = [f"RQ-{index:06d}" for index in range(1, 8201)]
    if [row["case_id"] for row in cases] != expected_ids:
        raise RuntimeError("RQ registry is not contiguous and stable")
    if [row["case_id"] for row in rows] != expected_ids:
        raise RuntimeError("W1 rows do not match the frozen registry")
    if set(classifications) != set(expected_ids):
        raise RuntimeError("v5 classifications do not cover the registry")
    for case, row in zip(cases, rows):
        for key in (
            "case_id",
            "D",
            "field_discriminant",
            "finite_norm",
            "finite_ideal_hnf",
        ):
            w1_key = "d" if key == "D" else key
            if case[key] != row[w1_key]:
                raise RuntimeError(f"{case['case_id']}: identity mismatch at {key}")

    empty_support = [row for row in rows if row["support_count"] == 0]
    quadratic_support = [
        row
        for row in rows
        if row["support_count"] > 0 and max(row["support_orders"]) <= 2
    ]
    higher_support = [
        row
        for row in rows
        if row["support_count"] > 0 and max(row["support_orders"]) > 2
    ]
    if [len(empty_support), len(quadratic_support), len(higher_support)] != [
        3936,
        1560,
        2704,
    ]:
        raise RuntimeError("structural trichotomy changed")
    if any(any(value != 0 for value in row["sign_log"]) for row in empty_support):
        raise RuntimeError("empty support with nontrivial sign class")
    if any(
        not row["sign_log"] or all(value == 0 for value in row["sign_log"])
        for row in quadratic_support + higher_support
    ):
        raise RuntimeError("nonempty support with trivial sign class")

    empty_v5 = Counter(classifications[row["case_id"]] for row in empty_support)
    quadratic_v5 = Counter(
        classifications[row["case_id"]] for row in quadratic_support
    )
    higher_v5 = Counter(
        classifications[row["case_id"]] for row in higher_support
    )
    displaced_empty = sorted(
        row["case_id"]
        for row in empty_support
        if classifications[row["case_id"]] != "PROVED_TRIVIAL"
    )
    if empty_v5 != Counter({"PROVED_TRIVIAL": 3899, "FRONTIER": 37}):
        raise RuntimeError("v5 empty-support cross-tab changed")
    if quadratic_v5 != Counter({"ENGINE_A_NONTRIVIAL_ELIGIBLE": 1560}):
        raise RuntimeError("quadratic-support cross-tab changed")
    if higher_v5 != Counter(
        {
            "FRONTIER": 1591,
            "ENGINE_C_ELIGIBLE": 881,
            "ENGINE_B_ELIGIBLE": 232,
        }
    ):
        raise RuntimeError("higher-support cross-tab changed")
    if any(
        row["obstruction"] != "EXPONENT_CAP"
        for row in rows
        if row["case_id"] in displaced_empty
    ):
        raise RuntimeError("unexpected cause of the 37-row v5 discrepancy")

    queue_character_count = sum(
        int(support_count) * row_count
        for support_count, row_count
        in queue["quadratic_support_count_histogram"].items()
    )
    if (
        queue["quadratic_packet_count"] != 1560
        or queue_character_count != 2232
        or euler["case_count"] != 1560
        or euler["supported_quadratic_character_count"] != 2232
        or euler["characters_with_zero_euler_product"] != 672
        or euler["cases_with_zero_euler_product"] != 603
        or euler["cases_with_all_supported_euler_products_zero"] != 346
    ):
        raise RuntimeError("Engine-A reconciliation changed")
    odd = v5["odd_index_landscape"]
    if (
        odd["odd_index_above_two_count"] != 446
        or odd["nonempty_support_count"] != 0
    ):
        raise RuntimeError("odd-index replay summary changed")

    rerun_identical = True
    rerun_sha = None
    if not args.skip_enumeration_rerun:
        rerun_identical, rerun_sha = rerun_enumeration()
        if not rerun_identical:
            raise RuntimeError("clean PARI enumeration differs from the banked backbone")

    source_paths = [
        "data/range-v1.json",
        "artifacts/frozen-ideal-census-v1.json",
        "artifacts/w1-full-census-v1.json",
        "artifacts/full-census-yield-declaration-v5.json",
        "artifacts/engine-a-queue-analysis-v1.json",
        "artifacts/engine-a-euler-degeneracy-v1.json",
        "scripts/enumerate_frozen_ideals.py",
        "scripts/enumerate_frozen_ideals.gp",
        "scripts/audit_census_paper_layer0.py",
    ]
    payload = {
        "schema": "effective-stark-census-paper-layer0-reconciliation-v1",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_EXACT_RECONCILIATION",
        "predicate_provenance": "GENUINE",
        "publication_universe": {
            "field_parameter": "squarefree radicand D",
            "D_min": 2,
            "D_max": 200,
            "finite_modulus_type": "all nonzero integral ideals of O_K",
            "finite_ideal_norm_max": 100,
            "one_place_representatives": "conjugate pairs identified",
            "field_count": 121,
            "raw_ideal_count": 13939,
            "representative_count": 8200,
            "nonmaximal_form_order_moduli_in_universe": False,
        },
        "clean_enumeration_rerun": {
            "performed": not args.skip_enumeration_rerun,
            "mathematical_payload_identical": rerun_identical,
            "ephemeral_output_sha256": rerun_sha,
        },
        "structural_trichotomy": {
            "T_empty_support": 3936,
            "Q_nonempty_quadratic_support": 1560,
            "H_nonempty_higher_order_support": 2704,
            "sum": 8200,
        },
        "higher_order_mechanism_cross_tab": {
            "ENGINE_B_ELIGIBLE": 232,
            "ENGINE_C_ELIGIBLE": 881,
            "FRONTIER": 1591,
            "sum": 2704,
        },
        "v5_reconciliation": {
            "banked_routing_trivial_count": 3899,
            "structural_empty_support_count": 3936,
            "empty_support_rows_previously_routed_FRONTIER": 37,
            "cause": (
                "v5 applied EXPONENT_CAP before the empty-support theorem "
                "to 37 W1 engine-NONE rows"
            ),
            "affected_case_ids": displaced_empty,
            "mathematical_consequence": (
                "the census-paper trichotomy uses 3936/1560/2704; "
                "v5 remains a preserved historical routing declaration"
            ),
        },
        "quadratic_stratum_reconciliation": {
            "rows": 1560,
            "supported_quadratic_character_occurrences": 2232,
            "distinct_quartic_fields": 912,
            "zero_Euler_character_occurrences": 672,
            "rows_affected_by_zero_Euler_factors": 603,
            "rows_with_all_supported_derivatives_zero": 346,
            "classification_rule": (
                "the 346 rows remain in Q because the trichotomy is by "
                "Fourier support, even though exact evaluation gives X_A=1"
            ),
        },
        "parity_replay": {
            "odd_index_above_two_rows": 446,
            "nonempty_support_rows": 0,
        },
        "source_sha256": {path: sha256(path) for path in source_paths},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print("CENSUS_LAYER0_RECONCILIATION=PASS")
    print("TRICHOTOMY=3936+1560+2704=8200")
    print("V5_EMPTY_SUPPORT_CORRECTION=37")
    print(f"OUTPUT={args.output}")


if __name__ == "__main__":
    main()
