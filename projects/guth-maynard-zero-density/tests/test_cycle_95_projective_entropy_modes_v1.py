import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "conventions"))

from projective_entropy_modes_v1 import (  # noqa: E402
    laurent_coefficients,
    mode_class,
    verify_all,
)


class ProjectiveEntropyModesTests(unittest.TestCase):
    def test_central_relation(self) -> None:
        self.assertEqual(laurent_coefficients(0, 0, 3, 2, 5, 3, 3), {})
        self.assertTrue(mode_class(0, 0).exact_stationarity_possible)

    def test_u_zero(self) -> None:
        self.assertFalse(mode_class(0, 2).exact_stationarity_possible)
        self.assertEqual(mode_class(0, 2).name, "U_ZERO_V_NONZERO")

    def test_sum_zero(self) -> None:
        self.assertFalse(mode_class(3, -3).exact_stationarity_possible)
        self.assertEqual(mode_class(3, -3).name, "SUM_ZERO_U_NONZERO")

    def test_equal_nonzero_exponents(self) -> None:
        self.assertFalse(mode_class(-2, 0).exact_stationarity_possible)

    def test_general_modes(self) -> None:
        for u, v in ((1, 2), (-1, 3), (4, -1)):
            self.assertFalse(mode_class(u, v).exact_stationarity_possible)
            self.assertTrue(laurent_coefficients(u, v, 5, 3, 7, 4, 2))

    def test_verification(self) -> None:
        row = verify_all()
        self.assertIn("iff u=v=0", row["exact_mode_classification"])
        self.assertIn("no uniform lower bound", row["noncentral_boundary"])


if __name__ == "__main__":
    unittest.main()

