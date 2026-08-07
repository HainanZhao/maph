import unittest

from proof.verify_lane_b_arbitrary_width_frontier import _case


class ArbitraryWidthFrontierTests(unittest.TestCase):
    def test_checkerboard_lagrangian_and_coordinate_firewall(self):
        expected = {
            2: [0, 0, 0],
            3: [1, 2, 3],
            4: [1, 4, 5],
        }
        for width, genera in expected.items():
            case = _case(width, 4)
            self.assertEqual(
                [row["genus"] for row in case["length_rows"]],
                genera,
            )
            for row in case["length_rows"]:
                self.assertEqual(row["explicit_checkerboard_lagrangian_rank"], row["genus"])
                self.assertTrue(row["explicit_checkerboard_lagrangian_isotropic"])
                self.assertEqual(row["atomic_intersection"], row["canonical_intersection"])
                self.assertEqual(row["raw_transported_arf"], 0)
                self.assertTrue(row["all_b_modes_exact"])
                self.assertTrue(row["each_edge_has_at_most_one_nonexact_atom"])
                self.assertEqual(row["adjacent_window_span_rank"], row["genus"])


if __name__ == "__main__":
    unittest.main()
