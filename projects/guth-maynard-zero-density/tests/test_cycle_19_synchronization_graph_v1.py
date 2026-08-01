from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/synchronization_graph_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("synchronization_graph_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SynchronizationGraphTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_critical_exponents(self):
        row = self.rows["critical_exponents"]
        self.assertEqual(row["correlation_scale"], Fraction(2, 5))
        self.assertEqual(row["popular_ordered_pairs"], Fraction(27, 25))
        self.assertEqual(row["average_degree"], Fraction(6, 25))
        self.assertEqual(row["ordered_two_step_paths"], Fraction(33, 25))

    def test_simplex_is_positive(self):
        row = self.rows["finite_common_component_simplex"]
        self.assertGreater(row["small_gram_eigenvalue"], 0)
        self.assertGreater(row["large_gram_eigenvalue"], 0)

    def test_simplex_has_all_popular_pairs(self):
        row = self.rows["finite_common_component_simplex"]
        self.assertEqual(row["popular_ordered_pairs"], row["R"] * (row["R"] - 1))
        self.assertGreaterEqual(row["popular_ordered_pairs"], row["registered_pair_lower"])

    def test_two_step_path_bound_is_sharp_for_complete_graph(self):
        row = self.rows["finite_common_component_simplex"]
        self.assertEqual(row["ordered_two_step_paths"], row["path_lower"])

    def test_entropy_countermodel(self):
        self.assertEqual(self.rows["finite_common_component_simplex"]["phase_code_entropy"], 0)


if __name__ == "__main__":
    unittest.main()
