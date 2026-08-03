from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "proof" / "verify_cycle_194_meromorphic_anti_channel.py"


class Cycle194MeromorphicAntiChannelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        completed = subprocess.run(
            [sys.executable, str(SCRIPT)],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.result = json.loads(completed.stdout)

    def test_all_six_physical_anti_principal_parts_are_forced(self) -> None:
        forced = self.result["forced_anti_fibre"]
        self.assertEqual(forced["dimension"], 6)
        self.assertTrue(forced["all_six_anti_coordinates_source_forced"])
        self.assertTrue(forced["F24_preserves_A"])
        self.assertTrue(
            all(
                record["anti_difference_has_nonzero_simple_principal_part"]
                for record in forced["principal_part_records"]
            )
        )

    def test_spectral_projection_retains_odd_raw_differences(self) -> None:
        retention = self.result["spectral_anti_retention"]
        self.assertTrue(retention["all_six_odd_raw_differences_retained"])
        self.assertEqual(len(retention["retention_records"]), 6)
        self.assertTrue(
            retention["capital_Gamma_normalization_retained_separately"]
        )
        self.assertTrue(retention["AFK_phase_retained_separately"])

    def test_coincident_poles_require_an_orbit_sum(self) -> None:
        collisions = self.result["primary_pole_collision_lattice"]
        interior = self.result["interior_periodization"]
        self.assertIn("z+3t", collisions["collision_law"])
        self.assertGreater(collisions["finite_witness_count"], 0)
        self.assertFalse(interior["termwise_principal_parts_permitted_in_interior"])
        self.assertTrue(interior["coincident_pole_residue_orbit_required"])

    def test_strict_interior_tail_has_exact_decay_condition(self) -> None:
        recurrence = self.result["residue_orbit_recurrence"]
        tail = recurrence["tail_asymptotics"]
        self.assertIn("|q|*|q_tilde|^(-1/24)", tail["root_limit"])
        self.assertIn("23/24", tail["strict_chamber_log_certificate"])
        self.assertTrue(tail["residue_orbit_absolute_convergence"])
        self.assertFalse(tail["all_points_nonvanishing_claimed"])
        self.assertIn(
            "not identically zero",
            tail["nonzero_interior_asymptotic_sector"],
        )


if __name__ == "__main__":
    unittest.main()
