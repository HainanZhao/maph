"""Tests for the Cycle 2 Stream B Route A source-level audit."""

import ast
import importlib.util
import json
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "audit_cycle2_stream_b_route_a.py"
ARTIFACT = PROJECT / "artifacts" / "cycle-2-stream-b-route-a-v1.json"


def load_module():
    spec = importlib.util.spec_from_file_location("cycle2_stream_b_route_a", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CycleTwoStreamBRouteATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def test_every_preregistered_transfer_is_present(self):
        report = self.module.build_report()
        rows = {row["id"]: row for row in report["rows"]}
        self.assertEqual(len(rows), 13)
        for key in (
            "SB-A1-smoothing-identity",
            "SB-A2-uniform-smooth-cutoff-and-fourier-tail",
            "SB-A4-local-zero-count-and-separated-extraction",
            "SB-A7-original-detector-coefficients",
            "SB-A10-powered-coefficients-and-normalization",
            "SB-A11-support-dyadic-decomposition-and-threshold-transfer",
            "SB-A13-mean-value-branch-hypotheses",
        ):
            self.assertIn(key, rows)
        self.assertEqual(rows["SB-A8-bounded-k-small-regime"]["scope"], "small-n regime")
        self.assertEqual(rows["SB-A9-bounded-k-large-regime"]["scope"], "large-n regime")

    def test_blockers_are_retained_not_promoted(self):
        report = self.module.build_report()
        self.assertEqual(
            report["blockers"],
            [
                "SB-A4-local-zero-count-and-separated-extraction",
                "SB-A13-mean-value-branch-hypotheses",
            ],
        )
        self.assertIn("NOT PASS", report["pass_state"])
        rows = {row["id"]: row for row in report["rows"]}
        self.assertEqual(rows["SB-A4-local-zero-count-and-separated-extraction"]["status"], "OBSERVED")
        self.assertEqual(rows["SB-A13-mean-value-branch-hypotheses"]["status"], "OBSERVED")

    def test_no_float_literals_in_audit_script(self):
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
        self.assertEqual(
            [node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, float)],
            [],
        )

    def test_sealed_report_hashes_the_report(self):
        artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        body = {
            key: value
            for key, value in artifact.items()
            if key not in {"mathematical_and_source_audit_sha256", "replay"}
        }
        self.assertEqual(
            artifact["mathematical_and_source_audit_sha256"], self.module.canonical_sha256(body)
        )
        self.assertEqual(artifact["replay"]["script_sha256"], self.module.sha256(SCRIPT))


if __name__ == "__main__":
    unittest.main()
