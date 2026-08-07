#!/usr/bin/env python3
"""Build deterministic Zenodo and arXiv release files."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path


DOI = "10.5281/zenodo.21826970"
ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper" / "qfib-width-four"
ARCHIVE_FILES = {
    "README.md": PAPER / "README.md",
    "LICENSE.md": PAPER / "LICENSE.md",
    "paper/main.pdf": PAPER / "main.pdf",
    "paper/main.tex": PAPER / "main.tex",
    "paper/references.bib": PAPER / "references.bib",
    "paper/literature-audit.md": PAPER / "literature-audit.md",
    "paper/verification.md": PAPER / "verification.md",
    "paper/build_release.py": PAPER / "build_release.py",
    "proof/qfib_width4_unimodality_proof.py": (
        ROOT / "proof" / "qfib_width4_unimodality_proof.py"
    ),
    "proof/qfib_width4_unimodality_proof.md": (
        ROOT / "proof" / "qfib_width4_unimodality_proof.md"
    ),
}
ZIP_TIMESTAMP = (2026, 8, 6, 0, 0, 0)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def zip_entry(name: str, data: bytes) -> tuple[zipfile.ZipInfo, bytes]:
    info = zipfile.ZipInfo(name, ZIP_TIMESTAMP)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = (0o755 if name.endswith(".py") else 0o644) << 16
    return info, data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    contents = {name: path.read_bytes() for name, path in ARCHIVE_FILES.items()}
    assert DOI.encode() in contents["paper/main.tex"]
    assert DOI.encode() in contents["README.md"]
    manifest = {
        "claim": "[m+4 choose 4]_F is unimodal for every integer m >= 1",
        "doi": DOI,
        "files": {
            name: {"bytes": len(data), "sha256": sha256(data)}
            for name, data in sorted(contents.items())
        },
        "schema": "qfib-width-four-release-v1",
    }
    manifest_data = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()

    pdf_target = args.output / "01-width-four-q-fibonomial-paper.pdf"
    tex_target = args.output / "02-width-four-q-fibonomial-source.tex"
    zip_target = args.output / "03-width-four-q-fibonomial-replay.zip"
    shutil.copyfile(PAPER / "main.pdf", pdf_target)
    shutil.copyfile(PAPER / "main.tex", tex_target)
    with zipfile.ZipFile(zip_target, "w", compresslevel=9) as archive:
        for name, data in sorted(contents.items()):
            info, payload = zip_entry(name, data)
            archive.writestr(info, payload)
        info, payload = zip_entry("MANIFEST.json", manifest_data)
        archive.writestr(info, payload)

    result = {
        path.name: {"bytes": path.stat().st_size, "sha256": sha256(path.read_bytes())}
        for path in (pdf_target, tex_target, zip_target)
    }
    (args.output / "release-checksums.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
