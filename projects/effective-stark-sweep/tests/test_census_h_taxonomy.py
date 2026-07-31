import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


class CensusHTaxonomyTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.routes = load(
            "artifacts/roblot-sextic-route-inventory-v1.json"
        )
        cls.fields = load(
            "artifacts/roblot-sextic-field-inventory-v1.json"
        )
        cls.threeclass = load(
            "artifacts/roblot-sextic-3class-v1.json"
        )
        cls.sextic = load(
            "artifacts/roblot-sextic-population-v1.json"
        )
        cls.taxonomy = load("artifacts/census-h-taxonomy-v1.json")

    def test_deduplicated_sextic_population(self):
        counts = self.routes["counts"]
        self.assertEqual(counts["inventory_kernels"], 764)
        self.assertEqual(counts["exact_route_complete"], 764)
        self.assertEqual(counts["distinct_primitive_field_keys"], 407)
        self.assertEqual(counts["field_keys_requiring_certificate"], 382)
        self.assertEqual(
            counts["field_keys_short_circuited_by_exact_local_failure"],
            25,
        )
        self.assertEqual(counts["sequential_exact_route_comparisons"], 109)

    def test_field_sweep_and_exact_three_class_obstructions(self):
        statuses = self.fields["counts"]["status"]
        self.assertEqual(statuses["EXACT_FIELD_GATES_COMPLETE"], 309)
        self.assertEqual(
            statuses["NEEDS_STRONG_3_CLASS_CERTIFICATE"], 73
        )
        self.assertEqual(
            self.threeclass["status"],
            "COMPLETE_EXACT_3CLASS_OBSTRUCTION_POPULATION",
        )
        counts = self.threeclass["counts"]
        self.assertEqual(counts["residual_fields"], 73)
        self.assertEqual(counts["full_bnfcertify_controls"], 4)
        self.assertEqual(counts["exact_unramified_cyclic_cubics"], 77)
        self.assertEqual(counts["failures"], 0)
        for record in self.threeclass["records"]:
            self.assertEqual(
                record["status"], "EXACT_UNRAMIFIED_CYCLIC_CUBIC"
            )
            self.assertEqual(
                record["relative_cubic_root_count_in_H"], 0
            )
            self.assertEqual(
                record["relative_discriminant_ideal_norm"], 1
            )
            self.assertTrue(
                record["cubic_polynomial_discriminant_square"]
            )

    def test_every_sextic_kernel_has_an_exact_decision(self):
        self.assertEqual(
            self.sextic["status"], "COMPLETE_EXACT_POPULATION_SCREEN"
        )
        counts = self.sextic["counts"]
        self.assertEqual(counts["inventory_kernels"], 764)
        self.assertEqual(counts["exact_applicability_decisions"], 764)
        self.assertEqual(counts["incomplete_kernels"], 0)
        self.assertEqual(counts["applicable_kernels"], 259)
        self.assertEqual(counts["applicable_rows"], 206)
        self.assertEqual(counts["nonapplicable_kernels"], 505)
        self.assertTrue(
            all(
                control["passed"]
                for control in self.sextic[
                    "frozen_control_replay"
                ].values()
            )
        )

    def test_h_taxonomy_and_frontier(self):
        counts = self.taxonomy["counts"]
        self.assertEqual(counts["H_rows"], 2704)
        self.assertEqual(counts["engine_b_route_eligible"], 232)
        self.assertEqual(counts["engine_c_route_eligible"], 881)
        self.assertEqual(counts["exclusive_frontier"], 1591)
        self.assertEqual(
            counts["roblot_full_row_status"][
                "FULL_ROW_WEAK_COVERAGE"
            ],
            1079,
        )
        self.assertEqual(counts["mechanism_status_incomplete"], 5)
        self.assertEqual(counts["all_known_mechanisms_fail"], 1359)
        wall = self.taxonomy["frontier_tables"][
            "q_sqrt_21_order_six_wall"
        ]
        self.assertEqual(wall["case_id"], "RQ-000692")
        self.assertEqual(wall["d"], 21)
        self.assertEqual(wall["support_orders"], [2, 6])
        self.assertEqual(wall["shintani_index"], 6)
        self.assertTrue(wall["all_known_mechanisms_fail"])
        self.assertEqual(
            wall["roblot_sextic"]["status"],
            "COMPLETE_HYPOTHESIS_FAILURE",
        )


if __name__ == "__main__":
    unittest.main()
