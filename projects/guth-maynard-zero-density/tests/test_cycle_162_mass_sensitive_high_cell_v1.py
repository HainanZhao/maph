import unittest
from fractions import Fraction
from conventions.mass_sensitive_high_cell_v1 import B, low_codegree_mass_upper, oriented_star_square_lower, refined_high_l1_square_lower, theorem_record

class MassSensitiveHighCellTests(unittest.TestCase):
    def test_refinement_loss_is_explicit(self):
        self.assertEqual(refined_high_l1_square_lower(Fraction(576)), Fraction(1))
        self.assertEqual(B, 288)
    def test_star_mass_is_literal_squared_edge_mass(self):
        self.assertEqual(oriented_star_square_lower(certificate_l1_square=Fraction(64), tau=Fraction(1, 4)), Fraction(1))
    def test_low_level_bound(self):
        self.assertEqual(low_codegree_mass_upper(threshold=Fraction(3), total_square_mass=Fraction(5)), Fraction(15))
    def test_boundary(self):
        self.assertIn("does not", theorem_record()["boundary"])

if __name__ == "__main__":
    unittest.main()
