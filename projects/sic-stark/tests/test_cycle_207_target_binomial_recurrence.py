from __future__ import annotations

import unittest

from proof.verify_cycle_207_target_binomial_recurrence import run


class TargetBinomialRecurrenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.result = run()

    def test_relation_class_has_the_declared_generator_actions(self) -> None:
        basis = self.result["relation_basis_audit"]
        self.assertTrue(basis["T1_T2_preserve_class"])
        self.assertTrue(basis["reflection_negates_class"])
        self.assertEqual(len(basis["records"]), 3)

    def test_every_elementary_target_binomial_is_retained(self) -> None:
        ledger = self.result["target_binomial_ledger"]
        self.assertEqual(ledger["target_binomial_count"], 25)
        self.assertEqual(
            ledger["factorwise_signature_match_count"]
            + ledger["factorwise_signature_mismatch_count"],
            25,
        )
        self.assertTrue(ledger["common_scalar_cancels_only_between_formed_products"])

    def test_no_signature_classification_claims_an_endpoint_value(self) -> None:
        records = self.result["target_binomial_ledger"]["records"]
        self.assertTrue(all(
            record["endpoint_value_status"] == "NOT_EVALUATED_NO_NONVANISHING_CLAIM"
            for record in records
        ))

    def test_scope_keeps_multifactor_identities_open(self) -> None:
        self.assertIn("multifactor", self.result["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
