"""Ensure the Cycle-163 correction supplies the generated-handoff target."""
from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class Cycle163StatusCorrectionTests(unittest.TestCase):
    def test_v1_has_no_target_and_v2_is_explicitly_non_counted(self) -> None:
        original = json.loads(
            (ROOT / "artifacts/cycle-163-spectral-ray-interface-v1.json").read_text()
        )
        self.assertNotIn("remaining_target", original)
        correction = (ROOT / "docs/cycle-163-spectral-ray-interface-v2.md").read_text()
        self.assertIn("non-counted metadata correction", correction)
        self.assertIn("Cycle 164 / B002", correction)


if __name__ == "__main__":
    unittest.main()
