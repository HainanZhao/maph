import unittest

from discovery.audit_g1_explicit_common_basis import excluded_pairs
from discovery.audit_g1_opposite_explicit_all_width import audit as audit_opposite
from proof.verify_g1_arbitrary_width_generic_tightness import verify


class G1ArbitraryWidthTests(unittest.TestCase):
    def test_common_basis_regression_through_width_eight(self):
        payload = verify(8)
        self.assertEqual(payload["checked_widths"], [4, 8])
        for row in payload["rows"]:
            width = row["width"]
            self.assertEqual(row["common_basis_edges"], width * width - 1)
            self.assertEqual(row["terminal_homology_rank"], width * width - 1)
            self.assertEqual(row["dual_p_components"], 1)
            self.assertEqual(row["dual_x_components"], width // 2)
            self.assertEqual(row["dual_x_components"], row["dual_all_components"])

    def test_exceptional_formula_cardinality(self):
        for width in range(4, 31):
            k = width // 2
            expected = k - 1 + (k - 2) * (k - 3) // 2
            self.assertEqual(len(excluded_pairs(width)), expected)

    def test_opposite_phase_candidate_through_width_eight(self):
        payload = audit_opposite(8)
        for row in payload["rows"]:
            width = row["width"]
            self.assertTrue(row["tree_connected"])
            self.assertEqual(row["tree_edge_count"], row["target_tree_edge_count"])
            self.assertEqual(row["common_basis_count"], width * width - 1)
            self.assertEqual(row["terminal_rank"], width * width - 1)
            self.assertTrue(row["each_component_has_one_terminal"])
            self.assertTrue(row["dual_complement_connected"])


if __name__ == "__main__":
    unittest.main()
