from __future__ import annotations

from fractions import Fraction as Q
import importlib.util
from pathlib import Path
import unittest


PROJECT = Path(__file__).resolve().parents[1]
CONVENTIONS = PROJECT / "conventions/row_lattice_beatty_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("row_lattice_beatty_v1", CONVENTIONS)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Cycle43RowLatticeBeattyV1Tests(unittest.TestCase):
    def test_target_windows(self):
        row = load_module().target_ledger()
        self.assertEqual(row["log_resonance_window"], Q(-36, 25))
        self.assertEqual(row["integer_shift_window"], Q(-11, 25))

    def test_shift_and_curvature(self):
        row = load_module().target_ledger()
        self.assertEqual(row["small_k_shift_scale"], Q(2, 5))
        self.assertEqual(row["linearization_error"], Q(-1, 5))
        self.assertGreater(row["linearization_error"], row["integer_shift_window"])

    def test_maximal_occupancy(self):
        row = load_module().target_ledger(Q(9, 5))
        self.assertEqual(row["integer_shift_window"], Q(-7, 5))

    def test_claim_boundary(self):
        document = (PROJECT / "docs/cycle-43-row-lattice-beatty-v1.md").read_text(encoding="utf-8")
        self.assertIn("stress model", document)
        self.assertIn("is mandatory", document)
        self.assertIn("does not reduce an", document)


if __name__ == "__main__":
    unittest.main()
