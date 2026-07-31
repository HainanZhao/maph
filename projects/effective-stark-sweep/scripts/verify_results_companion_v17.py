#!/usr/bin/env python3
"""Verify an extracted DOI-bearing v1.4 release companion."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tarfile
import tempfile
from pathlib import Path


BASE_V16_SHA256 = "9e4169375bf862f3d934d7dba0e2dff1c40de54bcecafb59beb3695027415b73"
EXPECTED = {
    "paper/effective-stark-results.tex":
        "22479df93285670166b435bc8302a36bbdd9f644384c114cdf1b885533c1d378",
    "paper/effective-stark-results.pdf":
        "3214bd8797179d09204872fcb881b7d84fd20277cde667907a0843cf2a75af29",
    "paper/effective-stark-results-supplement.tex":
        "6becd0f6b4f3efbc95f5b8921560a768786944cc4721752e3b65e75697bfa72d",
    "paper/effective-stark-results-supplement.pdf":
        "919388eca0966dcdebe34848979e98204923e9f2611621959960ab45dbf787ac",
    "paper/effective-stark-results-supplement-rq000013-addendum.tex":
        "db596c23c60a3410e57d3484c10300647b749142b7ad3c95918b3f5e0776da9b",
    "paper/effective-stark-results-supplement-rq000013-addendum.pdf":
        "be5ad90928c8a2f0cf602fd5a90f38e0ab6a808a370a553872662fd951f315b2",
    "artifacts/zenodo-results-record-metadata-v7.json":
        "e4a305af1a0647afc64c937765e4432bb6466473261980d1d151bc7a48e0af70",
    "artifacts/zenodo-results-v1.4-draft-reservation-v1.json":
        "42a770840a6456f1cfe03a36718aa46a20204dae0bd2ba6c31bf4fb126b365b1",
    "artifacts/engine-c-fourier-convention-correction-v3.json":
        "651f039c178c47b3ca683d6d7a9e8c3660747cb8e8c1b33c5e4a875626ea3731",
    "artifacts/results-paper-referee-audit-v4.json":
        "46310a37ba500de4501d33db77811284c42d2adb63398ae9fa9fa46beba1b2d4",
    "artifacts/results-paper-release-doi-audit-v1.json":
        "3a143ad903955e4614e907ca33004fe2922fae878677b15a4dbfde9c99b5319d",
}
DOI = "10.5281/zenodo.21712478"


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
        "effective-stark-results-companion-v16.tar.gz"
    )
    if sha256(archive) != BASE_V16_SHA256:
        raise RuntimeError("immutable pre-DOI v16 hash changed")
    with tempfile.TemporaryDirectory(prefix="stark-v16-check-") as temporary:
        target = Path(temporary)
        with tarfile.open(archive, "r:gz") as tar:
            tar.extractall(target, filter="data")
        base = target / "effective-stark-results-companion-v16"
        completed = subprocess.run(
            [
                "python3",
                str(
                    base
                    / "projects/effective-stark-sweep/scripts/"
                    "verify_results_companion_v16.py"
                ),
                str(base),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode or "RESULTS_COMPANION_V16=VERIFIED" not in completed.stdout:
            raise RuntimeError(
                f"nested v16 replay failed\n{completed.stdout}{completed.stderr}"
            )


def verify_release(root: Path) -> None:
    project = root / "projects/effective-stark-sweep"
    for relative, expected in EXPECTED.items():
        if sha256(project / relative) != expected:
            raise RuntimeError(f"DOI-bearing release hash changed: {relative}")
    for relative in (
        "paper/effective-stark-results.tex",
        "paper/effective-stark-results-supplement.tex",
        "paper/effective-stark-results-supplement-rq000013-addendum.tex",
        "artifacts/zenodo-results-record-metadata-v7.json",
    ):
        if DOI not in (project / relative).read_text():
            raise RuntimeError(f"reserved DOI absent from {relative}")

    reservation = json.loads(
        (project / "artifacts/zenodo-results-v1.4-draft-reservation-v1.json").read_text()
    )
    engine_c = json.loads(
        (project / "artifacts/engine-c-fourier-convention-correction-v3.json").read_text()
    )
    referee = json.loads(
        (project / "artifacts/results-paper-referee-audit-v4.json").read_text()
    )
    release = json.loads(
        (project / "artifacts/results-paper-release-doi-audit-v1.json").read_text()
    )
    if (
        reservation["status"] != "DOI_RESERVED_UNPUBLISHED"
        or reservation["mutation"]["publication_action_taken"]
    ):
        raise RuntimeError("Zenodo reservation boundary changed")
    if (
        engine_c["claim_tag"] != "VERIFIED_EXACT_CONVENTION_DOI_REAUDIT"
        or not engine_c["mathematical_convention_unchanged_from_v2"]
    ):
        raise RuntimeError("Engine-C DOI re-audit gate failed")
    if (
        referee["claim_tag"]
        != "VERIFIED_V1_4_DOI_BEARING_PREPUBLICATION_AUDIT"
        or referee["structural_lemmas"] != "PASS"
    ):
        raise RuntimeError("full DOI-bearing referee gate failed")
    if (
        release["status"] != "PASS_EXACT_RELEASE_SOURCE_DELTA"
        or release["mathematical_claim_change_from_pre_doi_freeze"] != "NONE"
    ):
        raise RuntimeError("release-delta gate failed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive_root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.archive_root).resolve()
    verify_manifest(root)
    verify_base(root)
    verify_release(root)
    print("RESULTS_COMPANION_V17=VERIFIED")


if __name__ == "__main__":
    main()
