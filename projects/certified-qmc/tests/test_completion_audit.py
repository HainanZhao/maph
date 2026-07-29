from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from src.certificate import canonical_sha256
from scripts.audit_production_phase_completion import release_package
from scripts.finalize_supply_side_paper import replace_block


ROOT = Path(__file__).resolve().parents[1]


class CompletionAuditTests(unittest.TestCase):
    def test_completion_audit_is_self_hashed_and_requirement_complete(self):
        completed = subprocess.run(
            [
                sys.executable,
                str(
                    ROOT
                    / "scripts"
                    / "audit_production_phase_completion.py"
                ),
            ],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(completed.stdout)
        supplied = payload.pop("audit_sha256")
        self.assertEqual(supplied, canonical_sha256(payload))
        self.assertEqual(len(payload["checks"]), 14)
        names = {
            row["requirement"] for row in payload["checks"]
        }
        for cycle in ("Cycle 013", "Cycle 014", "Cycle 015",
                      "Cycles 016-017", "Cycle 018", "Cycle 019"):
            self.assertTrue(
                any(name.startswith(cycle) for name in names),
                cycle,
            )
        counted = sum(payload["counts"].values())
        self.assertEqual(counted, len(payload["checks"]))
        self.assertIn(
            payload["overall"], ("IN_PROGRESS", "COMPLETE", "FAILED")
        )

    def test_post_release_register_retains_all_promotion_controls(self):
        text = (
            ROOT / "docs" / "post-release-optimization-register.md"
        ).read_text()
        for required in (
            "Montgomery",
            "SIMD",
            "dual-shadow",
            "bit-identical",
            "published DOI",
        ):
            self.assertIn(required, text)

    def test_release_package_requires_every_manifested_file(self):
        with tempfile.TemporaryDirectory() as directory:
            release = Path(directory)
            assets = []
            for index in range(4):
                path = release / f"asset-{index}.bin"
                path.write_bytes(bytes([index]) * (index + 1))
                assets.append(
                    {
                        "filename": path.name,
                        "bytes": path.stat().st_size,
                        "sha256": sha256(path.read_bytes()).hexdigest(),
                    }
                )
            ancillary = []
            for name in ("LICENSE", "LICENSE-DATA", "REPRODUCING.md"):
                path = release / name
                path.write_text(name)
                ancillary.append(
                    {
                        "filename": path.name,
                        "bytes": path.stat().st_size,
                        "sha256": sha256(path.read_bytes()).hexdigest(),
                    }
                )
            manifest = {
                "schema": "test-release",
                "assets": assets,
                "ancillary_files": ancillary,
            }
            manifest["manifest_sha256"] = canonical_sha256(manifest)
            (release / "release-manifest.json").write_text(
                json.dumps(manifest, sort_keys=True) + "\n"
            )
            self.assertEqual(
                release_package(release)["status"], "PASSED"
            )
            (release / "LICENSE").write_text("tampered")
            self.assertEqual(
                release_package(release)["status"], "FAILED"
            )

    def test_paper_result_blocks_have_exact_marker_contract(self):
        source = (
            "before\n"
            "<!-- BEGIN GENERATED X -->\nold\n"
            "<!-- END GENERATED X -->\n"
            "after\n"
        )
        replaced = replace_block(source, "X", "new")
        self.assertIn(
            "<!-- BEGIN GENERATED X -->\n\nnew\n\n"
            "<!-- END GENERATED X -->",
            replaced,
        )
        self.assertNotIn("old", replaced)
        with self.assertRaisesRegex(ValueError, "marker contract"):
            replace_block("no markers", "X", "new")

    def test_workstream_d_recorder_is_human_explicit_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "decision.json"
            command = [
                sys.executable,
                str(
                    ROOT
                    / "scripts"
                    / "record_workstream_d_decision.py"
                ),
                "--decision",
                "public-benchmark",
                "--human-response",
                "Use the public benchmark.",
                "--output",
                str(output),
            ]
            subprocess.run(
                command,
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(output.read_text())
            supplied = payload.pop("decision_sha256")
            self.assertEqual(supplied, canonical_sha256(payload))
            self.assertEqual(
                payload["human_decision"], "public-benchmark"
            )
            self.assertTrue(payload["workstream_d_scoping_authorized"])
            repeated = subprocess.run(
                command,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(repeated.returncode, 0)
            self.assertIn(
                "already exists", repeated.stderr + repeated.stdout
            )


if __name__ == "__main__":
    unittest.main()
