#!/usr/bin/env python3
"""Audit a one-sided homology-injective terminal-slice tree encoder."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from discovery.search_g1_paired_fundamental_cycles import _labels  # noqa: E402
from discovery.search_g1_relative_trees import _side  # noqa: E402
from proof.verify_lane_b_arbitrary_width_frontier import _case  # noqa: E402
from src.conventions import cubic_box  # noqa: E402


def audit(width, maximum_length):
    rows = []
    target = width * width - 1
    for length in range(2, maximum_length + 1):
        structural = _case(width, length)["length_rows"][-1]
        vertices, edges = cubic_box((length, width, width))
        labels = _labels(structural, edges)
        genus = structural["genus"]
        result = _side(
            width, vertices, edges, labels, length - 1, genus, "left"
        )
        rows.append({
            "length": length,
            "genus": genus,
            "available_homology_dimension": 2 * genus,
            "target_boundary_dimension": target,
            **result,
        })
    return {
        "status": "OBSERVED exact GF(2) prefix-encoder audit",
        "width": width,
        "rows": rows,
        "claim_boundary": (
            "A successful finite row is an exact one-sided tree encoder. "
            "A bounded width census does not prove a symbolic-width construction."
        ),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--width", type=int, required=True)
    parser.add_argument("--maximum-length", type=int, default=6)
    args = parser.parse_args()
    print(json.dumps(audit(**vars(args)), indent=2, sort_keys=True))
