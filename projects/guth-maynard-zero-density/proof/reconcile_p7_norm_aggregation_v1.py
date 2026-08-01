#!/usr/bin/env python3
"""Lightweight two-route reconciliation for the sealed P7-1 gate.

This is a source/algebra/replay check, not a hostile audit and not a theorem
search.  It preserves the distinction between the fixed-character calculation
and the still-open character-family problem.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
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


OUT = ROOT / "artifacts/p7-norm-aggregation-v1.json"
SELF = Path(__file__).resolve()
ROUTE_A = ROOT / "proof/run_p7_norm_aggregation_route_a_v1.py"
ROUTE_B = ROOT / "proof/run_p7_norm_aggregation_route_b_v1.py"
ROUTE_B_CORRECTION = ROOT / "proof/correct_p7_norm_aggregation_route_b_v2.py"
DOC = ROOT / "docs/p7-norm-aggregation-v1.md"
TESTS = ROOT / "tests/test_p7_norm_aggregation_v1.py"
CONVENTIONS = ROOT / "conventions/p7_norm_aggregation_v1.py"
ARTIFACT_A = ROOT / "artifacts/p7-norm-aggregation-route-a-v1.json"
ARTIFACT_B = ROOT / "artifacts/p7-norm-aggregation-route-b-v1.json"
ARTIFACT_B_CORRECTION = ROOT / "artifacts/p7-norm-aggregation-route-b-v2-correction.json"


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def artifact_matches_route(label: str, script: Path, artifact: Path) -> dict[str, object]:
    module = load_module(f"p7_{label}_route", script)
    current = module.render(module.report())
    require(artifact.is_file() and artifact.read_bytes() == current, f"{label} artifact fails deterministic replay")
    return json.loads(current)


def report() -> dict[str, object]:
    runtime = require_pinned_runtime()
    sources: dict[str, object] = {}
    for label, row in C.SOURCES.items():
        path = ROOT / row["path"]
        require(digest(path) == row["sha256"], f"source mismatch: {label}")
        sources[label] = {"path": row["path"], "sha256": row["sha256"]}
    route_a = artifact_matches_route("a", ROUTE_A, ARTIFACT_A)
    route_b = artifact_matches_route("b", ROUTE_B, ARTIFACT_B)
    correction_module = load_module("p7_b_label_correction", ROUTE_B_CORRECTION)
    correction_bytes = correction_module.render(correction_module.report())
    require(ARTIFACT_B_CORRECTION.is_file() and ARTIFACT_B_CORRECTION.read_bytes() == correction_bytes, "Route B label correction fails deterministic replay")
    correction = json.loads(correction_bytes)
    expected = {"A_chi_3_17": -2, "A_chi_pi4_17": 2}
    a_values = {"A_chi_3_17": route_a["witness"]["A_chi_3_17"], "A_chi_pi4_17": route_a["witness"]["A_chi_pi4_17"]}
    b_values = correction["canonical_witness"]
    require(a_values == expected == b_values, "route witness values disagree")
    a_pi = [row["quotient_cardinality"] for row in route_a["pi_power_quotients"]["rows"]]
    b_pi = [row["quotient_count"] for row in route_b["ray_character_calculation"]["pi_power"]["rows"]]
    require(a_pi == [1, 1, 1, 2] == b_pi, "route pi-power quotient data disagree")
    require(route_b["norm_aggregation"]["identity"] == "a_Q(i)(n)=sum_{d|n} chi_-4(d)", "norm identity missing")
    normalize = route_b["normalization"]
    require(normalize["precise_outcome"] == "EXPONENT_HARMLESS_IN_THE_POLYNOMIAL_LENGTH_HEIGHT_REGIME", "normalization scope changed")
    require(normalize["unconditional_limit"].startswith("NOT_ESTABLISHED"), "unrestricted normalisation was overclaimed")
    require("does not exclude" in route_b["type_mismatch"]["non_no_go"], "type mismatch was promoted to no-go")
    identities = {
        "conventions": {"path": str(CONVENTIONS.relative_to(ROOT)), "sha256": digest(CONVENTIONS)},
        "document": {"path": str(DOC.relative_to(ROOT)), "sha256": digest(DOC)},
        "route_a_script": {"path": str(ROUTE_A.relative_to(ROOT)), "sha256": digest(ROUTE_A)},
        "route_a_artifact": {"path": str(ARTIFACT_A.relative_to(ROOT)), "sha256": digest(ARTIFACT_A)},
        "route_b_script": {"path": str(ROUTE_B.relative_to(ROOT)), "sha256": digest(ROUTE_B)},
        "route_b_artifact": {"path": str(ARTIFACT_B.relative_to(ROOT)), "sha256": digest(ARTIFACT_B)},
        "route_b_label_correction_script": {"path": str(ROUTE_B_CORRECTION.relative_to(ROOT)), "sha256": digest(ROUTE_B_CORRECTION)},
        "route_b_label_correction_artifact": {"path": str(ARTIFACT_B_CORRECTION.relative_to(ROOT)), "sha256": digest(ARTIFACT_B_CORRECTION)},
        "tests": {"path": str(TESTS.relative_to(ROOT)), "sha256": digest(TESTS)},
    }
    return {
        "artifact_id": "p7-norm-aggregation-v1",
        "epistemic_status": "PROVED",
        "gate": C.GATE_ID,
        "gate_outcome": "PASS_SCOPED_TYPE_MISMATCH_AND_NORMALIZATION",
        "claim_boundary": "Closes only the finite witness, norm identity, and stated fixed-character normalization check. It does not prove a joint character-family large-value, zero-density, or prime-ideal theorem.",
        "review_policy": "LIGHTWEIGHT_SOURCE_ALGEBRA_REPLAY_RECONCILIATION; no hostile audit initiated.",
        "source_integrity": sources,
        "artifact_identity": identities,
        "route_independence": {"status": "OBSERVED", "route_a": "finite residue-ring multiplication tables", "route_b": "local splitting/cardinality and generator calculations", "shared_implementation": False, "shared_frozen_scope_only": ["source paths and hashes", "field/modulus labels", "runtime/resource caps"]},
        "reconciliation": {
            "status": "PROVED",
            "ray_quotients": {"mod_3": 2, "pi_power_e_1_through_4": a_pi},
            "exact_conductors": ["(3)", "(1+i)^4"],
            "witness": expected,
            "label_reconciliation": correction["correction"]["repair"],
            "norm_identity": route_b["norm_aggregation"]["identity"],
            "normalization": {"outcome": normalize["precise_outcome"], "covered_regime": "N<=T^C fixed C, including source's N<T reduction", "uncovered_regime": normalize["unconditional_limit"]},
            "direct_import_boundary": "Different A_chi prevent verbatim use of a one-common-coefficient polynomial theorem on joint (chi,t) samples.",
            "non_no_go": route_b["type_mismatch"]["non_no_go"],
        },
        "contained_preexisting_test_issue": {"status": "CONTAINED", "statement": "The sealed P7-v2 builder replays, but its existing unit test expects an exact list element 'no-search/no-hostile-audit' while the immutable artifact stores the longer element 'no-search/no-hostile-audit boundary'. This is a test-assertion mismatch, not a mathematical or artifact replay failure; no sealed preregistration file was edited."},
        "non_promotion": list(C.NON_PROMOTION),
        "resource_contract": C.RESOURCE_LIMITS,
        "replay": {"script": str(SELF.relative_to(ROOT)), "script_sha256": digest(SELF), "runtime": runtime, "write_command": "python3 proof/reconcile_p7_norm_aggregation_v1.py --write", "check_command": "python3 proof/reconcile_p7_norm_aggregation_v1.py --check"},
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
    require(elapsed < C.RESOURCE_LIMITS["wall_seconds_strictly_less_than"] * 1_000_000_000, "reconciliation exceeded wall cap")
    require(rss < C.RESOURCE_LIMITS["rss_kib_strictly_less_than"], "reconciliation exceeded RSS cap")
    if args.write:
        require(not OUT.exists(), "refusing to overwrite sealed P7-1 reconciliation")
        OUT.write_bytes(data)
    else:
        require(OUT.is_file() and OUT.read_bytes() == data, "P7-1 reconciliation mismatch; issue a correction rather than overwrite")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
