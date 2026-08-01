#!/usr/bin/env python3
"""Corrected, deterministic P7-1 reconciliation without a hostile audit."""
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


OUT = ROOT / "artifacts/p7-norm-aggregation-v2-correction.json"
SELF = Path(__file__).resolve()
FILES = {
    "route_a_script": ROOT / "proof/run_p7_norm_aggregation_route_a_v1.py",
    "route_a_artifact": ROOT / "artifacts/p7-norm-aggregation-route-a-v1.json",
    "route_b_script": ROOT / "proof/run_p7_norm_aggregation_route_b_v1.py",
    "route_b_artifact": ROOT / "artifacts/p7-norm-aggregation-route-b-v1.json",
    "route_b_correction_script": ROOT / "proof/correct_p7_norm_aggregation_route_b_v2.py",
    "route_b_correction_artifact": ROOT / "artifacts/p7-norm-aggregation-route-b-v2-correction.json",
    "prior_reconciliation": ROOT / "artifacts/p7-norm-aggregation-v1.json",
    "conventions": ROOT / "conventions/p7_norm_aggregation_v1.py",
    "document": ROOT / "docs/p7-norm-aggregation-v2-correction.md",
    "tests": ROOT / "tests/test_p7_norm_aggregation_v2.py",
}


def require(value: bool, message: str) -> None:
    if not value:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replay_route(name: str, script: Path, artifact: Path) -> dict[str, object]:
    module = load(name, script)
    data = module.render(module.report())
    require(artifact.read_bytes() == data, f"{name} artifact does not replay")
    return json.loads(data)


def report() -> dict[str, object]:
    runtime = require_pinned_runtime()
    a = replay_route("p7_a_v1", FILES["route_a_script"], FILES["route_a_artifact"])
    b = replay_route("p7_b_v1", FILES["route_b_script"], FILES["route_b_artifact"])
    bc = replay_route("p7_b_v2", FILES["route_b_correction_script"], FILES["route_b_correction_artifact"])
    source_rows: dict[str, object] = {}
    for label, row in C.SOURCES.items():
        path = ROOT / row["path"]
        require(digest(path) == row["sha256"], f"pinned source mismatch: {label}")
        source_rows[label] = {"path": row["path"], "sha256": row["sha256"]}
    expected = {"A_chi_3_17": -2, "A_chi_pi4_17": 2}
    a_values = {"A_chi_3_17": a["witness"]["A_chi_3_17"], "A_chi_pi4_17": a["witness"]["A_chi_pi4_17"]}
    require(a_values == expected == bc["canonical_witness"], "canonical witness mismatch")
    pi_a = [row["quotient_cardinality"] for row in a["pi_power_quotients"]["rows"]]
    pi_b = [row["quotient_count"] for row in b["ray_character_calculation"]["pi_power"]["rows"]]
    require(pi_a == [1, 1, 1, 2] == pi_b, "ray quotient mismatch")
    norm = b["norm_aggregation"]
    normalized = b["normalization"]
    require(norm["identity"] == "a_Q(i)(n)=sum_{d|n} chi_-4(d)", "norm identity missing")
    require(normalized["precise_outcome"] == "EXPONENT_HARMLESS_IN_THE_POLYNOMIAL_LENGTH_HEIGHT_REGIME", "incorrect normalization conclusion")
    require(normalized["unconditional_limit"].startswith("NOT_ESTABLISHED"), "unrestricted regime overclaimed")
    identities = {label: {"path": str(path.relative_to(ROOT)), "sha256": digest(path)} for label, path in FILES.items()}
    return {
        "artifact_id": "p7-norm-aggregation-v2-correction",
        "epistemic_status": "PROVED",
        "gate": C.GATE_ID,
        "gate_outcome": "PASS_SCOPED_TYPE_MISMATCH_AND_NORMALIZATION",
        "claim_boundary": "The finite witness, norm identity, and fixed-character normalization check only. No joint character-family large-value, zero-density, or prime-ideal theorem is proved.",
        "review_policy": "LIGHTWEIGHT_SOURCE_ALGEBRA_REPLAY_RECONCILIATION; no hostile audit initiated.",
        "correction": {"predecessor": {"path": str(FILES["prior_reconciliation"].relative_to(ROOT)), "sha256": digest(FILES["prior_reconciliation"])}, "defect": "v1's test used an accidental exact-string assertion after the values had already been reconciled by a versioned label correction", "repair": "v2 checks the exact mathematical boundary and records both prior label/test defects without changing predecessor bytes", "mathematical_effect": "none"},
        "source_integrity": source_rows,
        "artifact_identity": identities,
        "route_independence": {"status": "OBSERVED", "route_a": "exact finite residue-ring multiplication tables", "route_b": "local splitting/cardinality and generator calculation", "shared_implementation": False, "preserved_label_correction": True},
        "reconciliation": {"status": "PROVED", "ray_quotients": {"mod_3": 2, "pi_power_e_1_through_4": pi_a}, "exact_conductors": ["(3)", "(1+i)^4"], "witness": expected, "norm_identity": norm["identity"], "normalization": {"outcome": normalized["precise_outcome"], "covered_regime": "N<=T^C fixed C, including the source proof's N<T reduction", "uncovered_regime": normalized["unconditional_limit"]}, "direct_import_boundary": "Because A_chi differs, a theorem assuming one common coefficient vector cannot be invoked verbatim on joint (chi,t) samples.", "non_no_go": b["type_mismatch"]["non_no_go"]},
        "contained_test_issues": ["Route B v1 parenthesized-label schema mismatch, corrected in its preserved v2 correction.", "P7-1 v1 reconciliation's literal-substring test mismatch, corrected here.", "Pre-existing P7 preregistration-v2 test list-element mismatch; its builder replay remains valid and no sealed preregistration byte was edited."],
        "non_promotion": list(C.NON_PROMOTION),
        "resource_contract": C.RESOURCE_LIMITS,
        "replay": {"script": str(SELF.relative_to(ROOT)), "script_sha256": digest(SELF), "runtime": runtime, "write_command": "python3 proof/reconcile_p7_norm_aggregation_v2_correction.py --write", "check_command": "python3 proof/reconcile_p7_norm_aggregation_v2_correction.py --check"},
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
    require(elapsed < C.RESOURCE_LIMITS["wall_seconds_strictly_less_than"] * 1_000_000_000, "v2 reconciliation exceeded wall cap")
    require(rss < C.RESOURCE_LIMITS["rss_kib_strictly_less_than"], "v2 reconciliation exceeded RSS cap")
    if args.write:
        require(not OUT.exists(), "refusing to overwrite sealed P7-1 v2 correction")
        OUT.write_bytes(data)
    else:
        require(OUT.is_file() and OUT.read_bytes() == data, "P7-1 v2 reconciliation mismatch; issue a correction rather than overwrite")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as error:
        print(error, file=sys.stderr)
        raise SystemExit(1)
