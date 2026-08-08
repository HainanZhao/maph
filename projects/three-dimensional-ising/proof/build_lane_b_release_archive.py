#!/usr/bin/env python3
"""Build deterministic Lane B manuscript and proof-release files."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
from pathlib import Path
import shutil
import tarfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper/canonical-spin-structure-compression"
PREFIX = "lane-b-separator-compression-2026-08"
PDF_NAME = "00_separator-compression-cubic-lattice-ising-strips.pdf"
SOURCE_NAME = "01_manuscript-source.zip"
ARCHIVE_NAME = "02_proof-replay-archive.tar.gz"
CHECKSUM_NAME = "03_SHA256SUMS.txt"

EXCLUDED_PARTS = {"__pycache__", ".pytest_cache"}
EXCLUDED_SUFFIXES = {".aux", ".bbl", ".blg", ".log", ".out", ".toc", ".pyc"}
EXCLUDED_NAMES = {"main.pdf", "failure-ledger-supplement.pdf"}
TOP_FILES = ("GOAL.md", "LANE_B_GOAL.md", "PROGRAM.md", "README.md", "requirements.txt")
TREES = ("artifacts", "discovery", "docs", "proof", "src", "tests", "paper")
SOURCE_FILES = (
    "README.md",
    "main.tex",
    "references.bib",
    "encoder-incidence-firewall.tex",
    "polynomial-core-firewall.tex",
    "width4-normal-base-trace.tex",
    "width4-base-trace.tex",
    "failure-ledger-supplement.tex",
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def included_files() -> list[tuple[str, bytes]]:
    result: list[tuple[str, bytes]] = []
    for name in TOP_FILES:
        path = ROOT / name
        result.append((name, path.read_bytes()))
    for tree in TREES:
        base = ROOT / tree
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(ROOT)
            if any(part in EXCLUDED_PARTS for part in relative.parts):
                continue
            if path.suffix in EXCLUDED_SUFFIXES or path.name in EXCLUDED_NAMES:
                continue
            result.append((relative.as_posix(), path.read_bytes()))
    names = [name for name, _ in result]
    if len(names) != len(set(names)):
        raise RuntimeError("release archive contains duplicate paths")
    return sorted(result)


def manifest(files: list[tuple[str, bytes]]) -> bytes:
    return "".join(f"{sha256_bytes(data)}  {name}\n" for name, data in files).encode()


def build_tar(files: list[tuple[str, bytes]]) -> bytes:
    all_files = files + [("MANIFEST.sha256", manifest(files))]
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w", format=tarfile.PAX_FORMAT) as archive:
        for name, data in sorted(all_files):
            info = tarfile.TarInfo(f"{PREFIX}/{name}")
            info.size = len(data)
            info.mtime = 0
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.mode = 0o755 if name.endswith((".py", ".sh")) else 0o644
            archive.addfile(info, io.BytesIO(data))
    compressed = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=compressed, mtime=0, compresslevel=9) as handle:
        handle.write(raw.getvalue())
    return compressed.getvalue()


def build_source_zip() -> bytes:
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in SOURCE_FILES:
            path = PAPER / name
            if not path.is_file():
                raise RuntimeError(f"missing manuscript source: {name}")
            info = zipfile.ZipInfo(f"canonical-spin-structure-compression/{name}")
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, path.read_bytes())
    return stream.getvalue()


def write_release(output: Path) -> dict[str, str]:
    output.mkdir(parents=True, exist_ok=True)
    files = included_files()
    payloads = {
        PDF_NAME: (PAPER / "main.pdf").read_bytes(),
        SOURCE_NAME: build_source_zip(),
        ARCHIVE_NAME: build_tar(files),
    }
    for name, data in payloads.items():
        (output / name).write_bytes(data)
    checksums = "".join(f"{sha256_bytes(data)}  {name}\n" for name, data in sorted(payloads.items()))
    (output / CHECKSUM_NAME).write_text(checksums)
    payloads[CHECKSUM_NAME] = checksums.encode()
    return {name: sha256_bytes(data) for name, data in sorted(payloads.items())}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    checksums = write_release(args.output_dir.resolve())
    for name, digest in checksums.items():
        print(f"{digest}  {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
