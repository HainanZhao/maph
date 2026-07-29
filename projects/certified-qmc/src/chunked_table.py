"""Hash-chained JSONL manifests for chunked certified tables."""

from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path
from typing import Iterable, Iterator


ZERO_HASH = "0" * 64


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("ascii")


def file_sha256(path: Path) -> str:
    hasher = sha256()
    block = bytearray(1024 * 1024)
    view = memoryview(block)
    with path.open("rb", buffering=0) as stream:
        while count := stream.readinto(view):
            hasher.update(view[:count])
    return hasher.hexdigest()


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


def iter_chain(path: Path) -> Iterator[dict]:
    """Authenticate a JSONL hash chain without retaining prior rows."""
    if not path.exists():
        return
    previous = ZERO_HASH
    with path.open("rb") as stream:
        for sequence, line in enumerate(stream):
            if not line.endswith(b"\n"):
                raise ValueError("manifest has an unterminated final line")
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
            yield record
            previous = supplied


def read_chain(path: Path) -> list[dict]:
    """Authenticate and materialize a chain for small-data callers."""
    return list(iter_chain(path))


def chunk_records(records: Iterable[dict]) -> list[dict]:
    return [record for record in records if record["event"] == "CHUNK"]


def iter_chunk_records(records: Iterable[dict]) -> Iterator[dict]:
    for record in records:
        if record["event"] == "CHUNK":
            yield record
