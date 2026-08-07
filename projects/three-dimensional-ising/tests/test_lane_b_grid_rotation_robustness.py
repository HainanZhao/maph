import unittest

from proof.verify_lane_b_grid_rotation_robustness import verify


class GridRotationRobustnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = verify()

    def test_complete_cube_rotation_census(self):
        self.assertEqual(self.payload["rotation_census"], {"0": 2, "1": 54, "2": 200})

    def test_selected_rotations_and_physical_contraction(self):
        for prime in self.payload["primes"]:
            rows = [row for row in self.payload["rows"] if row["prime"] == prime]
            self.assertEqual(
                {row["rotation"]: (row["genus"], row["spin_structure_count"]) for row in rows},
                {"planar_genus_zero": (0, 1), "maximum_genus_two": (2, 16)},
            )
            self.assertEqual(len({row["physical_even_subgraph_value"] for row in rows}), 1)
            self.assertTrue(all(
                row["normalized_arf_sum"] == row["physical_even_subgraph_value"]
                for row in rows
            ))


if __name__ == "__main__":
    unittest.main()
