import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/anchor_aware_correction_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("anchor_aware_correction_v1", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AnchorAwareCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_phase_row_is_flat(self):
        self.assertEqual(self.rows["flat_phase_row"]["normalized_coordinate_squared"], 1 / self.rows["flat_phase_row"]["norm_squared"])

    def test_augmented_determinant_zero(self):
        self.assertEqual(self.rows["flat_phase_row"]["augmented_determinant"], 0)

    def test_distance_zero(self):
        self.assertEqual(self.rows["flat_phase_row"]["distance_to_row_span_squared"], 0)

    def test_full_column_span(self):
        row = self.rows["full_column_rank"]
        self.assertGreaterEqual(row["k"], row["N"])
        self.assertEqual(row["reconstruction"], row["detector"])

    def test_anchor_cap_subpower(self):
        self.assertEqual(self.rows["anchor_reformulation"]["anchor_cap"], "r=X^o(1)")


if __name__ == "__main__":
    unittest.main()
