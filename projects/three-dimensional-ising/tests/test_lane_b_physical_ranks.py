"""Regression tests for the physical Sp(6,2) rank reduction."""

import unittest

from proof.verify_lane_b_physical_ranks import verify


class LaneBPhysicalRankTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = verify()

    def test_spin_structures_and_arf_reconstruction(self) -> None:
        self.assertEqual(self.result["even_spin_structures"], 36)
        self.assertEqual(self.result["odd_spin_structures"], 28)
        for evaluation in self.result["evaluations"].values():
            self.assertTrue(evaluation["arf_reconstruction"])

    def test_exhaustive_symplectic_search(self) -> None:
        for evaluation in self.result["evaluations"].values():
            search = evaluation["symplectic_search"]
            self.assertEqual(search["symplectic_bases"], 1451520)
            self.assertEqual(search["profiles"]["2,4,7,4,2"], 138240)
            self.assertEqual(search["profiles"]["2,4,8,4,2"], 1313280)

    def test_exact_generic_rank_seven_witness(self) -> None:
        witness = self.result["exact_rank_seven_survivor"]
        self.assertEqual(witness["ordered_symplectic_basis"], [1, 34, 4, 8, 17, 32])
        self.assertEqual(witness["generic_TT_rank_over_Q(t)"], [2, 4, 7, 4, 2])
        self.assertEqual(witness["coefficientwise_row_identity"], "row_4 - row_6 = 0")

    def test_symmetry_derives_row_identity(self) -> None:
        symmetry = self.result["rank_reduction_symmetry_derivation"]
        self.assertTrue(symmetry["facial_boundary_space_preserved"])
        self.assertTrue(symmetry["sector_polynomials_preserved"])
        self.assertTrue(symmetry["quadratic_form_preserved"])
        self.assertEqual(
            symmetry["derived_flattening_identity"],
            "row_4 = row_6 for all eight columns",
        )


if __name__ == "__main__":
    unittest.main()
