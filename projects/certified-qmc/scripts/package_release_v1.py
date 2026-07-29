#!/usr/bin/env python3
"""Create deterministic source and table archives for release v1.0."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
FIDELITY_AUDIT = (
    ROOT / "certificates" / "cycles-016-017-production-audit.json"
)
USABILITY_AUDIT = (
    ROOT / "certificates" / "cycle-018-usability-audit.json"
)
PRIME_SCHEDULE = ROOT / "data" / "primes-schedule-v1.json"
PRIME_MANIFEST = (
    ROOT / "certificates" / "cycle-014-prime-schedule-manifest.json"
)
ENGINE_ORACLE = ROOT / "certificates" / "engine-oracle-set-v1.json"
ENGINE_ORACLE_PREREG = ROOT / "data" / "engine-oracle-set-v1.json"
PACKAGING_PREFLIGHT = (
    ROOT / "certificates" / "cycle-018-packaging-preflight.json"
)


def digest(path: Path) -> str:
    block = bytearray(1024 * 1024)
    view = memoryview(block)
    hasher = sha256()
    with path.open("rb", buffering=0) as stream:
        while count := stream.readinto(view):
            hasher.update(view[:count])
    return hasher.hexdigest()


def canonical_sha(value: object) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
    ).hexdigest()


def load_self_hashed(path: Path, field: str) -> dict:
    value = json.loads(path.read_text())
    supplied = value.pop(field)
    if canonical_sha(value) != supplied:
        raise ValueError(f"{path.name} self-hash mismatch")
    value[field] = supplied
    return value


def checked_audit(path: Path, gate: str) -> dict:
    value = load_self_hashed(path, "certificate_sha256")
    if value["gate"].get(gate) is not True:
        raise ValueError(f"{path.name} release gate is not passed")
    return value


def run_archive(command: list[str], destination: Path) -> None:
    with destination.open("wb") as output:
        tar = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            cwd=REPO,
        )
        assert tar.stdout is not None
        compressed = subprocess.run(
            ["zstd", "-19", "--single-thread", "-q", "-c"],
            stdin=tar.stdout,
            stdout=output,
            check=True,
        )
        tar.stdout.close()
        return_code = tar.wait()
        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, command)
        if compressed.returncode != 0:
            raise RuntimeError("zstd compression failed")


def git_commit_timestamp(revision: str) -> str:
    return subprocess.check_output(
        ["git", "show", "-s", "--format=%cI", revision],
        cwd=REPO,
        text=True,
    ).strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fidelity", type=Path, required=True)
    parser.add_argument("--usability", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--revision", default="certified-qmc-v1.0"
    )
    args = parser.parse_args()
    fidelity = args.fidelity.resolve()
    usability = args.usability.resolve()
    output = args.output.resolve()

    checked_audit(
        FIDELITY_AUDIT, "cycles_016_017_exit_gate_passed"
    )
    checked_audit(
        USABILITY_AUDIT, "cycle_018_data_gate_passed"
    )
    oracle = load_self_hashed(ENGINE_ORACLE, "oracle_sha256")
    if oracle["claim_tag"] != "VERIFIED" or oracle["counts"]["total"] != 298:
        raise ValueError("engine oracle release gate is not passed")
    packaging_preflight = checked_audit(
        PACKAGING_PREFLIGHT,
        "cycle_018_packaging_preflight_passed",
    )
    if (
        packaging_preflight["implementation"][
            "scripts/package_release_v1.py"
        ]
        != digest(Path(__file__))
    ):
        raise ValueError(
            "packaging preflight does not bind this release packager"
        )
    if not (fidelity / "dataset-sha256.json").is_file():
        raise ValueError("fidelity SHA manifest is absent")
    if not (usability / "manifest.jsonl").is_file():
        raise ValueError("usability dataset is absent")
    if subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=REPO, text=True
    ).strip():
        raise ValueError("release packaging requires a clean worktree")
    revision = subprocess.check_output(
        ["git", "rev-parse", "--verify", args.revision],
        cwd=REPO,
        text=True,
    ).strip()
    revision_timestamp = git_commit_timestamp(revision)

    if output.exists():
        raise ValueError("release output already exists")
    output.mkdir(parents=True)
    source_archive = output / "certified-qmc-v1.0-source.tar.zst"
    fidelity_archive = output / "certified-qmc-v1.0-fidelity.tar.zst"
    usability_archive = (
        output / "certified-qmc-v1.0-usability.tar.zst"
    )
    oracle_archive = output / "certified-qmc-v1.0-engine-oracle.tar.zst"

    run_archive(
        [
            "git",
            "archive",
            "--format=tar",
            f"--mtime={revision_timestamp}",
            "--prefix=certified-qmc-v1.0/source/",
            f"{revision}:projects/certified-qmc",
        ],
        source_archive,
    )
    for dataset, destination, prefix in (
        (fidelity, fidelity_archive, "tables/fidelity-v2"),
        (usability, usability_archive, "tables/usability-v1"),
    ):
        run_archive(
            [
                "tar",
                "--sort=name",
                "--mtime=@0",
                "--owner=0",
                "--group=0",
                "--numeric-owner",
                "--transform",
                f"s,^,{prefix}/,",
                "-C",
                str(dataset),
                "-cf",
                "-",
                ".",
            ],
            destination,
        )
    run_archive(
        [
            "tar",
            "--sort=name",
            "--mtime=@0",
            "--owner=0",
            "--group=0",
            "--numeric-owner",
            "--transform",
            "s,^,oracle/,",
            "-C",
            str(ROOT),
            "-cf",
            "-",
            str(ENGINE_ORACLE.relative_to(ROOT)),
            str(ENGINE_ORACLE_PREREG.relative_to(ROOT)),
        ],
        oracle_archive,
    )

    assets = []
    for path, role, license_id in (
        (source_archive, "source", "Apache-2.0"),
        (
            oracle_archive,
            "engine conformance oracle",
            "CC-BY-4.0",
        ),
        (
            fidelity_archive,
            "supplementary fidelity tables",
            "CC-BY-4.0",
        ),
        (
            usability_archive,
            "supplementary usability tables",
            "CC-BY-4.0",
        ),
    ):
        assets.append(
            {
                "filename": path.name,
                "role": role,
                "license": license_id,
                "bytes": path.stat().st_size,
                "sha256": digest(path),
            }
        )
    ancillary_sources = (
        (ROOT / "LICENSE", output / "LICENSE"),
        (ROOT / "LICENSE-DATA", output / "LICENSE-DATA"),
        (ROOT / "REPRODUCING.md", output / "REPRODUCING.md"),
    )
    for source, destination in ancillary_sources:
        shutil.copy2(source, destination)
    ancillary_files = [
        {
            "filename": destination.name,
            "bytes": destination.stat().st_size,
            "sha256": digest(destination),
        }
        for _, destination in ancillary_sources
    ]
    manifest = {
        "schema": "certified-qmc-release-v1.0-manifest",
        "version": "1.0",
        "git_revision": revision,
        "source_vectors_embedded": False,
        "licenses": {
            "code": "Apache-2.0",
            "project_authored_data": "CC-BY-4.0",
        },
        "prime_schedule_sha256": digest(PRIME_SCHEDULE),
        "prime_verification_manifest_sha256": digest(
            PRIME_MANIFEST
        ),
        "fidelity_audit_sha256": digest(FIDELITY_AUDIT),
        "usability_audit_sha256": digest(USABILITY_AUDIT),
        "engine_oracle_sha256": digest(ENGINE_ORACLE),
        "engine_oracle_self_hash": oracle["oracle_sha256"],
        "packaging_preflight_sha256": digest(PACKAGING_PREFLIGHT),
        "packaging_preflight_self_hash": packaging_preflight[
            "certificate_sha256"
        ],
        "assets": assets,
        "ancillary_files": ancillary_files,
        "doi": None,
        "announcement_permitted": False,
        "boundary": (
            "The DOI and announcement flag are filled only from the "
            "confirmed external deposition response."
        ),
    }
    manifest["manifest_sha256"] = canonical_sha(manifest)
    (output / "release-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    )
    print(output)


if __name__ == "__main__":
    main()
