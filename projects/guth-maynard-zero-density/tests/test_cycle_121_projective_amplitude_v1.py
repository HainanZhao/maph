import unittest

from conventions.projective_amplitude_v1 import ProjectiveAmplitudeData, theorem_record


class ProjectiveAmplitudeTests(unittest.TestCase):
    def test_amplitude_cancellation(self) -> None:
        row = ProjectiveAmplitudeData(D=60, B=17, C=21, q0=3, m=7, v=-2)
        self.assertAlmostEqual(row.leading_amplitude, row.simplified_amplitude, places=14)

    def test_anchor_relation_required(self) -> None:
        with self.assertRaises(ValueError):
            ProjectiveAmplitudeData(D=60, B=17, C=20, q0=3, m=7, v=0)

    def test_record(self) -> None:
        row = theorem_record()
        self.assertIn("no remaining power of H", row["amplitude_collapse"])
        self.assertIn("hat(U)(-H0 P(z_v))", row["radial_profile"])
        self.assertIn("O(1/m)", row["remainder"])
        self.assertIn("no arithmetic cancellation", row["boundary"])


if __name__ == "__main__":
    unittest.main()
