#!/usr/bin/env python3
"""Seal the exact finite multiplicity-to-distinct support transfer."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
DOC = ROOT / "docs/p6-multiplicity-transfer-v1.md"
OUT = ROOT / "artifacts/p6-multiplicity-transfer-v1.json"
SOURCE = ROOT / "artifacts/sources/g1-literature-audit-v1/extracted-2507.08296v2/Large_Value_Estimates_for_Dirichlet_Polynomials_with_Characters_and_Zero_Density_of_Dirichlet___L_-Functions.tex"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def finite_transfer(multiplicities: list[int], local_cap: int) -> dict[str, int]:
    require(local_cap >= 1, "local cap must be positive")
    require(all(1 <= value <= local_cap for value in multiplicities), "multiplicity exceeds local cap")
    distinct = len(multiplicities)
    total = sum(multiplicities)
    require(total <= local_cap * distinct, "finite transfer failed")
    return {"distinct": distinct, "multiplicity_weighted": total, "upper_bound": local_cap * distinct}


def payload() -> dict[str, object]:
    require(sys.flags.optimize == 0, "optimized Python is rejected")
    source_text = SOURCE.read_text(encoding="utf-8")
    for anchor in (
        "where $N(\\sigma,T,\\chi)$ denotes the number of zeros",
        "The zeros $(\\rho, \\chi)$ with $\\beta \\geq \\sigma",
        "N(\\sigma, T+ 1, \\chi) - N(\\sigma, T, \\chi) \\ll \\log qT",
    ):
        require(anchor in source_text, f"missing frozen CGL anchor: {anchor}")
    examples = [
        finite_transfer([1], 1),
        finite_transfer([1, 3, 2, 3], 3),
        finite_transfer([7, 7, 7], 7),
    ]
    return {
        "artifact_id": "p6-multiplicity-transfer-v1",
        "epistemic_status": "PROVED",
        "theorem": {
            "hypothesis": "Each distinct labeled zero has multiplicity at most L, supplied by a multiplicity-inclusive local unit-strip zero count.",
            "conclusion": "The multiplicity-weighted count is at most L times the distinct-support count; a distinct well-spaced selection therefore transfers without duplicating ordinates.",
            "density_effect": "When L is polylogarithmic in qT, the transfer changes only the (qT)^o(1) factor.",
        },
        "external_unproved_input": {
            "epistemic_status": "CONJECTURED",
            "id": "LOCAL_MULTIPLICITY_COUNT_LC",
            "disposition": "Moved to S06_EXTERNAL_INPUTS; exact primary theorem, ranges, endpoints, and uniformity remain to be checked.",
        },
        "gate_effect": "S03 is no longer an independent structural obstruction conditional on LC; no density theorem is promoted.",
        "finite_exact_examples": examples,
        "source": {"path": str(SOURCE.relative_to(ROOT)), "sha256": digest(SOURCE), "anchors_only": True},
        "document": {"path": str(DOC.relative_to(ROOT)), "sha256": digest(DOC)},
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)},
        "hostile_audit": "DEFERRED_TO_PAPER_STAGE",
        "replay": "python3 proof/p6_multiplicity_transfer_v1.py --check",
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
        require(not OUT.exists(), "refusing to overwrite multiplicity-transfer artifact")
        OUT.write_bytes(encoded)
    else:
        require(OUT.is_file() and OUT.read_bytes() == encoded, "multiplicity-transfer artifact mismatch")
    print(json.dumps({"artifact": OUT.name, "status": "ok"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
