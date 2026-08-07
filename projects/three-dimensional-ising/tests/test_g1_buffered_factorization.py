import unittest

from proof.verify_g1_buffered_factorization import verify


class G1BufferedFactorizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = verify(maximum_symbolic_width=8, maximum_global_width=4)

    def test_global_coordinate_placement(self):
        row = self.payload["global_coordinate_rows"][0]
        self.assertEqual(row["shape"], [11, 4, 4])
        self.assertEqual(row["left_terminal_rank"], 15)
        self.assertEqual(row["right_terminal_rank"], 15)
        self.assertEqual(row["suffix_handle_genus"], 8)
        self.assertIn("diagonal", row["two_slab_buffer"]["matrix_form"])

    def test_even_exceptional_rank_one_updates(self):
        self.assertEqual(
            [(row["width"], row["rank_one_scalar"])
             for row in self.payload["exceptional_rank_one_relations"]],
            [(4, 0), (6, 0), (8, 0)],
        )


if __name__ == "__main__":
    unittest.main()
