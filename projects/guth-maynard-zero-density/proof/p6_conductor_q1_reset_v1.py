#!/usr/bin/env python3
"""Seal the exact conductor-level reset of the auxiliary divisor q1."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
DOC = ROOT / "docs/p6-conductor-q1-reset-v1.md"
OUT = ROOT / "artifacts/p6-conductor-q1-reset-v1.json"
PRIMITIVE = ROOT / "artifacts/p6-primitive-to-all-transfer-v1.json"
RECONCILIATION = ROOT / "artifacts/p6-cgl-v2-reconciliation-v1.json"
SOURCE = ROOT / "artifacts/sources/g1-literature-audit-v1/extracted-2507.08296v2/Large_Value_Estimates_for_Dirichlet_Polynomials_with_Characters_and_Zero_Density_of_Dirichlet___L_-Functions.tex"

FROZEN_HASHES = {
    PRIMITIVE: "2edccf46d15229fb8b8ff2c9510d0912f73228da681577ca66d869a8d8acf0d7",
    RECONCILIATION: "cf59aa63b97d69c672fafa0b0ca49221d9005c3da6ccd61f05d37f4bcbc68e49",
    SOURCE: "0b9ebb6b604944b7c59a9ec37a75c48f6a08f88611f911ff5f02dc013b848e2f",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def exact_rows() -> list[dict[str, object]]:
    rows = []
    for sigma in (Fraction(1, 2), Fraction(7, 10), Fraction(4, 5), Fraction(9, 10)):
        a = 1 - sigma
        first_q = Fraction(7, 3) * a
        first_t = 2 * a
        second = Fraction(30, 13) * a
        uniform = Fraction(7, 3) * a
        require(first_t <= uniform and first_q == uniform and second <= uniform, "uniform exponent domination failed")
        rows.append({
            "sigma": str(sigma),
            "first_q_exponent": str(first_q),
            "first_t_exponent": str(first_t),
            "second_qt_exponent": str(second),
            "uniform_qt_exponent": str(uniform),
        })
    return rows


def payload() -> dict[str, object]:
    require(sys.flags.optimize == 0, "optimized Python is rejected")
    for path, expected in FROZEN_HASHES.items():
        require(digest(path) == expected, f"frozen input changed: {path.name}")
    primitive = json.loads(PRIMITIVE.read_text(encoding="utf-8"))
    require(primitive["epistemic_status"] == "PROVED", "primitive transfer status changed")
    require(primitive["lemma"]["epistemic_status"] == "PROVED", "primitive lemma status changed")
    require(primitive["lemma"]["exact_partition"]["identity"].startswith("sum_{chi mod q}"), "conductor partition changed")
    source_text = SOURCE.read_text(encoding="utf-8")
    for anchor in (
        "For any divisor $q_1 \\mid q$",
        "we can restrict our analysis to primitive characters modulo $q$",
        "applying our final estimate for all factors of $q$ and summing",
    ):
        require(anchor in source_text, f"missing source anchor: {anchor}")
    return {
        "artifact_id": "p6-conductor-q1-reset-v1",
        "epistemic_status": "PROVED",
        "theorem": {
            "hypothesis": "For every exact conductor d|q, the primitive estimate is available after the fresh admissible choice q1'=d.",
            "conclusion": "Apply the final monotone d-envelope before summing conductors; no original q1|q must divide d or be dominated termwise.",
            "all_character_envelope": "tau(q)*(qT)^o(1)*(q^(7a/3)T^(2a)+(qT)^(30a/13)), a=1-sigma",
            "uniform_consequence": "(qT)^((7/3)(1-sigma)+o(1)) conditional on the primitive input",
        },
        "external_input": {
            "epistemic_status": "CONJECTURED",
            "statement": "The primitive CGL-style analytic estimate with q1'=d and all source hypotheses.",
        },
        "gate_effect": "Z06 q1-sensitive termwise domination is removed as an independent conductor-transfer obligation; prescribed-q1 intermediate uses and S06 remain open.",
        "exact_exponent_rows": exact_rows(),
        "frozen_inputs": {str(path.relative_to(ROOT)): expected for path, expected in FROZEN_HASHES.items()},
        "document": {"path": str(DOC.relative_to(ROOT)), "sha256": digest(DOC)},
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)},
        "hostile_audit": "DEFERRED_TO_PAPER_STAGE",
        "replay": "python3 proof/p6_conductor_q1_reset_v1.py --check",
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
        require(not OUT.exists(), "refusing to overwrite q1-reset artifact")
        OUT.write_bytes(encoded)
    else:
        require(OUT.is_file() and OUT.read_bytes() == encoded, "q1-reset artifact mismatch")
    print(json.dumps({"artifact": OUT.name, "status": "ok"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
