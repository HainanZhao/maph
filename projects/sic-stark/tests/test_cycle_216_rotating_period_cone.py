"""Regression checks for the Cycle 216 rotating-period cone audit."""
from __future__ import annotations

import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))

from verify_cycle_216_rotating_period_cone import run  # noqa: E402


class RotatingPeriodConeTests(unittest.TestCase):
    def test_full_frozen_audit(self) -> None:
        result = run()
        cone = result["rotating_cone_audit"]
        density = result["endpoint_density_audit"]
        matrices = result["one_step_source_matrix_audit"]
        packet = result["packet_boundary_audit"]
        self.assertTrue(cone["all_divisors_covered_symbolically"])
        self.assertFalse(cone["interior_pole_crossing"])
        self.assertEqual(cone["endpoint_u_one_corridor_width"], "0 (one-sided limit)")
        self.assertTrue(density["limiting_m_zero_pole_trajectories_dense_on_real_contour"])
        self.assertFalse(matrices["one_step_factorization_reaches_M_E"])
        self.assertEqual(packet["all_label_t_defects"], list(range(2, 13)))


if __name__ == "__main__":
    unittest.main()
