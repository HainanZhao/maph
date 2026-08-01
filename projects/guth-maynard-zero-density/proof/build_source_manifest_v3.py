#!/usr/bin/env python3
"""Build/check the frozen Cycle-2 source-byte manifest, version 3.

This is an inventory correction, not a source-authority or G0 certificate.
Unlike v2, it deliberately records no proof-script consumers: the inventory is
therefore stable under later proof-script additions or edits.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

from build_source_manifest_v2 import DIRECT_METADATA as V2_DIRECT_METADATA
from build_source_manifest_v2 import EXTRACTED_CANONICAL


PROJECT = Path(__file__).resolve().parents[1]
SOURCES = PROJECT / "artifacts" / "sources"
ARTIFACT = PROJECT / "artifacts" / "source-manifest-verification-v3.json"
V2_BUILDER = PROJECT / "proof" / "build_source_manifest_v2.py"
V2_BUILDER_SHA256 = "9f2407f67d561ccbcfa91ab87759aa522ebd8c835f78bd45113bf53a8f548cb3"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def metadata(source: str, role: str, access: str, urls: tuple[str, ...] = ()) -> dict[str, object]:
    return {
        "source": source,
        "role": role,
        "license_or_access_class": access,
        "provenance_urls": list(urls),
    }


# V2 remains frozen and supplies the unchanged descriptive rows.  This copy is
# intentionally pinned, so a later v2 edit cannot silently alter the v3 build.
DIRECT_METADATA = dict(V2_DIRECT_METADATA)
DIRECT_METADATA.update({
    "kedlaya-2007-errorbounds-author.pdf": metadata(
        "K. S. Kedlaya, 18.785 course notes (direct author-primary copy)",
        "error-bounds note used in explicit-formula access audit",
        "OBSERVED direct author-primary access; no CC licence is asserted or inherited for these bytes",
        ("https://kskedlaya.org/18.785/errorbounds.pdf",),
    ),
    "kedlaya-2007-von-mangoldt-author.pdf": metadata(
        "K. S. Kedlaya, 18.785 course notes (direct author-primary copy)",
        "von-Mangoldt note used in explicit-formula access audit",
        "OBSERVED direct author-primary access; no CC licence is asserted or inherited for these bytes",
        ("https://kskedlaya.org/18.785/von-mangoldt.pdf",),
    ),
    "mit-dspace-1721.1-101679-metadata.json": metadata(
        "MIT DSpace item 1721.1/101679, 18.785 Analytic Number Theory, Spring 2007",
        "frozen official item metadata for course identity, non-withdrawn status, and rights record",
        "OBSERVED official item-level record: Usage Restrictions: Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0)",
        ("https://dspace.mit.edu/server/api/pid/find?id=1721.1%2F101679",),
    ),
    "mit-ocw-18-785-2007-sword-official.zip": metadata(
        "MIT DSpace SWORD bitstream for item 1721.1/101679",
        "frozen official archive containing the course lecture-note PDF members",
        "OBSERVED official archive under the associated item-level CC BY-NC-SA 3.0 rights record; no claim is made about separately hosted author-copy bytes",
        ("https://dspace.mit.edu/server/api/core/bitstreams/7292f134-d4a7-4063-bd7e-2084259b8fa9/content",),
    ),
    "mit-ocw-18-785-2007-errorbounds-official.pdf": metadata(
        "MIT DSpace SWORD archive member, 18.785 course notes",
        "extracted official error-bounds PDF member",
        "OBSERVED official PDF member under the associated item-level CC BY-NC-SA 3.0 rights record; no claim is made about separately hosted author-copy bytes",
        ("https://dspace.mit.edu/server/api/core/bitstreams/7292f134-d4a7-4063-bd7e-2084259b8fa9/content",),
    ),
    "mit-ocw-18-785-2007-von-mangoldt-official.pdf": metadata(
        "MIT DSpace SWORD archive member, 18.785 course notes",
        "extracted official von-Mangoldt PDF member",
        "OBSERVED official PDF member under the associated item-level CC BY-NC-SA 3.0 rights record; no claim is made about separately hosted author-copy bytes",
        ("https://dspace.mit.edu/server/api/core/bitstreams/7292f134-d4a7-4063-bd7e-2084259b8fa9/content",),
    ),
})

GENERIC_DERIVED = metadata(
    "locally generated rendering of the adjacent frozen source file",
    "local rendered-text derivative used for search/navigation",
    "OBSERVED local derivative; no separate licence assertion is made",
)


def extracted_metadata(relative_path: str) -> dict[str, object]:
    if relative_path.endswith("00README.json"):
        return metadata(
            "metadata emitted with the locally extracted frozen source archive",
            "extracted archive README/metadata record",
            "OBSERVED local extraction metadata; no separate licence assertion",
        )
    if relative_path.endswith("LargevaluesDirichlet17.tex"):
        return metadata(
            "Guth--Maynard arXiv:2405.20552v2 source archive",
            "canonical extracted TeX input",
            "OBSERVED arXiv-source extraction; formal licence not recorded here",
            ("https://export.arxiv.org/e-print/2405.20552v2",),
        )
    if relative_path.endswith("InghamPostArXiv.tex"):
        return metadata(
            "Chourasiya--Simonic explicit-Ingham source archive",
            "canonical extracted TeX input",
            "OBSERVED local source extraction; formal licence not recorded here",
        )
    if relative_path.endswith("HalfIsolatedv2.tex"):
        return metadata(
            "Maynard--Pratt arXiv:2206.11729 source archive",
            "canonical extracted TeX input",
            "OBSERVED arXiv-source extraction; formal licence not recorded here",
            ("https://export.arxiv.org/e-print/2206.11729",),
        )
    raise AssertionError(f"no extracted-file metadata for {relative_path}")


def item(path: Path, scope: str, info: dict[str, object]) -> dict[str, object]:
    return {
        "relative_path": path.relative_to(SOURCES).as_posix(),
        "scope": scope,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "source": info["source"],
        "role": info["role"],
        "license_or_access_class": info["license_or_access_class"],
        "provenance_urls": info["provenance_urls"],
        "epistemic_status": "OBSERVED",
    }


def build() -> dict[str, object]:
    if sha256(V2_BUILDER) != V2_BUILDER_SHA256:
        raise RuntimeError("frozen v2 descriptive-row builder hash changed")
    direct = sorted(path for path in SOURCES.iterdir() if path.is_file())
    expected = {path.name for path in direct if not path.name.endswith(".rendered.txt")}
    missing, stale = expected - set(DIRECT_METADATA), set(DIRECT_METADATA) - expected
    if missing or stale:
        raise RuntimeError(f"direct-source metadata coverage changed: missing={sorted(missing)}, stale={sorted(stale)}")
    direct_items = [
        item(path, "direct_source_file", GENERIC_DERIVED if path.name.endswith(".rendered.txt") else DIRECT_METADATA[path.name])
        for path in direct
    ]
    extracted_items = []
    for relative_path in EXTRACTED_CANONICAL:
        path = SOURCES / relative_path
        if not path.is_file():
            raise RuntimeError(f"missing canonical extracted input: {relative_path}")
        extracted_items.append(item(path, "extracted_canonical_input", extracted_metadata(relative_path)))
    aliases: dict[tuple[int, str], list[str]] = {}
    for row in direct_items:
        aliases.setdefault((row["bytes"], row["sha256"]), []).append(row["relative_path"])
    return {
        "schema": 3,
        "title": "Cycle-2 source manifest and byte verifier",
        "epistemic_status": "OBSERVED",
        "supersedes": "source-manifest-verification-v2 for current direct-source inventory and access-scope correction; v1 and v2 are preserved",
        "claim_boundary": "OBSERVED byte inventory and stated access metadata only. It establishes neither mathematical source authority nor G0 PASS.",
        "v2_correction": {
            "epistemic_status": "PROVED",
            "inventory_status": "v2 is stale: it predates the frozen DSpace item metadata and official SWORD archive plus two extracted official PDFs.",
            "license_scope_correction": "v2's CC BY-NC-SA 4.0 author-copy rows are incorrect in scope. V3 records direct Kedlaya author-primary access without CC inheritance, and records CC BY-NC-SA 3.0 only as an official item-level right for the SWORD/PDF route.",
        },
        "inventory_rules": {
            "direct_source_files": "every regular file immediately under artifacts/sources at the v3 freeze",
            "extracted_canonical_inputs": list(EXTRACTED_CANONICAL),
            "duplicate_policy": "aliases are retained and reported; no duplicate is deleted",
            "g0_consumer_scope": "OMITTED_BY_DESIGN: no proof-script consumer inventory is asserted or scanned, so later proof scripts cannot change this source-byte inventory.",
            "frozen_v2_descriptive_row_builder_sha256": V2_BUILDER_SHA256,
        },
        "items": sorted(direct_items + extracted_items, key=lambda row: row["relative_path"]),
        "explicit_duplicate_alias_groups": [
            {"bytes": size, "sha256": digest, "members": sorted(members), "epistemic_status": "OBSERVED"}
            for (size, digest), members in sorted(aliases.items()) if len(members) > 1
        ],
        "policy_absences": [{
            "source": "Iwaniec, Lectures on the Riemann Zeta Function (AMS, 2014), Theorem 10.1, pp. 37--38",
            "urls": ["https://doi.org/10.1090/ulect/062", "https://bookstore.ams.org/ULECT/62"],
            "access_class": "ABSENT_BY_POLICY",
            "reason": "The personally purchased, watermarked AMS PDF is view-only and duplication is prohibited. No PDF, OCR, page image, text extract, or copied excerpt is stored in this repository.",
            "epistemic_status": "OBSERVED",
        }],
        "verification": {
            "algorithm": "SHA-256",
            "manifest_builder": "proof/build_source_manifest_v3.py",
            "builder_sha256": sha256(Path(__file__).resolve()),
            "verified": True,
            "epistemic_status": "OBSERVED",
        },
    }


def encoded(manifest: dict[str, object]) -> bytes:
    return (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = encoded(build())
    if args.write:
        ARTIFACT.write_bytes(payload)
        print(f"wrote {ARTIFACT.relative_to(PROJECT)}")
        return 0
    if not ARTIFACT.is_file() or ARTIFACT.read_bytes() != payload:
        print("source manifest v3 does not match frozen inventory; rerun --write", file=sys.stderr)
        return 1
    print(json.dumps({"verified": True, "artifact": ARTIFACT.name}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
