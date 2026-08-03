from __future__ import annotations

import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))

from verify_cycle_199_abel_pole_geometry import (  # noqa: E402
    abel_pole_pairs,
    nonpinching_channels,
    ratio_geometry,
    run,
)


class AbelPoleGeometryTests(unittest.TestCase):
    def test_geodesic_ratio_has_positive_imaginary_part(self) -> None:
        result = ratio_geometry()
        self.assertEqual(result["upper_half_plane_sign"], "+")
        self.assertIn("4*Im(tau)", result["imaginary_part"])

    def test_six_pole_pairs_are_oriented_oppositely(self) -> None:
        result = abel_pole_pairs()
        self.assertEqual(result["pinching_channels"], [0, 4, 8, 12, 16, 20])
        for record in result["records"]:
            self.assertEqual(record["residues_in_lambda"]["sum"], "0")
            self.assertIn("negative", record["imaginary_signs"]["Lambda_plus"])
            self.assertIn("positive", record["imaginary_signs"]["Lambda_minus"])

    def test_remaining_channels_do_not_pinch(self) -> None:
        result = nonpinching_channels()
        self.assertTrue(result["only_six_channels_pinch"])

    def test_scope_remains_constructive_not_closed(self) -> None:
        result = run()
        self.assertIn("does not supply", result["claim_boundary"])
        self.assertIn("regular-plus-residue", result["next_required_construction"])


if __name__ == "__main__":
    unittest.main()
