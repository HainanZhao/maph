from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
from pathlib import Path
import unittest


PROJECT = Path(__file__).resolve().parents[1]
CONVENTIONS = PROJECT / "conventions/annular_sampling_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("annular_sampling_v1", CONVENTIONS)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Cycle41AnnularSamplingV1Tests(unittest.TestCase):
    def test_s3_leakage(self):
        row = load_module().leakage(3)
        self.assertEqual(row["leakage_exponent"], Q(47, 10))
        self.assertEqual(row["leakage_margin"], Q(7, 5))

    def test_s4_leakage(self):
        row = load_module().leakage(4)
        self.assertEqual(row["leakage_exponent"], Q(67, 10))
        self.assertEqual(row["leakage_margin"], Q(2, 5))

    def test_decay_order(self):
        self.assertEqual(load_module().registered_scales()["decay_order"], 9)

    def test_claim_boundary(self):
        document = (PROJECT / "docs/cycle-41-annular-sampling-v1.md").read_text(encoding="utf-8")
        self.assertIn("changes sign", document)
        self.assertIn("count of absolute near collisions", document)
        self.assertIn("No kernel-count, density, or interval gain", document)


if __name__ == "__main__":
    unittest.main()
