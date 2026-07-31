import hashlib
import json
from pathlib import Path
import subprocess
import tarfile
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ResultsPaperTrackA2Test(unittest.TestCase):
    def test_publication_candidate_v2_hashes_every_top_level_file(self):
        candidate = json.loads(
            (
                ROOT
                / "artifacts/results-paper-v1.4-publication-candidate-v2.json"
            ).read_text()
        )
        self.assertFalse(candidate["claim_boundary"]["doi_reserved"])
        self.assertFalse(
            candidate["claim_boundary"]["publication_action_taken"]
        )
        for row in candidate["proposed_top_level_files"]:
            path = ROOT / row["source"]
            self.assertEqual(path.stat().st_size, row["bytes"])
            self.assertEqual(
                hashlib.sha256(path.read_bytes()).hexdigest(),
                row["sha256"],
            )
        metadata = candidate["metadata"]
        self.assertEqual(
            hashlib.sha256((ROOT / metadata["path"]).read_bytes()).hexdigest(),
            metadata["sha256"],
        )

    def test_exact_v13_to_v14_editorial_diff(self):
        completed = subprocess.run(
            ["python3", "scripts/audit_results_paper_a2.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("RESULTS_PAPER_TRACK_A2_AUDIT=PASS", completed.stdout)

    def test_v16_pre_doi_companion_replays_after_extraction(self):
        freeze = json.loads(
            (
                ROOT
                / "artifacts/results-paper-companion-local-freeze-v16.json"
            ).read_text()
        )
        self.assertEqual(freeze["status"], "LOCAL_FROZEN_PRE_DOI_NOT_PUBLIC")
        archive = ROOT / freeze["archive"]
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            with tarfile.open(archive, "r:gz") as tar:
                tar.extractall(target, filter="data")
            extracted = target / "effective-stark-results-companion-v16"
            completed = subprocess.run(
                [
                    "python3",
                    str(
                        extracted
                        / "projects/effective-stark-sweep/scripts/"
                        "verify_results_companion_v16.py"
                    ),
                    str(extracted),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("RESULTS_COMPANION_V16=VERIFIED", completed.stdout)


if __name__ == "__main__":
    unittest.main()
