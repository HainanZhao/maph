import json
from pathlib import Path
import tempfile
import unittest

from proof.cycle_seal_v1 import freeze_inputs, render, sha256, validate_prior


class CycleSealTests(unittest.TestCase):
    def test_hash_freeze_and_relative_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "input.txt"
            source.write_text("frozen\n", encoding="utf-8")
            record = freeze_inputs(root, {"input": (source, sha256(source))})
            self.assertEqual(record["input"]["path"], "input.txt")

    def test_hash_mismatch_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "input.txt"
            source.write_text("changed\n", encoding="utf-8")
            with self.assertRaises(RuntimeError):
                freeze_inputs(root, {"input": (source, "0" * 64)})

    def test_prior_status_and_render(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "prior.json"
            path.write_text(json.dumps({"status": "SEALED"}), encoding="utf-8")
            self.assertEqual(validate_prior(path, "SEALED")["status"], "SEALED")
            with self.assertRaises(RuntimeError):
                validate_prior(path, "OTHER")
        self.assertEqual(render({"b": 1, "a": 2}), b'{\n  "a": 2,\n  "b": 1\n}\n')


if __name__ == "__main__":
    unittest.main()
