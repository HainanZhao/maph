#!/usr/bin/env python3
"""Verify an extracted Effective-Stark results companion v1.4 layer."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tarfile
import tempfile
from pathlib import Path


BASE_V13_SHA256 = "1ecca96bd388ab2cafa27c091380121db4749e41ae794c2326439adbbe87b608"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(root: Path, relative: str) -> dict:
    return json.loads((root / relative).read_text())


def verify_manifest(root: Path) -> None:
    for line in (root / "MANIFEST.sha256").read_text().splitlines():
        expected, relative = line.split("  ", 1)
        actual = sha256(root / relative)
        if actual != expected:
            raise RuntimeError(f"manifest mismatch: {relative}")


def verify_base(root: Path) -> None:
    archive = (
        root
        / "projects/effective-stark-sweep/dist/"
        "effective-stark-results-companion-v13.tar.gz"
    )
    if sha256(archive) != BASE_V13_SHA256:
        raise RuntimeError("immutable v13 companion hash changed")
    with tempfile.TemporaryDirectory(prefix="stark-v13-check-") as temporary:
        target = Path(temporary)
        with tarfile.open(archive, "r:gz") as tar:
            tar.extractall(target, filter="data")
        base = target / "effective-stark-results-companion-v13"
        verify_manifest(base)


def verify_corrections(root: Path) -> None:
    circularity = load(
        root,
        "projects/dedekind-stark-phase/artifacts/circularity-audit-v1.json",
    )
    if circularity["claim_tag"] != "CONTAINED_ORIENTATION_CIRCULARITY":
        raise RuntimeError("withdrawn-replay correction tag changed")
    gates = circularity["gates"]
    if (
        gates["weak_unit_sealed_before_lprime"] != "PASS"
        or gates["dominant_gauge_data_independent"] != "PASS"
        or gates["character_orientation_data_independent"] != "FAIL"
        or gates["artin_transport_replay_present"] != "FAIL"
    ):
        raise RuntimeError("circularity gate record changed")

    quartic = load(
        root,
        "projects/dedekind-stark-phase/artifacts/"
        "roblot-quartic-gate-sealed-v1.json",
    )
    expected = {
        "RQ-000129",
        "RQ-001280",
        "RQ-001569",
        "RQ-001894",
        "RQ-007519",
    }
    if {row["case_id"] for row in quartic["screen"]} != expected:
        raise RuntimeError("five-case Roblot population changed")
    if not all(
        row["A1"] and row["A2"] and row["A3"]
        for row in quartic["screen"]
    ):
        raise RuntimeError("a five-case Roblot hypothesis failed")

    phase = load(
        root,
        "projects/dedekind-stark-phase/artifacts/all-five-phase-gates-v1.json",
    )
    if (
        phase["claim_tag"]
        != "NUMERICAL_PHASE_MATCH_WITH_CERTIFIED_LPRIME_BALLS"
        or phase["case_count"] != 5
    ):
        raise RuntimeError("retained numerical phase record changed")


def verify_rq000013(root: Path) -> None:
    project = root / "projects/effective-stark-sweep"
    record = json.loads(
        (
            project
            / "artifacts/rq000013-engine-a-imprimitive-certificate-v1.json"
        ).read_text()
    )
    result = record["exact_result"]
    if (
        result["E_chi"] != 2
        or result["I_chi"] != 2
        or result["packet_power_identity"]
        != "X_[0]=u^2; X_[1]=u^(-2)"
    ):
        raise RuntimeError("RQ-000013 exact result changed")
    completed = subprocess.run(
        ["gp", "-fq", "scripts/certify_rq000013_engine_a.gp"],
        cwd=project,
        text=True,
        capture_output=True,
        check=False,
    )
    if (
        completed.returncode
        or "RQ000013_ENGINE_A_CERTIFIED=1" not in completed.stdout
    ):
        raise RuntimeError(
            f"RQ-000013 GP replay failed\n{completed.stdout}{completed.stderr}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "archive_root",
        nargs="?",
        default=".",
        help="extracted effective-stark-results-companion-v14 directory",
    )
    args = parser.parse_args()
    root = Path(args.archive_root).resolve()
    verify_manifest(root)
    verify_base(root)
    verify_corrections(root)
    verify_rq000013(root)
    print("RESULTS_COMPANION_V14=VERIFIED")


if __name__ == "__main__":
    main()
