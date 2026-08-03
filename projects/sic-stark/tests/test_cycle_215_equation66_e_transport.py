from __future__ import annotations

import unittest

from proof.verify_cycle_215_equation66_e_transport import run


class Equation66ETransportTests(unittest.TestCase):
    def setUp(self):
        self.result = run()

    def test_e_changes_the_lens_parameters_and_positive_period(self):
        audit = self.result["direct_parameter_audit"]
        self.assertEqual(audit["transformed_lens_parameters_p_k_r_s"], [-5, 24, 115, 24])
        self.assertEqual(audit["transformed_phase_coefficient"], 547)
        self.assertTrue(audit["omega1_E_equals_minus_omega1"])
        self.assertFalse(audit["frozen_positive_period_hypothesis_for_E"])

    def test_no_channel_global_scalar_survives_bare_t_inversion(self):
        audit = self.result["bare_packet_inversion_audit"]
        self.assertEqual(audit["ratio_t_exponents"], list(range(2, 13)))
        self.assertFalse(audit["label_independent_kappa_h_possible"])


if __name__ == "__main__":
    unittest.main()
