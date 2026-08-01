#!/usr/bin/env python3
"""Build or verify the metadata-only Cycle-2 source manifest, version 2.

This inventory deliberately does *not* assess the mathematical authority of a
source.  It is a byte-level provenance record of the locally frozen objects
and the extracted TeX/README inputs on which the proof scripts depend.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


PROJECT = Path(__file__).resolve().parents[1]
SOURCES = PROJECT / "artifacts" / "sources"
ARTIFACT = PROJECT / "artifacts" / "source-manifest-verification-v2.json"

# This is intentionally a narrow, reviewable list rather than a recursive
# inventory of every file unpacked from an upstream tarball.
EXTRACTED_CANONICAL = (
    "arxiv-2405.20552v2/00README.json",
    "arxiv-2405.20552v2/LargevaluesDirichlet17.tex",
    "chourasiya-simonic-2025-explicit-ingham/00README.json",
    "chourasiya-simonic-2025-explicit-ingham/InghamPostArXiv.tex",
    "maynard-pratt-2206.11729/HalfIsolatedv2.tex",
)

GENERIC_DERIVED = {
    "source": "locally generated rendering of the adjacent frozen source file",
    "role": "local rendered-text derivative used for search/navigation",
    "license_or_access_class": (
        "OBSERVED local derivative; no separate licence assertion is made"
    ),
    "provenance_urls": [],
}


def metadata(source: str, role: str, access: str, urls: tuple[str, ...] = ()) -> dict:
    return {
        "source": source,
        "role": role,
        "license_or_access_class": access,
        "provenance_urls": list(urls),
    }


# Each direct regular file must have a row.  The fallback-free coverage check
# below makes adding a new frozen source an explicit metadata decision.
DIRECT_METADATA = {
    "arxiv-2405.20552v2.pdf": metadata(
        "Guth--Maynard, arXiv:2405.20552v2",
        "arXiv v2 rendered paper",
        "OBSERVED open arXiv access; formal licence not recorded here",
        ("https://arxiv.org/pdf/2405.20552v2",),
    ),
    "arxiv-2405.20552v2.tar": metadata(
        "Guth--Maynard, arXiv:2405.20552v2",
        "arXiv v2 TeX source archive",
        "OBSERVED arXiv source access; formal licence not recorded here",
        ("https://export.arxiv.org/e-print/2405.20552v2",),
    ),
    "bui-heath-brown-2013-simple-zeros.pdf": metadata(
        "Bui--Heath-Brown, Simple zeros of the Riemann zeta-function",
        "frozen paper PDF for multiplicity/simple-zero comparisons",
        "OBSERVED locally frozen article copy; licence/access terms not recorded",
    ),
    "bui-heath-brown-2013-simple-zeros.tar": metadata(
        "Bui--Heath-Brown, Simple zeros of the Riemann zeta-function",
        "frozen source archive",
        "OBSERVED locally frozen source archive; licence/access terms not recorded",
    ),
    "chourasiya-simonic-2025-explicit-ingham.pdf": metadata(
        "Chourasiya--Simonic, explicit Ingham source",
        "frozen preprint PDF for explicit-formula comparison",
        "OBSERVED open preprint copy; formal licence not recorded here",
    ),
    "chourasiya-simonic-2025-explicit-ingham.tar": metadata(
        "Chourasiya--Simonic, explicit Ingham source",
        "frozen TeX source archive",
        "OBSERVED locally frozen source archive; licence/access terms not recorded",
    ),
    "cully-hugill-johnston-2023-rvm-i.tar": metadata(
        "Cully-Hugill--Johnston, Riemann--von Mangoldt I",
        "frozen source archive for zero-counting constants",
        "OBSERVED locally frozen source archive; licence/access terms not recorded",
    ),
    "cully-hugill-johnston-2024-rvm-ii.pdf": metadata(
        "Cully-Hugill--Johnston, Riemann--von Mangoldt II",
        "frozen paper PDF for zero-counting constants",
        "OBSERVED locally frozen paper copy; licence/access terms not recorded",
    ),
    "cully-hugill-johnston-2024-rvm-ii.tar": metadata(
        "Cully-Hugill--Johnston, Riemann--von Mangoldt II",
        "frozen source archive",
        "OBSERVED locally frozen source archive; licence/access terms not recorded",
    ),
    "ford-2002-zero-free-regions.pdf": metadata(
        "Ford, Zero-free regions for the Riemann zeta function",
        "frozen paper PDF for zero-free-region comparisons",
        "OBSERVED locally frozen article copy; licence/access terms not recorded",
    ),
    "guth-maynard-2405.20552v2-source.tar": metadata(
        "Guth--Maynard, arXiv:2405.20552v2",
        "alias of the arXiv v2 TeX source archive",
        "OBSERVED arXiv source access; formal licence not recorded here",
        ("https://export.arxiv.org/e-print/2405.20552v2",),
    ),
    "guth-maynard-2405.20552v2.pdf": metadata(
        "Guth--Maynard, arXiv:2405.20552v2",
        "alias of the arXiv v2 rendered paper",
        "OBSERVED open arXiv access; formal licence not recorded here",
        ("https://arxiv.org/pdf/2405.20552v2",),
    ),
    "guth-maynard-annals-aam.pdf": metadata(
        "Guth--Maynard Annals author accepted manuscript",
        "Oxford repository accepted manuscript",
        "OBSERVED repository manuscript access; reuse licence not recorded",
        ("https://ora.ox.ac.uk/objects/uuid%3Aad11b8bf-ad2b-4ebf-a627-647f023c378f",),
    ),
    "hasanalizade-shen-wong-2022-counting-zeros.pdf": metadata(
        "Hasanalizade--Shen--Wong, counting zeros",
        "frozen paper PDF for explicit zero-counting bounds",
        "OBSERVED locally frozen article copy; licence/access terms not recorded",
    ),
    "hasanalizade-shen-wong-2022-counting-zeros.tar": metadata(
        "Hasanalizade--Shen--Wong, counting zeros",
        "frozen source archive",
        "OBSERVED locally frozen source archive; licence/access terms not recorded",
    ),
    "huxley-1972-inventiones15-gdz-volume.pdf": metadata(
        "Huxley, Inventiones Mathematicae 15 (1972)",
        "GDZ volume scan used for historical density-estimate comparison",
        "OBSERVED digital-library scan; rights/licence not recorded",
        ("https://gdz.sub.uni-goettingen.de/",),
    ),
    "jutila-1977-zero-density-estimates-l-functions.pdf": metadata(
        "Jutila, Zero-density estimates for L-functions",
        "frozen historical paper scan for density comparisons",
        "OBSERVED locally frozen scan; rights/licence not recorded",
    ),
    "kedlaya-2007-errorbounds-author.pdf": metadata(
        "Kedlaya, 2007 course notes (author-hosted copy)",
        "error-bound note used in explicit-formula source audit",
        "OBSERVED MIT OCW provenance; CC BY-NC-SA 4.0",
        (
            "https://dspace.mit.edu/handle/1721.1/101679",
            "https://creativecommons.org/licenses/by-nc-sa/4.0/",
        ),
    ),
    "kedlaya-2007-von-mangoldt-author.pdf": metadata(
        "Kedlaya, 2007 course notes (author-hosted copy)",
        "von-Mangoldt note used in explicit-formula source audit",
        "OBSERVED MIT OCW provenance; CC BY-NC-SA 4.0",
        (
            "https://dspace.mit.edu/handle/1721.1/101679",
            "https://creativecommons.org/licenses/by-nc-sa/4.0/",
        ),
    ),
    "maynard-pratt-2206.11729.pdf": metadata(
        "Maynard--Pratt, arXiv:2206.11729",
        "frozen arXiv PDF for short-interval ingredients",
        "OBSERVED open arXiv access; formal licence not recorded here",
        ("https://arxiv.org/pdf/2206.11729",),
    ),
    "maynard-pratt-2206.11729.tar": metadata(
        "Maynard--Pratt, arXiv:2206.11729",
        "frozen arXiv TeX source archive",
        "OBSERVED arXiv source access; formal licence not recorded here",
        ("https://export.arxiv.org/e-print/2206.11729",),
    ),
    "montgomery-1969-inventiones8-gdz-volume.pdf": metadata(
        "Montgomery, Inventiones Mathematicae 8 (1969)",
        "GDZ volume scan for mean-value-theorem comparison",
        "OBSERVED digital-library scan; rights/licence not recorded",
        ("https://gdz.sub.uni-goettingen.de/",),
    ),
    "ora-accepted-manuscript.pdf": metadata(
        "Guth--Maynard Annals author accepted manuscript",
        "alias of Oxford repository accepted manuscript",
        "OBSERVED repository manuscript access; reuse licence not recorded",
        ("https://ora.ox.ac.uk/objects/uuid%3Aad11b8bf-ad2b-4ebf-a627-647f023c378f",),
    ),
    "platt-trudgian-2021-rh-3e12.pdf": metadata(
        "Platt--Trudgian, RH verified to height 3e12",
        "frozen paper PDF for computational zero-verification context",
        "OBSERVED locally frozen article copy; licence/access terms not recorded",
    ),
    "platt-trudgian-2021-rh-3e12.tar": metadata(
        "Platt--Trudgian, RH verified to height 3e12",
        "frozen source archive",
        "OBSERVED locally frozen source archive; licence/access terms not recorded",
    ),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def proof_consumers(relative_path: str) -> list[str]:
    """Find direct textual references, preserving this as OBSERVED metadata."""
    basename = Path(relative_path).name
    consumers = []
    for path in sorted((PROJECT / "proof").rglob("*")):
        if not path.is_file() or path.suffix not in {".py", ".sh"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if relative_path in text or basename in text:
            consumers.append(path.relative_to(PROJECT).as_posix())
    return consumers


def direct_files() -> list[Path]:
    return sorted(path for path in SOURCES.iterdir() if path.is_file())


def item(path: Path, *, scope: str, info: dict) -> dict:
    relative_path = path.relative_to(SOURCES).as_posix()
    return {
        "relative_path": relative_path,
        "scope": scope,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "source": info["source"],
        "role": info["role"],
        "license_or_access_class": info["license_or_access_class"],
        "provenance_urls": info["provenance_urls"],
        "proof_script_consumers": proof_consumers(relative_path),
        "epistemic_status": "OBSERVED",
    }


def extracted_metadata(relative_path: str) -> dict:
    if relative_path.endswith("00README.json"):
        return metadata(
            "metadata emitted with the locally extracted frozen source archive",
            "extracted archive README/metadata record",
            "OBSERVED local extraction metadata; no separate licence assertion",
        )
    if relative_path.endswith("LargevaluesDirichlet17.tex"):
        return metadata(
            "Guth--Maynard arXiv:2405.20552v2 source archive",
            "canonical extracted TeX input read by proof scripts",
            "OBSERVED arXiv-source extraction; formal licence not recorded here",
            ("https://export.arxiv.org/e-print/2405.20552v2",),
        )
    if relative_path.endswith("InghamPostArXiv.tex"):
        return metadata(
            "Chourasiya--Simonic explicit-Ingham source archive",
            "canonical extracted TeX input retained for source audit",
            "OBSERVED local source extraction; formal licence not recorded here",
        )
    if relative_path.endswith("HalfIsolatedv2.tex"):
        return metadata(
            "Maynard--Pratt arXiv:2206.11729 source archive",
            "canonical extracted TeX input read by proof scripts",
            "OBSERVED arXiv-source extraction; formal licence not recorded here",
            ("https://export.arxiv.org/e-print/2206.11729",),
        )
    raise AssertionError(f"no extracted-file metadata for {relative_path}")


def build() -> dict:
    direct = direct_files()
    direct_names = {path.name for path in direct}
    metadata_required = {name for name in direct_names if not name.endswith(".rendered.txt")}
    missing = metadata_required - set(DIRECT_METADATA)
    stale = set(DIRECT_METADATA) - metadata_required
    if missing or stale:
        raise RuntimeError(
            "direct-source metadata coverage changed: "
            f"missing={sorted(missing)}, stale={sorted(stale)}"
        )

    direct_items = []
    for path in direct:
        info = GENERIC_DERIVED if path.name.endswith(".rendered.txt") else DIRECT_METADATA[path.name]
        direct_items.append(item(path, scope="direct_source_file", info=info))
    extracted_items = []
    for relative_path in EXTRACTED_CANONICAL:
        path = SOURCES / relative_path
        if not path.is_file():
            raise RuntimeError(f"missing canonical extracted input: {relative_path}")
        extracted_items.append(
            item(path, scope="extracted_canonical_input", info=extracted_metadata(relative_path))
        )
    all_items = direct_items + extracted_items
    grouped: dict[tuple[int, str], list[str]] = {}
    for row in direct_items:
        grouped.setdefault((row["bytes"], row["sha256"]), []).append(row["relative_path"])
    aliases = [
        {
            "bytes": size,
            "sha256": digest,
            "members": sorted(members),
            "epistemic_status": "OBSERVED",
        }
        for (size, digest), members in sorted(grouped.items())
        if len(members) > 1
    ]
    return {
        "schema": 2,
        "title": "Cycle-2 source manifest and byte verifier",
        "epistemic_status": "OBSERVED",
        "claim_boundary": (
            "Metadata-only inventory and byte checks. It makes no claim that any "
            "source establishes a mathematical theorem or that local copies are "
            "complete reproductions of upstream records."
        ),
        "inventory_rules": {
            "direct_source_files": "every regular file immediately under artifacts/sources",
            "extracted_canonical_inputs": list(EXTRACTED_CANONICAL),
            "duplicate_policy": "aliases are retained and recorded; no duplicate is deleted",
        },
        "items": sorted(all_items, key=lambda row: row["relative_path"]),
        "explicit_duplicate_alias_groups": aliases,
        "policy_absences": [
            {
                "source": "Iwaniec, Lectures on the Riemann Zeta Function (AMS, 2014), Theorem 10.1, pp. 37--38",
                "urls": [
                    "https://doi.org/10.1090/ulect/062",
                    "https://bookstore.ams.org/ULECT/62",
                ],
                "access_class": "ABSENT_BY_POLICY",
                "reason": (
                    "The personally purchased, watermarked AMS PDF is view-only and "
                    "duplication is prohibited. No PDF, OCR, page image, text extract, "
                    "or copied excerpt is stored in this repository."
                ),
                "epistemic_status": "OBSERVED",
            }
        ],
        "verification": {
            "algorithm": "SHA-256",
            "manifest_builder": "proof/build_source_manifest_v2.py",
            "builder_sha256": sha256(Path(__file__).resolve()),
            "verified": True,
            "epistemic_status": "OBSERVED",
        },
    }


def encoded(manifest: dict) -> bytes:
    return (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true", help="write the deterministic artifact")
    action.add_argument("--check", action="store_true", help="check the artifact against current bytes")
    args = parser.parse_args()
    manifest = build()
    payload = encoded(manifest)
    if args.write:
        ARTIFACT.write_bytes(payload)
        print(f"wrote {ARTIFACT.relative_to(PROJECT)}")
        return 0
    if not ARTIFACT.is_file():
        print(f"missing {ARTIFACT.relative_to(PROJECT)}", file=sys.stderr)
        return 1
    if ARTIFACT.read_bytes() != payload:
        print("source manifest v2 does not match current inventory; rerun --write", file=sys.stderr)
        return 1
    print(json.dumps({"verified": True, "artifact": ARTIFACT.name}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
