#!/usr/bin/env python3
"""Seal exact conditional density-to-short-interval endpoint algebra."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import sys


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUT = ROOT / "artifacts/cycle-5-conditional-density-to-short-interval-map-v1.json"
DOC = ROOT / "docs/cycle-5-conditional-density-to-short-interval-map-v1.md"
STREAM_C = ROOT / "artifacts/cycle-2-stream-c-two-route-reconciliation-v2.json"
G0 = ROOT / "artifacts/g0-full-reconstruction-v3.json"
INPUT_HASHES = {
    DOC: "12375068aa4ce7424403817629c245185acf04a992009736e267e057cc7c86b5",
    STREAM_C: "b69e0caeb5d5ed5c8072acb62263d15c2b02470df0c10889287508837c9e706d",
    G0: "5a3ec153c843d0c89d9a987ad043cdf9513a171d581f98447a9c12930d26cc4f",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def endpoint_rows(eta: Fraction) -> dict[str, str]:
    require(Fraction(0) < eta < Fraction(4, 13), "eta must lie in (0,4/13)")
    baseline = Fraction(30, 13)
    coefficient = baseline - eta
    uniform = 1 - 1 / coefficient
    almost_all = 1 - 2 / coefficient
    uniform_gain = Fraction(17, 30) - uniform
    almost_gain = Fraction(2, 15) - almost_all
    require(uniform == (17 - 13 * eta) / (30 - 13 * eta), "uniform endpoint identity failed")
    require(almost_all == (4 - 13 * eta) / (30 - 13 * eta), "almost-all endpoint identity failed")
    require(uniform_gain == 169 * eta / (30 * (30 - 13 * eta)), "uniform gain identity failed")
    require(almost_gain == 169 * eta / (15 * (30 - 13 * eta)), "almost-all gain identity failed")
    require(almost_gain == 2 * uniform_gain, "gain ratio identity failed")
    return {
        "eta": text(eta),
        "density_coefficient": text(coefficient),
        "uniform_theta": text(uniform),
        "almost_all_theta": text(almost_all),
        "uniform_improvement": text(uniform_gain),
        "almost_all_improvement": text(almost_gain),
    }


def payload() -> dict[str, object]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}, "runtime mismatch")
    frozen: dict[str, dict[str, str]] = {}
    for path, wanted in INPUT_HASHES.items():
        require(path.is_file(), f"missing input {path.name}")
        got = digest(path)
        require(got == wanted, f"input hash changed: {path.name}")
        frozen[path.name] = {"path": str(path.relative_to(ROOT)), "sha256": got}
    stream = json.loads(STREAM_C.read_text(encoding="utf-8"))
    serialized = json.dumps(stream, sort_keys=True)
    require("17/30" in serialized and "2/15" in serialized, "G0 endpoint anchors missing")
    return {
        "artifact_id": "cycle-5-conditional-density-to-short-interval-map-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_CONDITIONAL_PROPAGATION_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "Exact endpoint algebra conditional on a proof-grade global density coefficient and every G0 explicit-formula/near-one/zero-free/multiplicity/range input. No density gain or new prime theorem is proved.",
        "conditional_input": "B_eta=30/13-eta with 0<eta<4/13, uniformly available throughout the frozen explicit-formula density range with the G0 logarithmic controls",
        "general_map": {
            "uniform": "theta=1-1/B",
            "almost_all": "theta=1-2/B",
        },
        "exact_rows": [endpoint_rows(Fraction(1, 100)), endpoint_rows(Fraction(1, 20)), endpoint_rows(Fraction(1, 10)), endpoint_rows(Fraction(1, 4))],
        "symbolic_identities": {
            "uniform_theta": "(17-13*eta)/(30-13*eta)",
            "almost_all_theta": "(4-13*eta)/(30-13*eta)",
            "uniform_gain": "169*eta/[30*(30-13*eta)]",
            "almost_all_gain": "169*eta/[15*(30-13*eta)]",
        },
        "frozen_hashes": frozen,
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE", "checks": "exact Fraction algebra, G0 anchors, hashes, replay"},
        "replay": {"check_command": "python3 proof/build_cycle_5_conditional_short_interval_map_v1.py --check", "test_command": "python3 -m unittest tests.test_cycle_5_conditional_short_interval_map_v1 -v"},
    }


def render(value: dict[str, object]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    encoded = render(payload())
    if args.write:
        require(not OUT.exists(), "refusing to overwrite conditional propagation artifact")
        OUT.write_bytes(encoded)
    else:
        require(OUT.is_file() and OUT.read_bytes() == encoded, "conditional propagation artifact mismatch")
    print(json.dumps({"artifact": OUT.name, "status": "ok"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
