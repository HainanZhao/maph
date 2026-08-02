import hashlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "artifacts/cycle-167-affine-fibre-transport-v1.json"
CORRECTION = ROOT / "docs/cycle-167-affine-fibre-transport-scope-correction-v1.md"
ORIGINAL_SHA256 = "7ba12c9d0534c0d0d151bce753fa24191c4e174af839ca12b86d65911779ed1b"


class Cycle167ScopeCorrectionTests(unittest.TestCase):
    def test_original_is_preserved_and_scope_is_narrowed(self):
        self.assertEqual(hashlib.sha256(ORIGINAL.read_bytes()).hexdigest(), ORIGINAL_SHA256)
        original = json.loads(ORIGINAL.read_text(encoding="utf-8"))
        self.assertIn("one-step affine multiplicative", original["claim_boundary"])
        correction = CORRECTION.read_text(encoding="utf-8")
        self.assertIn("reduced-rational affine multiplicative", correction)
        self.assertIn("No identity, convention, finite test, parent-count result", correction)


if __name__ == "__main__":
    unittest.main()
