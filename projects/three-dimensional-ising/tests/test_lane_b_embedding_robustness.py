import unittest

from proof.verify_lane_b_embedding_robustness import verify


class EmbeddingRobustnessTests(unittest.TestCase):
    def test_same_graph_different_genus_and_same_physical_value(self):
        result = verify()
        by_rotation = {}
        for row in result["rows"]:
            by_rotation.setdefault(row["rotation"], set()).add(
                (row["genus"], row["spin_structure_count"])
            )
            self.assertTrue(row["physical_values_agree"])
            self.assertEqual(row["graph_to_surface_homology_rank"], 2 * row["genus"])
        self.assertEqual(by_rotation["minimum_genus_one"], {(1, 4)})
        self.assertEqual(by_rotation["maximum_genus_two"], {(2, 16)})


if __name__ == "__main__":
    unittest.main()
