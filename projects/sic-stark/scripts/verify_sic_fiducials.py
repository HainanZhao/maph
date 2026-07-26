#!/usr/bin/env python3
"""Verify built-in low-dimensional Weyl--Heisenberg SIC fiducials."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.sic import (  # noqa: E402
    hesse_fiducial,
    max_frame_residual,
    max_sic_residual,
    qubit_tetrahedral_fiducial,
    sic_residuals,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dimension",
        type=int,
        choices=(2, 3),
        default=3,
        help="built-in exact-form fiducial to verify",
    )
    parser.add_argument(
        "--show-residuals",
        action="store_true",
        help="print every nonidentity displacement residual",
    )
    arguments = parser.parse_args()

    fiducial = (
        qubit_tetrahedral_fiducial()
        if arguments.dimension == 2
        else hesse_fiducial()
    )
    residuals = sic_residuals(fiducial)
    print(f"dimension: {arguments.dimension}")
    print(f"orbit size: {arguments.dimension ** 2}")
    print(f"maximum SIC residual: {max_sic_residual(fiducial):.3e}")
    print(f"maximum frame residual: {max_frame_residual(fiducial):.3e}")
    if arguments.show_residuals:
        for displacement, residual in sorted(residuals.items()):
            print(f"{displacement}: {residual:+.16e}")


if __name__ == "__main__":
    main()
