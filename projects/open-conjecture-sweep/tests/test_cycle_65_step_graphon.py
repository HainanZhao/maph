import pathlib
import subprocess
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class Cycle65StepGraphonTest(unittest.TestCase):
    def test_sources_compile_and_exact_controls(self):
        with tempfile.TemporaryDirectory() as raw:
            tmp_path = pathlib.Path(raw)
            search = tmp_path / "search"
            exact = tmp_path / "exact"
            subprocess.run([
                "g++", "-O3", "-std=c++20",
                str(ROOT / "discovery/cycle65_step_graphon_search.cpp"), "-o", str(search)
            ], check=True)
            subprocess.run([
                "g++", "-O3", "-std=c++20",
                str(ROOT / "proof/cycle65_step_graphon_exact.cpp"), "-o", str(exact)
            ], check=True)
            # The full frozen DE is intentionally not a unit test. Supply three
            # valid candidate files; the exact executable still checks all
            # 3,125 grid rows and its independent 1,024-assignment controls.
            candidate = tmp_path / "candidates.tsv"
            candidate.write_text(
                "seed\trank\tp\tq\tw01\tw10\tw11\tlog_ratio\tt_H\tm\tfloat_deficit\n"
                "0\t0\t0.5\t0.5\t1\t1\t1\t0\t1\t1\t0\n"
            )
            out = tmp_path / "out"
            subprocess.run([str(exact), str(out), str(candidate), str(candidate), str(candidate)], check=True)
            text = (out / "exact-summary.json").read_text()
            self.assertIn('"grid_rows": 3125', text)
            self.assertIn('"grid_negative": 0', text)
            self.assertIn('"grid_zero_other": 0', text)
            self.assertIn('"candidate_negative": 0', text)


if __name__ == "__main__":
    unittest.main()
