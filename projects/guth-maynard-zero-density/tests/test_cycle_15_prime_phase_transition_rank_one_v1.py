from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/prime_phase_transition_rank_one_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("prime_phase_transition_rank_one_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PrimePhaseTransitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_exact_finite_identity(self):
        for fourth, norm in zip(self.rows["finite_fourth_counts"], self.rows["finite_square_norms"]):
            self.assertEqual(fourth["formula"], norm["total"])

    def test_phase_transition(self):
        row = self.rows["phase_transition"]
        self.assertEqual(row["p_star"], Fraction(24, 5))
        self.assertEqual(row["coherent_exponent"], row["random_bulk_exponent"])

    def test_generic_gm_terms(self):
        row = self.rows["rank_one_gm_translation"]
        self.assertEqual((row["gm_term_1"], row["gm_term_2"], row["gm_term_3"]), (Fraction(6, 5), Fraction(8, 5), Fraction(8, 5)))

    def test_target_saving(self):
        row = self.rows["rank_one_gm_translation"]
        self.assertEqual(row["target_exponent"], Fraction(36, 25))
        self.assertEqual(row["required_saving"], Fraction(4, 25))
        self.assertEqual(row["saving_in_v"], Fraction(4, 5))


if __name__ == "__main__":
    unittest.main()
