#!/usr/bin/env python3
"""Build the deterministic DOI-bearing census v1.0 companion."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import tarfile
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
NAME = "effective-stark-census-companion-v1"

FIXED = (
    "companion/CENSUS-RELEASE-V1.0.md",
    "paper/effective-stark-census.tex",
    "paper/effective-stark-census.pdf",
    "paper/effective-stark-census.log",
    "artifacts/zenodo-census-v1.0-draft-reservation-v1.json",
    "artifacts/zenodo-census-record-metadata-v1.json",
    "artifacts/census-paper-layer0-reconciliation-v1.json",
    "artifacts/census-q-packet-corpus-audit-v1.json",
    "artifacts/census-h-taxonomy-v2.json",
    "artifacts/engine-b-transport-manifest-v5.json",
    "artifacts/engine-b-transport-ledger-v4.json",
    "artifacts/rq000013-engine-a-imprimitive-certificate-v1.json",
    "artifacts/b5079-hilbert-ray-containment-v1.json",
    "artifacts/hilbert-ray-containment-tranche-v1.json",
    "artifacts/b5086-transport-geometry-v1.json",
    "artifacts/final-direct-source-coprime-screen-v1.json",
    "artifacts/frozen-ideal-census-v1.json",
    "artifacts/census-q-arb-audit-v1.json",
    "artifacts/q-euler-deleted-prime-cover-theorem-v1.json",
    "artifacts/w1-full-census-v1.json",
    "artifacts/engine-a-queue-analysis-v1.json",
    "artifacts/engine-a-euler-degeneracy-v1.json",
    "artifacts/b5025-euler-deletion-transports-v2.json",
    "artifacts/b5025-label-aware-transports-v1.json",
    "artifacts/b5022-label-aware-transports-v1.json",
    "artifacts/rq000039-engine-b-transport-v1.json",
    "data/census-paper-preregistration-v1.json",
    "data/census-paper-preregistration-amendment-v18.json",
    "discovery/export_q_euler_local_features.gp",
    "discovery/q-euler-local-features-v1.json",
    "discovery/q-euler-local-features-v1.transcript",
    "discovery/analyze_q_euler_patterns.py",
    "discovery/q-euler-pattern-analysis-v2.json",
    "discovery/q-four-support-counterexample-search-v2.json",
    "discovery/search_q_four_support_all_zero.gp",
    "discovery/search_q_four_support_counterexample.py",
    "docs/cycle-127-census-referee-revision.md",
    "docs/cycle-128-q-euler-degeneracy-pattern-preregistration.md",
    "docs/cycle-128-q-euler-deleted-prime-cover-theorem.md",
    "docs/cycle-128-q-four-support-falsification-amendment-v1.md",
    "docs/cycle-129-census-zenodo-release-preregistration.md",
    "proof/audit_q_euler_deleted_prime_cover.py",
    "scripts/enumerate_frozen_ideals.py",
    "scripts/enumerate_frozen_ideals.gp",
    "scripts/audit_census_paper.py",
    "scripts/audit_census_referee_revision.py",
    "scripts/build_census_companion_v1.py",
    "scripts/verify_census_companion_v1.py",
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs() -> tuple[str, ...]:
    rows = tuple(
        str(path.relative_to(PROJECT))
        for path in sorted((PROJECT / "artifacts/census-q-packets-v1").rglob("*"))
        if path.is_file()
    )
    return tuple(sorted(set(FIXED + rows)))


def payload(files: tuple[str, ...]) -> bytes:
    manifest = "".join(f"{sha256(PROJECT / item)}  {item}\n" for item in files)
    content = io.BytesIO()
    with tarfile.open(fileobj=content, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for relative in files:
            path = PROJECT / relative
            info = tar.gettarinfo(str(path), arcname=f"{NAME}/{relative}")
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.mtime = 0
            info.mode = 0o755 if relative.endswith((".py", ".gp")) else 0o644
            with path.open("rb") as stream:
                tar.addfile(info, stream)
        data = manifest.encode()
        info = tarfile.TarInfo(f"{NAME}/MANIFEST.sha256")
        info.size = len(data)
        info.uid = info.gid = info.mtime = 0
        info.mode = 0o644
        tar.addfile(info, io.BytesIO(data))
    result = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=result, compresslevel=9, mtime=0) as stream:
        stream.write(content.getvalue())
    return result.getvalue()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=PROJECT / "dist" / f"{NAME}.tar.gz")
    args = parser.parse_args()
    files = inputs()
    missing = [item for item in files if not (PROJECT / item).is_file()]
    if missing:
        raise FileNotFoundError(missing)
    data = payload(files)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(data)
    print(f"CENSUS_COMPANION_FILES={len(files)}")
    print(f"CENSUS_COMPANION_BYTES={len(data)}")
    print(f"CENSUS_COMPANION_SHA256={hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
