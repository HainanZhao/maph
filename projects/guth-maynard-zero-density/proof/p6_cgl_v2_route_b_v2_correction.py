#!/usr/bin/env python3
"""Versioned exact-algebra correction for the sealed P6 Route B v1 record.

This does not rewrite Route B v1.  It pins the v1 source and artifact,
records the inadequate v1 margin assertion, and independently checks the
integer/radical statements that the v1 artifact displayed.  All row-level
source reconstruction remains the v1 record; this is only a correction to
the v1 exact-algebra verification evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import resource
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
ROUTE_B_V1_SCRIPT = ROOT / "proof/p6_cgl_v2_route_b_v1.py"
ROUTE_B_V1_ARTIFACT = ROOT / "artifacts/p6-cgl-v2-route-b-v1.json"
OUT = ROOT / "artifacts/p6-cgl-v2-route-b-v2-correction.json"
WALL_CAP_NS = 60_000_000_000
RSS_CAP_KIB = 262_144


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payload() -> dict[str, object]:
    source = ROUTE_B_V1_SCRIPT.read_text(encoding="utf-8")
    route_b = json.loads(ROUTE_B_V1_ARTIFACT.read_text(encoding="utf-8"))
    require(
        "require(7 * 13 - 30 == 61, \"30/13 margin arithmetic failure\")" in source,
        "Route B v1 defect signature changed; correction must be re-reviewed",
    )
    require(route_b["exact_algebra"]["q1_equals_q"]["bases_or_coefficients"] == [
        "q^(7/3)*T^2", "9/4", "(10-sqrt(10))/3", "30/13"
    ], "Route B v1 q1=q algebra changed")
    comparisons = route_b["exact_algebra"]["q1_equals_q"]["uniform_comparisons"]
    require("7/3-30/13=1/39" in comparisons, "Route B v1 does not claim the affected margin")

    # Exact replacements: no floating point or numerical square roots.
    require(2 * 3 <= 7, "2 <= 7/3 failed")
    require(7 * 4 - 9 * 3 == 1, "7/3-9/4 identity failed")
    require(10 > 9, "sqrt(10)>3 radicand comparison failed")
    require(7 * 13 - 30 * 3 == 1, "7/3-30/13 identity failed")
    require((40 * 40 - 160) == 1440, "B(beta=1) radical normalization failed")

    return {
        "artifact_id": "p6-cgl-v2-route-b-v2-correction",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "Correction of Route B v1's exact-algebra verification only. It does "
            "not alter any of the 46 row dispositions, close an analytic input, "
            "repair the CGL preprint, or prove a zero-density theorem."
        ),
        "supersedes_for_exact_margin_check_only": "p6-cgl-v2-route-b-v1",
        "preserved_v1": {
            "script": str(ROUTE_B_V1_SCRIPT.relative_to(ROOT)),
            "script_sha256": digest(ROUTE_B_V1_SCRIPT),
            "artifact": str(ROUTE_B_V1_ARTIFACT.relative_to(ROOT)),
            "artifact_sha256": digest(ROUTE_B_V1_ARTIFACT),
        },
        "defect": {
            "tag": "ROUTE_B_V1_MARGIN_CHECK_IRRELEVANT",
            "v1_assertion": "7 * 13 - 30 == 61",
            "why_insufficient": (
                "It is true but is not the cleared-denominator identity for "
                "7/3 - 30/13 = 1/39."
            ),
            "affected_claim": "Route B v1's machine-checked support for the displayed 1/39 margin.",
            "containment": "The v1 artifact remains preserved; no theorem was promoted from it.",
        },
        "corrected_exact_checks": {
            "2<=7/3": {"cleared_integer_check": "2*3<=7", "result": True},
            "7/3-9/4": {"cleared_integer_check": "7*4-9*3=1", "result": "1/12"},
            "sqrt(10)>3": {"radicand_check": "10>9", "result": True},
            "7/3-30/13": {"cleared_integer_check": "7*13-30*3=1", "result": "1/39"},
            "B_at_beta_1": {
                "normalization_check": "40^2-160=1440; sqrt(160)=4sqrt(10)",
                "result": "(10-sqrt(10))/3",
            },
        },
        "row_level_effect": {
            "canonical_row_count_unchanged": route_b["canonical_row_count"],
            "mandatory_l12_subchecks_unchanged": route_b["mandatory_l12_subchecks"],
            "overall_disposition_unchanged": route_b["overall_disposition"],
            "open_blockers_unchanged": route_b["open_blockers"],
        },
        "replay": {
            "command": "python3 proof/p6_cgl_v2_route_b_v2_correction.py --check",
            "python_implementation": sys.implementation.name,
            "python_version": ".".join(map(str, sys.version_info[:3])),
            "optimized": sys.flags.optimize,
            "wall_cap_ns": WALL_CAP_NS,
            "rss_cap_kib": RSS_CAP_KIB,
        },
    }


def render(value: dict[str, object]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    require(args.write != args.check, "choose exactly one of --write or --check")
    require(sys.flags.optimize == 0, "correction rejects optimized Python")
    require(sys.version_info[:3] == (3, 12, 3) and sys.platform.startswith("linux"), "correction requires CPython 3.12.3 on linux")
    started = time.monotonic_ns()
    value = payload()
    elapsed = time.monotonic_ns() - started
    rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    require(elapsed < WALL_CAP_NS, "correction exceeded 60-second wall cap")
    require(rss < RSS_CAP_KIB, "correction exceeded 256-MiB RSS cap")
    encoded = render(value)
    if args.write:
        require(not OUT.exists(), "refusing to overwrite correction artifact")
        OUT.write_bytes(encoded)
    else:
        require(OUT.is_file(), "correction artifact is absent")
        require(OUT.read_bytes() == encoded, "correction artifact mismatch")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as err:
        print(err, file=sys.stderr)
        raise SystemExit(1)
