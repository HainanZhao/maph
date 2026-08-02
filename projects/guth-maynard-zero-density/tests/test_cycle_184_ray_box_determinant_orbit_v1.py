import unittest

from conventions.ray_box_determinant_orbit_v1 import lcm_resonance, nonrational_two_ray_family, verify_all


class Cycle184RayBoxDeterminantOrbitTest(unittest.TestCase):
    def test_lcm_identity_is_exact(self) -> None:
        record = lcm_resonance(v=6, u=4, w=10, A=17, B=29, alpha_left=1, alpha_right=2)
        self.assertEqual(record["left_side"], record["right_side"])
        self.assertEqual(record["F"] % record["gcd_u_w"], 0)

    def test_nonnatural_family_is_subseed_and_nonsquare(self) -> None:
        family = nonrational_two_ray_family(3)
        self.assertTrue(family["fibres"]["all_depths_below_seed"])
        self.assertNotEqual(family["determinant"]["F"], 0)
        self.assertLess(family["populated_box"]["one_box_lower_bound"], 3**23)

    def test_replay_boundary(self) -> None:
        record = verify_all()
        self.assertIn("no independent error", record["lcm_resonance"])
        self.assertIn("no upper bound", record["boundary"])


if __name__ == "__main__":
    unittest.main()
