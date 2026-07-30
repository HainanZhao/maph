#!/usr/bin/env python3
"""Build a deterministic public companion archive for the results paper."""

from __future__ import annotations

import gzip
import hashlib
import io
import json
import shutil
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "v10"
NAME = f"effective-stark-results-companion-{VERSION}"
DIST = ROOT / "dist"
ARCHIVE = DIST / f"{NAME}.tar.gz"
FREEZE = ROOT / "artifacts/results-paper-companion-local-freeze-v10.json"

SEEDS = {
    "paper/effective-stark-results.tex",
    "paper/effective-stark-results.pdf",
    "paper/effective-stark-results-supplement.tex",
    "paper/effective-stark-results-supplement.pdf",
    "companion/README.md",
    "companion/ENVIRONMENT.md",
    "companion/EXPECTED_OUTPUT.txt",
    "requirements-dev.txt",
    "scripts/verify_results_companion.py",
    "scripts/build_results_companion.py",
    "scripts/audit_results_paper_full.py",
    "scripts/audit_engine_a_euler_degeneracy.py",
    "scripts/audit_engine_c_fourier_convention.py",
    "scripts/screen_engine_a_euler_degeneracy.gp",
    "scripts/certify_engine_b_archimedean_places.gp",
    "scripts/correct_engine_c_e6_primitive_packets.py",
    "scripts/run_engine_c_packet_bridge.py",
    "scripts/generic_engine_c_packet_bridge.gp",
    "data/engine-a-uniform-theorem-v1.json",
    "data/engine-c-general-e-theory-v4.json",
    "data/q7-p7-case-v1.json",
    "data/q14-p7-case-v1.json",
    "data/rq000108-case-v1.json",
    "data/rq000021-case-v1.json",
    "data/q57-norm27-case-v1.json",
    "data/rq002955-case-v1.json",
    "data/q33-p11-order10-case-v1.json",
    "data/rq000458-dual-case-v1.json",
    "data/q6-norm8-case-v3.json",
    "data/engine-c-e6-tranche-01-packet-bridge-v1.json",
    "data/literature-perimeter-v1.json",
    "artifacts/engine-b-archimedean-place-audit-v1.json",
    "artifacts/engine-a-euler-degeneracy-v1.json",
    "artifacts/engine-a-euler-degeneracy-v1.transcript",
    "artifacts/engine-c-fourier-convention-correction-v1.json",
    "artifacts/engine-c-claim-scope-correction-v1.json",
    "artifacts/engine-c-e6-primitive-packet-correction-v1.json",
    "artifacts/engine-c-e6-primitive-packet-correction-v1.transcript",
    "artifacts/engine-c-e6-tranche-01-unit-orbits-v1.json",
    "artifacts/engine-c-w3-tranche-01-verified-v1.json",
    "artifacts/results-paper-index-parity-lemma-v1.json",
    "artifacts/results-paper-odd-index-parity-audit-v1.json",
    "artifacts/results-paper-full-referee-audit-v2.json",
    "artifacts/shintani-1978-source-map-v1.json",
}

GLOBS = (
    "artifacts/q7-p7-*",
    "artifacts/q14-p7-*",
    "artifacts/rq000108-*",
    "artifacts/rq000021-*",
    "artifacts/rq57-norm27-*",
    "artifacts/rq002955-*",
    "artifacts/rq001107-*",
    "artifacts/rq000458-engine-b-*",
    "artifacts/engine-c-character-selection-v1.*",
    "artifacts/engine-c-packet-bridge-v1.*",
    "artifacts/engine-c-packet-root-reality-v1.json",
    "artifacts/engine-c-theta-targets-v1.*",
    "artifacts/engine-c-unit-orbits-v1.*",
    "artifacts/engine-c-w3-tranche-01-boundary-v1.json",
    "artifacts/engine-c-e6-tranche-01-selection-v1.*",
    "artifacts/engine-c-e6-tranche-01-theta-v1.*",
    "artifacts/engine-c-e6-tranche-01-unit-orbits-v1.*",
    "artifacts/engine-c-e6-tranche-01-packet-bridge-v1.*",
    "scripts/q7_p7_*",
    "scripts/q14_p7_*",
    "scripts/rq000108_*",
    "scripts/rq000021_*",
    "scripts/rq57_norm27_*",
    "scripts/rq002955_*",
    "scripts/rq001107_*",
    "scripts/certify_q7_p7_packet.py",
    "scripts/certify_q14_p7_packet.py",
    "scripts/certify_rq000108_packet.py",
    "scripts/certify_rq000021_packet.py",
    "scripts/certify_rq57_norm27_packet.py",
    "scripts/certify_rq002955_packet.py",
    "scripts/certify_rq001107_packet.py",
)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def existing(relative: str) -> bool:
    path = ROOT / relative
    return path.is_file() and "__pycache__" not in path.parts


def referenced_paths(payload: object) -> set[str]:
    found: set[str] = set()
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key in {"path", "artifact", "script", "transcript"}:
                if isinstance(value, str) and existing(value):
                    found.add(value)
            if key == "source_hashes" and isinstance(value, dict):
                found.update(path for path in value if existing(path))
            found.update(referenced_paths(value))
    elif isinstance(payload, list):
        for value in payload:
            found.update(referenced_paths(value))
    return found


def collect() -> list[str]:
    files = set(SEEDS)
    for pattern in GLOBS:
        files.update(
            str(path.relative_to(ROOT))
            for path in ROOT.glob(pattern)
            if path.is_file() and "failed" not in path.name
        )
    changed = True
    while changed:
        changed = False
        for relative in tuple(files):
            path = ROOT / relative
            if not path.is_file():
                raise FileNotFoundError(relative)
            if path.suffix != ".json":
                continue
            try:
                additions = referenced_paths(json.loads(path.read_text()))
            except json.JSONDecodeError:
                continue
            before = len(files)
            files.update(additions)
            changed |= len(files) != before
    return sorted(files)


def write_manifest(tree: Path, files: list[str]) -> None:
    lines = [
        f"{sha(tree / relative)}  {relative}"
        for relative in files
    ]
    (tree / "MANIFEST.sha256").write_text("\n".join(lines) + "\n")


def tar_bytes(tree: Path, files: list[str]) -> bytes:
    output = io.BytesIO()
    with tarfile.open(fileobj=output, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for relative in [*files, "MANIFEST.sha256"]:
            source = tree / relative
            info = tar.gettarinfo(str(source), arcname=f"{NAME}/{relative}")
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.mtime = 0
            info.mode = 0o755 if relative.startswith("scripts/") else 0o644
            with source.open("rb") as handle:
                tar.addfile(info, handle)
    compressed = io.BytesIO()
    with gzip.GzipFile(
        filename="",
        mode="wb",
        fileobj=compressed,
        compresslevel=9,
        mtime=0,
    ) as gz:
        gz.write(output.getvalue())
    return compressed.getvalue()


def main() -> None:
    files = collect()
    with tempfile.TemporaryDirectory(prefix="stark-companion-") as temporary:
        tree = Path(temporary)
        for relative in files:
            target = tree / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        write_manifest(tree, files)
        payload = tar_bytes(tree, files)

    DIST.mkdir(exist_ok=True)
    if ARCHIVE.exists() and ARCHIVE.read_bytes() != payload:
        raise RuntimeError(
            f"{ARCHIVE} already exists with different bytes; bump VERSION"
        )
    ARCHIVE.write_bytes(payload)
    archive_sha = sha(ARCHIVE)
    freeze = {
        "schema": f"effective-stark-results-companion-local-freeze-{VERSION}",
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "LOCAL_FROZEN_NOT_PUBLIC",
        "archive": str(ARCHIVE.relative_to(ROOT)),
        "archive_sha256": archive_sha,
        "archive_bytes": ARCHIVE.stat().st_size,
        "file_count_excluding_manifest": len(files),
        "paper_tex_sha256": sha(ROOT / "paper/effective-stark-results.tex"),
        "paper_pdf_sha256": sha(ROOT / "paper/effective-stark-results.pdf"),
        "public_identifier": None,
        "publication_action_taken": False,
    }
    if FREEZE.exists():
        previous = json.loads(FREEZE.read_text())
        stable_keys = (
            "status",
            "archive",
            "archive_sha256",
            "archive_bytes",
            "file_count_excluding_manifest",
            "paper_tex_sha256",
            "paper_pdf_sha256",
            "public_identifier",
            "publication_action_taken",
        )
        if all(previous.get(key) == freeze.get(key) for key in stable_keys):
            freeze = previous
        else:
            raise RuntimeError(
                f"{FREEZE} already exists for a different source state; "
                "bump VERSION"
            )
    else:
        FREEZE.write_text(json.dumps(freeze, indent=2, sort_keys=True) + "\n")
    print(f"COMPANION_FILE_COUNT={len(files)}")
    print(f"COMPANION_ARCHIVE_SHA256={archive_sha}")
    print("COMPANION_LOCAL_FREEZE=PASS")


if __name__ == "__main__":
    main()
