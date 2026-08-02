from fractions import Fraction
import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/variable_rank_self_dual_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("variable_rank_self_dual_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class VariableRankSelfDualTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_table_size(self):
        self.assertEqual(len(self.rows["tradeoff_table"]), 5)

    def test_every_reconstruction_positive(self):
        self.assertTrue(all(row["reconstruction"] > 0 for row in self.rows["tradeoff_table"]))

    def test_self_dual_block_count(self):
        row = self.rows["self_dual"]
        self.assertEqual(row["block_count"], row["missing_saving"])

    def test_self_dual_block_size(self):
        row = self.rows["self_dual"]
        self.assertEqual(row["block_size"], row["target_rows"])

    def test_self_dual_reconstruction(self):
        self.assertEqual(self.rows["self_dual"]["reconstruction"], Fraction(2, 25))


if __name__ == "__main__":
    unittest.main()
