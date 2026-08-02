import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "conventions"))

from fejer_vdc_resonance_v1 import (  # noqa: E402
    NEW_CUTOFF,
    OLD_CUTOFF,
    annular_net_terms,
    block_ledger,
    central_resonance,
    resonance_terms,
    verify_all,
)

Q = Fraction


class FejerVdcResonanceTests(unittest.TestCase):
    def test_derivative_hypothesis_range(self) -> None:
        self.assertEqual(
            resonance_terms(NEW_CUTOFF)["second_derivative_ceiling"], Q(-28, 75)
        )

    def test_active_dominance(self) -> None:
        for xi in (OLD_CUTOFF, Q(9, 20), NEW_CUTOFF):
            self.assertEqual(central_resonance(xi), xi / 2 + Q(1, 6))

    def test_cutoff_and_width(self) -> None:
        self.assertEqual(NEW_CUTOFF, Q(37, 75))
        self.assertEqual(NEW_CUTOFF - OLD_CUTOFF, Q(17, 225))

    def test_strict_endpoint(self) -> None:
        self.assertTrue(block_ledger(OLD_CUTOFF)["strictly_closed"])
        endpoint = block_ledger(NEW_CUTOFF)
        self.assertFalse(endpoint["strictly_closed"])
        self.assertEqual(endpoint["margin"], 0)

    def test_annular_schwartz_decay_absorbs_growth(self) -> None:
        central = annular_net_terms(Q(9, 20), Q(0))
        annulus = annular_net_terms(Q(9, 20), Q(1, 10))
        self.assertTrue(all(annulus[key] < central[key] for key in central))

    def test_verification(self) -> None:
        row = verify_all()
        self.assertEqual(row["band_width"], "17/225")
        self.assertIn("exponent-pair", row["gate"])


if __name__ == "__main__":
    unittest.main()

