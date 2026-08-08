#!/usr/bin/env python3
"""Seal and replay the public Lane B Zenodo inventory."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402


OUTPUT = ROOT / "artifacts/zenodo-canonical-spin-structure-compression-published-v1.json"
RECORD = "https://zenodo.org/api/records/21845273"
EXPECTED = {
    "00_separator-compression-cubic-lattice-ising-strips.pdf": (481421, "3815bf7b95346f7722f899c527ea05bb12eb0cce755c83c8496a0c49e9ec6e01"),
    "01_manuscript-source.zip": (46951, "9f104a7f8d00b0edf0563c0404da81d9f09e37ffce0c10b57b9e69e7e4d09361"),
    "02_proof-replay-archive.tar.gz": (618085, "b5ca8ba9e64426a8a2438559e8404b134f9fa4e1ec1bbeaea9c4a5f40e5e77cc"),
    "03_SHA256SUMS.txt": (310, "b3c96e241d049e9648828ebd4ee5834e06a14012e7d8a4068114d263b8d86139"),
}
HASHES = {
    "publication_note": ("docs/lane-b-zenodo-publication.md", "986760754e98c3a60f9a6ebe9538821a1b6acc1967edd79b5588595333ef1df3"),
    "release_builder": ("proof/build_lane_b_release_archive.py", "9682aa5733a5e366c49391586418199fe36c99628d0cc1f78ddd1fe9b2faeb2e"),
    "scaffold": ("proof/cycle_seal_v1.py", "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163"),
}


def payload():
    with urllib.request.urlopen(RECORD, timeout=60) as response:
        record = json.load(response)
    files = {}
    for item in sorted(record["files"], key=lambda row: row["key"]):
        with urllib.request.urlopen(item["links"]["self"], timeout=120) as response:
            data = response.read()
        files[item["key"]] = {
            "bytes": len(data),
            "md5": hashlib.md5(data).hexdigest(),
            "sha256": hashlib.sha256(data).hexdigest(),
        }
    observed = {name: (row["bytes"], row["sha256"]) for name, row in files.items()}
    if observed != EXPECTED:
        raise RuntimeError("public Zenodo inventory changed")
    return {
        "schema": "zenodo-canonical-spin-structure-compression-published-v1",
        "status": "PUBLISHED",
        "author": "Hainan Zhao",
        "published_at_date": "2026-08-08",
        "record_id": 21845273,
        "version_doi": record["doi"],
        "concept_doi": record["conceptdoi"],
        "title": record["metadata"]["title"],
        "files": files,
        "lexical_order": sorted(files),
        "default_preview": "00_separator-compression-cubic-lattice-ising-strips.pdf",
        "claim_boundary": "The archive publishes the finite-lattice separator-compression results; it does not claim a thermodynamic solution of the three-dimensional Ising model.",
        "frozen_hashes": freeze_inputs(ROOT, {k: (ROOT / p, h) for k, (p, h) in HASHES.items()}),
        "runtime": check_runtime("lane-b-zenodo-publication"),
        "sealer": {"path": "proof/build_lane_b_zenodo_publication_record.py", "sha256": sha256(Path(__file__))},
        "replay": {"artifact_check": "python3 proof/build_lane_b_zenodo_publication_record.py --check"},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
