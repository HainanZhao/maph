#!/usr/bin/env python3
"""Build the deterministic DOI-bearing v1.4 release companion."""

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
NAME = "effective-stark-results-companion-v17"
ARCHIVE = PROJECT / "dist" / f"{NAME}.tar.gz"
FREEZE = PROJECT / "artifacts" / "results-paper-companion-local-freeze-v17.json"

FILES = (
    "projects/effective-stark-sweep/companion/CORRECTION-V1.4-FINAL.md",
    "projects/effective-stark-sweep/dist/effective-stark-results-companion-v16.tar.gz",
    "projects/effective-stark-sweep/paper/effective-stark-results.tex",
    "projects/effective-stark-sweep/paper/effective-stark-results.pdf",
    "projects/effective-stark-sweep/paper/effective-stark-results-supplement.tex",
    "projects/effective-stark-sweep/paper/effective-stark-results-supplement.pdf",
    "projects/effective-stark-sweep/paper/effective-stark-results-supplement-rq000013-addendum.tex",
    "projects/effective-stark-sweep/paper/effective-stark-results-supplement-rq000013-addendum.pdf",
    "projects/effective-stark-sweep/artifacts/zenodo-results-record-metadata-v7.json",
    "projects/effective-stark-sweep/artifacts/zenodo-results-v1.4-draft-reservation-v1.json",
    "projects/effective-stark-sweep/artifacts/engine-c-fourier-convention-correction-v3.json",
    "projects/effective-stark-sweep/scripts/audit_engine_c_fourier_convention_v3.py",
    "projects/effective-stark-sweep/artifacts/results-paper-referee-audit-v4.json",
    "projects/effective-stark-sweep/scripts/audit_results_paper_full.py",
    "projects/effective-stark-sweep/artifacts/results-paper-release-doi-audit-v1.json",
    "projects/effective-stark-sweep/scripts/audit_results_release_doi.py",
    "projects/effective-stark-sweep/scripts/build_results_companion_v17.py",
    "projects/effective-stark-sweep/scripts/verify_results_companion_v17.py",
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
        raise FileNotFoundError(f"missing DOI-bearing release inputs: {missing}")
    with tempfile.TemporaryDirectory(prefix="stark-v17-") as temporary:
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
        "schema": "effective-stark-results-companion-local-freeze-v17",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "LOCAL_FROZEN_DOI_BEARING_NOT_PUBLIC",
        "reserved_doi": "10.5281/zenodo.21712478",
        "archive": str(ARCHIVE.relative_to(PROJECT)),
        "archive_sha256": sha256(ARCHIVE),
        "archive_bytes": ARCHIVE.stat().st_size,
        "file_count_excluding_manifest": len(FILES),
        "base_v16_sha256": sha256(
            PROJECT / "dist" / "effective-stark-results-companion-v16.tar.gz"
        ),
        "correction_scope": [
            "all pre-DOI v16 correction records preserved",
            "reserved DOI inserted into release-facing sources",
            "versioned Engine-C and full-referee DOI-bearing re-audits",
            "exact release-source delta from immutable v1.3",
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
    print(f"COMPANION_V17_FILE_COUNT={len(FILES)}")
    print(f"COMPANION_V17_SHA256={sha256(ARCHIVE)}")
    print("COMPANION_V17_LOCAL_FREEZE=PASS")


if __name__ == "__main__":
    main()
