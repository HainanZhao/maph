#!/usr/bin/env python3
"""Audit and optionally seal the quadratic deleted-prime cover theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FEATURES = ROOT / "discovery/q-euler-local-features-v1.json"
ANALYSIS = ROOT / "discovery/q-euler-pattern-analysis-v2.json"
SEARCH = ROOT / "discovery/q-four-support-counterexample-search-v2.json"
LABELS = ROOT / "artifacts/engine-a-euler-degeneracy-v1.json"
Q_AUDIT = ROOT / "artifacts/census-q-packet-corpus-audit-v1.json"
Q_MANIFEST = ROOT / "artifacts/census-q-packets-v1/manifest.json"
Q_ROWS = ROOT / "artifacts/census-q-packets-v1/rows"
PREREG = ROOT / "docs/cycle-128-q-euler-degeneracy-pattern-preregistration.md"
LOCAL_GP = ROOT / "discovery/export_q_euler_local_features.gp"
OUT = ROOT / "artifacts/q-euler-deleted-prime-cover-theorem-v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def verify_recorded_hashes(payload: dict) -> None:
    for relative, expected in payload.get("source_hashes", {}).items():
        path = ROOT / relative
        if sha256(path) != expected:
            raise RuntimeError(f"source hash changed: {relative}")
    transcript = payload.get("transcript")
    if transcript and sha256(ROOT / transcript["path"]) != transcript["sha256"]:
        raise RuntimeError(f"transcript hash changed: {transcript['path']}")


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


def replay_counterexample(search: dict) -> dict:
    row = search["counterexample"]
    hnf = row["finite_ideal_hnf"]
    prelude = (
        f'CASE_ID="{row["case_id"]}";\n'
        f'D_VALUE={row["base_radicand"]};\n'
        f"H11={hnf[0][0]};H12={hnf[0][1]};"
        f"H21={hnf[1][0]};H22={hnf[1][1]};\n"
    )
    completed = subprocess.run(
        ["gp", "-q"],
        input=prelude + LOCAL_GP.read_text(),
        text=True,
        capture_output=True,
        cwd=ROOT,
        timeout=60,
        check=False,
    )
    if (
        completed.returncode
        or "Q_EULER_LOCAL_FEATURE_EXPORT_VERIFIED=1" not in completed.stdout
    ):
        raise RuntimeError(completed.stdout + completed.stderr)
    if int(scalar(completed.stdout, "SUPPORTED_CHARACTER_COUNT")) != 4:
        raise RuntimeError("expanded-range counterexample support changed")
    if int(scalar(completed.stdout, "ZERO_EULER_CHARACTER_COUNT")) != 4:
        raise RuntimeError("expanded-range counterexample no longer all-zero")
    characters = []
    for index in range(1, 5):
        prefix = f"CHARACTER_{index}"
        removed_count = int(scalar(completed.stdout, f"{prefix}_REMOVED_COUNT"))
        local_values = [
            int(
                scalar(
                    completed.stdout,
                    f"{prefix}_REMOVED_{removed}_PRIMITIVE_VALUE",
                )
            )
            for removed in range(1, removed_count + 1)
        ]
        if 1 not in local_values:
            raise RuntimeError(f"counterexample character {index} is not covered")
        characters.append(
            {
                "ray_character": scalar(completed.stdout, f"{prefix}_COORDS"),
                "deleted_prime_values": local_values,
            }
        )
    return {
        "case_id": row["case_id"],
        "base_radicand": row["base_radicand"],
        "finite_norm": row["finite_norm"],
        "finite_ideal_hnf": hnf,
        "ray_cyc": scalar(completed.stdout, "RAY_CYC"),
        "sign_log": scalar(completed.stdout, "SIGN_LOG"),
        "characters": characters,
        "conclusion": "four supported characters and four zero Euler products",
        "claim_tag": "PROVED",
    }


def compute_certificate() -> dict:
    features = load(FEATURES)
    analysis = load(ANALYSIS)
    search = load(SEARCH)
    labels = load(LABELS)
    q_audit = load(Q_AUDIT)
    q_manifest = load(Q_MANIFEST)
    for payload in (features, analysis, search):
        verify_recorded_hashes(payload)

    rows = features["records"]
    if len(rows) != 1560:
        raise RuntimeError("quadratic row population changed")
    label_by_id = {row["case_id"]: row for row in labels["records"]}
    packet_rows = {path.stem.upper(): load(path) for path in Q_ROWS.glob("rq-*.json")}
    if len(packet_rows) != 1560:
        raise RuntimeError("packet row-file population changed")

    character_count = 0
    zero_character_count = 0
    deleted_occurrences = 0
    split_deleted_occurrences = 0
    all_zero_ids = []
    support_histogram: Counter[int] = Counter()
    all_zero_support_histogram: Counter[int] = Counter()
    character_errors = []
    packet_errors = []

    for row in rows:
        support_histogram[row["support_count"]] += 1
        local_all_zero = True
        row_zero_count = 0
        for index, character in enumerate(row["characters"], start=1):
            character_count += 1
            local_zero = any(
                prime["primitive_character_value"] == 1
                for prime in character["deleted_primes"]
            )
            deleted_occurrences += len(character["deleted_primes"])
            split_deleted_occurrences += sum(
                prime["primitive_character_value"] == 1
                for prime in character["deleted_primes"]
            )
            if local_zero != character["zero_euler"]:
                character_errors.append(f"{row['case_id']}:{index}")
            row_zero_count += local_zero
            zero_character_count += local_zero
            local_all_zero = local_all_zero and local_zero

        frozen = label_by_id[row["case_id"]]
        if (
            row_zero_count != frozen["zero_euler_characters"]
            or row["support_count"] != frozen["supported_quadratic_characters"]
            or local_all_zero != row["all_supported_euler_factors_zero"]
        ):
            packet_errors.append(row["case_id"] + ":label")
        packet = packet_rows[row["case_id"]]
        polynomial_is_x_minus_1 = packet["packet_factor_over_K"] == "x - 1"
        if polynomial_is_x_minus_1 != local_all_zero:
            packet_errors.append(row["case_id"] + ":polynomial")
        if local_all_zero:
            all_zero_ids.append(row["case_id"])
            all_zero_support_histogram[row["support_count"]] += 1

    if character_errors or packet_errors:
        raise RuntimeError(
            f"cover audit errors: characters={character_errors[:3]}, "
            f"packets={packet_errors[:3]}"
        )
    if (character_count, zero_character_count, len(all_zero_ids)) != (2232, 672, 346):
        raise RuntimeError("headline degeneracy counts changed")
    matrix = analysis["candidate_confusion_matrices"][
        "exact_universal_local_criterion"
    ]
    if matrix["fp"]["count"] or matrix["fn"]["count"]:
        raise RuntimeError("analysis exact criterion has errors")
    if q_audit["chain"]["final_sha256"] != q_manifest["chain"]["final_sha256"]:
        raise RuntimeError("quadratic corpus hash chain disagrees")

    counterexample = replay_counterexample(search)
    return {
        "schema": "effective-stark-q-euler-deleted-prime-cover-theorem-v1",
        "status": "PASS_PROVED_THEOREM_AND_FINITE_COROLLARY",
        "theorem": {
            "name": "quadratic deleted-prime cover criterion",
            "statement": (
                "In the quadratic-support regime, the entire positive packet is "
                "value one if and only if every supported character has a prime "
                "deleted from the selected modulus at which its primitive "
                "quadratic character has value +1."
            ),
            "equivalent_conditions": [
                "X_A=1 for every ray class A",
                "every supported imprimitive derivative L'_m(0,chi) is zero",
                "E_chi=0 for every supported chi",
                "the deleted split-prime sets cover every supported chi",
            ],
            "proof_route": (
                "quadratic imprimitive Euler product, positivity/nonvanishing of "
                "the remaining class-number/regulator factor, and exact Fourier "
                "inversion on the ray class group"
            ),
            "claim_tag": "PROVED",
            "range_dependence": "none beyond the quadratic-support hypotheses",
        },
        "finite_census_corollary": {
            "rows": len(rows),
            "supported_character_occurrences": character_count,
            "zero_euler_character_occurrences": zero_character_count,
            "deleted_prime_occurrences": deleted_occurrences,
            "split_deleted_prime_occurrences": split_deleted_occurrences,
            "all_zero_rows": len(all_zero_ids),
            "support_histogram": {
                str(key): value for key, value in sorted(support_histogram.items())
            },
            "all_zero_support_histogram": {
                str(key): value
                for key, value in sorted(all_zero_support_histogram.items())
            },
            "least_all_zero_case_id": min(all_zero_ids),
            "character_level_false_positives": 0,
            "character_level_false_negatives": 0,
            "row_level_false_positives": 0,
            "row_level_false_negatives": 0,
            "packet_polynomial_equivalence_errors": 0,
            "claim_tag": "PROVED",
        },
        "falsification_result": {
            "withdrawn_candidate": (
                "four supported quadratic characters prevent total Euler "
                "degeneracy"
            ),
            "status": "REFUTED",
            "counterexample": counterexample,
        },
        "source_hashes": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (
                FEATURES,
                ANALYSIS,
                SEARCH,
                LABELS,
                Q_AUDIT,
                Q_MANIFEST,
                PREREG,
                LOCAL_GP,
                Path(__file__),
            )
        },
        "corpus_chain_sha256": q_audit["chain"]["final_sha256"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-artifact", action="store_true")
    args = parser.parse_args()
    computed = compute_certificate()
    if args.write_artifact:
        OUT.write_text(json.dumps(computed, indent=2, sort_keys=True) + "\n")
    else:
        if not OUT.exists():
            raise RuntimeError("sealed theorem artifact is missing")
        sealed = load(OUT)
        if sealed != computed:
            raise RuntimeError("sealed theorem artifact differs from replay")
    print("Q_EULER_DELETED_PRIME_COVER_THEOREM=PASS")
    print("Q_EULER_DELETED_PRIME_COVER_ROWS=346")
    print("Q_FOUR_SUPPORT_NONDEGENERACY=REFUTED")


if __name__ == "__main__":
    main()
