from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DimensionSixCyclicParameterLedgerTests(unittest.TestCase):
    def test_exact_parameter_match_and_pentagon_gates(self) -> None:
        output = subprocess.check_output(
            [
                sys.executable,
                str(
                    ROOT
                    / "scripts"
                    / "dimension_six_cyclic_parameter_ledger.py"
                ),
            ],
            text=True,
        )
        result = json.loads(output)
        self.assertTrue(result["parameter_match"]["common_6n_torus"])
        self.assertTrue(result["parameter_match"]["six_central_sectors"])
        self.assertTrue(
            result["parameter_match"][
                "singular_sector_requires_qgamma_regularization"
            ]
        )
        self.assertFalse(result["direct_pentagon_gates"]["fixed_order"])
        self.assertFalse(
            result["direct_pentagon_gates"][
                "punctured_fermat_parameter_at_every_sector"
            ]
        )
        self.assertFalse(
            result["direct_pentagon_gates"][
                "characteristic_nodes_form_subgroup"
            ]
        )
        self.assertFalse(
            result["direct_pentagon_gates"][
                "cyclic_quotient_alone_retains_both_coordinates"
            ]
        )
        for record in result["records"]:
            self.assertTrue(record["combined_commutator_is_primitive"])
            self.assertEqual(record["characteristic_node_count"], 36)
            self.assertEqual(
                sorted(record["central_sector_counts"].values()),
                [6] * 6,
            )
            self.assertEqual(
                len(record["singular_nonzero_characteristics"]),
                5,
            )
            self.assertTrue(
                record["central_sector_preserved_by_stabilizer"]
            )
            self.assertFalse(record["node_set_is_subgroup"])
            self.assertFalse(record["fixed_cyclic_order_on_both_sides"])
            self.assertEqual(
                record["inter_level_lattice_determinant"],
                -504,
            )
            self.assertEqual(
                record["inter_level_smith_invariants"],
                [1, 504],
            )
            self.assertEqual(
                record["inter_level_six_torsion_order"],
                6,
            )
            self.assertFalse(
                record[
                    "inter_level_correspondence_"
                    "captures_full_characteristic_group"
                ]
            )


if __name__ == "__main__":
    unittest.main()
