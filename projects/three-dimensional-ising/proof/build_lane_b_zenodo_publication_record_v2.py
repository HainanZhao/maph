#!/usr/bin/env python3
"""Seal and replay the corrected Lane B Zenodo inventory and retraction."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import urllib.error
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256  # noqa: E402


OUTPUT = ROOT / "artifacts/zenodo-canonical-spin-structure-compression-published-v2.json"
RECORD_ID = 21847231
RECORD = f"https://zenodo.org/api/records/{RECORD_ID}"
HTML = f"https://zenodo.org/records/{RECORD_ID}"
OLD_RECORD_ID = 21845273
OLD_RECORD = f"https://zenodo.org/api/records/{OLD_RECORD_ID}"
EXPECTED = {
    "00_separator-compression-cubic-lattice-ising-strips.pdf": (495227, "83b327cbee63086a5896f07290d4622eb04cd6c85718b0c0be3d0384f7da8c59"),
    "01_manuscript-source.zip": (48142, "c733fb98b0b0321e216202da90358a27e01f32e34467e6b5ddafd880b4d15ce8"),
    "02_proof-replay-archive.tar.gz": (721771, "b497225f002230d4cb7a1df520fbec3df771d67e4268c366fa01e0e7ea0cf847"),
    "03_SHA256SUMS.txt": (310, "24dd4639b63da4102b4ae64017cf474b4563e193ea7a395bb711e0c543ee9e4a"),
}
HASHES = {
    "publication_note": ("docs/lane-b-zenodo-publication-v2.md", "819b39dd639f729ad5fa37a0e406411e6dd1bc799f50a0557167ded9cf0ef904"),
    "release_builder": ("proof/build_lane_b_release_archive_v2.py", "6e80ee6e7904983e292d1e7ec354bc2670e90a3bc07b14161605684a6a61c4a5"),
    "cycle18_correction": ("artifacts/cycle-18-b18-character-duality-correction-v3.json", "2ad56484632aab8f9f72d31daabe83865a18797ed41c2b90d2062cdf8af7ffc7"),
    "scaffold": ("proof/cycle_seal_v1.py", "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163"),
}
DEFAULT_PREVIEW = "/records/21847231/preview/00_separator-compression-cubic-lattice-ising-strips.pdf"


def get_json(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=60) as response:
        return json.load(response)


def payload():
    record = get_json(RECORD)
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
        raise RuntimeError("corrected public Zenodo inventory changed")

    with urllib.request.urlopen(HTML, timeout=60) as response:
        html = response.read().decode("utf-8", errors="replace")
    if DEFAULT_PREVIEW not in html:
        raise RuntimeError("corrected record does not expose the expected default preview")

    try:
        get_json(OLD_RECORD)
    except urllib.error.HTTPError as exc:
        if exc.code != 410:
            raise
        old_tombstone = json.loads(exc.read().decode("utf-8"))
    else:
        raise RuntimeError("unsupported original Zenodo record is not tombstoned")
    if old_tombstone.get("status") != 410:
        raise RuntimeError("old record tombstone does not report HTTP 410")
    message = json.dumps(old_tombstone, sort_keys=True).lower()
    if "retracted" not in message:
        raise RuntimeError("old record tombstone does not identify retraction")

    return {
        "schema": "zenodo-canonical-spin-structure-compression-published-v2",
        "status": "PUBLISHED_CORRECTED",
        "claim_status": "PROVED",
        "author": "Hainan Zhao",
        "published_at_date": "2026-08-08",
        "record_id": RECORD_ID,
        "version_doi": record["doi"],
        "concept_doi": record["conceptdoi"],
        "title": record["metadata"]["title"],
        "files": files,
        "lexical_order": sorted(files),
        "default_preview": DEFAULT_PREVIEW,
        "superseded_record": {
            "record_id": OLD_RECORD_ID,
            "version_doi": "10.5281/zenodo.21845273",
            "status": "RETRACTED_HTTP_410",
            "supported": False,
        },
        "claim_boundary": "The corrected archive proves finite-lattice separator compression after repairing the internal-cut character duality; it does not claim a thermodynamic solution of the three-dimensional Ising model.",
        "frozen_hashes": freeze_inputs(ROOT, {k: (ROOT / p, h) for k, (p, h) in HASHES.items()}),
        "runtime": check_runtime("lane-b-zenodo-publication-v2"),
        "sealer": {"path": "proof/build_lane_b_zenodo_publication_record_v2.py", "sha256": sha256(Path(__file__))},
        "replay": {"artifact_check": "python3 proof/build_lane_b_zenodo_publication_record_v2.py --check"},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
