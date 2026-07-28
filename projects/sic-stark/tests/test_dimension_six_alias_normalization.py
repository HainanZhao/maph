from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "dimension_six_alias_normalization.py"


class DimensionSixAliasNormalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            ["python3", str(SCRIPT)],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.payload = json.loads(completed.stdout)

    def test_normalized_packet_stays_at_minus_q(self) -> None:
        self.assertIn(";q,-q)", self.payload["normalized_alias_series"])

    def test_fourier_gauge_is_separate(self) -> None:
        ratios = self.payload["ratios"]
        self.assertEqual(ratios["Z_times_Bernoulli"]["value"], "+1")
        self.assertEqual(ratios["extracted_Fourier_gauge"]["value"], "-q")
        self.assertEqual(
            self.payload["ordinary_transform_alias_argument"],
            "q^2",
        )

    def test_bailey_gap_is_not_overclaimed(self) -> None:
        self.assertTrue(
            self.payload["normalization_does_not_close_Bailey_gap"]
        )


if __name__ == "__main__":
    unittest.main()
