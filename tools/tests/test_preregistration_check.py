from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.preregistration_check import PreflightError, validate_preregistration


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PROJECT = REPOSITORY_ROOT / "projects/guth-maynard-zero-density"


def write_preregistration(root: Path, manifest: dict[str, object]) -> Path:
    (root / "artifacts").mkdir()
    (root / "artifacts/input.json").write_text("{}\n")
    docs = root / "docs"
    docs.mkdir()
    path = docs / "cycle-999-fixture-preregistration-v1.md"
    path.write_text("# Fixture\n\n<!-- research-freeze-v1\n" + json.dumps(manifest, indent=2) + "\n-->\n")
    return path


def valid_manifest() -> dict[str, object]:
    entry = {"kind": "expression", "value": "X^(1/2)", "rationale": "frozen fixture"}
    return {
        "schema": "research-preregistration-freeze-v1",
        "cycle": 999,
        "parameters": {"scale": entry},
        "resource_caps": {"search": {"kind": "integer", "value": 0, "rationale": "no search"}},
        "formula_families": ["exact fixture identity"],
        "selection_rule": ["fixed fixture row"],
        "failure_rule": ["reject malformed field"],
        "pre_execution": {"timestamp_utc": "2026-08-02T00:00:00Z", "git_head": "UNBORN", "git_state": "fixture"},
        "input_paths": ["artifacts/input.json"],
    }


class PreregistrationCheckTest(unittest.TestCase):
    def test_valid_manifest_and_input_hash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            path = write_preregistration(root, valid_manifest())
            checked = validate_preregistration(path, expected_cycle=999)
            self.assertEqual(checked["cycle"], 999)
            self.assertEqual(checked["input_hashes"][0]["path"], "artifacts/input.json")

    def test_head_drift_requires_explicit_replay_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            manifest = valid_manifest()
            manifest["pre_execution"]["git_head"] = "not-current"
            path = write_preregistration(root, manifest)
            with self.assertRaisesRegex(PreflightError, "head drift"):
                validate_preregistration(path)
            self.assertEqual(validate_preregistration(path, enforce_manifest_head=False)["cycle"], 999)

    def test_rejects_placeholder_and_missing_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            manifest = valid_manifest()
            manifest["parameters"] = {"scale": {"kind": "symbolic", "value": "", "rationale": "bad"}}
            path = write_preregistration(root, manifest)
            with self.assertRaisesRegex(PreflightError, "missing value"):
                validate_preregistration(path)
            path.write_text("# no freeze\n")
            with self.assertRaisesRegex(PreflightError, "exactly one"):
                validate_preregistration(path)

    def test_legacy_frozen_cycles_are_detected_not_rewritten(self) -> None:
        docs = [
            PROJECT / "docs/cycle-181-common-intercept-packet-preregistration-v1.md",
            PROJECT / "docs/cycle-182-fibre-line-rigidity-preregistration-v1.md",
        ]
        for path in docs:
            with self.assertRaisesRegex(PreflightError, "exactly one"):
                validate_preregistration(path)


if __name__ == "__main__":
    unittest.main()
