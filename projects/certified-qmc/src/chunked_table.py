"""Hash-chained JSONL manifests for chunked certified tables."""

from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path
from typing import Iterable


ZERO_HASH = "0" * 64


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def record_hash(record_without_hash: dict) -> str:
    return sha256(canonical_bytes(record_without_hash)).hexdigest()


def append_record(path: Path, payload: dict, previous: str) -> dict:
    record = dict(payload)
    record["previous_line_sha256"] = previous
    record["line_sha256"] = record_hash(record)
    with path.open("ab") as stream:
        stream.write(canonical_bytes(record) + b"\n")
        stream.flush()
        os.fsync(stream.fileno())
    return record


def read_chain(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records = []
    previous = ZERO_HASH
    for sequence, line in enumerate(path.read_bytes().splitlines()):
        record = json.loads(line)
        if record.get("sequence") != sequence:
            raise ValueError("manifest sequence is not contiguous")
        supplied = record.pop("line_sha256", None)
        if record.get("previous_line_sha256") != previous:
            raise ValueError("manifest previous-hash link failed")
        expected = record_hash(record)
        if supplied != expected:
            raise ValueError("manifest line hash failed")
        record["line_sha256"] = supplied
        records.append(record)
        previous = supplied
    return records


def chunk_records(records: Iterable[dict]) -> list[dict]:
    return [record for record in records if record["event"] == "CHUNK"]
