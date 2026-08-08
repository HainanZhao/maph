#!/usr/bin/env python3
"""Seal and replay the post-review Lane B Zenodo inventory."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof import build_lane_b_zenodo_publication_record_v2 as base  # noqa: E402
from proof.cycle_seal_v1 import run_cli, sha256  # noqa: E402


OUTPUT = ROOT / "artifacts/zenodo-canonical-spin-structure-compression-published-v3.json"
base.RECORD_ID = 21848792
base.RECORD = "https://zenodo.org/api/records/21848792"
base.HTML = "https://zenodo.org/records/21848792"
base.EXPECTED = {
    "00_separator-compression-cubic-lattice-ising-strips.pdf": (485034, "199456bad51e34348d16249f74da1663f207eccec342f10ab21010584144f833"),
    "01_manuscript-source.zip": (48536, "b0ba1ec9a98b421bf5348ee1baf8b4446f0e1dd99b795f9b38620a8f5ddee349"),
    "02_proof-replay-archive.tar.gz": (724322, "6445ea2b926c29876947025db1b48b3564ffe72fb920bb517f19e14595bd9a91"),
    "03_SHA256SUMS.txt": (310, "e50324d0a5b95900530e7e5e69646a80ec40a3da385b3404fdac284eb21a2436"),
}
base.HASHES = {
    "publication_note": ("docs/lane-b-zenodo-publication-v3.md", "c03b7e29e769954040c89bec23832657a3b0bbf6f60409e1cbf8a978c6d18823"),
    "release_builder": ("proof/build_lane_b_release_archive_v3.py", "09f8d6354694271ba6a8e29da50bafb84368d83ffbbfa7715db98c01716fe797"),
    "release_builder_base": ("proof/build_lane_b_release_archive_v2.py", "6e80ee6e7904983e292d1e7ec354bc2670e90a3bc07b14161605684a6a61c4a5"),
    "scaffold": ("proof/cycle_seal_v1.py", "c4a09e7baa8a5588d4c6855a533eb933c85791707ed9653437644c1e1ad6c163"),
}
base.DEFAULT_PREVIEW = "/records/21848792/preview/00_separator-compression-cubic-lattice-ising-strips.pdf"


def payload():
    result = base.payload()
    result["schema"] = "zenodo-canonical-spin-structure-compression-published-v3"
    result["status"] = "PUBLISHED_POST_REVIEW_CORRECTION"
    result["previous_version_doi"] = "10.5281/zenodo.21847231"
    result["sealer"] = {
        "path": "proof/build_lane_b_zenodo_publication_record_v3.py",
        "sha256": sha256(Path(__file__)),
    }
    result["replay"] = {
        "artifact_check": "python3 proof/build_lane_b_zenodo_publication_record_v3.py --check"
    }
    return result


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
