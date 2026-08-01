#!/usr/bin/env python3
"""P1R-FS Route A: direct exact proof of the fixed-splice obstruction."""
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
OUTPUT = ROOT / "artifacts/p1r-fs-route-a-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "p1r_preregistration_v4": (ROOT / "artifacts/cycle-4-p1r-preregistration-v4.json", "e2aeec9ec90e1fea0a9eade53d5ff1e57020df48bd92ae852121a941fbadd7f9"),
    "p1r_preregistration_v4_hostile_audit": (ROOT / "artifacts/cycle-4-p1r-preregistration-v4-hostile-audit-v1.json", "bdb60d416fee628d309e025a493c45383ccc50e3ee41a9bdb0d6b8a7d73235ad"),
    "huxley_pdf": (ROOT / "artifacts/sources/huxley-1972-inventiones15-gdz-volume.pdf", "5946d8579810f0754e972d42a09ed2a703604b8fb4e6377f14caaa5dc48f9797"),
    "classical_ledger": (ROOT / "docs/literature-ledger-classical-inputs.md", "5005dc96deca85d930b710000b1faccdce093e8574dc44f9730fa4a570529f11"),
    "envelope_sensitivity": (ROOT / "artifacts/g1-envelope-sensitivity-reconciliation-v1.json", "850b825698722d628340b762867c98774dae53443aecde581138c6830993b60e"),
}
TARGET = Fraction(30, 13)
SPLICE = Fraction(7, 10)
LEFT_MIN = Fraction(1, 2)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def check_runtime() -> dict[str, Any]:
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "P1R-FS Route A requires non-optimized CPython 3.12.3")
    return runtime


def ingham_coefficient(sigma: Fraction) -> Fraction:
    require(LEFT_MIN <= sigma < SPLICE, "sigma outside frozen strict left branch")
    return Fraction(3, 1) / (Fraction(2, 1) - sigma)


def epsilon_witness(eta: Fraction) -> dict[str, Fraction]:
    """Return an exact left-branch point with I(sigma)>30/13-eta."""
    require(Fraction(0, 1) < eta < TARGET, "eta must lie strictly between 0 and 30/13")
    threshold = Fraction(169, 1) * eta / (Fraction(300, 1) - Fraction(130, 1) * eta)
    h = min(Fraction(1, 10), threshold / 2)
    sigma = SPLICE - h
    value = ingham_coefficient(sigma)
    require(Fraction(0, 1) < h <= Fraction(1, 10), "witness h outside certified interval")
    require(h < threshold, "witness does not meet exact threshold")
    require(value > TARGET - eta, "witness fails strict supremum inequality")
    return {"eta": eta, "threshold": threshold, "h": h, "sigma": sigma, "I_sigma": value, "target_minus_eta": TARGET - eta}


def prove() -> dict[str, Any]:
    runtime = check_runtime()
    frozen: dict[str, dict[str, str]] = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        frozen[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}

    prereg = load_json(INPUTS["p1r_preregistration_v4"][0])
    hostile = load_json(INPUTS["p1r_preregistration_v4_hostile_audit"][0])
    require(prereg.get("status") == "SEALED_PREREGISTRATION", "P1R preregistration status mismatch")
    require(prereg.get("p1r_fs", {}).get("gate_status") == "PREREGISTERED_UNEXECUTED", "P1R-FS prior-gate status mismatch")
    require(prereg.get("p1r_fs", {}).get("completed_theorem") is False, "preregistration improperly records a theorem")
    require(hostile.get("status") == "PASS", "P1R preregistration hostile audit did not pass")
    ledger = INPUTS["classical_ledger"][0].read_text(encoding="utf-8")
    require("N(\\alpha,T)\\ll T^{3(1-\\alpha)/(2-\\alpha)}(\\log T)^5" in ledger, "pinned Ingham/Huxley formula missing")
    require("1/2\\le\\alpha\\le3/4" in ledger, "pinned Ingham/Huxley range missing")

    # Polynomial cross-multiplication proves the identity for every sigma in
    # the frozen interval; the following distinct rational points guard the
    # implementation without substituting finite sampling for the proof.
    for sigma in (LEFT_MIN, Fraction(3, 5), Fraction(69, 100)):
        lhs = TARGET - ingham_coefficient(sigma)
        rhs = Fraction(30, 1) * (SPLICE - sigma) / (Fraction(13, 1) * (Fraction(2, 1) - sigma))
        require(lhs == rhs and rhs > 0, "fixed-splice identity implementation mismatch")
    endpoint_value = Fraction(3, 1) / (Fraction(2, 1) - SPLICE)
    require(endpoint_value == TARGET, "left endpoint limit mismatch")
    examples = [epsilon_witness(x) for x in (Fraction(1, 1000), Fraction(1, 13), Fraction(1, 1), Fraction(2, 1))]

    return {
        "artifact_id": "p1r-fs-route-a-v1",
        "epistemic_status": "PROVED",
        "theorem_id": "P1R-FS-A",
        "claim_boundary": "Exact source-anchored theorem for the frozen fixed-splice envelope class only. It is not a lower bound for N(sigma,T), not saturation of the Guth--Maynard method, not a new density estimate, and not a short-interval theorem.",
        "runtime": runtime,
        "prover": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "architecture": {
            "left_range": "1/2 <= sigma < 7/10",
            "left_coefficient": "I(sigma)=3/(2-sigma)",
            "right_branch": "arbitrary and permitted to change only for sigma >= 7/10",
            "global_certificate_semantics": "a uniform coefficient B must upper-bound every retained left value and every right-branch value",
        },
        "exact_proof": {
            "universal_identity": "30/13-I(sigma)=30(7/10-sigma)/(13(2-sigma))",
            "identity_certificate": "After multiplying by the positive 13(2-sigma), both sides have numerator 30(7/10-sigma).",
            "strict_left_upper_bound": "I(sigma)<30/13 for every sigma<7/10 in the frozen range.",
            "endpoint_limit": "lim_{sigma upward 7/10} I(sigma)=3/(2-7/10)=30/13",
            "epsilon_witness_rule": "For 0<eta<30/13, let H_eta=169 eta/(300-130 eta), h=min(1/10,H_eta/2), sigma=7/10-h; then h<H_eta and I(sigma)>30/13-eta.",
            "supremum": "sup_{1/2<=sigma<7/10} I(sigma)=30/13",
            "formal_obstruction": "For every eta in (0,30/13), the retained left branch has a value exceeding 30/13-eta. Therefore no modification confined to sigma>=7/10 can certify a strict global coefficient 30/13-eta within this architecture.",
            "sampled_witness_regressions": [{key: q(value) for key, value in row.items()} for row in examples],
        },
        "out_of_scope": ["changing the left branch", "moving the splice", "a left-neighborhood improvement", "an actual lower bound for zero density", "termwise or method-wide saturation"],
        "falsifier": "A frozen source/range/hash mismatch, a failed universal cross-multiplication identity, a failed epsilon witness, or a claim about an architecture that changes the left branch invalidates promotion.",
    }


def render(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = prove()
    if args.write:
        require(not OUTPUT.exists(), "refusing to overwrite P1R-FS Route A artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(result))
    else:
        require(OUTPUT.is_file(), "P1R-FS Route A artifact is absent")
        require(OUTPUT.read_bytes() == render(result), "P1R-FS Route A artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "epistemic_status": result["epistemic_status"], "theorem_id": result["theorem_id"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
