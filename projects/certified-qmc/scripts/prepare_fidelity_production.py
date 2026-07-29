#!/usr/bin/env python3
"""Freeze the Cycles 016-017 fidelity production inputs and gates."""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.crt import choose_moduli
from src.scaled_integer import balanced_crt_bits, error_numerator_bound


SCHEDULE = ROOT / "data" / "primes-schedule-v1.json"
SPEC = ROOT / "data" / "cycles-016-017-fidelity-spec.json"
PREREG = ROOT / "data" / "cycles-016-017-preregistration.json"
INPUT_DIR = ROOT / ".run-inputs"
UNSW_BASE = "https://web.maths.unsw.edu.au/~fkuo/lattice"
DIMENSION = 3600
WORK_PRIME_LIMIT = 3738
PILOT_MEDIAN_NS_PER_UPDATE = "2.482743143245874"
MAXIMUM_NS_PER_UPDATE = "3.10342892905734250"
MINIMUM_MONITORED_UPDATES = 5_000_000_000

EXPECTED_HASHES = {
    "lattice-29102-1024.3600":
        "d42503eda84c7fede8d2513d674a9eca4075041dc4cf8c2e0995b46b035b5ce9",
    "lattice-29102-2048.3600":
        "4f39beafc1531dce6368f1f7e2020a3427a85a1d34d21a795914217d4c5e2ae8",
    "lattice-29102-4096.3600":
        "c16b51add83f91efa8a9323be3d12f5e90c3e4a4a21359d3a2b42d2afccc90ea",
    "lattice-29102-8192.3600":
        "89722aea5b7854345035c8afca9b62d284b55bc0eefdd50f54c8dc7ad2319d74",
    "lattice-29102-16384.3600":
        "7a182dc21b2e089cbf58ab79ed0cd0b92ed49348a8cd96ce036c76f7c91f29d2",
    "lattice-29102-32768.3600":
        "30d9cceb8639da07fabdd4ac493fb93628f6db41054595156a335302013e012e",
    "lattice-29102-65536.3600":
        "4a278eca915ae62d03dc578e4c91200b3d65b8dac29f7aa8b7197112cedac527",
    "lattice-29102-131072.3600":
        "aedcccd7ec9e658ceccfff2630f3ef31232d4e588b765a49de7976f804bd07a3",
    "lattice-29102-262144.3600":
        "b499955f65e4061c266c3b2ed048ce3a7e09e3554f018a7f051e2100a6056781",
    "lattice-29102-524288.3600":
        "ea396c2343e9f1850568edc559806564f64d7a793e3a644b4da793de2da788d6",
    "lattice-29102-1048576.3600":
        "04b844e3401e89356a1c339d2f96fe8c15d062c9c2316dc2bd81b3a65e1d39cf",
    "lattice-39102-1024-1048576.3600":
        "48c219ad626c2848a711d99a23363f348d9065e9ab53d8304f35c811b4e78dae",
}


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: object) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
    ).hexdigest()


def validate_vector(path: Path) -> None:
    rows = path.read_text().splitlines()
    if len(rows) != DIMENSION:
        raise ValueError(f"{path.name}: expected {DIMENSION} rows")
    for expected, line in enumerate(rows, 1):
        row, component = map(int, line.split())
        if row != expected or component < 1:
            raise ValueError(f"{path.name}: invalid row {expected}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen-at-utc", required=True)
    args = parser.parse_args()
    if not args.frozen_at_utc.endswith("Z"):
        raise ValueError("frozen timestamp must be UTC and end in Z")

    for filename, expected in EXPECTED_HASHES.items():
        path = INPUT_DIR / filename
        validate_vector(path)
        actual = digest(path)
        if actual != expected:
            raise RuntimeError(
                f"frozen input mismatch for {filename}: {actual}"
            )

    schedule = json.loads(SCHEDULE.read_text())
    primes = [
        int(row["p"])
        for row in schedule["primes"][:WORK_PRIME_LIMIT]
    ]
    weights = [
        Fraction(1, index * index)
        for index in range(1, DIMENSION + 1)
    ]
    cell_budgets = {}
    for exponent in range(10, 21):
        modulus = 2**exponent
        bound = error_numerator_bound(modulus, weights)
        count = len(choose_moduli(primes, bound))
        cell_budgets[modulus] = {
            "proved_numerator_bound_bits": bound.bit_length(),
            "proved_balanced_crt_bits": balanced_crt_bits(bound),
            "work_prime_count": count,
            "incremental_updates_per_table": (
                modulus * DIMENSION * count
            ),
        }

    page_snapshot = (
        ROOT
        / "third_party"
        / "terms"
        / "2026-07-29"
        / "unsw-lattice-index.html"
    )
    page_hash = digest(page_snapshot)
    extensible = "lattice-39102-1024-1048576.3600"
    tables = []
    for family in ("fixed-29102", "extensible-39102"):
        for exponent in range(10, 21):
            modulus = 2**exponent
            filename = (
                f"lattice-29102-{modulus}.3600"
                if family == "fixed-29102"
                else extensible
            )
            file_hash = EXPECTED_HASHES[filename]
            tables.append(
                {
                    "table_id": f"unsw-{family}-n{modulus}-j2",
                    "source_id": f"unsw-{family}",
                    "source_citation": f"{UNSW_BASE}/{filename}",
                    "source_path": str(
                        (INPUT_DIR / filename).relative_to(ROOT)
                    ),
                    "source_snapshot_sha256": page_hash,
                    "source_file_sha256": file_hash,
                    "N": modulus,
                    "dimension": DIMENSION,
                    "weight_power": 2,
                    "work_prime_count": cell_budgets[modulus][
                        "work_prime_count"
                    ],
                }
            )

    spec = {
        "schema": "certified-qmc-chunked-production-spec-v1",
        "run_id": "cycles-016-017-fidelity-v1",
        "frozen_at_utc": args.frozen_at_utc,
        "prefix_block_size": 512,
        "parallel_workers": 4,
        "prime_schedule": "data/primes-schedule-v1.json",
        "prime_schedule_manifest": (
            "certificates/cycle-014-prime-schedule-manifest.json"
        ),
        "preregistrations": [
            "data/cycles-016-017-preregistration.json",
            "data/workstream-b-production-freeze.json",
            "data/workstream-b-streaming-pilot-preregistration-v2.json",
        ],
        "throughput_monitor": {
            "claim_tag": "NUMERICAL",
            "pilot_median_aggregate_ns_per_update":
                PILOT_MEDIAN_NS_PER_UPDATE,
            "maximum_aggregate_ns_per_update": MAXIMUM_NS_PER_UPDATE,
            "drift_fraction": "0.25",
            "minimum_updates_before_enforcement":
                MINIMUM_MONITORED_UPDATES,
            "failure_exit_code": 76,
            "action": (
                "PAUSE_AND_INVESTIGATE; do not silently continue or "
                "change the threshold"
            ),
        },
        "tables": tables,
        "boundary": (
            "VERIFIED output is a keyed merit supply artifact. UNSW "
            "vectors remain external and are not redistributed."
        ),
    }
    SPEC.write_text(json.dumps(spec, indent=2, sort_keys=True) + "\n")
    spec_hash = digest(SPEC)

    audit_seed = 16017
    prereg = {
        "schema": (
            "certified-qmc-cycles-016-017-production-"
            "preregistration-v1"
        ),
        "frozen_at_utc": args.frozen_at_utc,
        "production_started": False,
        "production_spec": {
            "path": str(SPEC.relative_to(ROOT)),
            "sha256": spec_hash,
        },
        "pre_run_freeze": {
            "input_table_hashes": EXPECTED_HASHES,
            "phase_0_29102_n1024_hash_match": True,
            "unsw_index_snapshot_sha256": page_hash,
            "prime_schedule_sha256": digest(SCHEDULE),
            "grid": (
                "families 29102 + 39102; N=2^10..2^20; "
                "every prefix d=1..3600; gamma_j=j^-2"
            ),
            "evaluation_order": (
                "prime-major; within each family/N column update the "
                "running product once per dimension and emit every "
                "prefix; no per-cell restart"
            ),
            "external_vectors_redistributed": False,
            "full_exact_branch_authorized": True,
            "exact_arb_fallback": "DESIGNED_BUT_UNUSED",
        },
        "kernel_freeze": {
            "representation": "plain __int128 remainder",
            "pilot_source_sha256":
                "f21c5cc9ab825ea402258fd5832e7ee0b33ebf5f60c2c3fab9cec7484339dd42",
            "compiler_flags_frozen": (
                "-O3 -std=c11 -Wall -Wextra -Wpedantic "
                "-D_POSIX_C_SOURCE=200809L"
            ),
            "changes_forbidden_until_after_release": [
                "Montgomery reduction",
                "lazy reduction",
                "compiler-flag changes",
                "vectorization passes",
            ],
        },
        "cell_budgets": {
            str(modulus): value
            for modulus, value in cell_budgets.items()
        },
        "total_fidelity_incremental_updates": sum(
            int(table["N"])
            * int(table["dimension"])
            * int(table["work_prime_count"])
            for table in tables
        ),
        "run_gate": {
            "maximum_node_days": 7,
            "pilot_projection_node_days": "1.5776183140488904",
            "maximum_aggregate_ns_per_update":
                MAXIMUM_NS_PER_UPDATE,
            "minimum_updates_before_drift_enforcement":
                MINIMUM_MONITORED_UPDATES,
            "throughput_drift_action": "PAUSE_AND_INVESTIGATE",
            "overflow_prime_indices": [3738, 3739],
            "overflow_failure_action": "HALT_AND_ESCALATE",
            "manifest_or_hash_failure_action": "HALT_AND_ESCALATE",
        },
        "post_run_audit": {
            "selection": (
                "uniform pseudorandom sampling over 22 tables x 3600 "
                "prefixes using Python random.Random"
            ),
            "seed": audit_seed,
            "sample_count": 100,
            "selected_entry_required_status": "VERIFIED",
            "independent_oracle_entries": [
                {
                    "table_id": "unsw-fixed-29102-n1024-j2",
                    "N": 1024,
                    "d": 16,
                    "mode": "independent Python scaled-integer oracle",
                },
                {
                    "table_id": "unsw-extensible-39102-n2048-j2",
                    "N": 2048,
                    "d": 8,
                    "mode": "independent Python scaled-integer oracle",
                },
                {
                    "table_id": "unsw-fixed-29102-n1048576-j2",
                    "N": 1048576,
                    "d": 16,
                    "mode": (
                        "from-scratch direct evaluation, budgeted "
                        "separately"
                    ),
                },
            ],
        },
        "halt_conditions": [
            "oracle mismatch",
            "overflow-prime failure",
            "manifest/hash break",
            "throughput drift above frozen ceiling",
            "any deviation from a frozen threshold or kernel",
        ],
        "boundary": (
            "Thresholds, input hashes, audit seed, and oracle entries "
            "are fixed before the first production merit is evaluated."
        ),
    }
    prereg["preregistration_sha256"] = canonical_sha(prereg)
    PREREG.write_text(json.dumps(prereg, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "spec": str(SPEC),
                "spec_sha256": spec_hash,
                "preregistration": str(PREREG),
                "preregistration_sha256": digest(PREREG),
                "table_count": len(tables),
                "total_fidelity_incremental_updates":
                    prereg["total_fidelity_incremental_updates"],
                "work_prime_counts": {
                    str(modulus): value["work_prime_count"]
                    for modulus, value in cell_budgets.items()
                },
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
