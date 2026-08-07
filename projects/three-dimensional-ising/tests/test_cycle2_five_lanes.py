from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.verify_cycle2_five_lanes import build_report  # noqa: E402


class CycleTwoFiveLaneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_report()

    def test_all_lanes_present(self) -> None:
        self.assertEqual(len(self.report["lanes"]), 5)
        self.assertEqual(
            self.report["selection_after_all_tests"]["selected_lane"],
            "B_spin_structure_compression",
        )

    def test_tetrahedron_and_layer_witnesses(self) -> None:
        lane = self.report["lanes"]["A_tetrahedron_integrability"]
        self.assertEqual(lane["status"], "RESTRICTED_NO_GO")
        self.assertNotEqual(lane["periodic_layer"]["difference"], "0")

    def test_spin_structure_rank(self) -> None:
        lane = self.report["lanes"]["B_spin_structure_compression"]
        calibration = lane["calibration_graph"]
        slab = lane["cubic_graph"]
        self.assertEqual(calibration["F_matrix_rank_over_Q(t)"], 2)
        self.assertEqual(calibration["homology_sector_polynomials"]["00"]["0"], 1)
        self.assertEqual(calibration["homology_sector_polynomials"]["11"]["18"], 1)
        self.assertTrue(slab["minimum_genus_certified"])
        self.assertTrue(slab["arf_reconstruction_verified"])
        self.assertEqual(slab["F_matrix_rank_over_Q(t)"], 2)
        self.assertEqual(slab["fourier_support"], 4)
        self.assertEqual(slab["homology_sector_polynomials"]["00"]["0"], 1)

    def test_gauge_sector_count(self) -> None:
        lane = self.report["lanes"]["C_higher_form_fermionization"]
        self.assertEqual(
            lane["sector_count_if_flux_is_left_unrestricted"]["3"][
                "gauge_inequivalent_link_fields"
            ],
            1024,
        )

    def test_crossing_is_not_matchgate(self) -> None:
        lane = self.report["lanes"]["D_local_tensor_transformation"]
        self.assertTrue(lane["local_parity_tensor"]["matchgate"])
        self.assertEqual(lane["ordinary_crossing_tensor"]["grassmann_pluecker_residual"], 2)
        self.assertTrue(lane["bounded_auxiliary_extension"]["component_identity_verified"])
        self.assertIn("2^c", lane["bounded_auxiliary_extension"]["global_cost"])

    def test_blocking_generates_higher_interactions(self) -> None:
        lane = self.report["lanes"]["E_exact_renormalization_closure"]
        self.assertNotEqual(lane["four_body_multiplicative_walsh_ratio"], "1")
        self.assertNotEqual(lane["six_body_multiplicative_walsh_ratio"], "1")


if __name__ == "__main__":
    unittest.main()
