import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "conventions/anchor_aware_scope_correction_v2.py"


def load_module():
    spec = importlib.util.spec_from_file_location("anchor_aware_scope_correction_v2", PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AnchorAwareScopeCorrectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = load_module().verify_all()

    def test_one_anchor_floor(self):
        row = self.rows["one_anchor"]
        self.assertEqual(row["kernel_lower"], row["evaluation_floor"] - row["approximation_error"])

    def test_multi_anchor_coefficients_large(self):
        self.assertGreater(self.rows["multi_anchor"]["l1_norm"], 1)

    def test_original_detector_valid(self):
        self.assertIn("sqrt(rho)", self.rows["valid_direction"])

    def test_adaptive_direction_needs_gate(self):
        self.assertIn("evaluation floor", self.rows["adaptive_direction_gate"])


if __name__ == "__main__":
    unittest.main()
