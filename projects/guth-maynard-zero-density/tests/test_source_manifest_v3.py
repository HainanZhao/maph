"""Regression tests for the source-manifest v3 inventory correction."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "build_source_manifest_v3.py"
ARTIFACT = PROJECT / "artifacts" / "source-manifest-verification-v3.json"
SOURCES = PROJECT / "artifacts" / "sources"
CANONICAL = {
    "arxiv-2405.20552v2/00README.json",
    "arxiv-2405.20552v2/LargevaluesDirichlet17.tex",
    "chourasiya-simonic-2025-explicit-ingham/00README.json",
    "chourasiya-simonic-2025-explicit-ingham/InghamPostArXiv.tex",
    "maynard-pratt-2206.11729/HalfIsolatedv2.tex",
}


class SourceManifestV3Tests(unittest.TestCase):
    def test_frozen_inventory_replays(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT), "--check"], check=True)

    def test_direct_and_extracted_coverage_is_exact(self) -> None:
        manifest = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        direct = {row["relative_path"] for row in manifest["items"] if row["scope"] == "direct_source_file"}
        self.assertEqual(direct, {path.name for path in SOURCES.iterdir() if path.is_file()})
        extracted = {row["relative_path"] for row in manifest["items"] if row["scope"] == "extracted_canonical_input"}
        self.assertEqual(extracted, CANONICAL)
        self.assertEqual(len(direct), 36)
        self.assertEqual(len(extracted), 5)

    def test_access_correction_and_consumer_exclusion(self) -> None:
        manifest = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        rows = {row["relative_path"]: row for row in manifest["items"]}
        for name in ("kedlaya-2007-errorbounds-author.pdf", "kedlaya-2007-von-mangoldt-author.pdf"):
            access = rows[name]["license_or_access_class"]
            self.assertIn("direct author-primary", access)
            self.assertIn("no CC licence", access)
        for name in (
            "mit-dspace-1721.1-101679-metadata.json",
            "mit-ocw-18-785-2007-sword-official.zip",
            "mit-ocw-18-785-2007-errorbounds-official.pdf",
            "mit-ocw-18-785-2007-von-mangoldt-official.pdf",
        ):
            self.assertIn("CC BY-NC-SA 3.0", rows[name]["license_or_access_class"])
        self.assertNotIn("proof_script_consumers", json.dumps(manifest))
        self.assertTrue(manifest["inventory_rules"]["g0_consumer_scope"].startswith("OMITTED_BY_DESIGN"))
        self.assertEqual(manifest["v2_correction"]["epistemic_status"], "PROVED")
        self.assertEqual(manifest["policy_absences"][0]["access_class"], "ABSENT_BY_POLICY")

    def test_duplicate_aliases_are_retained(self) -> None:
        manifest = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        groups = {tuple(group["members"]) for group in manifest["explicit_duplicate_alias_groups"]}
        self.assertIn(("arxiv-2405.20552v2.tar", "guth-maynard-2405.20552v2-source.tar"), groups)
        self.assertIn(("arxiv-2405.20552v2.pdf", "guth-maynard-2405.20552v2.pdf"), groups)
        self.assertIn(("guth-maynard-annals-aam.pdf", "ora-accepted-manuscript.pdf"), groups)


if __name__ == "__main__":
    unittest.main()
