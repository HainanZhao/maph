#!/usr/bin/env python3
"""Check the first infinite non-periodic four-mode dark family."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.fourier_suppression import (  # noqa: E402
    four_mode_self_family_closed_form,
    four_mode_self_family_coefficient,
    four_mode_reflection_self_coefficient,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--reflection-b-limit", type=int, default=80)
    args = parser.parse_args()
    if args.limit < 0:
        parser.error("--limit must be nonnegative")
    if args.reflection_b_limit < 0:
        parser.error("--reflection-b-limit must be nonnegative")

    print("a  coefficient  status  closed form")
    for a in range(args.limit + 1):
        coefficient = four_mode_self_family_coefficient(a)
        status = "dark" if coefficient == 0 else "bright"
        closed_form = four_mode_self_family_closed_form(a)
        comparison = "match" if coefficient == closed_form else "FAIL"
        print(f"{a:2d} {coefficient:>24d}  {status:6s}  {comparison}")

    print("\nzeros of (0,a,b,a) -> itself in the scanned rectangle")
    for a in range(1, args.limit + 1):
        zeros = [
            b
            for b in range(args.reflection_b_limit + 1)
            if four_mode_reflection_self_coefficient(a, b) == 0
        ]
        print(f"a={a:2d}: {zeros}")


if __name__ == "__main__":
    main()
