import unittest

from proof.verify_global_phase_telescoping import verify


class GlobalPhaseTelescopingTests(unittest.TestCase):
    def test_phase_potential_and_integer_core_identity(self):
        result = verify()
        self.assertTrue(result["history_independence_checked"])
        self.assertTrue(all(row["all_spin_structures_agree"] for row in result["prime_rows"]))


if __name__ == "__main__":
    unittest.main()

