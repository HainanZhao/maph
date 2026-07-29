from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import unittest

from src.certificate import canonical_sha256


PROJECT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict:
    return json.loads((PROJECT / "certificates" / name).read_text())


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


class Cycle013Tests(unittest.TestCase):
    def test_licensing_dispositions_and_snapshots_replay(self):
        artifact = load("cycle-013-licensing.json")
        supplied = artifact.pop("certificate_sha256")
        self.assertEqual(canonical_sha256(artifact), supplied)
        classifications = {
            source["id"]: source["classification"]
            for source in artifact["sources"]
        }
        self.assertEqual(classifications["unsw-lattice-page"], "UNCLEAR")
        self.assertEqual(classifications["magic-point-shop"], "UNCLEAR")
        self.assertEqual(
            classifications["qmcpy-frozen-commit"], "REDISTRIBUTABLE"
        )
        for source in artifact["sources"]:
            snapshot = source["snapshot"]
            self.assertEqual(
                digest(PROJECT / snapshot["body_path"]),
                snapshot["body_sha256"],
            )
            self.assertEqual(
                digest(PROJECT / snapshot["response_headers_path"]),
                snapshot["response_headers_sha256"],
            )
        policy = artifact["production_vector_policy"]
        self.assertFalse(policy["embedded_vectors"])
        self.assertFalse(policy["human_escalation_required"])
        self.assertEqual(
            policy["mode"], "KEYED_MERITS_WITHOUT_EMBEDDED_VECTORS"
        )
        for license_record in artifact["artifact_licenses"].values():
            self.assertEqual(
                digest(PROJECT / license_record["path"]),
                license_record["sha256"],
            )

    def test_release_dependency_manifest_replays(self):
        artifact = load("cycle-013-dependency-manifest.json")
        supplied = artifact.pop("certificate_sha256")
        self.assertEqual(canonical_sha256(artifact), supplied)
        self.assertTrue(
            artifact["gate"]["cycle_013_dependency_gate_passed"]
        )
        self.assertFalse(
            artifact["dependency_policy"]["fftw_present"]
        )
        self.assertFalse(artifact["build_graph"]["contains_fftw"])
        self.assertTrue(artifact["clean_room"]["build_succeeded"])
        for source, expected in artifact["release_sources"].items():
            self.assertEqual(digest(PROJECT / source), expected)
        for binary in artifact["dynamic_dependencies"]:
            self.assertFalse(binary["contains_fftw"])
            self.assertNotIn(
                "libfftw3.so.3", binary["elf_needed"]
            )
        for binary in artifact["clean_room"]["binaries"]:
            self.assertFalse(binary["contains_fftw"])


if __name__ == "__main__":
    unittest.main()
