import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "proof/check_cycle_17_prime_phase_separable_search_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("check_cycle_17", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Cycle17SearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().validate()

    def test_registered_status(self):
        self.assertEqual(self.rows["status"], "BASELINE_APPROACHED")

    def test_best_row(self):
        self.assertEqual(self.rows["best"]["m"], 16)
        self.assertEqual(self.rows["best"]["count"], 67)

    def test_larger_sizes_do_not_cross(self):
        self.assertEqual(set(self.rows["larger_size_best"]), {"32", "48", "64"})
        self.assertTrue(all(row["count_exponent"] < 36 / 25 for row in self.rows["larger_size_best"].values()))


if __name__ == "__main__":
    unittest.main()
