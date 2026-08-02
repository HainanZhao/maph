from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
from pathlib import Path
import unittest


PROJECT = Path(__file__).resolve().parents[1]
CONVENTIONS = PROJECT / "conventions/hollow_notch_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("hollow_notch_v1", CONVENTIONS)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Cycle40HollowNotchV1Tests(unittest.TestCase):
    def test_s3(self):
        row = load_module().coherent_floor(3)
        self.assertEqual(row["vector_floor"], Q(8))
        self.assertEqual(row["global_floor_excess_over_ampr"], Q(19, 10))

    def test_s4(self):
        row = load_module().coherent_floor(4)
        self.assertEqual(row["vector_floor"], Q(10))
        self.assertEqual(row["global_floor_excess_over_ampr"], Q(29, 10))

    def test_fixed_m_floor(self):
        module = load_module()
        self.assertEqual(module.coherent_floor(3)["fixed_m_floor"], Q(77, 10))
        self.assertEqual(module.coherent_floor(4)["fixed_m_floor"], Q(97, 10))

    def test_claim_boundary(self):
        document = (PROJECT / "docs/cycle-40-hollow-notch-v1.md").read_text(encoding="utf-8")
        self.assertIn("not a counterexample", document)
        self.assertIn("No bound for this notched operator", document)
        self.assertIn("no kernel-count, density, or interval improvement", document)


if __name__ == "__main__":
    unittest.main()
