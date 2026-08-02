import unittest

from conventions.coordinate_anova_v1 import anova_ledger, component_types, verify_all


class Cycle60CoordinateAnovaTests(unittest.TestCase):
    def test_s3_counts(self) -> None:
        data = anova_ledger(3)
        self.assertEqual(data["subset_component_count"], 16)
        self.assertEqual(data["nonconstant_component_count"], 15)
        self.assertEqual(data["symmetry_type_count"], 8)

    def test_s4_counts(self) -> None:
        data = anova_ledger(4)
        self.assertEqual(data["subset_component_count"], 32)
        self.assertEqual(data["nonconstant_component_count"], 31)
        self.assertEqual(data["symmetry_type_count"], 10)

    def test_type_multiplicities(self) -> None:
        self.assertEqual(sum(row["subset_multiplicity"] for row in component_types(4)), 32)

    def test_distinguished_components(self) -> None:
        rows = component_types(4)
        self.assertEqual(sum(bool(row["is_constant_component"]) for row in rows), 1)
        self.assertEqual(sum(bool(row["is_full_interaction"]) for row in rows), 1)

    def test_full_kernel(self) -> None:
        data = verify_all()
        self.assertIn("C_m(h_e,h_f)", data["s4"]["full_interaction_quadratic_norm"])


if __name__ == "__main__":
    unittest.main()
