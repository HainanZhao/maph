#!/usr/bin/env python3
"""Versioned label correction for the independent P7-1 Route B artifact.

Route B v1's calculation is retained byte-for-byte.  Its sole defect is that
the pi^4 aggregated coefficient was labeled ``A_chi_pi4(17)`` rather than the
frozen canonical schema ``A_chi_pi4_17``.  This correction does not change a
number, source, proof step, or scope boundary.
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
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from conventions import p7_norm_aggregation_v1 as C
from conventions.proof_runtime_v2 import require_pinned_runtime


OUT = ROOT / "artifacts/p7-norm-aggregation-route-b-v2-correction.json"
SELF = Path(__file__).resolve()
V1_SCRIPT = ROOT / "proof/run_p7_norm_aggregation_route_b_v1.py"
V1_ARTIFACT = ROOT / "artifacts/p7-norm-aggregation-route-b-v1.json"


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def report() -> dict[str, object]:
    runtime = require_pinned_runtime()
    raw = json.loads(V1_ARTIFACT.read_text(encoding="utf-8"))
    values = raw["ray_character_calculation"]["aggregated_values"]
    require(values == {"A_chi_3(17)": -2, "A_chi_pi4(17)": 2}, "Route B v1 calculation unexpectedly changed")
    canonical = {"A_chi_3_17": values["A_chi_3(17)"], "A_chi_pi4_17": values["A_chi_pi4(17)"]}
    return {
        "artifact_id": "p7-norm-aggregation-route-b-v2-correction",
        "epistemic_status": "PROVED",
        "gate": C.GATE_ID,
        "claim_boundary": "Versioned label correction only. Route B v1's algebra and all non-promotion boundaries are preserved unchanged.",
        "correction": {"predecessor": {"script": {"path": str(V1_SCRIPT.relative_to(ROOT)), "sha256": digest(V1_SCRIPT)}, "artifact": {"path": str(V1_ARTIFACT.relative_to(ROOT)), "sha256": digest(V1_ARTIFACT)}}, "defect": "Route B v1 used parenthesized labels for the two aggregated values while Route A/canonical reconciliation use underscore labels.", "cause": "schema spelling mismatch only", "affected_claims": "none; the integer values and all derivations are unchanged", "repair": "record the explicit bijection A_chi_3(17)->A_chi_3_17 and A_chi_pi4(17)->A_chi_pi4_17"},
        "canonical_witness": canonical,
        "preserved_v1_values": values,
        "resource_contract": C.RESOURCE_LIMITS,
        "replay": {"script": str(SELF.relative_to(ROOT)), "script_sha256": digest(SELF), "runtime": runtime, "write_command": "python3 proof/correct_p7_norm_aggregation_route_b_v2.py --write", "check_command": "python3 proof/correct_p7_norm_aggregation_route_b_v2.py --check"},
    }


def render(value: dict[str, object]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    require(args.write != args.check, "choose exactly one of --write or --check")
    started = time.monotonic_ns()
    data = render(report())
    elapsed = time.monotonic_ns() - started
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    require(elapsed < C.RESOURCE_LIMITS["wall_seconds_strictly_less_than"] * 1_000_000_000, "Route B correction exceeded wall cap")
    require(rss < C.RESOURCE_LIMITS["rss_kib_strictly_less_than"], "Route B correction exceeded RSS cap")
    if args.write:
        require(not OUT.exists(), "refusing to overwrite sealed Route B correction")
        OUT.write_bytes(data)
    else:
        require(OUT.is_file() and OUT.read_bytes() == data, "Route B correction mismatch; issue a further correction rather than overwrite")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
