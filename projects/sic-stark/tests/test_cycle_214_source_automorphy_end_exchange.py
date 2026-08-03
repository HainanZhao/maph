from __future__ import annotations

import unittest

from proof.verify_cycle_214_source_automorphy_end_exchange import run


class SourceAutomorphyEndExchangeTests(unittest.TestCase):
    def setUp(self):
        self.result = run()

    def test_e_exchanges_both_cusp_labels(self):
        records = self.result["candidate_audit"]["records"]
        exchange = next(record for record in records if record["name"] == "E=J0*S")
        self.assertEqual(exchange["cusp_infinity_image"], [5, 0])
        self.assertEqual(exchange["cusp_zero_image"], [0, 5])
        self.assertTrue(exchange["preserves_Q"])

    def test_e_reverses_the_stabilizer_step(self):
        audit = self.result["flow_conjugacy_audit"]
        self.assertEqual(audit["E_A6_E_inverse"], audit["A6_inverse"])

    def test_covariance_remains_a_transformed_tuple_statement(self):
        audit = self.result["source_domain_audit"]
        self.assertEqual(audit["E_covariance"]["same_beta_oriented_packet_identification"], "NOT_SUPPLIED_BY_DECLARED_THEOREMS")
        self.assertIn("a source-derived exchange involution on W", audit["not_supplied_by_frozen_theorem"])


if __name__ == "__main__":
    unittest.main()
