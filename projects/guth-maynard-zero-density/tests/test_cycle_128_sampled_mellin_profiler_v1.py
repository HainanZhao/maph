import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "discovery/cycle-128-sampled-mellin-profiler-v1.json"


class SampledMellinProfilerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(OUTPUT.read_text(encoding="utf-8"))

    def test_frozen_runtime(self) -> None:
        self.assertEqual(self.payload["mpmath_version"], "1.2.1")
        self.assertEqual(self.payload["decimal_digits"], 80)
        self.assertEqual(len(self.payload["rows"]), 18)

    def test_aggregate_counts(self) -> None:
        radius_one = [row for row in self.payload["rows"] if row["radius"] == 1]
        radius_four = [row for row in self.payload["rows"] if row["radius"] == 4]
        self.assertEqual(sum(row["total_hits"] for row in radius_one), 16)
        self.assertEqual(sum(row["total_hits"] for row in radius_four), 48)
        self.assertEqual(max(row["max_ray_multiplicity"] for row in self.payload["rows"]), 1)

    def test_convergents_and_high_branch(self) -> None:
        self.assertEqual(sum(row["nonconvergent_rays"] for row in self.payload["rows"]), 0)
        self.assertEqual(sum(row["rays_above_cycle125_threshold"] for row in self.payload["rows"]), 0)
        self.assertEqual(max(row["longest_popular_chain"] for row in self.payload["rows"]), 3)


if __name__ == "__main__":
    unittest.main()
