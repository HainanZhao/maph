import unittest

from conventions.joint_radial_alias_v1 import JointAliasData, theorem_record


class JointRadialAliasTests(unittest.TestCase):
    def test_joint_stationarity_and_value(self) -> None:
        row = JointAliasData(D=72, p0=2, q0=3, n_prime=11, m=7, u=-2, v=4, ell=19)
        self.assertAlmostEqual(row.phase(row.H_saddle, row.n_saddle), row.stationary_value, places=10)
        self.assertLess(row.hessian_determinant, 0.0)

    def test_amplitude_collapse(self) -> None:
        row = JointAliasData(D=60, p0=3, q0=2, n_prime=13, m=8, u=1, v=-3, ell=17)
        self.assertAlmostEqual(row.total_amplitude, row.simplified_amplitude, places=13)

    def test_record(self) -> None:
        row = theorem_record()
        self.assertIn("signature zero", row["hessian"])
        self.assertIn("-ell n'g^u", row["stationary_value"])
        self.assertIn("(q0/p0)g^(u+v)", row["total_amplitude"])
        self.assertIn("-(u+v)/D", row["cutoffs"])
        self.assertIn("e(-ell n'g^u)", row["factorization"])
        self.assertIn("no bilinear estimate", row["boundary"])


if __name__ == "__main__":
    unittest.main()
