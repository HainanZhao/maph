import unittest
from pathlib import Path


class Cycle174FormatCorrectionTests(unittest.TestCase):
    def test_only_format_change_is_described(self) -> None:
        text = (Path(__file__).resolve().parents[1] / "docs/cycle-174-adaptive-slack-transport-format-correction-v1.md").read_text()
        self.assertIn("No identity, convention, test, threshold", text)
