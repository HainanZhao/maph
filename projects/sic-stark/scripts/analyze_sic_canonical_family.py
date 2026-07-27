#!/usr/bin/env python3
"""Print exact invariants of the canonical SIC--Stark dimension family."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.sic_stark import canonical_family_record  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, default=4)
    parser.add_argument("--stop", type=int, default=20)
    arguments = parser.parse_args()
    if arguments.start < 4 or arguments.stop < arguments.start:
        parser.error("require 4 <= start <= stop")

    print(
        "d  Q=<a,b,c>       Delta=(d+1)(d-3)  det(L)  "
        "L^3 mod d       #orbits  TCC eqs    HJ word"
    )
    for dimension in range(arguments.start, arguments.stop + 1):
        record = canonical_family_record(dimension)
        print(
            f"{dimension:<2} {str(record['form']):<17} "
            f"{record['discriminant']:<19} "
            f"{record['determinant']:<7} "
            f"{str(record['cube_mod_dimension']):<15} "
            f"{record['zauner_orbit_count']:<8} "
            f"{record['tcc_equation_count']:<10} "
            f"{record['jacobi_word']}"
        )


if __name__ == "__main__":
    main()
