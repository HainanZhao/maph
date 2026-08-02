import unittest

from conventions.projective_radial_phase_v1 import RadialPhaseData, theorem_record


class ProjectiveRadialPhaseTests(unittest.TestCase):
    def test_saddle_identity(self) -> None:
        row = RadialPhaseData(D=48, p0=2, q0=3, n=11, n_prime=7, m=5, u=-2, v=3)
        self.assertAlmostEqual(row.projective_phase(row.z_saddle), row.radial_frequency, places=12)
        self.assertGreater(row.projective_curvature, 0.0)

    def test_residual_orientation(self) -> None:
        for u in (-1, 0, 1):
            row = RadialPhaseData(D=80, p0=1, q0=1, n=21, n_prime=9, m=10, u=u, v=0)
            if abs(row.residual) <= row.A / 2:
                self.assertEqual(row.radial_frequency > 0, row.residual > 0)

    def test_record(self) -> None:
        row = theorem_record()
        self.assertIn("H P_(u,v)(z)", row["normal_form"])
        self.assertIn("c/[z_v(1-z_v)]", row["curvature"])
        self.assertIn("retaining residual sign", row["signed_kernel"])
        self.assertIn("no cancellation estimate", row["boundary"])


if __name__ == "__main__":
    unittest.main()
