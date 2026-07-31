import hashlib
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ResultsV15IntegrationTest(unittest.TestCase):
    def test_main_is_first_and_addendum_is_not_top_level(self):
        record = json.loads(
            (
                ROOT
                / "artifacts/zenodo-results-v1.5-draft-upload-verification-v1.json"
            ).read_text()
        )
        ordering = record["ordering_and_preview"]
        self.assertTrue(ordering["main_paper_sorts_first"])
        self.assertEqual(ordering["standalone_addendum_top_level_count"], 0)
        self.assertEqual(
            ordering["draft_thumbnail_source"],
            "effective-stark-results-00-main-paper.pdf",
        )
        self.assertEqual(
            ordering["lexical_inventory"],
            sorted(ordering["lexical_inventory"]),
        )
        self.assertEqual(
            ordering["lexical_inventory"][0],
            "effective-stark-results-00-main-paper.pdf",
        )

    def test_remote_inventory_matches_local_frozen_bytes(self):
        record = json.loads(
            (
                ROOT
                / "artifacts/zenodo-results-v1.5-draft-upload-verification-v1.json"
            ).read_text()
        )
        self.assertEqual(
            record["status"], "DRAFT_UPLOADED_VERIFIED_UNPUBLISHED"
        )
        self.assertFalse(record["draft"]["publication_action_taken"])
        for row in record["files"]:
            source = ROOT / row["source"]
            self.assertEqual(source.stat().st_size, row["bytes"])
            self.assertEqual(
                hashlib.sha256(source.read_bytes()).hexdigest(),
                row["local_sha256"],
            )

    def test_integration_audit_replays(self):
        completed = subprocess.run(
            ["python3", "scripts/audit_results_v15_integration.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(
            result["status"], "PASS_MAIN_INTEGRATION_AND_EXACT_REPLAY"
        )
        self.assertFalse(
            result["checks"]["standalone_addendum_authorized_for_v15_top_level"]
        )

    def test_v18_companion_replays_after_extraction(self):
        freeze = json.loads(
            (
                ROOT
                / "artifacts/results-paper-companion-local-freeze-v18.json"
            ).read_text()
        )
        archive = ROOT / freeze["archive"]
        self.assertEqual(
            hashlib.sha256(archive.read_bytes()).hexdigest(),
            freeze["archive_sha256"],
        )
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            with tarfile.open(archive, "r:gz") as tar:
                tar.extractall(target, filter="data")
            extracted = target / "effective-stark-results-companion-v18"
            completed = subprocess.run(
                [
                    "python3",
                    str(
                        extracted
                        / "projects/effective-stark-sweep/scripts/"
                        "verify_results_companion_v18.py"
                    ),
                    str(extracted),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("RESULTS_COMPANION_V18=VERIFIED", completed.stdout)

    def test_v15_publication_matches_the_verified_draft(self):
        publication = json.loads(
            (
                ROOT / "artifacts/zenodo-results-publication-v6.json"
            ).read_text()
        )
        draft = json.loads(
            (
                ROOT
                / "artifacts/zenodo-results-v1.5-draft-upload-verification-v1.json"
            ).read_text()
        )
        self.assertEqual(
            publication["status"], "PUBLISHED_AND_PUBLICLY_VERIFIED"
        )
        self.assertEqual(
            publication["public_download_verdict"],
            "PASS_5_OF_5_BYTE_MD5_SHA256_MATCH",
        )
        self.assertEqual(
            publication["preview"]["verdict"],
            "PASS_MAIN_PAPER_FIRST_AND_DEFAULT_PREVIEW",
        )
        published = {
            row["name"]: (row["bytes"], row["md5"], row["sha256"])
            for row in publication["files"]
        }
        frozen = {
            row["filename"]: (
                row["bytes"],
                row["remote_md5"],
                row["local_sha256"],
            )
            for row in draft["files"]
        }
        self.assertEqual(published, frozen)


if __name__ == "__main__":
    unittest.main()
