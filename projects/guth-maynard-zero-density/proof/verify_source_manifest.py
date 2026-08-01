#!/usr/bin/env python3
"""Verify the frozen Cycle-1 Guth--Maynard source objects."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys


PROJECT = Path(__file__).resolve().parents[1]
SOURCES = PROJECT / "artifacts" / "sources"

EXPECTED = {
    "guth-maynard-2405.20552v2-source.tar": {
        "sha256": "9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc",
        "bytes": 39943,
        "role": "arXiv v2 TeX source tarball",
        "url": "https://export.arxiv.org/e-print/2405.20552v2",
    },
    "guth-maynard-2405.20552v2.pdf": {
        "sha256": "915392cf7d0ecd108479814a9a1481e23423ef63415776471cec3975ae482cae",
        "bytes": 656298,
        "role": "arXiv v2 rendered PDF",
        "url": "https://arxiv.org/pdf/2405.20552v2",
    },
    "guth-maynard-annals-aam.pdf": {
        "sha256": "4a7b0e294c4b0e8580a3315e6dd418d351a295ebd03e9e2a35d69f0086607099",
        "bytes": 638669,
        "role": "Oxford repository author accepted manuscript for Annals publication",
        "url": (
            "https://ora.ox.ac.uk/objects/"
            "uuid%3Aad11b8bf-ad2b-4ebf-a627-647f023c378f/files/s73666708v"
        ),
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    rows = []
    ok = True
    for name, expected in EXPECTED.items():
        path = SOURCES / name
        exists = path.is_file()
        actual_bytes = path.stat().st_size if exists else None
        actual_hash = sha256(path) if exists else None
        row_ok = (
            exists
            and actual_bytes == expected["bytes"]
            and actual_hash == expected["sha256"]
        )
        ok &= row_ok
        rows.append(
            {
                "file": name,
                "role": expected["role"],
                "url": expected["url"],
                "expected_bytes": expected["bytes"],
                "actual_bytes": actual_bytes,
                "expected_sha256": expected["sha256"],
                "actual_sha256": actual_hash,
                "verified": row_ok,
            }
        )
    print(json.dumps({"schema": 1, "verified": ok, "sources": rows}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
