from fractions import Fraction as Q
import unittest

from conventions.freiman_phase_web_v1 import (
    geometric_height_lower_exponent,
    relation_ledger,
    valuation_relation,
    verify_all,
)


class Cycle78FreimanPhaseWebTests(unittest.TestCase):
    def test_exactness_margin(self) -> None:
        row = relation_ledger()
        self.assertEqual(row["ratio_error_exponent"], -Q(36, 25))
        self.assertEqual(row["cross_error_exponent"], -Q(8, 75))
        self.assertEqual(row["exactness_margin"], Q(8, 75))

    def test_valuation_completion(self) -> None:
        self.assertEqual(valuation_relation(5, -1, 2), 2)

    def test_height_encoding(self) -> None:
        self.assertEqual(geometric_height_lower_exponent(11), (11, -2))
        with self.assertRaises(ValueError):
            geometric_height_lower_exponent(-1)

    def test_verification(self) -> None:
        rows = verify_all()
        self.assertIn("r_0*g^j", rows["progression_image"])
        self.assertIn("Sidon", rows["scope_boundary"])


if __name__ == "__main__":
    unittest.main()
