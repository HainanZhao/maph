#!/usr/bin/env python3
"""Verify an extracted census v1.0 companion tree."""

from __future__ import annotations

import argparse
import hashlib
import subprocess
from pathlib import Path


DOI = "10.5281/zenodo.21729947"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tree", type=Path, required=True)
    args = parser.parse_args()
    root = args.tree.resolve()
    manifest = root / "MANIFEST.sha256"
    rows = manifest.read_text().splitlines()
    for row in rows:
        expected, relative = row.split("  ", 1)
        actual = hashlib.sha256((root / relative).read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError(f"manifest mismatch: {relative}")
    for relative in (
        "paper/effective-stark-census.tex",
        "companion/CENSUS-RELEASE-V1.0.md",
        "artifacts/zenodo-census-record-metadata-v1.json",
        "artifacts/zenodo-census-v1.0-draft-reservation-v1.json",
    ):
        if DOI not in (root / relative).read_text():
            raise RuntimeError(f"DOI missing: {relative}")
    for command in (
        ["python3", "proof/audit_q_euler_deleted_prime_cover.py"],
        ["python3", "scripts/audit_census_referee_revision.py"],
        ["python3", "scripts/audit_census_paper.py"],
    ):
        subprocess.run(command, cwd=root, check=True, timeout=180)
    print(f"CENSUS_COMPANION_MANIFEST_FILES={len(rows)}")
    print("CENSUS_COMPANION_EXTRACTED_REPLAY=PASS")


if __name__ == "__main__":
    main()
