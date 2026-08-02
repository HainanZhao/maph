from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
from pathlib import Path
import unittest


PROJECT = Path(__file__).resolve().parents[1]
CONVENTIONS = PROJECT / "conventions/localized_comb_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("localized_comb_v1", CONVENTIONS)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Cycle42LocalizedCombV1Tests(unittest.TestCase):
    def test_relaxation_loss(self):
        self.assertEqual(load_module().comb_ledger(3)["full_annulus_relaxation_loss"], Q(9, 10))

    def test_s3_diagonal(self):
        row = load_module().comb_ledger(3)
        self.assertEqual(row["localized_diagonal_vector"], Q(61, 10))
        self.assertEqual(row["lcam_target"], Q(61, 10))

    def test_s4_diagonal(self):
        row = load_module().comb_ledger(4)
        self.assertEqual(row["localized_diagonal_vector"], Q(71, 10))
        self.assertEqual(row["lcam_target"], Q(71, 10))

    def test_claim_boundary(self):
        document = (PROJECT / "docs/cycle-42-localized-comb-v1.md").read_text(encoding="utf-8")
        self.assertIn("superseded as the lead", document)
        self.assertIn("diagonal-sharp", document)
        self.assertIn("No kernel-count, density, or interval gain", document)


if __name__ == "__main__":
    unittest.main()
