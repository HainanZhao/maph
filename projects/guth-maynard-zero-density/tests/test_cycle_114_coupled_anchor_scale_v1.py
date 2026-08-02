import unittest

from conventions.coupled_anchor_scale_v1 import anchor_height_bound, gcd_convolution_expansion, gcd_convolution_sum, theorem_record


class CoupledAnchorScaleTests(unittest.TestCase):
    def test_gcd_expansion(self) -> None:
        for d in range(2, 15):
            for N, R in ((1, 1), (2, 3), (5, 7), (8, 9)):
                self.assertEqual(gcd_convolution_sum(d=d, N=N, R=R), gcd_convolution_expansion(d=d, N=N, R=R))

    def test_anchor_height(self) -> None:
        self.assertTrue(anchor_height_bound(Q=100, support_n_prime=50, support_m=40, B=100, C=40, p0=2, q0=1))
        self.assertFalse(anchor_height_bound(Q=100, support_n_prime=50, support_m=40, B=150, C=80, p0=3, q0=2))

    def test_theorem(self) -> None:
        row = theorem_record()
        self.assertIn("p0,q0<=1/a", row["anchor_bound"])
        self.assertIn("X^(13/30", row["aggregate"])
        self.assertIn("weak localization", row["boundary"])


if __name__ == "__main__":
    unittest.main()
