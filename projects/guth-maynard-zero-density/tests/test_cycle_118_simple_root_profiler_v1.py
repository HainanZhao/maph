import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SimpleRootProfilerTests(unittest.TestCase):
    def test_frozen_counts(self) -> None:
        data = json.loads((ROOT / "discovery/cycle-118-simple-root-profiler-v1.json").read_text())
        self.assertEqual(data["mpmath_version"], "1.2.1")
        self.assertEqual([row["simple"] for row in data["rows"]], [3461, 7400, 16128])
        last = data["rows"][-1]["signatures"]
        self.assertEqual(last["J0_NONZERO/J1_NONZERO/OPPOSITE"], 9184)
        self.assertEqual(last["J0_NONZERO/J1_NONZERO/SAME"], 6754)

    def test_examples_retain_payload(self) -> None:
        data = json.loads((ROOT / "discovery/cycle-118-simple-root-profiler-v1.json").read_text())
        for row in data["rows"]:
            for example in row["examples"].values():
                self.assertTrue({"A", "B", "C", "a", "b", "J0", "J1", "delta", "eta"} <= set(example))


if __name__ == "__main__":
    unittest.main()
