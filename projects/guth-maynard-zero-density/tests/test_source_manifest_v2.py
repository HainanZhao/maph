import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "build_source_manifest_v2.py"
ARTIFACT = PROJECT / "artifacts" / "source-manifest-verification-v2.json"
SOURCES = PROJECT / "artifacts" / "sources"


class SourceManifestV2Tests(unittest.TestCase):
    def test_manifest_fails_closed_after_official_source_additions(self) -> None:
        """V2 is historical: its checker must reject the enlarged inventory."""
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--check"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("direct-source metadata coverage changed", result.stderr)

    def test_exact_v2_inventory_delta_is_preserved(self) -> None:
        manifest = json.loads(ARTIFACT.read_text())
        expected = {path.name for path in SOURCES.iterdir() if path.is_file()}
        actual = {
            row["relative_path"]
            for row in manifest["items"]
            if row["scope"] == "direct_source_file"
        }
        self.assertEqual(
            expected - actual,
            {
                "mit-dspace-1721.1-101679-metadata.json",
                "mit-ocw-18-785-2007-errorbounds-official.pdf",
                "mit-ocw-18-785-2007-sword-official.zip",
                "mit-ocw-18-785-2007-von-mangoldt-official.pdf",
            },
        )
        self.assertEqual(actual - expected, set())
        self.assertTrue(all(row["epistemic_status"] == "OBSERVED" for row in manifest["items"]))

    def test_aliases_and_restricted_iwaniec_absence_are_explicit(self) -> None:
        manifest = json.loads(ARTIFACT.read_text())
        groups = {tuple(group["members"]) for group in manifest["explicit_duplicate_alias_groups"]}
        self.assertIn(
            ("arxiv-2405.20552v2.tar", "guth-maynard-2405.20552v2-source.tar"),
            groups,
        )
        self.assertIn(
            ("arxiv-2405.20552v2.pdf", "guth-maynard-2405.20552v2.pdf"),
            groups,
        )
        self.assertIn(
            ("guth-maynard-annals-aam.pdf", "ora-accepted-manuscript.pdf"),
            groups,
        )
        self.assertEqual(manifest["policy_absences"][0]["access_class"], "ABSENT_BY_POLICY")


if __name__ == "__main__":
    unittest.main()
