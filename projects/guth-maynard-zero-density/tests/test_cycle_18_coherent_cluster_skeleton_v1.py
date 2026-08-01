from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/coherent_cluster_skeleton_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("coherent_cluster_skeleton_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CoherentClusterSkeletonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_local_exponent(self):
        self.assertEqual(self.rows["local_large_values"]["cluster_exponent"], Fraction(3, 5))

    def test_selected_classical_branch(self):
        self.assertEqual(self.rows["local_large_values"]["selected_branch"], Fraction(-2, 5))

    def test_target_skeleton(self):
        self.assertEqual(self.rows["skeleton_translation"]["target_skeleton"], Fraction(21, 25))

    def test_saving_preserved(self):
        self.assertEqual(self.rows["skeleton_translation"]["required_saving"], Fraction(4, 25))


if __name__ == "__main__":
    unittest.main()
