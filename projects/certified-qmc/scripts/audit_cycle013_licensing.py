#!/usr/bin/env python3
"""Authenticate archived source terms and emit the Cycle-013 disposition."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "third_party" / "terms" / "2026-07-29"
OUTPUT = ROOT / "certificates" / "cycle-013-licensing.json"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: object) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
    ).hexdigest()


def archived(
    name: str,
    headers: str,
    expected_body: str,
    expected_headers: str,
) -> dict[str, object]:
    body_path = ARCHIVE / name
    headers_path = ARCHIVE / headers
    body_sha = digest(body_path)
    headers_sha = digest(headers_path)
    if body_sha != expected_body or headers_sha != expected_headers:
        raise RuntimeError(f"archived terms hash mismatch: {name}")
    return {
        "body_path": str(body_path.relative_to(ROOT)),
        "body_sha256": body_sha,
        "response_headers_path": str(headers_path.relative_to(ROOT)),
        "response_headers_sha256": headers_sha,
    }


def main() -> None:
    sources = [
        {
            "id": "unsw-lattice-page",
            "url": "https://web.maths.unsw.edu.au/~fkuo/lattice/index.html",
            "retrieved_at_utc": "2026-07-29T07:08:28Z",
            "snapshot": archived(
                "unsw-lattice-index.html",
                "unsw-lattice-index.headers",
                "bb8c5a8e38d84778fc1b18f1880890cfc6608d65b80a6f606b4aed7270f726ba",
                "adc5bc420f08558ac134f0fb5484bfb57971222279940cb1079bfe03adda2eb4",
            ),
            "classification": "UNCLEAR",
            "finding": (
                "The page offers downloads and citations but states no "
                "license or express redistribution permission."
            ),
            "release_mode": "KEYED_MERITS_WITHOUT_EMBEDDED_VECTORS",
        },
        {
            "id": "magic-point-shop",
            "url": (
                "https://people.cs.kuleuven.be/~dirk.nuyens/"
                "qmc-generators/"
            ),
            "retrieved_at_utc": "2026-07-29T07:08:29Z",
            "snapshot": archived(
                "magic-point-shop.html",
                "magic-point-shop.headers",
                "9e84e4fe88b2619a18d955dbcbe23f6004f16b1282651193fce2c4315d8569d3",
                "b46dc4c22ceef23887c8aa04cfa02ddab14b34d9d812bd08bc7d968a9bb41f7f",
            ),
            "classification": "UNCLEAR",
            "finding": (
                "The page requests citation and displays copyright, but "
                "states no license or express redistribution permission."
            ),
            "release_mode": "KEYED_MERITS_WITHOUT_EMBEDDED_VECTORS",
        },
        {
            "id": "qmcpy-frozen-commit",
            "url": (
                "https://raw.githubusercontent.com/QMCSoftware/"
                "QMCSoftware/a774f3a1297b982f2544742e8c691e035c9fc0a7/"
                "LICENSE"
            ),
            "commit": "a774f3a1297b982f2544742e8c691e035c9fc0a7",
            "retrieved_at_utc": "2026-07-29T07:08:30Z",
            "snapshot": archived(
                "qmcpy-a774f3a-LICENSE",
                "qmcpy-a774f3a-LICENSE.headers",
                "c24916df4d0aa8f54d7eaf2afae93acf2e8a018bfa561c56469736c94ef095da",
                "752187671c626eca72d467152636d77872c0984c22b34c66fa41a018c3855f51",
            ),
            "classification": "REDISTRIBUTABLE",
            "finding": (
                "The frozen LICENSE is Apache-2.0 and contains an express "
                "copyright redistribution grant subject to its conditions."
            ),
            "release_mode": "REDISTRIBUTABLE_WITH_LICENSE_AND_ATTRIBUTION",
        },
    ]
    payload = {
        "schema": "certified-qmc-cycle-013-licensing-v1",
        "claim_tag": "VERIFIED_TERMS_SNAPSHOT_AND_POLICY_DISPOSITION",
        "sources": sources,
        "production_vector_policy": {
            "embedded_vectors": False,
            "mode": "KEYED_MERITS_WITHOUT_EMBEDDED_VECTORS",
            "key_fields": [
                "source citation",
                "frozen snapshot hash",
                "entry index",
                "per-entry vector hash",
            ],
            "human_escalation_required": False,
            "reason": (
                "The production UNSW source is UNCLEAR, and keyed mode "
                "preserves certificate replay without embedding."
            ),
        },
        "artifact_licenses": {
            "code": {
                "spdx": "Apache-2.0",
                "path": "LICENSE",
                "sha256": digest(ROOT / "LICENSE"),
            },
            "tables_and_original_data": {
                "spdx": "CC-BY-4.0",
                "path": "LICENSE-DATA",
                "sha256": digest(ROOT / "LICENSE-DATA"),
                "excludes": (
                    "third-party vectors and archived third-party terms"
                ),
            },
        },
        "gate": {
            "all_terms_snapshots_authenticated": True,
            "all_sources_classified": True,
            "prohibited_source_intended_for_embedding": False,
            "keyed_mode_selected_for_unclear_sources": True,
            "cycle_013_licensing_gate_passed": True,
        },
        "boundary": (
            "This is a conservative project redistribution policy based "
            "on the archived text, not legal advice and not a declaration "
            "about copyrightability. UNCLEAR never authorizes embedding."
        ),
    }
    payload["certificate_sha256"] = canonical_digest(payload)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(OUTPUT)


if __name__ == "__main__":
    main()
