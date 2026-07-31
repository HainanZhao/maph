import hashlib
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ResultsPaperTrackA2Test(unittest.TestCase):
    def test_uploaded_candidate_v4_hashes_every_top_level_file(self):
        candidate = json.loads(
            (
                ROOT
                / "artifacts/results-paper-v1.4-publication-candidate-v4.json"
            ).read_text()
        )
        self.assertEqual(
            candidate["status"],
            "DRAFT_UPLOADED_VERIFIED_AWAITING_EXPLICIT_PUBLISH_APPROVAL",
        )
        self.assertFalse(candidate["draft"]["publication_action_taken"])
        sources = {
            "effective-stark-results-companion-v17.tar.gz":
                "dist/effective-stark-results-companion-v17.tar.gz",
            "effective-stark-results-supplement-rq000013-addendum.pdf":
                "paper/effective-stark-results-supplement-rq000013-addendum.pdf",
            "effective-stark-results-supplement-rq000013-addendum.tex":
                "paper/effective-stark-results-supplement-rq000013-addendum.tex",
            "effective-stark-results-supplement.pdf":
                "paper/effective-stark-results-supplement.pdf",
            "effective-stark-results-supplement.tex":
                "paper/effective-stark-results-supplement.tex",
            "effective-stark-results.pdf":
                "paper/effective-stark-results.pdf",
            "effective-stark-results.tex":
                "paper/effective-stark-results.tex",
        }
        self.assertEqual(set(sources), {row["filename"] for row in candidate["files"]})
        publication = json.loads(
            (
                ROOT / "artifacts/zenodo-results-publication-v5.json"
            ).read_text()
        )
        public_rows = {row["name"]: row for row in publication["files"]}
        for row in candidate["files"]:
            published = public_rows[row["filename"]]
            self.assertEqual(published["bytes"], row["bytes"])
            self.assertEqual(published["sha256"], row["local_sha256"])
        metadata = candidate["metadata"]
        self.assertEqual(
            hashlib.sha256(
                (ROOT / metadata["local_source"]).read_bytes()
            ).hexdigest(),
            metadata["local_sha256"],
        )

    def test_exact_v13_to_v14_editorial_diff(self):
        audit = json.loads(
            (
                ROOT
                / "artifacts/results-paper-release-doi-audit-v1.json"
            ).read_text()
        )
        self.assertEqual(
            audit["status"], "PASS_EXACT_RELEASE_SOURCE_DELTA"
        )
        self.assertEqual(
            audit["mathematical_claim_change_from_pre_doi_freeze"], "NONE"
        )

    def test_v17_doi_bearing_companion_replays_after_extraction(self):
        freeze = json.loads(
            (
                ROOT
                / "artifacts/results-paper-companion-local-freeze-v17.json"
            ).read_text()
        )
        self.assertEqual(
            freeze["status"], "LOCAL_FROZEN_DOI_BEARING_NOT_PUBLIC"
        )
        archive = ROOT / freeze["archive"]
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            with tarfile.open(archive, "r:gz") as tar:
                tar.extractall(target, filter="data")
            extracted = target / "effective-stark-results-companion-v17"
            completed = subprocess.run(
                [
                    "python3",
                    str(
                        extracted
                        / "projects/effective-stark-sweep/scripts/"
                        "verify_results_companion_v17.py"
                    ),
                    str(extracted),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("RESULTS_COMPANION_V17=VERIFIED", completed.stdout)

    def test_v14_publication_record_matches_the_frozen_candidate(self):
        publication = json.loads(
            (
                ROOT / "artifacts/zenodo-results-publication-v5.json"
            ).read_text()
        )
        candidate = json.loads(
            (
                ROOT
                / "artifacts/results-paper-v1.4-publication-candidate-v4.json"
            ).read_text()
        )
        self.assertEqual(
            publication["status"], "PUBLISHED_AND_PUBLICLY_VERIFIED"
        )
        self.assertTrue(publication["publication_response"]["submitted"])
        self.assertEqual(publication["publication_response"]["state"], "done")
        self.assertEqual(
            publication["public_download_verdict"],
            "PASS_7_OF_7_BYTE_MD5_SHA256_MATCH",
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
            for row in candidate["files"]
        }
        self.assertEqual(published, frozen)


if __name__ == "__main__":
    unittest.main()
