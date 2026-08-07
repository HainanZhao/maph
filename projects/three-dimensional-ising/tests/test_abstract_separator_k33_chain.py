import unittest

from proof.verify_abstract_separator_k33_chain import PRIMES, verify


class K33SeparatorChainTests(unittest.TestCase):
    def test_pair_bound_and_internal_h3_obstruction(self):
        result = verify()
        self.assertEqual(result["primes"], list(PRIMES))
        for row in result["rows"]:
            self.assertEqual(row["genus"], row["gadgets"])
            self.assertTrue(row["all_pair_ranks_at_most_two"])
            self.assertTrue(all(rank <= 4 for rank in row["binary_cut_rank_profile"]))
            if row["gadgets"] == 2:
                self.assertEqual(row["embeddable_zero_port_witness"]["rank_certificate"]["rank"], 2)
            if row["gadgets"] == 3:
                witness = row["embeddable_zero_port_witness"]
                self.assertEqual(witness["rank_certificate"]["rank"], 4)
                self.assertEqual(witness["all_24_affine_symplectic_local_relabeling_ranks"], [4] * 24)
            if row["gadgets"] >= 3:
                self.assertIn(4, row["minimum_internal_ranks_under_affine_symplectic_handle_relabeling"])


if __name__ == "__main__":
    unittest.main()
