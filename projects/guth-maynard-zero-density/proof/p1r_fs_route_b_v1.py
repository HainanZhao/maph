#!/usr/bin/env python3
"""Certify P1R-FS Route B by exact cleared-denominator arithmetic."""
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
OUTPUT = ROOT / "artifacts/p1r-fs-route-b-v1.json"
EXPECTED_RUNTIME = {
    "implementation": "CPython",
    "python": "3.12.3",
    "optimization_level": 0,
}
INPUTS: dict[str, tuple[Path, str]] = {
    "p1r_preregistration_v4": (
        ROOT / "artifacts/cycle-4-p1r-preregistration-v4.json",
        "e2aeec9ec90e1fea0a9eade53d5ff1e57020df48bd92ae852121a941fbadd7f9",
    ),
    "p1r_preregistration_v4_hostile_audit": (
        ROOT / "artifacts/cycle-4-p1r-preregistration-v4-hostile-audit-v1.json",
        "bdb60d416fee628d309e025a493c45383ccc50e3ee41a9bdb0d6b8a7d73235ad",
    ),
    "huxley_pdf": (
        ROOT / "artifacts/sources/huxley-1972-inventiones15-gdz-volume.pdf",
        "5946d8579810f0754e972d42a09ed2a703604b8fb4e6377f14caaa5dc48f9797",
    ),
    "classical_ledger": (
        ROOT / "docs/literature-ledger-classical-inputs.md",
        "5005dc96deca85d930b710000b1faccdce093e8574dc44f9730fa4a570529f11",
    ),
    "route_b_document": (
        ROOT / "docs/p1r-fs-route-b-v1.md",
        "935ee988f3074d0d7e29c2af0833bb0fa812948a65692d85ba92148446c785e7",
    ),
}

HALF = Fraction(1, 2)
ONE_FIFTH = Fraction(1, 5)
SEVEN_TENTHS = Fraction(7, 10)
THREE_QUARTERS = Fraction(3, 4)
BENCHMARK = Fraction(30, 13)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rational(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def check_runtime() -> dict[str, Any]:
    observed = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(
        observed == EXPECTED_RUNTIME,
        "P1R-FS Route B requires non-optimized CPython 3.12.3",
    )
    return observed


def ingham_coefficient_from_h(h: Fraction) -> Fraction:
    require(Fraction(0) < h <= ONE_FIFTH, "h must satisfy 0 < h <= 1/5")
    sigma = SEVEN_TENTHS - h
    direct = Fraction(3, 1) / (Fraction(2, 1) - sigma)
    cleared = Fraction(30, 1) / (Fraction(13, 1) + 10 * h)
    require(direct == cleared, "cleared Ingham coefficient identity failed")
    return cleared


def endpoint_gap(h: Fraction) -> Fraction:
    coefficient = ingham_coefficient_from_h(h)
    direct = BENCHMARK - coefficient
    cleared = 300 * h / (169 + 130 * h)
    require(direct == cleared, "cleared endpoint-gap identity failed")
    require(cleared > 0, "strict-left endpoint gap must be positive")
    return cleared


def eta_witness(eta: Fraction) -> dict[str, str]:
    require(Fraction(0) < eta < BENCHMARK, "eta must satisfy 0 < eta < 30/13")
    denominator = 300 - 130 * eta
    require(denominator > 0, "eta witness denominator must be positive")
    threshold = 169 * eta / denominator
    h = HALF * min(ONE_FIFTH, threshold)
    require(Fraction(0) < h <= ONE_FIFTH, "eta witness is outside the left range")
    require(h < threshold, "eta witness must be strictly below its gap threshold")
    gap = endpoint_gap(h)
    cleared_margin = eta * (169 + 130 * h) - 300 * h
    factored_margin = 169 * eta - h * (300 - 130 * eta)
    require(cleared_margin == factored_margin, "witness margin factorization failed")
    require(cleared_margin > 0, "witness strict gap margin is not positive")
    require(gap < eta, "eta witness does not approach the endpoint closely enough")
    coefficient = ingham_coefficient_from_h(h)
    require(coefficient > BENCHMARK - eta, "eta witness misses the lower target")
    return {
        "eta": rational(eta),
        "h": rational(h),
        "sigma": rational(SEVEN_TENTHS - h),
        "I_sigma": rational(coefficient),
        "gap": rational(gap),
        "strict_gap_margin": rational(cleared_margin),
    }


def finite_right_supremum(right_supremum: Fraction) -> dict[str, str]:
    combined = max(BENCHMARK, right_supremum)
    require(combined >= BENCHMARK, "combined supremum fell below the left supremum")
    expected = BENCHMARK if right_supremum <= BENCHMARK else right_supremum
    require(combined == expected, "two-branch maximum case split failed")
    return {
        "right_supremum": rational(right_supremum),
        "combined_supremum": rational(combined),
    }


def verify_frozen_inputs() -> dict[str, dict[str, str]]:
    frozen: dict[str, dict[str, str]] = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        observed = sha256(path)
        require(observed == expected, f"frozen input hash mismatch: {label}")
        frozen[label] = {"path": str(path.relative_to(ROOT)), "sha256": observed}

    prereg = load_json(INPUTS["p1r_preregistration_v4"][0])
    hostile = load_json(INPUTS["p1r_preregistration_v4_hostile_audit"][0])
    require(prereg.get("artifact_id") == "cycle-4-p1r-preregistration-v4", "wrong v4 preregistration")
    require(prereg.get("status") == "SEALED_PREREGISTRATION", "v4 preregistration is not sealed")
    fs = prereg.get("p1r_fs", {})
    require(fs.get("gate_status") == "PREREGISTERED_UNEXECUTED", "v4 FS premise is not unexecuted")
    require(
        fs.get("identity_algebra", {}).get("identity")
        == "30/13-3/(2-sigma)=30(7/10-sigma)/(13(2-sigma))",
        "v4 fixed-splice identity mismatch",
    )
    require(hostile.get("artifact_id") == "cycle-4-p1r-preregistration-v4-hostile-audit-v1", "wrong v4 hostile audit")
    require(hostile.get("status") == "PASS", "v4 hostile audit did not pass")
    require(
        hostile.get("audited_v4_hashes", {}).get("artifact")
        == INPUTS["p1r_preregistration_v4"][1],
        "hostile audit does not bind the pinned v4 artifact",
    )

    ledger = INPUTS["classical_ledger"][0].read_text(encoding="utf-8")
    required_fragments = (
        "| ING-HUX | Huxley, printed p. 164 = frozen `PDF p. 173`, (1.8)",
        "1/2\\le\\alpha\\le3/4",
        "T^{3(1-\\alpha)/(2-\\alpha)}(\\log T)^5",
        "1/2\\le\\sigma\\le7/10",
        "`PROVED` as a contemporaneous published restatement",
    )
    for fragment in required_fragments:
        require(fragment in ledger, f"classical ledger fragment missing: {fragment}")
    require(SEVEN_TENTHS < THREE_QUARTERS, "retained left endpoint is outside Huxley (1.8)")
    return frozen


def certificate() -> dict[str, Any]:
    runtime = check_runtime()
    frozen = verify_frozen_inputs()
    audit_etas = (Fraction(1, 1000), Fraction(1, 13), Fraction(1, 1), BENCHMARK - Fraction(1, 1000))
    witnesses = [eta_witness(eta) for eta in audit_etas]
    right_cases = [
        finite_right_supremum(Fraction(-100, 1)),
        finite_right_supremum(BENCHMARK),
        finite_right_supremum(Fraction(100, 1)),
    ]
    return {
        "artifact_id": "p1r-fs-route-b-v1",
        "epistemic_status": "PROVED",
        "status": "ROUTE_B_PASS_SCOPED_OBSTRUCTION",
        "claim_boundary": (
            "Exact fixed-splice obstruction conditional on the hash-pinned Huxley (1.8) restatement and sealed P1R v4 architecture. "
            "This is not a lower bound for the actual zero count, not saturation of the Guth--Maynard method, not a zero-density theorem, "
            "and not a short-interval theorem. Architectures changing or bypassing the retained left branch are outside scope."
        ),
        "gate_effect": "ROUTE_B_ONLY_PENDING_ROUTE_A_RECONCILIATION_AND_HOSTILE_AUDIT",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_inputs": frozen,
        "source_scope": {
            "epistemic_status": "PROVED",
            "authority": "Huxley (1.8), contemporaneous published restatement recorded by ING-HUX",
            "source_range": "1/2 <= sigma <= 3/4",
            "used_range": "1/2 <= sigma < 7/10",
            "coefficient": "I(sigma)=3/(2-sigma)",
            "log_factor": "(log T)^5 retained in the source statement; irrelevant to this coefficient-only asymptotic splice algebra",
        },
        "independence": {
            "route": "B",
            "representation": "h=7/10-sigma, cleared denominators, explicit rational eta witnesses, and image-inclusion supremum monotonicity",
            "route_a_inputs_read": [],
            "future_route_a_imports": [],
        },
        "strict_left_supremum": {
            "domain": "0 < h <= 1/5, equivalently 1/2 <= sigma < 7/10",
            "substitution": "sigma=7/10-h",
            "coefficient_identity": "I(7/10-h)=30/(13+10h)",
            "gap_identity": "30/13-I(7/10-h)=300h/(169+130h)",
            "upper_bound": "I(7/10-h)<30/13 for every 0<h<=1/5",
            "eta_quantifier": "for every rational eta with 0<eta<30/13",
            "eta_witness": "h_eta=(1/2)min(1/5,169eta/(300-130eta))",
            "witness_conclusion": "0<h_eta<=1/5 and I(7/10-h_eta)>30/13-eta",
            "exact_supremum": "sup_{1/2<=sigma<7/10} I(sigma)=30/13",
            "proof_kind": "exact rational-order supremum; the same inequalities establish the real supremum",
            "audit_witnesses": witnesses,
        },
        "arbitrary_right_branch": {
            "quantifier": "for every extended-real-valued J on [7/10,1]",
            "splice": "F_J=I on [1/2,7/10) and F_J=J on [7/10,1]",
            "set_inclusion": "I([1/2,7/10)) is a subset of F_J([1/2,1])",
            "supremum_identity": "sup F_J=max(30/13,sup J)",
            "obstruction": "sup F_J>=30/13, so no right-only replacement certifies a strict global coefficient below 30/13",
            "extended_cases": {"sup_J=-infinity": "sup F_J=30/13", "sup_J=+infinity": "sup F_J=+infinity"},
            "finite_exact_audit_cases": right_cases,
        },
        "falsifier": (
            "A frozen source/range mismatch, failure of either cleared identity, an inadmissible eta witness, failure of its strict gap margin, "
            "or failure of left-image inclusion in the full splice refutes the corresponding Route B conclusion."
        ),
        "replay": {
            "write_command": "python3 proof/p1r_fs_route_b_v1.py --write",
            "check_command": "python3 proof/p1r_fs_route_b_v1.py --check",
            "test_command": "python3 -m unittest tests/test_p1r_fs_route_b_v1.py -v",
        },
    }


def render(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = certificate()
    encoded = render(payload)
    if args.write:
        require(not OUTPUT.exists(), "refusing to overwrite P1R-FS Route B v1 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(encoded)
    else:
        require(OUTPUT.is_file(), "P1R-FS Route B v1 artifact is absent")
        require(OUTPUT.read_bytes() == encoded, "P1R-FS Route B v1 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
