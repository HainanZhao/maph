#!/usr/bin/env python3
"""Verify an extracted final pre-DOI v1.4 correction companion."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tarfile
import tempfile
from pathlib import Path


BASE_V15_SHA256 = "3a4950c7df0b5634c60996bd636df8192361ff2cfea6ff90fb01f3ffdfe5ff72"
ENGINE_C_V2_SHA256 = "edff581634c0e2abe3c6a50539e61ac1baca38f0ab1c96a956b89b8c92efe888"
REFEREE_V3_SHA256 = "90d1c4e75cdaa080e8939f57e6496b572ac20c94e5ecf2693fd243385281d3db"


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
        "effective-stark-results-companion-v15.tar.gz"
    )
    if sha256(archive) != BASE_V15_SHA256:
        raise RuntimeError("immutable v15 successor hash changed")
    with tempfile.TemporaryDirectory(prefix="stark-v15-check-") as temporary:
        target = Path(temporary)
        with tarfile.open(archive, "r:gz") as tar:
            tar.extractall(target, filter="data")
        base = target / "effective-stark-results-companion-v15"
        completed = subprocess.run(
            [
                "python3",
                str(
                    base
                    / "projects/effective-stark-sweep/scripts/"
                    "verify_results_companion_v15.py"
                ),
                str(base),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode or "RESULTS_COMPANION_V15=VERIFIED" not in completed.stdout:
            raise RuntimeError(
                f"nested v15 replay failed\n{completed.stdout}{completed.stderr}"
            )


def verify_successors(root: Path) -> None:
    project = root / "projects/effective-stark-sweep"
    engine_c_path = (
        project / "artifacts/engine-c-fourier-convention-correction-v2.json"
    )
    referee_path = project / "artifacts/results-paper-referee-audit-v3.json"
    if sha256(engine_c_path) != ENGINE_C_V2_SHA256:
        raise RuntimeError("Engine-C v2 re-audit hash changed")
    if sha256(referee_path) != REFEREE_V3_SHA256:
        raise RuntimeError("full referee v3 audit hash changed")
    engine_c = json.loads(engine_c_path.read_text())
    referee = json.loads(referee_path.read_text())
    if (
        engine_c["claim_tag"] != "VERIFIED_EXACT_CONVENTION_REAUDIT"
        or engine_c["verdict"] != "PASS"
        or not engine_c["mathematical_convention_unchanged_from_v1"]
    ):
        raise RuntimeError("Engine-C v2 gate failed")
    if (
        referee["claim_tag"] != "VERIFIED_V1_4_PREPUBLICATION_AUDIT"
        or referee["engine_c"]["fourier_convention"] != "PASS"
        or referee["structural_lemmas"] != "PASS"
    ):
        raise RuntimeError("full referee v3 gate failed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive_root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.archive_root).resolve()
    verify_manifest(root)
    verify_base(root)
    verify_successors(root)
    print("RESULTS_COMPANION_V16=VERIFIED")


if __name__ == "__main__":
    main()
