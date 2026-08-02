import unittest
from fractions import Fraction
from conventions.wrap_valuation_sidon_v1 import high_fiber_mass_lower, integer_forcing_bound, theorem_record
class T(unittest.TestCase):
 def test_ledgers(self): self.assertEqual(high_fiber_mass_lower(Fraction(8)), Fraction(4)); self.assertLess(integer_forcing_bound(3, 7), 1)
 def test_boundary(self): self.assertIn("does not", theorem_record()["boundary"])
if __name__=="__main__": unittest.main()
