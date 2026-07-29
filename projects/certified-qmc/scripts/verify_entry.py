#!/usr/bin/env python3
"""Verify one chunked merit-table entry without reading unrelated chunks."""

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

from src.chunked_table import canonical_bytes, chunk_records, file_sha256, read_chain
from src.crt import balanced_reconstruct, choose_moduli
from src.scaled_integer import error_numerator_bound, factor_denominator


def canonical_sha(value: object) -> str:
    return sha256(canonical_bytes(value)).hexdigest()


def load_self_hashed(path: Path, field: str) -> dict:
    value = json.loads(path.read_text())
    supplied = value.pop(field)
    if canonical_sha(value) != supplied:
        raise ValueError(f"{path.name} self-hash mismatch")
    value[field] = supplied
    return value


def main() -> None:
    parser = argparse.ArgumentParser(prog="verify-entry")
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--table", required=True)
    parser.add_argument("--N", type=int, required=True)
    parser.add_argument("--d", type=int, required=True)
    args = parser.parse_args()

    dataset = args.dataset.resolve()
    run_manifest = load_self_hashed(
        dataset / "run-manifest.json", "run_manifest_sha256"
    )
    index = load_self_hashed(
        dataset / "table-index.json", "index_sha256"
    )
    if run_manifest["table_index_sha256"] != index["index_sha256"]:
        raise ValueError("run manifest does not authenticate table index")
    records = read_chain(dataset / "manifest.jsonl")
    if not records or records[-1]["event"] != "SEAL":
        raise ValueError("dataset manifest is not sealed")
    seal = records[-1]
    if seal["run_manifest_sha256"] != run_manifest["run_manifest_sha256"]:
        raise ValueError("seal does not authenticate run manifest")
    if seal["table_index_sha256"] != index["index_sha256"]:
        raise ValueError("seal does not authenticate table index")

    candidates = [
        table
        for table in index["tables"]
        if table["table_id"] == args.table and table["N"] == args.N
    ]
    if len(candidates) != 1:
        raise ValueError("table and N do not identify one table")
    table = candidates[0]
    if not 1 <= args.d <= table["dimension"]:
        raise ValueError("dimension outside table")

    schedule_path = ROOT / run_manifest["prime_schedule"]["path"]
    if (
        file_sha256(schedule_path)
        != run_manifest["prime_schedule"]["sha256"]
    ):
        raise ValueError("prime schedule hash mismatch")
    schedule = json.loads(schedule_path.read_text())
    primes = [int(row["p"]) for row in schedule["primes"]]
    work_count = int(table["work_prime_count"])
    required_indices = [*range(work_count), 3738, 3739]

    available: dict[int, dict] = {}
    payload_bytes = 0
    for record in chunk_records(records):
        payload_bytes += int(record["bytes"])
        if (
            record["table_id"] == args.table
            and record["N"] == args.N
            and record["dimension_start"] <= args.d
            and record["dimension_end"] >= args.d
            and record["prime_index"] in required_indices
        ):
            if record["prime_index"] in available:
                raise ValueError("multiple chunks cover selected residue")
            available[record["prime_index"]] = record
    if sorted(available) != required_indices:
        raise ValueError("selected entry lacks required prime chunks")

    residues: dict[int, int] = {}
    touched = 0
    touched_chunks = []
    for prime_index in required_indices:
        record = available[prime_index]
        path = dataset / record["path"]
        raw = path.read_bytes()
        touched += len(raw)
        if len(raw) != record["bytes"] or file_sha256(path) != record["sha256"]:
            raise ValueError("selected chunk authentication failed")
        offset = args.d - record["dimension_start"]
        residue = struct.unpack_from("<Q", raw, offset * 8)[0]
        if residue >= primes[prime_index]:
            raise ValueError("selected residue is not reduced")
        residues[prime_index] = residue
        touched_chunks.append(record["path"])

    weights = [
        Fraction(1, index_value ** int(table["weight_power"]))
        for index_value in range(1, args.d + 1)
    ]
    bound = error_numerator_bound(args.N, weights)
    minimal_moduli = choose_moduli(primes[:3738], bound)
    if len(minimal_moduli) > work_count:
        raise ValueError("recorded work-prime count is insufficient")
    selected_moduli = primes[:work_count]
    numerator = balanced_reconstruct(
        [residues[index] for index in range(work_count)],
        selected_moduli,
        bound=bound,
    )
    overflow = []
    for prime_index in (3738, 3739):
        expected = numerator % primes[prime_index]
        equal = residues[prime_index] == expected
        overflow.append(
            {
                "prime_index": prime_index,
                "prime": str(primes[prime_index]),
                "stored_residue": str(residues[prime_index]),
                "reconstructed_residue": str(expected),
                "equal": equal,
            }
        )
    if not all(item["equal"] for item in overflow):
        raise ArithmeticError("universal overflow-prime check failed")

    denominator = args.N * prod(
        factor_denominator(args.N, weight) for weight in weights
    )
    value = Fraction(numerator, denominator)
    fraction_touched = Fraction(touched, payload_bytes)
    result = {
        "status": "VERIFIED",
        "claim_tag": "VERIFIED_SELECTED_ENTRY_REPLAY",
        "table": args.table,
        "N": args.N,
        "dimension": args.d,
        "weight_power": table["weight_power"],
        "generator_prefix_sha256": table[
            "generator_prefix_sha256"
        ][args.d - 1],
        "work_prime_count": work_count,
        "work_residues_reconstructed": work_count,
        "overflow_checks": overflow,
        "proved_numerator_bound": str(bound),
        "scaled_numerator": str(numerator),
        "scaled_denominator": str(denominator),
        "reduced_numerator": str(value.numerator),
        "reduced_denominator": str(value.denominator),
        "chunks_read": len(touched_chunks),
        "chunk_paths": touched_chunks,
        "dataset_payload_bytes": payload_bytes,
        "touched_payload_bytes": touched,
        "touched_payload_fraction": float(fraction_touched),
        "touched_payload_fraction_exact": (
            f"{fraction_touched.numerator}/{fraction_touched.denominator}"
        ),
        "boundary": (
            "VERIFIED authenticates the selected chunks, uniquely "
            "reconstructs the bounded exact numerator, and passes both "
            "universal overflow primes. The keyed vector itself is not "
            "embedded."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
