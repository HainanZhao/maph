#!/usr/bin/env python3
"""Search the structured near-witness family M=6*5^a, t=6^h."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.erdos700 import near_multiple_shifted_failure_depth  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-exponent", type=int, default=100)
    args = parser.parse_args()
    if args.max_exponent < 2:
        parser.error("max-exponent must be at least 2")

    checked = 0
    full_witnesses: list[tuple[int, int]] = []
    record_depth = -1
    record: tuple[int, int, int | None, int | None] | None = None

    for exponent in range(2, args.max_exponent + 1):
        multiple = 6 * 5**exponent
        multiplier = 6
        depth_parameter = 1
        while 6 * multiplier < 5**exponent:
            if depth_parameter % 5 != 3:
                checked += 1
                depth_2 = near_multiple_shifted_failure_depth(
                    multiple, multiplier, 2
                )
                depth_3 = near_multiple_shifted_failure_depth(
                    multiple, multiplier, 3
                )
                depth_5 = near_multiple_shifted_failure_depth(
                    multiple, multiplier, 5
                )
                if depth_5 is not None:
                    raise AssertionError("the construction should pass base 5")
                finite_depths = tuple(
                    depth for depth in (depth_2, depth_3) if depth is not None
                )
                if not finite_depths:
                    full_witnesses.append((exponent, depth_parameter))
                elif min(finite_depths) > record_depth:
                    record_depth = min(finite_depths)
                    record = (
                        exponent,
                        depth_parameter,
                        depth_2,
                        depth_3,
                    )
            multiplier *= 6
            depth_parameter += 1

    print(f"structured pairs checked={checked}")
    print(f"full witnesses={full_witnesses}")
    if record is not None:
        exponent, depth_parameter, depth_2, depth_3 = record
        print(
            f"record cover depth={record_depth}: "
            f"a={exponent}, h={depth_parameter}, "
            f"base-2 depth={depth_2}, base-3 depth={depth_3}"
        )


if __name__ == "__main__":
    main()
