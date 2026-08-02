import unittest
from conventions.cycle_184_phase_shift_correction_v1 import corrected_two_ray_family, verify_all

class Cycle184PhaseShiftCorrectionTest(unittest.TestCase):
    def test_shift_preserves_determinant(self) -> None:
        self.assertNotEqual(corrected_two_ray_family(3)["determinant"]["F"], 0)
    def test_withheld_boundary(self) -> None:
        self.assertIn("WITHHELD", verify_all()["original_deformation_disposition"])

if __name__ == "__main__":
    unittest.main()
