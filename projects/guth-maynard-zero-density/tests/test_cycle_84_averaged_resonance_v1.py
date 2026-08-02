import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "conventions"))

from averaged_resonance_v1 import (  # noqa: E402
    NEW_CUTOFF,
    OLD_CUTOFF,
    VOLUME_CUTOFF,
    block_ledger,
    incidence_terms,
    l1_terms,
    verify_all,
)

Q = Fraction


class AveragedResonanceTests(unittest.TestCase):
    def test_incidence_terms(self) -> None:
        row = incidence_terms(Q(1, 2))
        self.assertEqual(row["volume"], Q(23, 30))
        self.assertEqual(row["length"], Q(3, 5))
        self.assertEqual(row["crossing"], Q(5, 6))

    def test_outer_projector_terms(self) -> None:
        row = l1_terms(Q(1, 2))
        self.assertEqual(row["volume"], Q(11, 10))
        self.assertEqual(row["length"], Q(14, 15))
        self.assertEqual(row["crossing"], Q(7, 6))

    def test_cutoff_width_and_volume_gap(self) -> None:
        self.assertEqual(NEW_CUTOFF, Q(43, 75))
        self.assertEqual(NEW_CUTOFF - OLD_CUTOFF, Q(2, 25))
        self.assertEqual(VOLUME_CUTOFF - NEW_CUTOFF, Q(1, 15))

    def test_strictness_and_tie(self) -> None:
        self.assertTrue(block_ledger(OLD_CUTOFF)["strictly_closed"])
        endpoint = block_ledger(NEW_CUTOFF)
        self.assertFalse(endpoint["strictly_closed"])
        self.assertEqual(endpoint["margin"], 0)

    def test_annular_decay(self) -> None:
        central = l1_terms(Q(8, 15), Q(0))
        annular = l1_terms(Q(8, 15), Q(1, 20))
        self.assertTrue(all(annular[key] < central[key] for key in central))

    def test_verification(self) -> None:
        row = verify_all()
        self.assertEqual(row["band_width"], "2/25")
        self.assertEqual(row["crossing_gap_to_volume"], "1/15")
        self.assertIn("inverse theorem", row["gate"])


if __name__ == "__main__":
    unittest.main()

