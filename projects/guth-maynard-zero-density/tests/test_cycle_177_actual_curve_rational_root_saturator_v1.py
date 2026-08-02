from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "conventions/actual_curve_rational_root_saturator_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("actual_curve_rational_root_saturator_v1", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ActualCurveRationalRootSaturatorTest(unittest.TestCase):
    def test_exact_ledgers(self) -> None:
        module = load_module()
        row = module.verify_all()
        self.assertEqual(row["exponents"]["pair_target_gap"], module.Q(1, 5))
        self.assertEqual(row["exponents"]["triple_target_gap"], module.Q(1, 5))

    def test_pair_and_packet_scale(self) -> None:
        module = load_module()
        self.assertGreaterEqual(module.pair_weight(400, 5), module.pair_lower_bound(400, 5))
        packet = module.seeded_packet(400, 5)
        self.assertEqual(packet["depth"], 20)
        self.assertGreaterEqual(packet["row_count"], 41)


if __name__ == "__main__":
    unittest.main()
