from __future__ import annotations

import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))

from verify_cycle_199_full_theta_carrier import (  # noqa: E402
    BLOCKS,
    full_block_fourier_action,
    poincare_poisson_transport,
    run,
    source_label_coverage,
)


class FullThetaCarrierTests(unittest.TestCase):
    def test_all_four_blocks_are_fourier_closed(self) -> None:
        result = full_block_fourier_action()
        self.assertEqual(set(result["action"]), set(BLOCKS))
        self.assertTrue(result["F24_preserves_W"])
        self.assertEqual(result["action"]["B_(1,-)"]["target"], "B_(1,-)")

    def test_poincare_transport_is_on_full_fibre(self) -> None:
        result = poincare_poisson_transport()
        self.assertEqual(result["finite_fibre_dimension"], 24)
        self.assertTrue(result["continuous_discrete_Fourier_preserves_seed_fibre"])
        self.assertFalse(result["meromorphic_beta_kernel_in_seed_domain"])

    def test_all_source_labels_are_covered_without_alias_selection(self) -> None:
        result = source_label_coverage()
        self.assertEqual(result["records_checked"], 144)
        self.assertTrue(result["all_24_source_labels_covered"])
        self.assertTrue(result["all_four_blocks_accessed"])

    def test_scope_stays_below_endpoint_claim(self) -> None:
        result = run()
        self.assertIn("does not put the meromorphic beta kernel", result["claim_boundary"])
        self.assertIn("lambda-independent Abel endpoint", result["next_required_construction"])


if __name__ == "__main__":
    unittest.main()
