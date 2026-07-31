#!/usr/bin/env python3
"""Build the deterministic Track-A2 successor over companion v14."""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import shutil
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
REPO = PROJECT.parents[1]
NAME = "effective-stark-results-companion-v15"
ARCHIVE = PROJECT / "dist" / f"{NAME}.tar.gz"
FREEZE = PROJECT / "artifacts" / "results-paper-companion-local-freeze-v15.json"

FILES = (
    "projects/effective-stark-sweep/companion/CORRECTION-V1.4-A2.md",
    "projects/effective-stark-sweep/dist/effective-stark-results-companion-v14.tar.gz",
    "projects/effective-stark-sweep/paper/effective-stark-results.tex",
    "projects/effective-stark-sweep/paper/effective-stark-results.pdf",
    "projects/effective-stark-sweep/artifacts/results-paper-a2-wording-bibliography-audit-v1.json",
    "projects/effective-stark-sweep/scripts/audit_results_paper_a2.py",
    "projects/effective-stark-sweep/scripts/build_results_companion_v15.py",
    "projects/effective-stark-sweep/scripts/verify_results_companion_v15.py",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_tar(tree: Path) -> bytes:
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for relative in (*FILES, "MANIFEST.sha256"):
            source = tree / relative
            info = tar.gettarinfo(str(source), arcname=f"{NAME}/{relative}")
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.mtime = 0
            info.mode = 0o755 if "/scripts/" in relative else 0o644
            with source.open("rb") as stream:
                tar.addfile(info, stream)
    compressed = io.BytesIO()
    with gzip.GzipFile(
        filename="", mode="wb", fileobj=compressed, compresslevel=9, mtime=0
    ) as stream:
        stream.write(buffer.getvalue())
    return compressed.getvalue()


def main() -> None:
    missing = [relative for relative in FILES if not (REPO / relative).is_file()]
    if missing:
        raise FileNotFoundError(f"missing successor-layer inputs: {missing}")

    with tempfile.TemporaryDirectory(prefix="stark-v15-") as temporary:
        tree = Path(temporary)
        for relative in FILES:
            target = tree / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / relative, target)
        manifest = "\n".join(
            f"{sha256(tree / relative)}  {relative}" for relative in FILES
        )
        (tree / "MANIFEST.sha256").write_text(manifest + "\n")
        payload = build_tar(tree)

    ARCHIVE.parent.mkdir(exist_ok=True)
    if ARCHIVE.exists() and ARCHIVE.read_bytes() != payload:
        raise RuntimeError(f"{ARCHIVE} exists with different bytes; bump version")
    ARCHIVE.write_bytes(payload)
    record = {
        "schema": "effective-stark-results-companion-local-freeze-v15",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "LOCAL_FROZEN_NOT_PUBLIC",
        "archive": str(ARCHIVE.relative_to(PROJECT)),
        "archive_sha256": sha256(ARCHIVE),
        "archive_bytes": ARCHIVE.stat().st_size,
        "file_count_excluding_manifest": len(FILES),
        "base_v14_sha256": sha256(
            PROJECT / "dist" / "effective-stark-results-companion-v14.tar.gz"
        ),
        "correction_scope": [
            "all companion-v14 corrections preserved byte-for-byte",
            "Track-A2 Tangedal--Young bibliography pagination correction",
            "Track-A2 wording and prior-work citation audit",
        ],
        "publication_action_taken": False,
        "public_identifier": None,
    }
    if FREEZE.exists():
        frozen = json.loads(FREEZE.read_text())
        stable = tuple(key for key in record if key != "recorded_at_utc")
        if any(frozen.get(key) != record.get(key) for key in stable):
            raise RuntimeError(f"{FREEZE} describes different bytes; bump version")
    else:
        FREEZE.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(f"COMPANION_V15_FILE_COUNT={len(FILES)}")
    print(f"COMPANION_V15_SHA256={sha256(ARCHIVE)}")
    print("COMPANION_V15_LOCAL_FREEZE=PASS")


if __name__ == "__main__":
    main()
