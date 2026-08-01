import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class B3InputsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = json.loads(
            (
                ROOT
                / "artifacts"
                / "b3-quartic-kernel-inventory-v1.json"
            ).read_text()
        )
        cls.anchor = json.loads(
            (
                ROOT
                / "artifacts"
                / "b3-arb-weak-coefficient-anchor-v1.json"
            ).read_text()
        )
        cls.population = json.loads(
            (
                ROOT / "artifacts" / "b3-roblot-population-v1.json"
            ).read_text()
        )

    def test_kernel_inventory_is_frozen_without_target_data(self):
        self.assertEqual(
            self.inventory["status"],
            "FROZEN_BEFORE_FIELD_AND_PHASE_EVALUATION",
        )
        self.assertEqual(
            self.inventory["counts"],
            {
                "source_rows": 8200,
                "relevant_rows": 1512,
                "supported_order_four_characters": 4490,
                "inverse_pair_kernels": 2245,
                "w1_quartic_count_crosschecked_rows": 1069,
            },
        )
        wall = self.inventory["independence_wall"]
        self.assertTrue(
            wall["selection_uses_only_w1_group_and_sign_metadata"]
        )
        self.assertFalse(wall["engine_c_geometry_read"])
        self.assertFalse(wall["lprime_or_phase_artifact_read"])

    def test_arb_anchor_certifies_all_five_controls(self):
        self.assertEqual(
            self.anchor["status"],
            "PASS_FIVE_CONTROL_ARB_WEAK_COEFFICIENT_ANCHOR",
        )
        self.assertEqual(self.anchor["claim_tag"], "CERTIFIED_NUMERICAL")
        self.assertEqual(
            self.anchor["runtime"]["precisions_bits"], [256, 512]
        )
        self.assertEqual(
            {case["case_id"] for case in self.anchor["cases"]},
            {
                "RQ-000129",
                "RQ-001280",
                "RQ-001569",
                "RQ-001894",
                "RQ-007519",
            },
        )
        self.assertTrue(
            all(not value for value in self.anchor["independence_wall"].values())
        )
        for case in self.anchor["cases"]:
            self.assertTrue(case["fine_ball_nested_in_coarse"])
            self.assertTrue(
                case["archived_point_contained_in_512_bit_ball"]
            )
            for precision in ("256", "512"):
                run = case["runs"][precision]
                self.assertTrue(run["root_isolation"]["pairwise_disjoint"])
                self.assertEqual(
                    run["root_isolation"]["real_root_count"], 4
                )
                self.assertTrue(run["orbit_values_exclude_zero"])

    def test_population_has_complete_explicit_accounting(self):
        population = self.population
        self.assertEqual(
            population["status"], "COMPLETE_EXACT_POPULATION_SCREEN"
        )
        self.assertFalse(
            population["claim_boundary"]["phase_or_lprime_target_opened"]
        )
        counts = population["counts"]
        records = population["records"]
        self.assertEqual(counts["inventory_kernels"], 2245)
        self.assertEqual(counts["attempted_kernels"], 2245)
        self.assertEqual(len(records), 2245)
        self.assertEqual(
            [record["inventory_offset"] for record in records],
            list(range(2245)),
        )
        exact = [
            record
            for record in records
            if record["status"] == "EXACT_SCREEN_COMPLETE"
        ]
        failures = [
            record
            for record in records
            if record["status"] != "EXACT_SCREEN_COMPLETE"
        ]
        self.assertEqual(counts["exact_screen_complete"], len(exact))
        self.assertEqual(
            counts["tool_or_resource_failures"], len(failures)
        )
        self.assertEqual(
            counts["eligible_kernels"],
            sum(record["eligible"] for record in exact),
        )
        self.assertEqual(
            counts["noneligible_kernels"],
            sum(not record["eligible"] for record in exact),
        )
        for record in exact:
            self.assertTrue(record["A1"])
            self.assertTrue(record["A2"])
            self.assertEqual(
                record["eligible"],
                record["A1"] and record["A2"] and record["A3"],
            )
            if not record["A3"]:
                self.assertTrue(
                    any(
                        local[-2:] == [1, 0]
                        for local in record["A3_local_rows"]
                    )
                )
        for record in failures:
            self.assertFalse(record["eligible"])
            self.assertIn(
                record["status"],
                {
                    "TOOL_OR_CONSTRUCTION_FAILURE",
                    "RESOURCE_CAP_TIMEOUT",
                },
            )


if __name__ == "__main__":
    unittest.main()
