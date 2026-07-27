#!/usr/bin/env python3
"""Verify built-in low-dimensional Weyl--Heisenberg SIC fiducials."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.sic import (  # noqa: E402
    dimension_four_fiducial,
    hesse_fiducial,
    max_frame_residual,
    max_sic_residual,
    max_twisted_idempotency_residual,
    projector_displacement_coefficients,
    qubit_tetrahedral_fiducial,
    sic_residuals,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dimension",
        type=int,
        choices=(2, 3, 4),
        default=4,
        help="built-in exact-form fiducial to verify",
    )
    parser.add_argument(
        "--show-residuals",
        action="store_true",
        help="print every nonidentity displacement residual",
    )
    arguments = parser.parse_args()

    fiducials = {
        2: qubit_tetrahedral_fiducial,
        3: hesse_fiducial,
        4: dimension_four_fiducial,
    }
    fiducial = fiducials[arguments.dimension]()
    residuals = sic_residuals(fiducial)
    coefficients = projector_displacement_coefficients(fiducial)
    print(f"dimension: {arguments.dimension}")
    print(f"orbit size: {arguments.dimension ** 2}")
    print(f"maximum SIC residual: {max_sic_residual(fiducial):.3e}")
    print(f"maximum frame residual: {max_frame_residual(fiducial):.3e}")
    print(
        "maximum twisted-idempotency residual: "
        f"{max_twisted_idempotency_residual(coefficients, arguments.dimension):.3e}"
    )
    if arguments.show_residuals:
        for displacement, residual in sorted(residuals.items()):
            print(f"{displacement}: {residual:+.16e}")


if __name__ == "__main__":
    main()
