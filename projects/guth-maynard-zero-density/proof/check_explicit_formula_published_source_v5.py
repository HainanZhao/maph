#!/usr/bin/env python3
"""Correct v4 by proving the selected formula is in a published MIT item."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-2-stream-c-explicit-formula-published-source-v5.json"
FROZEN = {
    "v4_closure": ("artifacts/cycle-2-stream-c-explicit-formula-source-closure-v4.json", "1c4ecc54be6f681be788084c3637f1101996869e09015edac8cf41e6ab39d5f0"),
    "v4_checker": ("proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py", "72107f1f31e51d2aa9d0ea0eb22c247a1643e58a898232a7fd02c3dee5508064"),
    "metadata": ("artifacts/sources/mit-dspace-1721.1-101679-metadata.json", "4c1f262bc51efa23993a561f908871d35245ca462df90271d0bf2127283f24c7"),
    "official_formula": ("artifacts/sources/mit-ocw-18-785-2007-errorbounds-official.pdf", "b8b2acfbc4b22b25c898c0af8f74692a0d31bd6cf302e9f2d772d33a34fdd3e4"),
    "official_proof": ("artifacts/sources/mit-ocw-18-785-2007-von-mangoldt-official.pdf", "5f705a6d3804d555944298f87a8a53e2e4e5a13188a717679f8fb8b73095210a"),
    "official_sword": ("artifacts/sources/mit-ocw-18-785-2007-sword-official.zip", "d559229963960da2087918a95af6efd7ad8999a4ba63942a12aef63c5eceac57"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def values(metadata: dict[str, Any], key: str) -> list[str]:
    return [row["value"] for row in metadata["metadata"][key]]


def certificate() -> dict[str, Any]:
    hashes = {}
    for key, (relative, expected) in FROZEN.items():
        actual = sha256(ROOT / relative)
        assert actual == expected, f"published-source input changed: {relative}"
        hashes[key] = actual
    subprocess.run([sys.executable, str(ROOT / FROZEN["v4_checker"][0])], check=True,
                   capture_output=True, text=True)
    metadata = json.loads((ROOT / FROZEN["metadata"][0]).read_text())
    assert metadata["entityType"] == "Publication"
    assert values(metadata, "dspace.entity.type") == ["Publication"]
    assert values(metadata, "dc.type") == ["Learning Object"]
    assert values(metadata, "dc.date.issued") == ["2007-06"]
    assert values(metadata, "dc.contributor.author") == ["Kedlaya, Kiran"]
    assert metadata["inArchive"] and metadata["discoverable"] and not metadata["withdrawn"]
    closure = json.loads((ROOT / FROZEN["v4_closure"][0]).read_text())
    assert closure["official_pdf_members"][0]["locator"] == "Theorem 1, p. 1"
    assert "multiplicity" in closure["official_pdf_members"][1]["checked"]
    return {
        "artifact_id": "cycle-2-stream-c-explicit-formula-published-source-v5",
        "supersedes": "source closure v4 for epistemic publication classification only; v4 remains the official-byte/license/transfer record",
        "epistemic_status": "PROVED",
        "claim_boundary": "PROVED that the exact theorem and proof used by Stream C occur in an author-identified, issued, archived, discoverable MIT DSpace item whose authoritative entity type is Publication. The theorem hypotheses and multiplicity convention are checked through v4. This makes no peer-review claim and proves no new explicit formula.",
        "published_item": {
            "status": "PROVED",
            "institution": "Massachusetts Institute of Technology",
            "department": "Massachusetts Institute of Technology. Department of Mathematics",
            "handle": metadata["handle"],
            "title": metadata["name"],
            "author": values(metadata, "dc.contributor.author")[0],
            "date_issued": values(metadata, "dc.date.issued")[0],
            "dspace_entity_type": metadata["entityType"],
            "dc_type": values(metadata, "dc.type")[0],
            "in_archive": metadata["inArchive"],
            "discoverable": metadata["discoverable"],
            "withdrawn": metadata["withdrawn"],
            "scope": "Institutionally published learning object; no assertion of journal publication or peer review.",
        },
        "published_theorem": {
            "status": "PROVED",
            "formula_locator": "official archive member errorbounds.pdf, Theorem 1, p. 1",
            "proof_locator": "official archive member von_mangoldt.pdf, Theorem 1, pp. 1-6; residue computation p. 2",
            "hypotheses_checked": "x>=2 and T>0; half-weighted psi; zeros with |Im rho|<T; distance-to-other-prime-power remainder",
            "convention_checked": "zero residues counted with multiplicity",
            "application_transfer": "v4 checks integral endpoints, O(x(log x)^3/T) for 2<=T<=x, and the |gamma|/|rho| boundary bridge",
        },
        "frozen_hashes": hashes,
        "falsifier": "Any metadata state other than issued, archived, discoverable, nonwithdrawn Publication, or a changed official theorem/proof byte or hypothesis anchor, invalidates this classification.",
        "replay": {
            "script_sha256": sha256(Path(__file__)),
            "write_command": "python3 projects/guth-maynard-zero-density/proof/check_explicit_formula_published_source_v5.py --write",
            "check_command": "python3 projects/guth-maynard-zero-density/proof/check_explicit_formula_published_source_v5.py --check",
        },
    }


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = render(certificate())
    if args.write:
        OUTPUT.write_text(payload)
    elif not OUTPUT.is_file() or OUTPUT.read_text() != payload:
        raise SystemExit("published-source v5 mismatch")
    else:
        print(json.dumps({"artifact": OUTPUT.name, "verified": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
