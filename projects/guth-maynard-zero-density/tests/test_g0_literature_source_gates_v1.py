"""Regression tests for the bounded G0 literature/source gate audit."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "audit_g0_literature_source_gates_v1.py"
ARTIFACT = PROJECT / "artifacts" / "cycle-2-g0-literature-source-gate-audit-v1.json"


class G0LiteratureSourceGateAuditTests(unittest.TestCase):
    def test_deterministic_replay(self) -> None:
        result = subprocess.run([sys.executable, str(SCRIPT), "--check"], check=True, capture_output=True, text=True)
        self.assertIn('"verified": true', result.stdout)

    def test_all_selected_source_gates_and_scope(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        expected = {
            "MP-L24-and-GM-type-transfer", "Montgomery-discrete-MVT", "GM-internal-transfers",
            "Ingham-via-Huxley-restatement", "Huxley-near-one", "Ford-plus-Platt-VK",
            "HSW-Bui-local-multiplicity", "official-Kedlaya-formula-proof",
        }
        self.assertEqual({row["id"] for row in data["source_gates"]}, expected)
        self.assertTrue(all(row["status"] == "PROVED" for row in data["source_gates"]))
        recommendation = data["recommendation"]
        self.assertEqual((recommendation["status"], recommendation["source_hypothesis_gate"]), ("PROVED", "PASS"))
        self.assertIn("global G0 status", recommendation["not_evaluated"])

    def test_unread_and_disjunctive_sources_are_excluded_not_silenced(self) -> None:
        data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        audit = data["unread_or_disjunctive_source_audit"]
        self.assertEqual(audit["status"], "PROVED")
        self.assertIn("NO UNREAD OR DISJUNCTIVE", audit["result"])
        excluded = " ".join(audit["excluded"])
        self.assertIn("Original Ingham", excluded)
        self.assertIn("Jutila", excluded)
        self.assertIn("OBSERVED", audit["bibliographic_containment"])


if __name__ == "__main__":
    unittest.main()
