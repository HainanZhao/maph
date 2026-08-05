#!/usr/bin/env python3
"""Exact controls for the C68 five-cube Bernstein certificate engine."""

from __future__ import annotations

import csv
import json
import subprocess
import tempfile
from pathlib import Path


HEADER = ("x", "y", "z", "v", "lambda", "numerator", "denominator")


def write_polynomial(path: Path, rows: list[tuple[int, ...]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(HEADER)
        writer.writerows(rows)


def run(binary: Path, source: Path, output: Path, stem: str) -> dict:
    subprocess.run(
        [str(binary), str(source), str(output), "100", "1", stem],
        check=True,
        capture_output=True,
        text=True,
        env={"C68_THREADS": "1"},
    )
    return json.loads((output / "monotonicity-summary.json").read_text())


def main() -> int:
    binary = Path(__file__).with_name("cycle68_monotonicity_bernstein")
    if not binary.is_file():
        raise SystemExit(f"compile {binary.name} first")
    with tempfile.TemporaryDirectory(prefix="cycle68-bernstein-control-") as temporary:
        root = Path(temporary)
        source = root / "source"
        source.mkdir()
        # (x - 1/2)^2: its root Bernstein coefficients include a negative
        # coefficient, and exact midpoint subdivision closes both halves.
        write_polynomial(
            source / "positive-square.tsv",
            [
                (0, 0, 0, 0, 0, 1, 4),
                (1, 0, 0, 0, 0, -1, 1),
                (2, 0, 0, 0, 0, 1, 1),
            ],
        )
        positive = run(binary.resolve(), source, root / "positive", "positive-square")
        chart = positive["charts"]["positive-square"]
        assert positive["complete_cover"] is True
        assert chart["complete"] is True
        assert chart["certified_leaves"] == 2

        # x - 1/2 is negative on the left half and therefore cannot obtain a
        # complete nonnegative cover at the same depth.
        write_polynomial(
            source / "negative-line.tsv",
            [
                (0, 0, 0, 0, 0, -1, 2),
                (1, 0, 0, 0, 0, 1, 1),
            ],
        )
        negative = run(binary.resolve(), source, root / "negative", "negative-line")
        assert negative["complete_cover"] is False
        assert negative["charts"]["negative-line"]["unresolved"] > 0
    print("cycle68 monotonicity Bernstein controls: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
