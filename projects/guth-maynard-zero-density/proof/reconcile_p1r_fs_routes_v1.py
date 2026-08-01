#!/usr/bin/env python3
"""Reconcile two independent exact P1R-FS fixed-splice proofs."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/p1r-fs-route-reconciliation-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration_v4": (ROOT / "artifacts/cycle-4-p1r-preregistration-v4.json", "e2aeec9ec90e1fea0a9eade53d5ff1e57020df48bd92ae852121a941fbadd7f9"),
    "preregistration_v4_hostile": (ROOT / "artifacts/cycle-4-p1r-preregistration-v4-hostile-audit-v1.json", "bdb60d416fee628d309e025a493c45383ccc50e3ee41a9bdb0d6b8a7d73235ad"),
    "route_a_script": (ROOT / "proof/p1r_fs_route_a_v1.py", "ce87441984d5129b250a7a1f51070ffbe190e793fa2680e712fd6ca549bd5560"),
    "route_a_artifact": (ROOT / "artifacts/p1r-fs-route-a-v1.json", "c1bde2f7aa8675963b27e4b41e04d54717c7d875159d376950ff51240865d342"),
    "route_a_document": (ROOT / "docs/p1r-fs-route-a-v1.md", "0fc70245c16569fc2e533b35eba4987fe75eba6f5151e43c6781e04e09bcac72"),
    "route_a_tests": (ROOT / "tests/test_p1r_fs_route_a_v1.py", "43419ab347fbda816ff0cd30e5f79b41cd38ec43dde1869b58b6f5ef671d415c"),
    "route_b_script": (ROOT / "proof/p1r_fs_route_b_v1.py", "fdcff5384a9d8705cd6b7b862124d6a2e3869b8e4173396335d9481f2ad6cb60"),
    "route_b_artifact": (ROOT / "artifacts/p1r-fs-route-b-v1.json", "678df43e0e8b8abf485302410565c1cf3838bd6aea5ab554b20c20bb2bd03880"),
    "route_b_document": (ROOT / "docs/p1r-fs-route-b-v1.md", "935ee988f3074d0d7e29c2af0833bb0fa812948a65692d85ba92148446c785e7"),
    "route_b_tests": (ROOT / "tests/test_p1r_fs_route_b_v1.py", "19a323b6b2cb60350fdbf29fd43634501f310aa7b171b4c189a1ee808c0a3a39"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def check_runtime() -> dict[str, Any]:
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "P1R-FS reconciliation requires non-optimized CPython 3.12.3")
    return runtime


def reconcile() -> dict[str, Any]:
    runtime = check_runtime()
    frozen: dict[str, dict[str, str]] = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        frozen[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}

    prereg = load_json(INPUTS["preregistration_v4"][0])
    prereg_audit = load_json(INPUTS["preregistration_v4_hostile"][0])
    route_a = load_json(INPUTS["route_a_artifact"][0])
    route_b = load_json(INPUTS["route_b_artifact"][0])
    require(prereg.get("p1r_fs", {}).get("gate_status") == "PREREGISTERED_UNEXECUTED", "preregistered FS gate mismatch")
    require(prereg_audit.get("status") == "PASS", "preregistration hostile audit mismatch")
    require(route_a.get("artifact_id") == "p1r-fs-route-a-v1" and route_a.get("epistemic_status") == "PROVED", "Route A status mismatch")
    require(route_b.get("artifact_id") == "p1r-fs-route-b-v1" and route_b.get("epistemic_status") == "PROVED", "Route B status mismatch")
    require(route_a.get("prover", {}).get("sha256") == INPUTS["route_a_script"][1], "Route A executable identity mismatch")
    require(route_b.get("sealer", {}).get("sha256") == INPUTS["route_b_script"][1], "Route B executable identity mismatch")

    a_text = INPUTS["route_a_script"][0].read_text(encoding="utf-8")
    b_text = INPUTS["route_b_script"][0].read_text(encoding="utf-8")
    for forbidden in ("p1r_fs_route_b_v1", "p1r-fs-route-b-v1"):
        require(forbidden not in a_text, "Route A reads or names Route B")
    for forbidden in ("p1r_fs_route_a_v1", "p1r-fs-route-a-v1"):
        require(forbidden not in b_text, "Route B reads or names Route A")

    a_proof = route_a.get("exact_proof", {})
    b_proof = route_b.get("strict_left_supremum", {})
    require(a_proof.get("universal_identity") == "30/13-I(sigma)=30(7/10-sigma)/(13(2-sigma))", "Route A identity label mismatch")
    require(b_proof.get("coefficient_identity") == "I(7/10-h)=30/(13+10h)", "Route B coefficient identity mismatch")
    require(b_proof.get("gap_identity") == "30/13-I(7/10-h)=300h/(169+130h)", "Route B gap identity mismatch")
    require(a_proof.get("supremum") == b_proof.get("exact_supremum") == "sup_{1/2<=sigma<7/10} I(sigma)=30/13", "route supremum disagreement")
    a_obstruction = a_proof.get("formal_obstruction", "")
    require("modification confined to sigma>=7/10" in a_obstruction, "Route A right-only obstruction absent")
    require("right-only" in route_b.get("arbitrary_right_branch", {}).get("obstruction", ""), "Route B right-only obstruction absent")

    # Independent exact compatibility check between the routes' parameterizations.
    for h in (Fraction(1, 5), Fraction(1, 10), Fraction(1, 100), Fraction(1, 10**6)):
        sigma = Fraction(7, 10) - h
        direct = Fraction(3, 1) / (Fraction(2, 1) - sigma)
        cleared = Fraction(30, 1) / (Fraction(13, 1) + 10 * h)
        gap_a = Fraction(30, 13) - direct
        gap_b = 300 * h / (169 + 130 * h)
        require(direct == cleared and gap_a == gap_b and gap_a > 0, "route parameterization mismatch")

    return {
        "artifact_id": "p1r-fs-route-reconciliation-v1",
        "epistemic_status": "PROVED",
        "status": "TWO_ROUTE_RECONCILED_PENDING_HOSTILE_AUDIT",
        "theorem_id": "P1R-FS",
        "claim_boundary": "Two-route exact reconciliation for the frozen fixed-splice envelope class. This is not a lower bound for the actual zero count, not saturation of the Guth--Maynard method, not a new zero-density estimate, and not a short-interval theorem.",
        "runtime": runtime,
        "reconciler": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "independence_audit": {
            "status": "PASS",
            "route_a_representation": "direct sigma identity plus exact epsilon witness",
            "route_b_representation": "h substitution, cleared denominators, ordered image inclusion",
            "cross_route_file_references": [],
            "shared_inputs": ["sealed P1R v4 architecture", "Huxley source/ledger"],
        },
        "agreement": {
            "left_range": "1/2 <= sigma < 7/10",
            "left_coefficient": "I(sigma)=3/(2-sigma)",
            "strict_left_supremum": "30/13",
            "arbitrary_right_policy": "changes confined to sigma>=7/10",
            "conclusion": "Every uniform coefficient for the frozen splice is at least 30/13; equivalently, no right-only replacement certifies 30/13-eta for any eta>0 within this class.",
            "scope_exclusions": ["actual zero-density lower bound", "changed left branch", "moved splice", "full Guth--Maynard saturation", "new density or prime theorem"],
        },
        "gate_effect": "P1R-FS requires a final independent hostile audit before PLAN promotion.",
        "falsifier": "A frozen hash/status mismatch, a cross-route dependency, disagreement of the exact supremum/scope/architecture, or failure of the independent parameterization comparison invalidates reconciliation.",
    }


def render(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = reconcile()
    if args.write:
        require(not OUTPUT.exists(), "refusing to overwrite P1R-FS reconciliation artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(result))
    else:
        require(OUTPUT.is_file(), "P1R-FS reconciliation artifact is absent")
        require(OUTPUT.read_bytes() == render(result), "P1R-FS reconciliation artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": result["status"], "theorem_id": result["theorem_id"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
