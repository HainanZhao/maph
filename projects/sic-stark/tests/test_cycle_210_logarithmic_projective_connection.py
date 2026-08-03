from __future__ import annotations

import unittest

from proof.verify_cycle_210_logarithmic_projective_connection import run


class LogarithmicProjectiveConnectionTests(unittest.TestCase):
    def setUp(self):
        self.result = run()

    def test_complete_exponent_connection(self):
        connection = self.result["exponent_connection"]
        self.assertEqual(connection["record_count"], 36)
        self.assertTrue(connection["channel_independent"])

    def test_a6_multiplier_commutes(self):
        symmetry = self.result["a6_multiplier_commutation"]
        self.assertEqual(symmetry["record_count"], 36)
        self.assertTrue(symmetry["all_commute"])

    def test_basepoint_change_is_not_projectively_scalar(self):
        obstruction = self.result["basepoint_change_obstruction"]
        self.assertEqual(obstruction["entries"], {"base": "1", "shifted": "81/16"})
        self.assertFalse(obstruction["projectively_scalar"])


if __name__ == "__main__":
    unittest.main()
