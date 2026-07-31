#!/usr/bin/env python3
"""Verify an extracted Track-A2 successor companion."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tarfile
import tempfile
from pathlib import Path


BASE_V14_SHA256 = "6225d7660b2b6455480fd73e412b3937438d4dbb9f2f1c68cb4d7e3ac1052648"
TEX_SHA256 = "5fd43c986c70459cfcd6a347511d780d03374527153701a4137cb6fcc85e1b93"
PDF_SHA256 = "9ad56d9ab1e2be123f5ddae709c5d9efa6fefbdad77989d33a48bca90e145d8c"


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
        "effective-stark-results-companion-v14.tar.gz"
    )
    if sha256(archive) != BASE_V14_SHA256:
        raise RuntimeError("immutable v14 correction layer hash changed")
    with tempfile.TemporaryDirectory(prefix="stark-v14-check-") as temporary:
        target = Path(temporary)
        with tarfile.open(archive, "r:gz") as tar:
            tar.extractall(target, filter="data")
        base = target / "effective-stark-results-companion-v14"
        completed = subprocess.run(
            [
                "python3",
                str(
                    base
                    / "projects/effective-stark-sweep/scripts/"
                    "verify_results_companion_v14.py"
                ),
                str(base),
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode or "RESULTS_COMPANION_V14=VERIFIED" not in completed.stdout:
            raise RuntimeError(
                f"nested v14 replay failed\n{completed.stdout}{completed.stderr}"
            )


def verify_a2(root: Path) -> None:
    project = root / "projects/effective-stark-sweep"
    tex = project / "paper/effective-stark-results.tex"
    pdf = project / "paper/effective-stark-results.pdf"
    if sha256(tex) != TEX_SHA256 or sha256(pdf) != PDF_SHA256:
        raise RuntimeError("corrected manuscript hash changed")
    text = tex.read_text()
    required = (
        r"\paragraph{Historical scope.}",
        r"\cite{Zhao45}",
        r"\cite{Zhao78}",
        r"Tate \cite[Thm.~IV.5.4]{Tate1984}",
        "Arakawa's relative-index formula",
        r"Roblot \cite[Thms.~6.1 and~7.1]{Roblot2013}",
        r"J.\ Number Theory \textbf{133} (2013), 1045--1061",
    )
    if any(needle not in text for needle in required) or "1022--1045" in text:
        raise RuntimeError("Track-A2 wording or pagination gate failed")
    record = json.loads(
        (
            project
            / "artifacts/results-paper-a2-wording-bibliography-audit-v1.json"
        ).read_text()
    )
    if record["status"] != "PASS_EXACT_EDITORIAL_CORRECTION":
        raise RuntimeError("Track-A2 audit status changed")
    if any(value != "PASS" and not value.startswith("PASS_")
           for value in record["a2_gates"].values()):
        raise RuntimeError("a Track-A2 gate is not passing")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archive_root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.archive_root).resolve()
    verify_manifest(root)
    verify_base(root)
    verify_a2(root)
    print("RESULTS_COMPANION_V15=VERIFIED")


if __name__ == "__main__":
    main()
