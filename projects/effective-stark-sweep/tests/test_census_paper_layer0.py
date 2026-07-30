import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class CensusPaperLayer0Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads(
            (
                ROOT
                / "artifacts"
                / "census-paper-layer0-reconciliation-v1.json"
            ).read_text(encoding="utf-8")
        )
        cls.preregistration = json.loads(
            (
                ROOT / "data" / "census-paper-preregistration-v1.json"
            ).read_text(encoding="utf-8")
        )

    def test_frozen_range(self):
        universe = self.record["publication_universe"]
        self.assertEqual(universe["D_min"], 2)
        self.assertEqual(universe["D_max"], 200)
        self.assertEqual(universe["finite_ideal_norm_max"], 100)
        self.assertEqual(universe["field_count"], 121)
        self.assertEqual(universe["representative_count"], 8200)
        self.assertFalse(universe["nonmaximal_form_order_moduli_in_universe"])
        self.assertTrue(
            self.record["clean_enumeration_rerun"][
                "mathematical_payload_identical"
            ]
        )

    def test_support_first_trichotomy(self):
        split = self.record["structural_trichotomy"]
        self.assertEqual(
            [
                split["T_empty_support"],
                split["Q_nonempty_quadratic_support"],
                split["H_nonempty_higher_order_support"],
                split["sum"],
            ],
            [3936, 1560, 2704, 8200],
        )
        higher = self.record["higher_order_mechanism_cross_tab"]
        self.assertEqual(
            [
                higher["ENGINE_B_ELIGIBLE"],
                higher["ENGINE_C_ELIGIBLE"],
                higher["FRONTIER"],
                higher["sum"],
            ],
            [232, 881, 1591, 2704],
        )

    def test_v5_reconciliation_is_explicit(self):
        correction = self.record["v5_reconciliation"]
        self.assertEqual(correction["banked_routing_trivial_count"], 3899)
        self.assertEqual(correction["structural_empty_support_count"], 3936)
        self.assertEqual(
            correction["empty_support_rows_previously_routed_FRONTIER"], 37
        )
        self.assertEqual(len(correction["affected_case_ids"]), 37)

    def test_quadratic_counts_and_semantics(self):
        quadratic = self.record["quadratic_stratum_reconciliation"]
        self.assertEqual(quadratic["rows"], 1560)
        self.assertEqual(
            quadratic["supported_quadratic_character_occurrences"], 2232
        )
        self.assertEqual(quadratic["distinct_quartic_fields"], 912)
        self.assertEqual(quadratic["zero_Euler_character_occurrences"], 672)
        self.assertEqual(quadratic["rows_affected_by_zero_Euler_factors"], 603)
        self.assertEqual(
            quadratic["rows_with_all_supported_derivatives_zero"], 346
        )
        self.assertIn("remain in Q", quadratic["classification_rule"])

    def test_preregistered_gates(self):
        self.assertEqual(
            self.preregistration["packet_polynomial_policy"][
                "maximum_absolute_compositum_degree"
            ],
            32,
        )
        spot = self.preregistration["independent_analytic_spotcheck"]
        self.assertEqual(spot["sample_size"], 50)
        self.assertEqual(spot["target_decimal_digits"], 38)
        self.assertIn("halt publication", spot["failure_rule"])


if __name__ == "__main__":
    unittest.main()
