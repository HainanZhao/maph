import unittest

from conventions.balanced_highpass_mask_v1 import (
    circle_mean,
    gram_quadratic_form,
    positive_majorant_mass,
    signed_cell_witness,
    theorem_record,
)


class BalancedHighpassMaskTests(unittest.TestCase):
    def test_zero_fourier_mode(self) -> None:
        self.assertEqual(circle_mean({-1: 2, 1: 2}), 0j)
        self.assertEqual(circle_mean({0: 3, 1: 2}), 3)

    def test_gram_form_is_nonnegative(self) -> None:
        value = gram_quadratic_form(
            (-1, 1),
            (2.0, 3.0),
            (1 + 1j, 2 - 1j),
            (1 + 0j, 0 + 1j),
        )
        self.assertGreaterEqual(value, 0.0)

    def test_signed_cell_average_witness(self) -> None:
        rows = (-4.0, 7.0, 3.0, 2.0)
        index, value = signed_cell_witness(rows)
        self.assertEqual((index, value), (1, 7.0))
        self.assertGreaterEqual(value, sum(rows) / len(rows))

    def test_majorant_zero_mode_cost(self) -> None:
        self.assertEqual(100 * positive_majorant_mass(0.01), 1.0)

    def test_record_keeps_halo_and_entropy(self) -> None:
        row = theorem_record()
        self.assertIn("halo", row["balanced_real_part"])
        self.assertIn("E/P", row["signed_partition"])
        self.assertIn("no arithmetic cell", row["boundary"])


if __name__ == "__main__":
    unittest.main()
