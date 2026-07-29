"""Single-pass selected-entry replay for chunked certified tables."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from math import prod
from pathlib import Path
import struct
import sys
from typing import Iterable

from .chunked_table import (
    canonical_bytes,
    chunk_records,
    file_sha256,
    read_chain,
)
from .crt import balanced_reconstruct, choose_moduli
from .scaled_integer import error_numerator_bound, factor_denominator


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def canonical_sha(value: object) -> str:
    return sha256(canonical_bytes(value)).hexdigest()


def load_self_hashed(path: Path, field: str) -> dict:
    value = json.loads(path.read_text())
    supplied = value.pop(field)
    if canonical_sha(value) != supplied:
        raise ValueError(f"{path.name} self-hash mismatch")
    value[field] = supplied
    return value


class DatasetReplay:
    """Authenticate one dataset once and replay selected entries."""

    def __init__(self, dataset: Path, project_root: Path):
        self.dataset = dataset.resolve()
        self.project_root = project_root.resolve()
        self.run_manifest = load_self_hashed(
            self.dataset / "run-manifest.json",
            "run_manifest_sha256",
        )
        self.index = load_self_hashed(
            self.dataset / "table-index.json", "index_sha256"
        )
        if (
            self.run_manifest["table_index_sha256"]
            != self.index["index_sha256"]
        ):
            raise ValueError(
                "run manifest does not authenticate table index"
            )
        self.records = read_chain(self.dataset / "manifest.jsonl")
        if not self.records or self.records[-1]["event"] != "SEAL":
            raise ValueError("dataset manifest is not sealed")
        seal = self.records[-1]
        if (
            seal["run_manifest_sha256"]
            != self.run_manifest["run_manifest_sha256"]
            or seal["table_index_sha256"] != self.index["index_sha256"]
        ):
            raise ValueError("seal does not authenticate dataset metadata")
        schedule_path = (
            self.project_root
            / self.run_manifest["prime_schedule"]["path"]
        )
        if (
            file_sha256(schedule_path)
            != self.run_manifest["prime_schedule"]["sha256"]
        ):
            raise ValueError("prime schedule hash mismatch")
        schedule = json.loads(schedule_path.read_text())
        self.primes = [int(row["p"]) for row in schedule["primes"]]
        self.tables = {
            (table["table_id"], int(table["N"])): table
            for table in self.index["tables"]
        }
        self.chunks = chunk_records(self.records)
        self.payload_bytes = sum(
            int(record["bytes"]) for record in self.chunks
        )

    def _prepare(self, requests: Iterable[dict]) -> list[dict]:
        prepared = []
        seen = set()
        for request in requests:
            table_id = str(request["table"])
            modulus = int(request["N"])
            dimension = int(request["dimension"])
            key = (table_id, modulus, dimension)
            if key in seen:
                raise ValueError("duplicate selected-entry request")
            seen.add(key)
            candidates = self.tables.get((table_id, modulus))
            if candidates is None:
                raise ValueError("table and N do not identify one table")
            table = candidates
            if not 1 <= dimension <= int(table["dimension"]):
                raise ValueError("dimension outside table")
            work_count = int(table["work_prime_count"])
            required_indices = [*range(work_count), 3738, 3739]
            prepared.append(
                {
                    "table_id": table_id,
                    "N": modulus,
                    "dimension": dimension,
                    "table": table,
                    "work_count": work_count,
                    "required_indices": required_indices,
                    "required_set": set(required_indices),
                }
            )
        if not prepared:
            raise ValueError("selected-entry request set is empty")
        return prepared

    def verify(self, requests: Iterable[dict], *, compact: bool) -> list[dict]:
        prepared = self._prepare(requests)
        wanted_by_table: dict[str, list[dict]] = {}
        for request in prepared:
            wanted_by_table.setdefault(
                request["table_id"], []
            ).append(request)
        available: dict[tuple[str, int, int], dict] = {}
        for record in self.chunks:
            wanted = wanted_by_table.get(record["table_id"])
            if not wanted:
                continue
            prime_index = int(record["prime_index"])
            start = int(record["dimension_start"])
            end = int(record["dimension_end"])
            for request in wanted:
                dimension = request["dimension"]
                if (
                    start <= dimension <= end
                    and prime_index in request["required_set"]
                ):
                    key = (
                        request["table_id"],
                        dimension,
                        prime_index,
                    )
                    if key in available:
                        raise ValueError(
                            "multiple chunks cover selected residue"
                        )
                    available[key] = record

        results = []
        for request in prepared:
            table_id = request["table_id"]
            dimension = request["dimension"]
            required = request["required_indices"]
            if any(
                (table_id, dimension, prime_index) not in available
                for prime_index in required
            ):
                raise ValueError(
                    "selected entry lacks required prime chunks"
                )
            residues: dict[int, int] = {}
            touched = 0
            touched_chunks = []
            for prime_index in required:
                record = available[
                    (table_id, dimension, prime_index)
                ]
                path = self.dataset / record["path"]
                raw = path.read_bytes()
                touched += len(raw)
                if (
                    len(raw) != int(record["bytes"])
                    or sha256(raw).hexdigest() != record["sha256"]
                ):
                    raise ValueError(
                        "selected chunk authentication failed"
                    )
                offset = dimension - int(record["dimension_start"])
                residue = struct.unpack_from("<Q", raw, offset * 8)[0]
                if residue >= self.primes[prime_index]:
                    raise ValueError("selected residue is not reduced")
                residues[prime_index] = residue
                touched_chunks.append(record["path"])

            table = request["table"]
            modulus = request["N"]
            weights = [
                Fraction(
                    1,
                    index_value
                    ** int(table["weight_power"]),
                )
                for index_value in range(1, dimension + 1)
            ]
            bound = error_numerator_bound(modulus, weights)
            minimal_moduli = choose_moduli(
                self.primes[:3738], bound
            )
            work_count = request["work_count"]
            if len(minimal_moduli) > work_count:
                raise ValueError(
                    "recorded work-prime count is insufficient"
                )
            selected_moduli = self.primes[:work_count]
            numerator = balanced_reconstruct(
                [residues[index] for index in range(work_count)],
                selected_moduli,
                bound=bound,
            )
            overflow = []
            for prime_index in (3738, 3739):
                expected = numerator % self.primes[prime_index]
                equal = residues[prime_index] == expected
                overflow.append(
                    {
                        "prime_index": prime_index,
                        "prime": str(self.primes[prime_index]),
                        "stored_residue": str(
                            residues[prime_index]
                        ),
                        "reconstructed_residue": str(expected),
                        "equal": equal,
                    }
                )
            if not all(item["equal"] for item in overflow):
                raise ArithmeticError(
                    "universal overflow-prime check failed"
                )
            denominator = modulus * prod(
                factor_denominator(modulus, weight)
                for weight in weights
            )
            value = Fraction(numerator, denominator)
            fraction_touched = Fraction(
                touched, self.payload_bytes
            )
            result = {
                "status": "VERIFIED",
                "claim_tag": "VERIFIED_SELECTED_ENTRY_REPLAY",
                "table": table_id,
                "N": modulus,
                "dimension": dimension,
                "weight_power": table["weight_power"],
                "generator_prefix_sha256": table[
                    "generator_prefix_sha256"
                ][dimension - 1],
                "work_prime_count": work_count,
                "work_residues_reconstructed": work_count,
                "overflow_checks": overflow,
                "proved_numerator_bound": str(bound),
                "scaled_numerator": str(numerator),
                "scaled_denominator": str(denominator),
                "reduced_numerator": str(value.numerator),
                "reduced_denominator": str(value.denominator),
                "chunks_read": len(touched_chunks),
                "dataset_payload_bytes": self.payload_bytes,
                "touched_payload_bytes": touched,
                "touched_payload_fraction": float(
                    fraction_touched
                ),
                "touched_payload_fraction_exact": (
                    f"{fraction_touched.numerator}/"
                    f"{fraction_touched.denominator}"
                ),
                "boundary": (
                    "VERIFIED authenticates the selected chunks, "
                    "uniquely reconstructs the bounded exact numerator, "
                    "and passes both universal overflow primes. The "
                    "keyed vector itself is not embedded."
                ),
            }
            if not compact:
                result["chunk_paths"] = touched_chunks
            results.append(result)
        return results
