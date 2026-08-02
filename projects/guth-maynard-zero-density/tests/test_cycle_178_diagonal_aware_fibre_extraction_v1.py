from fractions import Fraction as Q
import unittest

from conventions.diagonal_aware_fibre_extraction_v1 import cross_label_remainder, extract_seeded_packet, verify_all


class Cycle178DiagonalAwareFibreExtractionTest(unittest.TestCase):
    def test_replay(self) -> None:
        rows = verify_all()
        self.assertIn("actual fixed-beta fibre", rows["theorem"])

    def test_near_cutoff_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "integer-forcing cutoff"):
            extract_seeded_packet(
                [(1, 0), (2, 0), (3, 0)],
                alpha=Q(0), beta=Q(0), x=4, height=1, strip_constant=1,
            )

    def test_light_cross_identity(self) -> None:
        result = cross_label_remainder([1, 2, 3], threshold=2)
        self.assertTrue(result["light"])
        self.assertEqual(result["ordered_cross_label_mass"], 22)
        self.assertGreaterEqual(result["ordered_cross_label_mass"], result["light_cross_lower_bound"])

    def test_minimum_gap_need_not_be_first(self) -> None:
        output = extract_seeded_packet(
            [(20, 10), (26, 13), (28, 14), (40, 20)],
            alpha=Q(1, 2), beta=Q(0), x=1000, height=20, strip_constant=1,
        )
        self.assertEqual(output["minimum_gap"]["left_row_index"], 1)
        self.assertEqual(output["seed"]["h"], 20)


if __name__ == "__main__":
    unittest.main()
