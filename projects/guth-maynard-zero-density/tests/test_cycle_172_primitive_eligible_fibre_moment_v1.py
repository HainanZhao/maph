import unittest

from conventions.primitive_eligible_fibre_moment_v1 import family, verify_all, verify_family


class Cycle172PrimitiveEligibleFibreMomentTests(unittest.TestCase):
    def test_exact_small_family(self) -> None:
        record = verify_family(3)
        self.assertEqual(record["row_count"], 2)
        self.assertIn("M=W/2", record["moment"])
        self.assertIn("g=c=u=v=1", record["projective"])

    def test_massed_family_preserves_complete_rows(self) -> None:
        data = family(12)
        self.assertEqual(len(data["rows"]), 5)
        self.assertEqual(data["rows"][0]["h"], 180)
        self.assertEqual(data["rows"][-1]["h_plus"], 160)

    def test_scoped_no_go_boundary(self) -> None:
        theorem = verify_all()
        self.assertEqual(theorem["checked_scales"], [1, 2, 3, 12])
        self.assertIn("outside the actual positive exponential curve", theorem["scope"])
