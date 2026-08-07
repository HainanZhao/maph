from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.cycle_seal_v1 import freeze_inputs, render, sha256  # noqa: E402


class CycleSealTests(unittest.TestCase):
    def test_render_is_deterministic(self) -> None:
        self.assertEqual(render({"b": 2, "a": 1}), b'{\n  "a": 1,\n  "b": 2\n}\n')

    def test_freeze_checks_hash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "input.txt"
            source.write_text("frozen\n")
            frozen = freeze_inputs(root, {"input": (source, sha256(source))})
            self.assertEqual(json.loads(json.dumps(frozen))["input"]["path"], "input.txt")
            with self.assertRaises(RuntimeError):
                freeze_inputs(root, {"input": (source, "0" * 64)})


if __name__ == "__main__":
    unittest.main()
