#!/usr/bin/env python3
"""Offline audit of the frozen official MIT DSpace SWORD bitstream.

The optional live check validates current REST metadata against the frozen
values.  The deterministic artifact itself uses only the frozen ZIP, PDFs,
and item metadata file; it makes no byte-identity claim about author copies.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import urllib.request
import zipfile


PROJECT = Path(__file__).resolve().parents[1]
SOURCES = PROJECT / "artifacts" / "sources"
OUTPUT = PROJECT / "artifacts" / "cycle-2-mit-sword-official-bitstream-audit-v1.json"
ZIP = SOURCES / "mit-ocw-18-785-2007-sword-official.zip"
ERROR_OFFICIAL = SOURCES / "mit-ocw-18-785-2007-errorbounds-official.pdf"
VON_OFFICIAL = SOURCES / "mit-ocw-18-785-2007-von-mangoldt-official.pdf"
ERROR_AUTHOR = SOURCES / "kedlaya-2007-errorbounds-author.pdf"
VON_AUTHOR = SOURCES / "kedlaya-2007-von-mangoldt-author.pdf"
ITEM = SOURCES / "mit-dspace-1721.1-101679-metadata.json"

BITSTREAM_ID = "7292f134-d4a7-4063-bd7e-2084259b8fa9"
BUNDLE_ID = "b4f16d16-1dc5-4da2-90bf-44165e4a568d"
ITEM_ID = "ef0f95e2-2e6c-4817-bf11-5e6285783f29"
HANDLE = "1721.1/101679"
ZIP_SHA256 = "d559229963960da2087918a95af6efd7ad8999a4ba63942a12aef63c5eceac57"
ZIP_MD5 = "12dd2876c82fa2d32242c487a1ebd2d0"
PATH_ERROR = "18-785-spring-2007/contents/lecture-notes/errorbounds.pdf"
PATH_VON = "18-785-spring-2007/contents/lecture-notes/von_mangoldt.pdf"


def digest(path: Path, algorithm: str = "sha256") -> str:
    hasher = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            hasher.update(block)
    return hasher.hexdigest()


def json_digest(value: object) -> str:
    return hashlib.sha256((json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()).hexdigest()


def text_page(pdf: Path, page: int) -> str:
    completed = subprocess.run(
        ["mutool", "draw", "-F", "txt", "-o", "-", str(pdf), str(page)],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


def page_count(pdf: Path) -> int:
    completed = subprocess.run(["mutool", "info", str(pdf)], check=True, capture_output=True, text=True)
    marker = next(line for line in completed.stdout.splitlines() if line.startswith("Pages:"))
    return int(marker.split(":", 1)[1].strip())


def values(item: dict, key: str) -> list[str]:
    return [row["value"] for row in item["metadata"].get(key, [])]


def frozen_item_audit() -> dict:
    item = json.loads(ITEM.read_text())
    assert item["id"] == item["uuid"] == ITEM_ID
    assert HANDLE in values(item, "dc.identifier.uri")[0]
    assert values(item, "dc.title") == ["18.785 Analytic Number Theory, Spring 2007"]
    assert values(item, "dc.contributor.author") == ["Kedlaya, Kiran"]
    rights = values(item, "dc.rights.uri")
    assert "Usage Restrictions: Attribution-NonCommercial-ShareAlike 3.0 Unported" in rights
    assert "http://creativecommons.org/licenses/by-nc-sa/3.0/" in rights
    return {
        "file": ITEM.name,
        "sha256": digest(ITEM),
        "item_uuid": ITEM_ID,
        "handle": HANDLE,
        "title": values(item, "dc.title")[0],
        "author": values(item, "dc.contributor.author")[0],
        "issued": values(item, "dc.date.issued")[0],
        "course_rights_metadata": rights,
        "license_interpretation_boundary": "OBSERVED item-level course metadata; this audit does not give legal advice or infer rights beyond the recorded field.",
        "epistemic_status": "OBSERVED",
    }


def zip_audit() -> dict:
    assert digest(ZIP) == ZIP_SHA256
    assert digest(ZIP, "md5") == ZIP_MD5
    with zipfile.ZipFile(ZIP) as archive:
        assert archive.testzip() is None
        assert len(archive.infolist()) == 304
        rows = []
        for internal, local in ((PATH_ERROR, ERROR_OFFICIAL), (PATH_VON, VON_OFFICIAL)):
            info = archive.getinfo(internal)
            internal_bytes = archive.read(internal)
            assert hashlib.sha256(internal_bytes).hexdigest() == digest(local)
            assert len(internal_bytes) == local.stat().st_size == info.file_size
            rows.append({
                "internal_path": internal,
                "internal_sha256": hashlib.sha256(internal_bytes).hexdigest(),
                "internal_bytes": len(internal_bytes),
                "zip_crc32_hex": f"{info.CRC:08x}",
                "compression_size": info.compress_size,
                "frozen_official_file": local.name,
                "frozen_official_sha256": digest(local),
                "exact_internal_to_frozen_official_bytes": True,
                "epistemic_status": "OBSERVED",
            })
    return {
        "file": ZIP.name,
        "bytes": ZIP.stat().st_size,
        "sha256": digest(ZIP),
        "md5_matching_dspace_bitstream_metadata": digest(ZIP, "md5"),
        "zip_integrity": "PASS: Python zipfile.testzip() returned no corrupt member",
        "entry_count": 304,
        "required_entries": rows,
        "epistemic_status": "OBSERVED",
    }


def anchor_audit() -> dict:
    error_page1 = text_page(ERROR_OFFICIAL, 1)
    von_page1 = text_page(VON_OFFICIAL, 1)
    von_page2 = text_page(VON_OFFICIAL, 2)
    for token in ("Theorem 1", "R(x, T", "distance from x"):
        assert token in error_page1
    for token in ("Theorem 1", "R(x, T"):
        assert token in von_page1
    for token in ("We now compute residues", "counted with multiplicity"):
        assert token in von_page2
    assert page_count(ERROR_OFFICIAL) == 4
    assert page_count(VON_OFFICIAL) == 6
    return {
        "tool": "mutool version 1.23.10",
        "errorbounds": {
            "pages": 4,
            "theorem_anchor": "page 1: Theorem 1 (von Mangoldt's formula), a truncated |Im(rho)|<T sum, R(x,T), and distance-to-prime-power qualification",
            "proof_anchor": "This unit says the formula will be proved in a later unit; it is not the proof source.",
        },
        "von_mangoldt": {
            "pages": 6,
            "theorem_anchor": "page 1: Theorem 1 (von Mangoldt's formula) with R(x,T)",
            "proof_anchor": "page 2: residue calculation states that every zero is counted with multiplicity and contributes -x^rho/rho.",
        },
        "epistemic_status": "OBSERVED",
    }


def author_relationship() -> dict:
    pairs = []
    for label, official, author in (("errorbounds", ERROR_OFFICIAL, ERROR_AUTHOR), ("von_mangoldt", VON_OFFICIAL, VON_AUTHOR)):
        official_hash, author_hash = digest(official), digest(author)
        assert official_hash != author_hash
        pairs.append({
            "unit": label,
            "official_file": official.name,
            "official_bytes": official.stat().st_size,
            "official_sha256": official_hash,
            "author_file": author.name,
            "author_bytes": author.stat().st_size,
            "author_sha256": author_hash,
            "byte_identity": "NOT_ASSERTED; observed SHA-256 values differ",
            "relationship_boundary": "Same course/unit naming supports a provenance comparison only; no content-equivalence or derivation claim is made here.",
            "epistemic_status": "OBSERVED",
        })
    return {"pairs": pairs, "epistemic_status": "OBSERVED"}


def live_api_check() -> dict:
    base = "https://dspace.mit.edu/server/api/core"
    def get(path: str) -> dict:
        with urllib.request.urlopen(base + path, timeout=30) as response:
            return json.load(response)
    bitstream = get(f"/bitstreams/{BITSTREAM_ID}")
    bundle = get(f"/bitstreams/{BITSTREAM_ID}/bundle")
    item = get(f"/bundles/{BUNDLE_ID}/item")
    assert bitstream["uuid"] == BITSTREAM_ID and bitstream["name"] == "sword-2016-03-11.original.zip"
    assert bitstream["bundleName"] == "SWORD" and bitstream["sizeBytes"] == ZIP.stat().st_size
    assert bitstream["checkSum"] == {"checkSumAlgorithm": "MD5", "value": ZIP_MD5}
    assert bundle["uuid"] == BUNDLE_ID and bundle["name"] == "SWORD"
    assert item["uuid"] == ITEM_ID and item["handle"] == HANDLE
    return {"status": "OBSERVED live API agreement", "item_uuid": ITEM_ID, "bundle_uuid": BUNDLE_ID, "bitstream_uuid": BITSTREAM_ID}


def build() -> dict:
    for path in (ZIP, ERROR_OFFICIAL, VON_OFFICIAL, ERROR_AUTHOR, VON_AUTHOR, ITEM):
        if not path.is_file():
            raise RuntimeError(f"missing frozen source: {path.name}")
    return {
        "artifact_id": "cycle-2-mit-sword-official-bitstream-audit-v1",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Independent provenance, ZIP, file-anchor, and byte audit. It does not prove a new explicit-formula theorem, give legal advice, or assert byte/content identity between official and author copies.",
        "dspace_recorded_api_metadata": {
            "item_uuid": ITEM_ID,
            "bundle_uuid": BUNDLE_ID,
            "bundle_name": "SWORD",
            "bitstream_uuid": BITSTREAM_ID,
            "bitstream_name": "sword-2016-03-11.original.zip",
            "bitstream_size_bytes": 5334292,
            "bitstream_md5": ZIP_MD5,
            "item_url": f"https://dspace.mit.edu/server/api/core/items/{ITEM_ID}",
            "bundle_url": f"https://dspace.mit.edu/server/api/core/bundles/{BUNDLE_ID}",
            "bitstream_url": f"https://dspace.mit.edu/server/api/core/bitstreams/{BITSTREAM_ID}",
            "epistemic_status": "OBSERVED",
        },
        "frozen_item_metadata": frozen_item_audit(),
        "official_sword_zip": zip_audit(),
        "theorem_and_proof_anchors": anchor_audit(),
        "author_copy_relationship": author_relationship(),
        "verification": {"builder": "proof/audit_mit_sword_official_bitstream_v1.py", "builder_sha256": digest(Path(__file__)), "zip_reader": "Python standard-library zipfile", "epistemic_status": "OBSERVED"},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--live-api", action="store_true")
    args = parser.parse_args()
    if args.live_api:
        print(json.dumps(live_api_check(), indent=2, sort_keys=True))
        return 0
    payload = (json.dumps(build(), indent=2, sort_keys=True) + "\n").encode()
    if args.write:
        OUTPUT.write_bytes(payload)
        print(f"wrote {OUTPUT.relative_to(PROJECT)}")
        return 0
    if not OUTPUT.is_file() or OUTPUT.read_bytes() != payload:
        print("official SWORD audit is stale; rerun with --write", file=sys.stderr)
        return 1
    print(json.dumps({"artifact": OUTPUT.name, "verified": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
