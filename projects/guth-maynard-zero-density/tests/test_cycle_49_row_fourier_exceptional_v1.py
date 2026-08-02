from fractions import Fraction as Q
import unittest

from conventions.row_fourier_exceptional_v1 import absolute_lcam_gap, exceptional_exponent, verify_all


class Cycle49RowFourierExceptionalTests(unittest.TestCase):
    def test_registered_exceptional_sets(self) -> None:
        self.assertEqual(exceptional_exponent(Q(7, 50)), Q(-13, 50))
        self.assertEqual(exceptional_exponent(Q(4, 25)), Q(-11, 50))
        self.assertEqual(exceptional_exponent(Q(17, 50)), Q(7, 50))

    def test_mean_square_scales(self) -> None:
        row = verify_all()["mean_square"]
        self.assertEqual(row["diagonal"], Q(57, 50))
        self.assertEqual(row["off_diagonal_absolute_bound"], Q(6, 25))
        self.assertEqual(row["off_diagonal_gap_below_diagonal"], Q(9, 10))

    def test_absolute_pairing_does_not_close(self) -> None:
        self.assertEqual(absolute_lcam_gap(4, Q(7, 50)), Q(39, 10))
        self.assertEqual(absolute_lcam_gap(3, Q(17, 50)), Q(27, 10))

    def test_gap_is_positive(self) -> None:
        for gap in verify_all()["absolute_lcam_gaps"].values():
            self.assertGreater(gap, 0)


if __name__ == "__main__":
    unittest.main()
