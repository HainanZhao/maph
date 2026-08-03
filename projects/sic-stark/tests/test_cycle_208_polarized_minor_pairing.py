from __future__ import annotations
import unittest
from proof.verify_cycle_208_polarized_minor_pairing import run

class CoordinateRingPullbackTests(unittest.TestCase):
    def setUp(self): self.result = run()
    def test_full_ideal_and_pullback_census(self):
        self.assertEqual(self.result["source_rank_one_ideal"]["generator_count"], 225)
        self.assertEqual(self.result["diagonal_pullbacks"]["pullback_count"], 225)
        self.assertEqual(self.result["exact_reduction_audit"]["identity_count"], 225)
        self.assertTrue(self.result["exact_reduction_audit"]["all_identities_checked"])
        self.assertEqual(self.result["nonmembership_witness"]["witness_count"], 225)
    def test_each_nonzero_coefficient_minor_has_an_exact_witness(self):
        witness = self.result["nonmembership_witness"]
        self.assertEqual(witness["witnesses"][0]["source_generator_value"], "1*1-1*1=0")
        self.assertIn("c_(0,0)*c_(1,1)-c_(0,1)*c_(1,0)", witness["witnesses"][0]["reduced_pullback_value"])
    def test_a6_does_not_determine_coefficients(self):
        audit=self.result["a6_audit"]
        self.assertTrue(audit["family_covariant"])
        self.assertEqual(audit["coefficient_constraints_from_A6"], 0)
    def test_scope_does_not_supply_a_map(self):
        self.assertEqual(self.result["gate_outcome"]["source_interface_coefficients"], "OPEN_NOT_SUPPLIED")

if __name__ == "__main__": unittest.main()
