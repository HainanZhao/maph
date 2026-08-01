from __future__ import annotations

from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CensusPaperManuscriptTest(unittest.TestCase):
    def test_cycle_130_referee_clarifications(self):
        source = (ROOT / "paper/effective-stark-census.tex").read_text()
        self.assertIn("2461+5739=8200", source)
        self.assertNotIn("2461+\\frac{11478}{2}=8200", source)
        self.assertIn("\\renewcommand{\\theenumi}{\\roman{enumi}}", source)
        self.assertIn("Prop.~4 and Eq.~(9)", source)
        self.assertIn("no doubly assigned row", source)
        self.assertIn("not a general theorem", source)
        self.assertIn("Of those 382, 309 complete", source)
        self.assertIn("48 reuse full \\texttt{bnfcertify}", source)
        self.assertIn("remaining 73", source)

    def test_compiled_manuscript_matches_frozen_artifacts(self):
        completed = subprocess.run(
            ["python3", "scripts/audit_census_paper.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("CENSUS_PAPER_AUDIT=PASS", completed.stdout)

    def test_cycle_127_referee_boundary(self):
        completed = subprocess.run(
            ["python3", "scripts/audit_census_referee_revision.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn(
            "CENSUS_REFEREE_REVISION_AUDIT=PASS", completed.stdout
        )

    def test_quadratic_deleted_prime_cover_theorem(self):
        completed = subprocess.run(
            ["python3", "proof/audit_q_euler_deleted_prime_cover.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn(
            "Q_EULER_DELETED_PRIME_COVER_THEOREM=PASS",
            completed.stdout,
        )
        self.assertIn(
            "Q_FOUR_SUPPORT_NONDEGENERACY=REFUTED",
            completed.stdout,
        )

    def test_all_order_deleted_prime_cover_audit(self):
        completed = subprocess.run(
            ["python3", "proof/audit_h_all_order_deleted_prime_cover.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn(
            "H_ALL_ORDER_DELETED_PRIME_COVER_AUDIT=PASS",
            completed.stdout,
        )
        self.assertIn("RQ_000692_ALL_ORDER_COVER=NO", completed.stdout)

    def test_corrected_direct_source_transport_audit(self):
        completed = subprocess.run(
            ["python3", "proof/audit_corrected_direct_source_transports.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            timeout=60,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn(
            "CORRECTED_DIRECT_SOURCE_TRANSPORT_AUDIT=PASS",
            completed.stdout,
        )


if __name__ == "__main__":
    unittest.main()
