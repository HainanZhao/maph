from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/dimension_six_interior_factorization_audit.py"


class DimensionSixInteriorFactorizationAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT)],
            check=True,
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        cls.data = json.loads(completed.stdout)

    def test_exact_helical_alias_reindexing(self) -> None:
        self.assertEqual(
            self.data["exact_inputs"]["alias_records_checked"],
            900,
        )
        self.assertTrue(
            self.data["exact_inputs"][
                "three_bibasic_classes_per_frequency"
            ]
        )

    def test_spectral_identity_is_verified(self) -> None:
        self.assertEqual(
            self.data["interior_meromorphic_spectral_identity"],
            "VERIFIED",
        )

    def test_pointwise_contour_claim_is_not_overstated(self) -> None:
        self.assertEqual(
            self.data["literal_pointwise_contour_periodization"],
            "OPEN",
        )
        self.assertEqual(len(self.data["pointwise_gap_list"]), 3)


if __name__ == "__main__":
    unittest.main()
