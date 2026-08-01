import hashlib
import importlib.util
from pathlib import Path
import unittest


PROJECT = Path(__file__).resolve().parents[1]
RUNTIME = PROJECT / "conventions/proof_runtime_v1.py"


class ProofRuntimeV1Tests(unittest.TestCase):
    def test_pinned_runtime(self) -> None:
        spec = importlib.util.spec_from_file_location("proof_runtime_v1", RUNTIME)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.assert_pinned_runtime()["version"], "3.12.3")
        self.assertEqual(len(hashlib.sha256(RUNTIME.read_bytes()).hexdigest()), 64)


if __name__ == "__main__":
    unittest.main()
