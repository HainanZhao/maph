import unittest

from conventions.anchored_fibre_product_determinant_v1 import (
    Anchor,
    convex_four_anchor_lower,
    determinant3,
    difference_data,
    first_rank_two_data,
    pair_mass,
    packet_safety,
    primitive_rank_one_data,
    terminal_bank,
    theorem_record,
)


class Cycle165AnchoredFibreProductTests(unittest.TestCase):
    def test_pair_mass_identity(self):
        self.assertEqual(pair_mass((3, 2, 1)), 11)

    def test_balanced_convexity_bound(self):
        # 11 anchors distributed among three label pairs: 4,4,3 is extremal.
        self.assertEqual(convex_four_anchor_lower(11, 3), 2)

    def test_exact_rank_two_determinant_and_cramer_signs(self):
        # alpha=1/3, alpha'=1/5, beta=0; each row is an exact strip hit.
        anchors = (
            Anchor(3, 5, 1, 1),
            Anchor(6, 10, 2, 2),
            Anchor(9, 5, 3, 1),
            Anchor(3, 15, 1, 3),
        )
        d, dp, k = difference_data(anchors)
        self.assertEqual(determinant3(d, tuple(-x for x in dp), k), 0)
        data = first_rank_two_data(d, dp, k)
        self.assertIsNotNone(data)
        assert data is not None
        self.assertEqual(data.denominator, -30)
        self.assertEqual(data.numerator, -10)
        self.assertEqual(data.numerator_prime, -6)
        self.assertEqual(data.content, 10)
        self.assertEqual(data.content_prime, 6)

    def test_disjoint_terminal_priority(self):
        self.assertEqual(terminal_bank((1, 2, 3), (2, 4, 6), (3, 6, 9), high_content=2), "rank_one_resonance")
        self.assertEqual(terminal_bank((3, 6, 0), (5, 0, 10), (0, 0, 0), high_content=5), "rank_two_high_first_seeded_packet")

    def test_signed_reduction_and_packet_safety(self):
        ledger = packet_safety(-30, -10, strip_constant=1, h_diameter=10)
        self.assertEqual((ledger["q"], ledger["a"], ledger["content"]), (3, 1, 10))
        self.assertTrue(ledger["range_safe"])
        self.assertTrue(ledger["error_interface"])
        self.assertEqual(ledger["C_star"], 1)

    def test_rank_one_resonance_vector(self):
        # alpha=1/3, alpha'=1/5: d=3v, d'=5v, k=0v.
        self.assertEqual(
            primitive_rank_one_data((3, 6, 9), (5, 10, 15), (0, 0, 0)),
            (3, 5, 0, (1, 2, 3)),
        )

    def test_claim_boundary(self):
        self.assertIn("does not bound", theorem_record()["boundary"])


if __name__ == "__main__":
    unittest.main()
