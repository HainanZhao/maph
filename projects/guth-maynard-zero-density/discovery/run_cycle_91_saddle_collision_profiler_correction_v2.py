#!/usr/bin/env python3
"""Correct Cycle 91 zero-count normalization using the preregistered rule."""
from __future__ import annotations

import argparse
import importlib.util
import json
import platform
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
V1_PATH = ROOT / "discovery/run_cycle_91_saddle_collision_profiler_v1.py"
OUTPUT = ROOT / "discovery/cycle-91-saddle-collision-profiler-correction-v2.json"
V1_JSON_SHA256 = "ffaf5dd1017b722f9c6b2c05e22e37ab5a6224e74e19954b199b15d08eb82575"
V1_SCRIPT_SHA256 = "f8bcf9888f97db66172190d9927106d7067e0adf4b5009121190bb6d5e2014c3"
PREREG_SHA256 = "0e5210b277c135f7d1359fb451878e0810421a11b6cbf66248b7d901a1dff61f"


def load_v1():
    spec = importlib.util.spec_from_file_location("cycle91_v1", V1_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load Cycle 91 v1")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_payload() -> dict[str, object]:
    v1 = load_v1()
    bases = [v1.one_scale(D) for D in v1.D_VALUES]
    rows = [v1.one_row(base, xi) for xi in v1.XI_VALUES for base in bases]
    summaries = []
    for xi in v1.XI_VALUES:
        label = f"{xi.numerator}/{xi.denominator}"
        selected = [row for row in rows if row["xi"] == label]
        count_slope = v1.slope(selected, "count_for_log")
        normalized = [
            {
                **row,
                "volume_ratio_for_log": row["count_for_log"] / row["volume_model"],
                "q_ratio_for_log": row["count_for_log"] / row["Q"],
            }
            for row in selected
        ]
        volume_ratio_slope = v1.slope(normalized, "volume_ratio_for_log")
        q_ratio_slope = v1.slope(normalized, "q_ratio_for_log")
        if q_ratio_slope > 0.15:
            classification = "OBSERVED_GROWING"
        elif q_ratio_slope < -0.15:
            classification = "OBSERVED_DECAYING"
        else:
            classification = "OBSERVED_FLAT"
        summaries.append(
            {
                "xi": label,
                "count_slope": count_slope,
                "count_over_volume_slope": volume_ratio_slope,
                "count_over_Q_slope": q_ratio_slope,
                "count_over_Q_classification": classification,
            }
        )
    return {
        "epistemic_status": "OBSERVED",
        "correction": {
            "version": 2,
            "cause": "v1 used 1e-300 instead of the preregistered max(C,1) numerator for normalized regressions",
            "v1_json_sha256": V1_JSON_SHA256,
            "v1_script_sha256": V1_SCRIPT_SHA256,
            "preregistration_sha256": PREREG_SHA256,
        },
        "runtime": {"python": platform.python_version(), "numpy": np.__version__},
        "rows": rows,
        "summaries": summaries,
        "claim_boundary": "Corrected finite-scale deterministic discovery only; no proof promotion.",
    }


def encoded_payload() -> bytes:
    return (json.dumps(build_payload(), indent=2, sort_keys=True) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    encoded = encoded_payload()
    if args.write:
        if OUTPUT.exists():
            raise SystemExit(f"refusing to overwrite corrected output: {OUTPUT}")
        OUTPUT.write_bytes(encoded)
        print(OUTPUT)
    else:
        if not OUTPUT.exists():
            raise SystemExit(f"missing corrected output: {OUTPUT}")
        if OUTPUT.read_bytes() != encoded:
            raise SystemExit("corrected output differs from deterministic replay")
        print(f"replay matched: {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

