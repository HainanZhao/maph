#!/usr/bin/env python3
"""Audit the exact DOI-bearing release-source delta from published v1.3."""

from __future__ import annotations

import hashlib
import json
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V13 = ROOT / "dist/effective-stark-results-companion-v13.tar.gz"
V13_SHA256 = "1ecca96bd388ab2cafa27c091380121db4749e41ae794c2326439adbbe87b608"
ARCHIVE_ROOT = "effective-stark-results-companion-v13"
MAIN = ROOT / "paper/effective-stark-results.tex"
MAIN_PDF = ROOT / "paper/effective-stark-results.pdf"
SUPPLEMENT = ROOT / "paper/effective-stark-results-supplement.tex"
SUPPLEMENT_PDF = ROOT / "paper/effective-stark-results-supplement.pdf"
ADDENDUM = ROOT / "paper/effective-stark-results-supplement-rq000013-addendum.tex"
ADDENDUM_PDF = ROOT / "paper/effective-stark-results-supplement-rq000013-addendum.pdf"
OUT = ROOT / "artifacts/results-paper-release-doi-audit-v1.json"
OLD_DOI = "10.5281/zenodo.21708121"
NEW_DOI = "10.5281/zenodo.21712478"
OLD_RANGE = r"J.\ Number Theory \textbf{133} (2013), 1022--1045,"
NEW_RANGE = r"J.\ Number Theory \textbf{133} (2013), 1045--1061,"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def archived_text(archive: tarfile.TarFile, relative: str) -> str:
    stream = archive.extractfile(f"{ARCHIVE_ROOT}/{relative}")
    if stream is None:
        raise RuntimeError(f"published v1.3 omits {relative}")
    return stream.read().decode()


def main() -> None:
    if sha256(V13) != V13_SHA256:
        raise RuntimeError("immutable v1.3 companion hash changed")
    with tarfile.open(V13, "r:gz") as archive:
        old_main = archived_text(archive, "paper/effective-stark-results.tex")
        old_supplement = archived_text(
            archive, "paper/effective-stark-results-supplement.tex"
        )

    expected_main = old_main.replace(OLD_RANGE, NEW_RANGE).replace(
        OLD_DOI, NEW_DOI
    )
    if old_main.count(OLD_RANGE) != 1 or old_main.count(OLD_DOI) != 1:
        raise RuntimeError("published main-source replacement count changed")
    if MAIN.read_text() != expected_main:
        raise RuntimeError(
            "DOI-bearing main source differs beyond pagination and DOI"
        )
    expected_supplement = old_supplement.replace(OLD_DOI, NEW_DOI)
    if old_supplement.count(OLD_DOI) != 1:
        raise RuntimeError("published supplement DOI count changed")
    if SUPPLEMENT.read_text() != expected_supplement:
        raise RuntimeError("supplement differs beyond the release DOI")

    addendum = ADDENDUM.read_text()
    required = (
        NEW_DOI,
        "The identity below is \\texttt{PROVED}",
        "only an \\texttt{OBSERVED} cross-check",
        r"E_\chi=1-\chi^\circ(\mathfrak p)=2",
        r"X_{[0]}=u^2,\qquad X_{[1]}=u^{-2}",
    )
    if any(needle not in addendum for needle in required):
        raise RuntimeError("DOI-bearing addendum omits a release gate")

    payload = {
        "schema": "effective-stark-results-paper-release-doi-audit-v1",
        "recorded_at_utc": "2026-07-31T00:00:00Z",
        "status": "PASS_EXACT_RELEASE_SOURCE_DELTA",
        "reserved_doi": NEW_DOI,
        "published_v1_3_archive_sha256": V13_SHA256,
        "source_delta": {
            "main": "Tangedal--Young page range plus archive DOI only",
            "supplement": "archive DOI only",
            "addendum": "new RQ-000013 proof row with reserved DOI",
        },
        "files": {
            str(path.relative_to(ROOT)): {
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in (
                MAIN,
                MAIN_PDF,
                SUPPLEMENT,
                SUPPLEMENT_PDF,
                ADDENDUM,
                ADDENDUM_PDF,
            )
        },
        "mathematical_claim_change_from_pre_doi_freeze": "NONE",
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("RESULTS_RELEASE_DOI_AUDIT=PASS")


if __name__ == "__main__":
    main()
