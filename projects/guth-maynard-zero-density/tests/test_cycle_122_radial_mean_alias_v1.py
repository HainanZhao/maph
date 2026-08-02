import unittest
from fractions import Fraction

from conventions.radial_mean_alias_v1 import alias_exponent_ledger, theorem_record


class RadialMeanAliasTests(unittest.TestCase):
    def test_left_endpoint_amplitude(self) -> None:
        row = alias_exponent_ledger(Fraction(16, 25))
        self.assertEqual(row["n_stationary_amplitude"], Fraction(-23, 150))
        self.assertEqual(row["Hc_scale"], Fraction(73, 75))

    def test_record(self) -> None:
        row = theorem_record()
        self.assertIn("U^(j)(0)=0", row["vanishing_moments"])
        self.assertIn("(cH0)^(-N)", row["zero_mode"])
        self.assertIn("n*=Hc/ell", row["nonzero_saddle"])
        self.assertIn("ell~K", row["alias_support"])
        self.assertIn("no bound", row["boundary"])

    def test_rejects_upper_edge(self) -> None:
        with self.assertRaises(ValueError):
            alias_exponent_ledger(Fraction(58, 75))


if __name__ == "__main__":
    unittest.main()
