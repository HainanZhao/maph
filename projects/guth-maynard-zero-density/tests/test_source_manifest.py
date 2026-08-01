import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "verify_source_manifest.py"


class SourceManifestTests(unittest.TestCase):
    def test_all_frozen_sources_match_hash_and_size(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT)],
            check=True,
            capture_output=True,
            text=True,
        )
        result = json.loads(completed.stdout)
        self.assertTrue(result["verified"])
        self.assertEqual(len(result["sources"]), 3)
        self.assertTrue(all(row["verified"] for row in result["sources"]))


if __name__ == "__main__":
    unittest.main()
