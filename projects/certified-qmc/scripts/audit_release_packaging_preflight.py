#!/usr/bin/env python3
"""Bank deterministic archive-plumbing checks before final packaging."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
sys.path.insert(0, str(ROOT))

from src.certificate import canonical_sha256
from src.chunked_table import file_sha256
from scripts.package_release_v1 import git_commit_timestamp, run_archive


OUTPUT = (
    ROOT / "certificates" / "cycle-018-packaging-preflight.json"
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def members(path: Path) -> list[str]:
    completed = subprocess.run(
        [
            "tar",
            "--use-compress-program=unzstd",
            "-tf",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.splitlines()


def paired(
    command: list[str],
    first: Path,
    second: Path,
) -> tuple[str, list[str]]:
    run_archive(command, first)
    run_archive(command, second)
    first_sha = file_sha256(first)
    second_sha = file_sha256(second)
    if first_sha != second_sha:
        raise ArithmeticError("archive regeneration is not byte-identical")
    first_members = members(first)
    if first_members != members(second):
        raise ArithmeticError("archive member lists differ")
    return first_sha, first_members


def main() -> None:
    with tempfile.TemporaryDirectory(
        prefix="certified-qmc-packaging-preflight-"
    ) as directory:
        temporary = Path(directory)
        dataset = temporary / "fixture"
        dataset.mkdir()
        (dataset / "manifest.jsonl").write_text(
            '{"event":"SEAL","sequence":0}\n'
        )
        chunks = dataset / "chunks"
        chunks.mkdir()
        (chunks / "p0.bin").write_bytes(bytes(range(32)))

        source_sha, source_members = paired(
            [
                "git",
                "archive",
                "--format=tar",
                f"--mtime={git_commit_timestamp('HEAD')}",
                "--prefix=certified-qmc-v1.0/source/",
                "HEAD:projects/certified-qmc",
            ],
            temporary / "source-a.tar.zst",
            temporary / "source-b.tar.zst",
        )
        table_sha, table_members = paired(
            [
                "tar",
                "--sort=name",
                "--mtime=@0",
                "--owner=0",
                "--group=0",
                "--numeric-owner",
                "--transform",
                "s,^,tables/fidelity-v2/,",
                "-C",
                str(dataset),
                "-cf",
                "-",
                ".",
            ],
            temporary / "table-a.tar.zst",
            temporary / "table-b.tar.zst",
        )
        oracle_sha, oracle_members = paired(
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
                "data/engine-oracle-set-v1.json",
                "REPRODUCING.md",
            ],
            temporary / "oracle-a.tar.zst",
            temporary / "oracle-b.tar.zst",
        )

    required_source = {
        "certified-qmc-v1.0/source/LICENSE",
        "certified-qmc-v1.0/source/LICENSE-DATA",
        "certified-qmc-v1.0/source/REPRODUCING.md",
        "certified-qmc-v1.0/source/scripts/package_release_v1.py",
        "certified-qmc-v1.0/source/scripts/verify_engine_oracle.py",
    }
    if not required_source <= set(source_members):
        raise ValueError("source archive lacks required release members")
    required_table = {
        "tables/fidelity-v2/./",
        "tables/fidelity-v2/./manifest.jsonl",
        "tables/fidelity-v2/./chunks/",
        "tables/fidelity-v2/./chunks/p0.bin",
    }
    if not required_table <= set(table_members):
        raise ValueError("table archive prefix/member contract failed")
    required_oracle = {
        "oracle/data/engine-oracle-set-v1.json",
        "oracle/REPRODUCING.md",
    }
    if not required_oracle <= set(oracle_members):
        raise ValueError("oracle archive prefix/member contract failed")

    payload = {
        "schema": "certified-qmc-cycle018-packaging-preflight-v1",
        "recorded_at_utc": utc_now(),
        "claim_tag": "VERIFIED",
        "implementation": {
            "scripts/package_release_v1.py": file_sha256(
                ROOT / "scripts" / "package_release_v1.py"
            ),
            "REPRODUCING.md": file_sha256(ROOT / "REPRODUCING.md"),
        },
        "source_archive": {
            "sha256": source_sha,
            "member_count": len(source_members),
            "required_members_present": True,
            "byte_identical_second_run": True,
        },
        "table_fixture_archive": {
            "sha256": table_sha,
            "member_count": len(table_members),
            "required_prefix_members_present": True,
            "byte_identical_second_run": True,
        },
        "oracle_fixture_archive": {
            "sha256": oracle_sha,
            "member_count": len(oracle_members),
            "required_prefix_members_present": True,
            "byte_identical_second_run": True,
        },
        "tools": {
            "git": subprocess.check_output(
                ["git", "--version"], text=True
            ).strip(),
            "tar": subprocess.check_output(
                ["tar", "--version"], text=True
            ).splitlines()[0],
            "zstd": subprocess.check_output(
                ["zstd", "--version"], text=True
            ).strip(),
        },
        "boundary": (
            "VERIFIED covers archive commands, deterministic regeneration, "
            "compression, and member prefixes on HEAD plus temporary data. "
            "Final dataset content remains gated on its production audits."
        ),
        "gate": {
            "source_archive_deterministic": True,
            "table_archive_deterministic": True,
            "oracle_archive_deterministic": True,
            "member_layout_contract_passed": True,
            "cycle_018_packaging_preflight_passed": True,
        },
    }
    payload["certificate_sha256"] = canonical_sha256(payload)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(OUTPUT)


if __name__ == "__main__":
    main()
