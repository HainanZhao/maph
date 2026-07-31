#!/usr/bin/env python3
"""Build the deterministic v1.4 correction layer over companion v13."""

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
NAME = "effective-stark-results-companion-v14"
ARCHIVE = PROJECT / "dist" / f"{NAME}.tar.gz"
FREEZE = PROJECT / "artifacts" / "results-paper-companion-local-freeze-v14.json"

FILES = (
    "projects/effective-stark-sweep/companion/CORRECTION-V1.4.md",
    "projects/effective-stark-sweep/dist/effective-stark-results-companion-v13.tar.gz",
    "projects/effective-stark-sweep/artifacts/engine-c-fourier-convention-correction-v1.json",
    "projects/effective-stark-sweep/scripts/audit_engine_c_fourier_convention.py",
    "projects/effective-stark-sweep/artifacts/rq000013-engine-a-imprimitive-certificate-v1.json",
    "projects/effective-stark-sweep/artifacts/rq000013-engine-a-imprimitive-certificate-v1.transcript",
    "projects/effective-stark-sweep/data/census-paper-imprimitive-worked-case-selection-v1.json",
    "projects/effective-stark-sweep/data/engine-a-uniform-theorem-v1.json",
    "projects/effective-stark-sweep/artifacts/engine-a-euler-degeneracy-v1.json",
    "projects/effective-stark-sweep/artifacts/engine-a-field-census-v1.json",
    "projects/effective-stark-sweep/scripts/certify_rq000013_engine_a.gp",
    "projects/effective-stark-sweep/scripts/certify_rq000013_engine_a.py",
    "projects/effective-stark-sweep/paper/effective-stark-results-supplement-rq000013-addendum.tex",
    "projects/effective-stark-sweep/paper/effective-stark-results-supplement-rq000013-addendum.pdf",
    "projects/effective-stark-sweep/docs/cycle-078-rq000013-imprimitive-engine-a.md",
    "projects/effective-stark-sweep/scripts/build_results_companion_v14.py",
    "projects/effective-stark-sweep/scripts/verify_results_companion_v14.py",
    "projects/dedekind-stark-phase/artifacts/circularity-audit-v1.json",
    "projects/dedekind-stark-phase/docs/circularity-audit-v1.md",
    "projects/dedekind-stark-phase/artifacts/all-five-phase-gates-v1.json",
    "projects/dedekind-stark-phase/artifacts/roblot-quartic-gate-sealed-v1.json",
    "projects/dedekind-stark-phase/docs/roblot-phase-clarification-lemma-v1.md",
    "projects/dedekind-stark-phase/scripts/compare_all_phase_gates.py",
    "projects/dedekind-stark-phase/scripts/canonicalize_phase_gauge.py",
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
        raise FileNotFoundError(f"missing correction-layer inputs: {missing}")

    with tempfile.TemporaryDirectory(prefix="stark-v14-") as temporary:
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
        "schema": "effective-stark-results-companion-local-freeze-v14",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "LOCAL_FROZEN_NOT_PUBLIC",
        "archive": str(ARCHIVE.relative_to(PROJECT)),
        "archive_sha256": sha256(ARCHIVE),
        "archive_bytes": ARCHIVE.stat().st_size,
        "file_count_excluding_manifest": len(FILES),
        "base_v13_sha256": sha256(
            PROJECT / "dist" / "effective-stark-results-companion-v13.tar.gz"
        ),
        "correction_scope": [
            "Engine-C sigma-positive Fourier convention",
            "withdrawn target-selected direct/inverse orientation replay",
            "five-case Roblot certified-case mu4 corollary",
            "RQ-000013 exact nonzero imprimitive Engine-A row",
        ],
        "publication_action_taken": False,
        "public_identifier": None,
    }
    if FREEZE.exists():
        frozen = json.loads(FREEZE.read_text())
        stable = (
            "status",
            "archive",
            "archive_sha256",
            "archive_bytes",
            "file_count_excluding_manifest",
            "base_v13_sha256",
            "correction_scope",
            "publication_action_taken",
            "public_identifier",
        )
        if any(frozen.get(key) != record.get(key) for key in stable):
            raise RuntimeError(f"{FREEZE} describes different bytes; bump version")
    else:
        FREEZE.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(f"COMPANION_V14_FILE_COUNT={len(FILES)}")
    print(f"COMPANION_V14_SHA256={sha256(ARCHIVE)}")
    print("COMPANION_V14_LOCAL_FREEZE=PASS")


if __name__ == "__main__":
    main()
