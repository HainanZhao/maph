from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.verify_lane_b_spin_parity_intertwiner import verify  # noqa: E402


class SpinParityIntertwinerTest(unittest.TestCase):
    def test_exact_bridge(self) -> None:
        payload = verify()
        self.assertEqual([row["width"] for row in payload["controls"]], [2, 2, 3])
        self.assertTrue(all(row.get("identity_holds", True) for row in payload["controls"]))


if __name__ == "__main__":
    unittest.main()
