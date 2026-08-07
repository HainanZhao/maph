from __future__ import annotations

import contextlib
import io
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "proof"))

import verify_cover_23_6_2_bounded_archive as archive  # noqa: E402
import verify_cover_23_6_2_branch_partition as partition  # noqa: E402
import verify_cover_23_6_2_cnf_primitives as primitives  # noqa: E402


def terminal_log(status: str | None, exit_code: int) -> str:
    status_line = f"s {status}\n" if status is not None else ""
    return (
        status_line
        + "c conflicts: 123 1.00 per second\n"
        + "c decisions: 456 2.00 per second\n"
        + "c total process time since initialization: 7.50 seconds\n"
        + "c total real time since initialization: 8.00 seconds\n"
        + "c maximum resident set size of process: 9.25 MB\n"
        + f"c exit {exit_code}\n"
    )


class ArchiveLogParserTests(unittest.TestCase):
    def parse(self, text: str) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "solver.log"
            path.write_text(text, encoding="ascii")
            return archive.parse_terminal_log(path)

    def test_live_log(self) -> None:
        row = self.parse("c progress without terminal statistics\n")
        self.assertEqual(row["status"], "LIVE")

    def test_unknown_limit_log(self) -> None:
        row = self.parse(terminal_log(None, 0))
        self.assertEqual(row["status"], "UNKNOWN_SOLVER_LIMIT")
        self.assertEqual(row["conflicts"], 123)
        self.assertEqual(row["decisions"], 456)
        self.assertEqual(row["real_seconds"], 8.0)

    def test_sat_log(self) -> None:
        row = self.parse(terminal_log("SATISFIABLE", 10))
        self.assertEqual(row["status"], "SATISFIABLE")

    def test_unsat_log(self) -> None:
        row = self.parse(terminal_log("UNSATISFIABLE", 20))
        self.assertEqual(row["status"], "UNSATISFIABLE")

    def test_mismatched_status_and_exit_is_rejected(self) -> None:
        with self.assertRaises(AssertionError):
            self.parse(terminal_log("SATISFIABLE", 20))

    def test_partial_terminal_block_is_rejected(self) -> None:
        with self.assertRaises(AssertionError):
            self.parse("c conflicts: 123 1.00 per second\n")


class IndependentControlTests(unittest.TestCase):
    def test_dpll(self) -> None:
        self.assertTrue(primitives.satisfiable([[1, 2], [-1, 2]]))
        self.assertFalse(primitives.satisfiable([[1], [-1]]))

    def test_excess_partitions(self) -> None:
        surviving = {row for row in partition.partitions(5) if len(row) >= 3}
        self.assertEqual(
            surviving,
            {(3, 1, 1), (2, 2, 1), (2, 1, 1, 1), (1, 1, 1, 1, 1)},
        )


class FreshCheckoutReplayTests(unittest.TestCase):
    def test_archive_replay_without_derived_cnfs(self) -> None:
        source = PROJECT / "discovery" / "out"
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "out"
            for name in archive.PRECURSOR_SUMMARIES:
                source_summary = source / name / "summary.json"
                target_summary = output / name / "summary.json"
                target_summary.parent.mkdir(parents=True)
                shutil.copyfile(source_summary, target_summary)
            for wave, branches in archive.WAVES.items():
                source_wave = source / wave
                target_wave = output / wave
                target_wave.mkdir(parents=True)
                shutil.copyfile(source_wave / "summary.json", target_wave / "summary.json")
                for branch in branches:
                    name = f"{branch}.solver.log"
                    shutil.copyfile(source_wave / name, target_wave / name)

            self.assertFalse(any(output.rglob("*.cnf")))
            previous_output, previous_argv = archive.OUTPUT, sys.argv
            archive.OUTPUT = output
            sys.argv = ["verify_cover_23_6_2_bounded_archive.py"]
            rendered = io.StringIO()
            try:
                with contextlib.redirect_stdout(rendered):
                    archive.main()
            finally:
                archive.OUTPUT, sys.argv = previous_output, previous_argv

            result = json.loads(rendered.getvalue())
            self.assertEqual(result["status"], "ARCHIVE_TERMINAL_PASS")
            self.assertEqual(result["derived_wave4_status"], "WALL_CAP_DERIVED")
            self.assertEqual(result["regenerated_cnfs"], 11)
            self.assertFalse(any(output.rglob("*.cnf")))


if __name__ == "__main__":
    unittest.main()
