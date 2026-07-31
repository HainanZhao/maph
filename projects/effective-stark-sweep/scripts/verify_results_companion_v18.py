#!/usr/bin/env python3
"""Verify an extracted DOI-bearing v1.5 release companion."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile


BASE_V17_SHA256 = (
    "e2a945edaddcec32e3aad10e67f8b960af0bc304b07ba5503ab7be62384b9506"
)
EXPECTED = {
    "paper/effective-stark-results.tex":
        "ed273d87b90dd2539a948b654ba3e6d98d211e276ccb87bc4684fd1d53caf7b9",
    "paper/effective-stark-results.pdf":
        "e0145fca96404ac1a82408e8744ce3acba7e2cc74608e6a8bca6adc7b756c54d",
    "paper/effective-stark-results-supplement.tex":
        "f0c0ed6c9834192a4e4f90a53c64b34c72448fb03a512b5b90eaa1957ff838d7",
    "paper/effective-stark-results-supplement.pdf":
        "7f98aa6b768f4b8b0122f708c11480f2daf6d7e64c2608f3593119c189c60b25",
    "artifacts/zenodo-results-record-metadata-v8.json":
        "c90726e332639bace9098a7266859a65d864c443923c54f2776a7d8a86a20139",
    "artifacts/zenodo-results-v1.5-draft-reservation-v1.json":
        "abcdc9a45b195ecc55fbb76b628e7e9a2f19d82836282a096d6070a1128cb9f0",
    "artifacts/results-paper-v1.5-integration-audit-v1.json":
        "8ee209b91ca9d4ee5826d77c56272837a3cadbee91f6582812e0c1d415e8ef7f",
    "companion/CORRECTION-V1.5-MAIN-PAPER-INTEGRATION.md":
        "7f710972894487937e6c9ec06a6c168770e0b2ab7fd452fda35d1ca8ea4fb893",
}
DOI = "10.5281/zenodo.21713178"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest(root: Path) -> None:
    for line in (root / "MANIFEST.sha256").read_text().splitlines():
        expected, relative = line.split("  ", 1)
        if sha256(root / relative) != expected:
            raise RuntimeError(f"manifest mismatch: {relative}")


def verify_base(root: Path) -> None:
    archive = (
        root
        / "projects/effective-stark-sweep/dist/"
        "effective-stark-results-companion-v17.tar.gz"
    )
    if sha256(archive) != BASE_V17_SHA256:
        raise RuntimeError("immutable published v1.4 companion changed")
    with tempfile.TemporaryDirectory(prefix="stark-v17-check-") as temporary:
        target = Path(temporary)
        with tarfile.open(archive, "r:gz") as tar:
            tar.extractall(target, filter="data")
        base = target / "effective-stark-results-companion-v17"
        completed = subprocess.run(
            [
                "python3",
                str(
                    base
                    / "projects/effective-stark-sweep/scripts/"
                    "verify_results_companion_v17.py"
                ),
                str(base),
            ],
            text=True,
            capture_output=True,
            check=False,
            timeout=600,
        )
        if (
            completed.returncode
            or "RESULTS_COMPANION_V17=VERIFIED" not in completed.stdout
        ):
            raise RuntimeError(
                f"nested v17 replay failed\n{completed.stdout}{completed.stderr}"
            )


def verify_release(root: Path) -> None:
    project = root / "projects/effective-stark-sweep"
    for relative, expected in EXPECTED.items():
        if sha256(project / relative) != expected:
            raise RuntimeError(f"v1.5 release hash changed: {relative}")
    for relative in (
        "paper/effective-stark-results.tex",
        "paper/effective-stark-results-supplement.tex",
        "artifacts/zenodo-results-record-metadata-v8.json",
        "companion/CORRECTION-V1.5-MAIN-PAPER-INTEGRATION.md",
    ):
        if DOI not in (project / relative).read_text():
            raise RuntimeError(f"reserved DOI absent from {relative}")

    reservation = json.loads(
        (
            project
            / "artifacts/zenodo-results-v1.5-draft-reservation-v1.json"
        ).read_text()
    )
    audit = json.loads(
        (
            project
            / "artifacts/results-paper-v1.5-integration-audit-v1.json"
        ).read_text()
    )
    if (
        reservation["status"] != "DOI_RESERVED_UNPUBLISHED"
        or reservation["mutation"]["publication_action_taken"]
    ):
        raise RuntimeError("Zenodo v1.5 reservation boundary changed")
    if (
        audit["status"] != "PASS_MAIN_INTEGRATION_AND_EXACT_REPLAY"
        or audit["checks"]["publication_action_taken"]
        or audit["checks"]["standalone_addendum_authorized_for_v15_top_level"]
    ):
        raise RuntimeError("v1.5 integration audit failed")

    members = {
        path.relative_to(project).as_posix()
        for path in project.rglob("*")
        if path.is_file()
    }
    if any(
        "supplement-rq000013-addendum" in member
        for member in members
        if not member.startswith("dist/")
    ):
        raise RuntimeError("standalone addendum leaked into v1.5 archive")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive_root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.archive_root).resolve()
    verify_manifest(root)
    verify_base(root)
    verify_release(root)
    print("RESULTS_COMPANION_V18=VERIFIED")


if __name__ == "__main__":
    main()
