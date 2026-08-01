import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest


PROJECT = Path(__file__).resolve().parents[1]
RUNTIME = PROJECT / "conventions/proof_runtime_v2.py"


class ProofRuntimeV2Tests(unittest.TestCase):
    def test_normal_runtime_passes(self) -> None:
        spec = importlib.util.spec_from_file_location("proof_runtime_v2", RUNTIME)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.require_pinned_runtime()["optimize"], 0)

    def test_optimized_runtime_fails_explicitly(self) -> None:
        code = (
            "import importlib.util;"
            f"p={str(RUNTIME)!r};"
            "s=importlib.util.spec_from_file_location('r',p);"
            "m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"
            "m.require_pinned_runtime()"
        )
        completed = subprocess.run([sys.executable, "-O", "-c", code], capture_output=True, text=True)
        self.assertNotEqual(completed.returncode, 0)
        self.assertIn("forbids -O/-OO", completed.stderr)


if __name__ == "__main__":
    unittest.main()
