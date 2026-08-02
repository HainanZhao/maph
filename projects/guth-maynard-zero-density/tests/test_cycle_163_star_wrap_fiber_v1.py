import unittest
from fractions import Fraction
from conventions.star_wrap_fiber_v1 import wrap_fiber_ledger, theorem_record

class StarWrapFiberTests(unittest.TestCase):
    def test_exact_factorization(self):
        row = wrap_fiber_ledger(((Fraction(1), Fraction(1)), (Fraction(1),)))
        self.assertEqual(row["R"], row["R_wrap"] * row["R_fiber"])
        self.assertEqual(row["wrap_square_mass"], Fraction(5))
    def test_boundary(self): self.assertIn("does not", theorem_record()["boundary"])

if __name__ == "__main__": unittest.main()
