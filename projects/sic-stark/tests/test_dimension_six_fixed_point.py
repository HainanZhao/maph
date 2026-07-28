from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DimensionSixFixedPointTests(unittest.TestCase):
    def test_divisibility_is_equivalent_to_fixed_point_vanishing(self) -> None:
        output = subprocess.check_output(
            [
                sys.executable,
                str(
                    ROOT
                    / "scripts"
                    / "dimension_six_fixed_point_equivalence.py"
                ),
            ],
            text=True,
        )
        result = json.loads(output)
        self.assertEqual(result["fixed_point_zero_order"], 1)
        self.assertEqual(result["denominator_norm"], 1)
        self.assertIn(
            "iff F(beta)=0",
            result["defect_conclusion"],
        )


if __name__ == "__main__":
    unittest.main()
