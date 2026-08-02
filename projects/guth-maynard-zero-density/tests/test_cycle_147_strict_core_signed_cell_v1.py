import unittest
from math import pi

from conventions.strict_core_signed_cell_v1 import (
    negative_halo_floor_scaled,
    phase_wedge_floor,
    signed_core_lower_bound,
    theorem_record,
)


class StrictCoreSignedCellTests(unittest.TestCase):
    def test_registered_phase_wedge_has_half_floor(self) -> None:
        floor = phase_wedge_floor(
            support_ceiling=3.0,
            core_radius_scaled=1.0 / 36.0,
            atom_phase_wedge=pi / 12.0,
        )
        self.assertAlmostEqual(floor, 0.5)

    def test_exact_phase_chart_has_stronger_floor(self) -> None:
        floor = phase_wedge_floor(
            support_ceiling=2.0,
            core_radius_scaled=1.0 / 24.0,
            atom_phase_wedge=0.0,
        )
        self.assertGreater(floor, 0.8)

    def test_core_lower_bound(self) -> None:
        self.assertEqual(
            signed_core_lower_bound(
                frequency_weight=10.0,
                pair_mass=7.0,
                cosine_floor=0.5,
            ),
            35.0,
        )

    def test_negative_halo_starts_outside_wider_collar(self) -> None:
        self.assertEqual(negative_halo_floor_scaled(support_ceiling=2.0), 0.125)

    def test_record_does_not_claim_target_mass(self) -> None:
        row = theorem_record()
        self.assertIn("one half", row["phase_wedge"])
        self.assertIn("not bounded below", row["actual_chart_scope"])
        self.assertIn("no theorem", row["mass_boundary"])
        self.assertIn("no paired norm", row["boundary"])


if __name__ == "__main__":
    unittest.main()
