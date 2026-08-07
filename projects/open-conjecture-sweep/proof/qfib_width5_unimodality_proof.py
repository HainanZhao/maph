#!/usr/bin/env python3
"""One-command exact replay for width-five q-Fibonomial unimodality."""

from __future__ import annotations

import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    runpy.run_path(
        str(ROOT / "experiments" / "qfib_width5_candidate_lemmas.py"),
        run_name="__main__",
    )
    runpy.run_path(
        str(ROOT / "experiments" / "qfib_width5_bad_class_unimodality.py"),
        run_name="__main__",
    )
    print("WIDTH5_QFIBONOMIAL_UNIMODALITY_PROOF_CHECK_PASSED")


if __name__ == "__main__":
    main()
