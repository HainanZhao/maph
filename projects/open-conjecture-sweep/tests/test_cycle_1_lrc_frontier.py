from __future__ import annotations

from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class LonelyRunnerFrontierTests(unittest.TestCase):
    def test_published_baselines_against_independent_bruteforce(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            binary = Path(temporary) / "lrc_ansatz_exact"
            subprocess.run(
                [
                    "g++", "-std=c++20", "-O3", "-DNDEBUG", "-Wall", "-Wextra", "-Wpedantic",
                    "-pthread", str(ROOT / "discovery/lrc_ansatz_exact.cpp"), "-o", str(binary),
                ],
                check=True,
            )
            for k, expected in ((6, 53), (7, 50)):
                tuples = Path(temporary) / f"k{k}-p47.txt"
                run = subprocess.run(
                    [
                        str(binary), "--k", str(k), "--p", "47", "--threads", "2",
                        "--max-seconds", "30", "--output", str(tuples),
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                self.assertIn(f"canonical_solutions={expected}\n", run.stdout)
                subprocess.run(
                    [
                        "python3", str(ROOT / "discovery/check_lrc_ansatz.py"), "--k", str(k),
                        "--p", "47", "--tuples", str(tuples), "--brute-force",
                        "--expected-count", str(expected),
                    ],
                    check=True,
                )


if __name__ == "__main__":
    unittest.main()
