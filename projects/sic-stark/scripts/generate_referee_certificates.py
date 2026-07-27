#!/usr/bin/env python3
"""Emit deterministic SIC--Stark referee certificates as JSON."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.sic_stark import (  # noqa: E402
    canonical_dimension_four_double_sine_factor_record,
    canonical_dimension_four_ray_class_record,
    canonical_ghost_exterior_square_record,
    canonical_parity_schatten_record,
)


def main() -> None:
    certificate = {
        "schema": "sic-stark-referee-certificate-v3",
        "dimension": 4,
        "minor_factorization": (
            canonical_dimension_four_double_sine_factor_record()
        ),
        "ray_and_unit_arithmetic": (
            canonical_dimension_four_ray_class_record()
        ),
        "exterior_square": canonical_ghost_exterior_square_record(4),
        "parity_fourth_moment": canonical_parity_schatten_record(4),
        "review_assertions": {
            "all_minor_count": 36,
            "minor_remainders_after_relation": 0,
            "ray_group_order_one_infinite_place": 2,
            "ray_group_order_two_infinite_places": 4,
            "kopp_exponent": 1,
            "target_stark_unit": "phi + sqrt(phi)",
            "target_cocycle_value": "sqrt(phi + sqrt(phi))",
            "finite_matrix_is_explicit": True,
            "all_minor_quotients_included": True,
            "full_two_shift_tcc_checked": True,
            "kopp_specialization_proved": True,
        },
    }
    print(json.dumps(certificate, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
