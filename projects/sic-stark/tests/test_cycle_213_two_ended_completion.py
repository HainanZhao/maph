from __future__ import annotations

import unittest

from proof.verify_cycle_213_two_ended_completion import run


class TwoEndedCompletionTests(unittest.TestCase):
    def setUp(self):
        self.result = run()

    def test_cusps_share_the_frozen_a6_multiplier(self):
        audit = self.result["a6_cusp_multiplier_audit"]
        self.assertEqual(audit["common_multiplier_exponent_mod_48"], 8)
        self.assertEqual([row["zeta_48_exponent"] for row in audit["records"]], [8, 8])

    def test_no_strict_scalar_invariant_pairing_survives(self):
        audit = self.result["scalar_pairing_audit"]
        self.assertEqual(audit["zeta_48_squared_exponent_mod_48"], 16)
        self.assertEqual(audit["nonzero_scalar_pairing_dimension"], 0)

    def test_character_valued_cross_pairing_keeps_the_distinction(self):
        audit = self.result["cross_pairing_audit"]
        self.assertTrue(audit["exchange_invariant"])
        self.assertEqual(audit["fixed_line_restriction_in_units_of_q"], 2)
        self.assertFalse(audit["descends_to_iota_coinvariant_quotient"])


if __name__ == "__main__":
    unittest.main()
