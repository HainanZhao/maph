"""Regression checks for the independent P6 CGL-v2 Route B package."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "proof/p6_cgl_v2_route_b_v1.py"
ARTIFACT = ROOT / "artifacts/p6-cgl-v2-route-b-v1.json"


class P6CGLV2RouteBV1Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(ARTIFACT.read_text())
        cls.by_id = {item["id"]: item for item in cls.data["rows"]}

    def test_replay_and_script_identity(self) -> None:
        check = subprocess.run([sys.executable, str(SCRIPT), "--check"], cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(check.returncode, 0, check.stderr)
        self.assertEqual(self.data["sealer"]["sha256"], hashlib.sha256(SCRIPT.read_bytes()).hexdigest())
        self.assertIn("wall_ns", check.stdout)
        self.assertIn("peak_rss_kib", check.stdout)

    def test_canonical_46_rows_and_l12_subchecks(self) -> None:
        expected = [*(f"S{i:02d}" for i in range(1, 7)), *(f"L{i:02d}" for i in range(1, 13)), *(f"M{i:02d}" for i in range(1, 9)), *(f"Z{i:02d}" for i in range(1, 11)), *(f"F{i:02d}" for i in range(1, 11))]
        self.assertEqual([item["id"] for item in self.data["rows"]], expected)
        self.assertEqual(self.data["canonical_row_count"], 46)
        self.assertEqual(self.data["mandatory_l12_subchecks"], ["L12.odd_prime", "L12.two_power"])
        self.assertEqual([item["id"] for item in self.by_id["L12"]["subchecks"]], ["L12.odd_prime", "L12.two_power"])

    def test_exact_crossings_and_uniform_margins(self) -> None:
        algebra = self.data["exact_algebra"]
        self.assertEqual(algebra["crossings"]["C3_polynomial"], "20*sigma^2-(43-3*beta)*sigma+24-6*beta")
        self.assertEqual(algebra["crossings"]["C4_sigma"], "7/10")
        self.assertEqual(algebra["crossings"]["C4_in_ingham"], "30/13")
        self.assertEqual(algebra["q1_equals_q"]["bases_or_coefficients"], ["q^(7/3)*T^2", "9/4", "(10-sqrt(10))/3", "30/13"])
        self.assertIn("7/3-30/13=1/39", algebra["q1_equals_q"]["uniform_comparisons"])

    def test_known_analytic_gaps_remain_open(self) -> None:
        blockers = set(self.data["open_blockers"])
        self.assertTrue({"S06_EXTERNAL_INPUTS", "Z03_TAIL_X_RANGE", "Z05_PRIMITIVE_EULER_FACTORS", "Z06_CONDUCTOR_SUM_Q1", "F08_T_SMOOTH_UNDEFINED"}.issubset(blockers))
        self.assertEqual(self.data["overall_disposition"], "OPEN_ANALYTIC_INPUT")
        self.assertIn("No q<=T^C restriction", self.data["unrepaired_gaps"]["tail"])
        self.assertIn("No definition of T-smooth", self.data["unrepaired_gaps"]["smoothness"])

    def test_no_route_a_dependency(self) -> None:
        source = SCRIPT.read_text().lower()
        self.assertNotIn("route_a", source)
        self.assertIn("does\nnot import a literal theorem-chain reconstruction", source)


if __name__ == "__main__":
    unittest.main()
