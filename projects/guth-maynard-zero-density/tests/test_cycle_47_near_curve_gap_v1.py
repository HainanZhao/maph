from fractions import Fraction as Q
import unittest

from conventions.near_curve_gap_v1 import geometric_scales, huxley_sargos_bound, verify_all


class Cycle47NearCurveGapTests(unittest.TestCase):
    def test_best_registered_order(self) -> None:
        rows = [(huxley_sargos_bound(k), k) for k in range(3, 21)]
        self.assertEqual(min(rows), (Q(8, 25), 3))

    def test_exact_gap(self) -> None:
        data = verify_all()
        self.assertEqual(data["huxley_sargos_gap"], Q(1, 25))

    def test_geometric_correction(self) -> None:
        geometry = geometric_scales()
        self.assertEqual(geometry["graph_second_derivative"], Q(-7, 25))
        self.assertEqual(geometry["euclidean_curvature"], Q(-19, 25))
        self.assertEqual(geometry["normal_tube"], Q(-1))

    def test_geometric_count(self) -> None:
        geometry = geometric_scales()
        self.assertEqual(geometry["affine_arclength"], Q(26, 75))
        self.assertEqual(geometry["howard_trifonov_count"], Q(26, 75))


if __name__ == "__main__":
    unittest.main()
