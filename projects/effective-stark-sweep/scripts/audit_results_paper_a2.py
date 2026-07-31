#!/usr/bin/env python3
"""Audit the Track-A2 wording and bibliography correction.

The immutable v1.3 source is read from its published companion archive.
The live v1.4 source must differ from it only in the Tangedal--Young
page range, while retaining the requested historical and overlap prose.
"""

from __future__ import annotations

import difflib
import hashlib
import tarfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper/effective-stark-results.tex"
PDF = ROOT / "paper/effective-stark-results.pdf"
V13 = ROOT / "dist/effective-stark-results-companion-v13.tar.gz"
V13_SHA256 = "1ecca96bd388ab2cafa27c091380121db4749e41ae794c2326439adbbe87b608"
V13_TEX_SHA256 = "29d0deb1da369cbf755bfb38946597978c1408bc62f1a3b2a0e0053e9f0810d3"
MEMBER = "effective-stark-results-companion-v13/paper/effective-stark-results.tex"
OLD_RANGE = r"J.\ Number Theory \textbf{133} (2013), 1022--1045,"
NEW_RANGE = r"J.\ Number Theory \textbf{133} (2013), 1045--1061,"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def main() -> None:
    if sha256(V13) != V13_SHA256:
        raise RuntimeError("immutable v1.3 companion hash changed")
    with tarfile.open(V13, "r:gz") as archive:
        extracted = archive.extractfile(MEMBER)
        if extracted is None:
            raise RuntimeError("v1.3 manuscript source is absent")
        old_bytes = extracted.read()
    if sha256_bytes(old_bytes) != V13_TEX_SHA256:
        raise RuntimeError("immutable v1.3 manuscript hash changed")

    old = old_bytes.decode()
    new = PAPER.read_text()
    expected = old.replace(OLD_RANGE, NEW_RANGE)
    if old.count(OLD_RANGE) != 1 or new != expected:
        difference = "".join(
            difflib.unified_diff(
                old.splitlines(keepends=True),
                new.splitlines(keepends=True),
                fromfile="published-v1.3",
                tofile="staged-v1.4",
            )
        )
        raise RuntimeError(
            "v1.4 main source differs from v1.3 beyond the frozen page-range fix\n"
            + difference
        )

    required = (
        r"\paragraph{Historical scope.}",
        r"\cite{Zhao45}",
        r"\cite{Zhao78}",
        "This survey-bounded historical\nobservation plays no role in the proofs.",
        r"Tate \cite[Thm.~IV.5.4]{Tate1984}",
        "Arakawa's relative-index formula",
        r"Roblot \cite[Thms.~6.1 and~7.1]{Roblot2013}",
        NEW_RANGE,
    )
    for needle in required:
        if needle not in new:
            raise RuntimeError(f"Track A2 text is absent: {needle}")
    if OLD_RANGE in new:
        raise RuntimeError("superseded Tangedal--Young page range remains")

    print(f"A2_TEX_SHA256={sha256(PAPER)}")
    print(f"A2_PDF_SHA256={sha256(PDF)}")
    print("RESULTS_PAPER_TRACK_A2_AUDIT=PASS")


if __name__ == "__main__":
    main()
