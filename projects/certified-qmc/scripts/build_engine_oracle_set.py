#!/usr/bin/env python3
"""Extract the preregistered compact engine oracle from sealed datasets."""

from __future__ import annotations

import argparse
from fractions import Fraction
from hashlib import sha256
import json
from math import prod
from pathlib import Path
import struct
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)

from src.certificate import canonical_sha256
from src.chunked_table import (
    canonical_bytes,
    file_sha256,
    iter_chain,
)
from src.crt import balanced_reconstruct, choose_moduli
from src.scaled_integer import error_numerator_bound, factor_denominator
from src.shadow_decision import candidate_score_fraction


PREREG = ROOT / "data" / "engine-oracle-set-v1.json"
FIDELITY_AUDIT = (
    ROOT / "certificates" / "cycles-016-017-production-audit.json"
)
USABILITY_AUDIT = (
    ROOT / "certificates" / "cycle-018-usability-audit.json"
)
SCHEDULE = ROOT / "data" / "primes-schedule-v1.json"


def canonical_sha(value: object) -> str:
    return sha256(canonical_bytes(value)).hexdigest()


def load_self_hashed(path: Path, field: str) -> dict:
    value = json.loads(path.read_text())
    supplied = value.pop(field)
    if canonical_sha(value) != supplied:
        raise ValueError(f"{path.name} self-hash mismatch")
    value[field] = supplied
    return value


def require_audit_gate(path: Path, gate: str) -> dict:
    value = load_self_hashed(path, "certificate_sha256")
    if value["gate"].get(gate) is not True:
        raise ValueError(f"{path.name}: required gate is not passed")
    return value


def dataset_context(dataset: Path) -> tuple[dict, dict]:
    run_manifest = load_self_hashed(
        dataset / "run-manifest.json", "run_manifest_sha256"
    )
    index = load_self_hashed(
        dataset / "table-index.json", "index_sha256"
    )
    if run_manifest["table_index_sha256"] != index["index_sha256"]:
        raise ValueError("run manifest does not authenticate table index")
    if run_manifest["prime_schedule"]["sha256"] != file_sha256(SCHEDULE):
        raise ValueError("dataset prime-schedule hash mismatch")
    return run_manifest, index


def weights_for(dimension: int, power: int) -> list[Fraction]:
    return [
        Fraction(1, index**power)
        for index in range(1, dimension + 1)
    ]


def replay_batch(
    dataset: Path,
    requests: list[dict],
    primes: list[int],
    logical_name: str,
) -> tuple[list[dict], dict]:
    run_manifest, index = dataset_context(dataset)
    tables = {table["table_id"]: table for table in index["tables"]}
    prepared = []
    wanted_dimensions: dict[str, set[int]] = {}
    required_by_entry: dict[tuple[str, int], list[int]] = {}
    for request in requests:
        table_id = request["table_id"]
        if table_id not in tables:
            raise ValueError(f"{dataset.name}: unknown table {table_id}")
        table = tables[table_id]
        dimension = int(request["dimension"])
        if not 1 <= dimension <= int(table["dimension"]):
            raise ValueError("oracle dimension is outside table")
        if (
            int(request["N"]) != int(table["N"])
            or int(request["weight_power"])
            != int(table["weight_power"])
        ):
            raise ValueError("oracle request/table metadata mismatch")
        weights = weights_for(dimension, int(table["weight_power"]))
        bound = error_numerator_bound(int(table["N"]), weights)
        available_count = int(table["work_prime_count"])
        minimal = choose_moduli(primes[:available_count], bound)
        required = [*range(len(minimal)), 3738, 3739]
        required_by_entry[(table_id, dimension)] = required
        wanted_dimensions.setdefault(table_id, set()).add(dimension)
        prepared.append((request, table, weights, bound, len(minimal)))

    available: dict[tuple[str, int, int], dict] = {}
    total_payload_bytes = 0
    selected_paths: set[str] = set()
    selected_record_by_path: dict[str, dict] = {}
    final_record = None
    for record in iter_chain(dataset / "manifest.jsonl"):
        final_record = record
        if record["event"] != "CHUNK":
            continue
        total_payload_bytes += int(record["bytes"])
        table_id = record["table_id"]
        dimensions = wanted_dimensions.get(table_id)
        if not dimensions:
            continue
        for dimension in dimensions:
            if (
                record["dimension_start"]
                <= dimension
                <= record["dimension_end"]
                and record["prime_index"]
                in required_by_entry[(table_id, dimension)]
            ):
                key = (table_id, dimension, record["prime_index"])
                if key in available:
                    raise ValueError("multiple chunks cover oracle residue")
                available[key] = record
                selected_paths.add(record["path"])
                selected_record_by_path[record["path"]] = record
    if final_record is None or final_record["event"] != "SEAL":
        raise ValueError(f"{dataset.name}: dataset is not sealed")
    if (
        final_record["run_manifest_sha256"]
        != run_manifest["run_manifest_sha256"]
    ):
        raise ValueError("seal does not authenticate run manifest")
    if (
        final_record["table_index_sha256"]
        != index["index_sha256"]
    ):
        raise ValueError("seal does not authenticate table index")
    if (
        int(final_record["dataset_payload_bytes"])
        != total_payload_bytes
    ):
        raise ValueError("seal payload-byte total mismatch")

    raw_cache: dict[str, bytes] = {}
    selected_payload_bytes = 0
    for relative in sorted(selected_paths):
        matching = selected_record_by_path[relative]
        path = dataset / relative
        raw = path.read_bytes()
        if (
            len(raw) != int(matching["bytes"])
            or file_sha256(path) != matching["sha256"]
        ):
            raise ValueError("selected oracle chunk authentication failed")
        raw_cache[relative] = raw
        selected_payload_bytes += len(raw)

    results = []
    for request, table, weights, bound, work_count in prepared:
        table_id = request["table_id"]
        dimension = int(request["dimension"])
        required = required_by_entry[(table_id, dimension)]
        if any(
            (table_id, dimension, prime_index) not in available
            for prime_index in required
        ):
            raise ValueError("oracle entry lacks required residue chunk")
        residues = {}
        chunk_hashes = {}
        for prime_index in required:
            record = available[(table_id, dimension, prime_index)]
            raw = raw_cache[record["path"]]
            offset = dimension - int(record["dimension_start"])
            residue = struct.unpack_from("<Q", raw, offset * 8)[0]
            if residue >= primes[prime_index]:
                raise ValueError("oracle residue is not reduced")
            residues[prime_index] = residue
            chunk_hashes[record["path"]] = record["sha256"]
        numerator = balanced_reconstruct(
            [residues[index] for index in range(work_count)],
            primes[:work_count],
            bound=bound,
        )
        overflow = []
        for prime_index in (3738, 3739):
            equal = residues[prime_index] == numerator % primes[prime_index]
            overflow.append(
                {
                    "prime_index": prime_index,
                    "equal": equal,
                    "stored_residue": str(residues[prime_index]),
                }
            )
        if not all(row["equal"] for row in overflow):
            raise ArithmeticError("oracle overflow-prime check failed")
        denominator = int(table["N"]) * prod(
            factor_denominator(int(table["N"]), weight)
            for weight in weights
        )
        value = Fraction(numerator, denominator)
        result = {
            **request,
            "claim_tag": "VERIFIED",
            "generator_prefix_sha256": table[
                "generator_prefix_sha256"
            ][dimension - 1],
            "minimal_work_prime_count": work_count,
            "proved_numerator_bound": str(bound),
            "reduced_numerator": str(value.numerator),
            "reduced_denominator": str(value.denominator),
            "overflow_checks": overflow,
            "authenticated_chunk_count": len(chunk_hashes),
            "authenticated_chunks_sha256": canonical_sha(chunk_hashes),
        }
        result["entry_sha256"] = canonical_sha(result)
        results.append(result)

    provenance = {
        "dataset": logical_name,
        "manifest_sha256": file_sha256(dataset / "manifest.jsonl"),
        "seal_line_sha256": final_record["line_sha256"],
        "run_manifest_sha256": run_manifest["run_manifest_sha256"],
        "selected_unique_chunk_count": len(selected_paths),
        "selected_payload_bytes": selected_payload_bytes,
        "dataset_payload_bytes": total_payload_bytes,
    }
    provenance["provenance_sha256"] = canonical_sha(provenance)
    return results, provenance


def exact_adversarial(case: dict) -> dict:
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
    result = {
        **case,
        "claim_tag": "VERIFIED",
        "left_score_numerator": str(left.numerator),
        "left_score_denominator": str(left.denominator),
        "right_score_numerator": str(right.numerator),
        "right_score_denominator": str(right.denominator),
        "comparison": comparison,
        "exact_equality": comparison == 0,
    }
    result["case_sha256"] = canonical_sha(result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fidelity", type=Path, required=True)
    parser.add_argument("--usability", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--recorded-at-utc", required=True)
    args = parser.parse_args()

    fidelity_audit = require_audit_gate(
        FIDELITY_AUDIT, "cycles_016_017_exit_gate_passed"
    )
    usability_audit = require_audit_gate(
        USABILITY_AUDIT, "cycle_018_data_gate_passed"
    )
    prereg = json.loads(PREREG.read_text())
    supplied_selection_sha = prereg.pop("selection_sha256")
    if canonical_sha(prereg) != supplied_selection_sha:
        raise ValueError("engine-oracle preregistration hash mismatch")
    prereg["selection_sha256"] = supplied_selection_sha
    schedule = json.loads(SCHEDULE.read_text())
    primes = [int(row["p"]) for row in schedule["primes"]]

    fidelity_requests = [
        row
        for row in prereg["table_merits"]
        if int(row["weight_power"]) == 2
    ]
    usability_requests = [
        row
        for row in prereg["table_merits"]
        if int(row["weight_power"]) in (1, 3)
    ]
    if len(fidelity_requests) != 254 or len(usability_requests) != 36:
        raise ArithmeticError("oracle request partition mismatch")

    fidelity_results, fidelity_provenance = replay_batch(
        args.fidelity.resolve(),
        fidelity_requests,
        primes,
        "fidelity-v2",
    )
    usability_results, usability_provenance = replay_batch(
        args.usability.resolve(),
        usability_requests,
        primes,
        "usability-v1",
    )
    if (
        fidelity_provenance["seal_line_sha256"]
        != fidelity_audit["dataset"]["seal_line_sha256"]
    ):
        raise ValueError(
            "fidelity dataset does not match its passed audit"
        )
    if (
        usability_provenance["seal_line_sha256"]
        != usability_audit["usability_dataset"][
            "manifest_last_line_sha256"
        ]
        or usability_provenance["manifest_sha256"]
        != usability_audit["usability_dataset"]["manifest_sha256"]
    ):
        raise ValueError(
            "usability dataset does not match its passed audit"
        )
    adversarial = [
        exact_adversarial(case)
        for case in prereg["adversarial_decision_cases"]
    ]
    payload = {
        "schema": "certified-qmc-engine-oracle-set-v1",
        "recorded_at_utc": args.recorded_at_utc,
        "claim_tag": "VERIFIED",
        "selection_preregistration": {
            "path": str(PREREG.relative_to(ROOT)),
            "file_sha256": file_sha256(PREREG),
            "selection_sha256": supplied_selection_sha,
        },
        "scope": (
            "Software-conformance oracle; not a representative sample "
            "of lattice-rule quality."
        ),
        "counts": {
            "fidelity_table_merits": len(fidelity_results),
            "usability_table_merits": len(usability_results),
            "adversarial_decision_cases": len(adversarial),
            "total": (
                len(fidelity_results)
                + len(usability_results)
                + len(adversarial)
            ),
        },
        "dataset_provenance": {
            "fidelity": fidelity_provenance,
            "usability": usability_provenance,
        },
        "table_merits": fidelity_results + usability_results,
        "adversarial_decision_cases": adversarial,
    }
    if payload["counts"]["total"] != 298:
        raise ArithmeticError("engine-oracle result count mismatch")
    payload["oracle_sha256"] = canonical_sha256(payload)
    args.output.resolve().write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    print(args.output.resolve())


if __name__ == "__main__":
    main()
