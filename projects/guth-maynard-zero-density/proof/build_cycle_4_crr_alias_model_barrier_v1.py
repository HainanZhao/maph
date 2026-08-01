#!/usr/bin/env python3
"""Seal the exact bookkeeping for the CRR logarithmic-alias model barrier v1.

The analytic existence proof is in the pinned document.  This replay checks
the frozen source context, the integer scale/carry identities, the exact
probabilistic-energy bound, and the q-exponent algebra.  It does not search
for a CRR witness or invoke a hostile audit.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-4-crr-alias-model-barrier-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "alias_conventions": (
        ROOT / "conventions/crr_alias_model_barrier_v1.py",
        "69126ff3a4291e3e625556e72079e1e4c222dc72481a18139d64b6ee7a683724",
    ),
    "crr_v2_conventions": (
        ROOT / "conventions/crr_formalization_v2.py",
        "0d960b76a4ad03cce43727159cf846696dbee732184df44b2ee0503b9ae18ce8",
    ),
    "crr_v2_artifact": (
        ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v2.json",
        "e26be797539eabe53ee765b7067d1c99fe4d440035e27785cf38aa64bc2fc84e",
    ),
    "document": (
        ROOT / "docs/cycle-4-crr-alias-model-barrier-v1.md",
        "ce616e72cac5cbc1a811e9414ac996e7ac47da94f9c2c004e6aa687b00e534b1",
    ),
    "gm_source_tex": (
        ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex",
        "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
    ),
}
SOURCE_FRAGMENTS = (
    "E(W):=\\#\\{w_1,w_2,w_3,w_4\\in W:\\,|w_1+w_2-w_3-w_4|\\le 1\\}",
    "If $U$ is the $1/T$-neighborhood of the set of rational numbers $r/s$",
    "\\tilde{f}(u) := T \\int  \\psi( T(u - u') ) f(u') du'",
    "\\begin{rmk}For the purposes of proving a zero density estimate",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction_text(value: Fraction) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def check_runtime() -> dict[str, Any]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, "CRR alias-model barrier v1 requires non-optimized CPython 3.12.3")
    return runtime


def frozen_inputs() -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for label, (path, expected_hash) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual_hash = sha256(path)
        require(actual_hash == expected_hash, f"frozen input hash mismatch: {label}")
        result[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual_hash}
    return result


def load_alias_conventions():
    path = INPUTS["alias_conventions"][0]
    spec = importlib.util.spec_from_file_location("crr_alias_model_barrier_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load alias-model conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_context() -> None:
    source = INPUTS["gm_source_tex"][0].read_text(encoding="utf-8")
    for fragment in SOURCE_FRAGMENTS:
        require(fragment in source, f"GM source fragment missing: {fragment}")
    crr = json.loads(INPUTS["crr_v2_artifact"][0].read_text(encoding="utf-8"))
    rational = crr.get("witness_schema", {}).get("rational_mass", {})
    require(
        rational.get("rational_net") == "coprime Q<=r,s<2Q, 3/4<=r/s<=5/4, intervals of radius 1/(100H)",
        "CRR-v2 actual rational-net convention mismatch",
    )
    require(
        rational.get("smoothing", "").startswith("Rtilde_W(u)^2=integral_R H psi1(H(u-u'))"),
        "CRR-v2 smoothing convention mismatch",
    )


def exact_rows() -> dict[str, Any]:
    c = load_alias_conventions()
    samples: list[dict[str, Any]] = []
    for q in (256, 257, 1024, 4096):
        data = c.scales(q)
        expected_upper = c.energy_expectation_upper(q)
        interval_energy = c.interval_energy(data["L"])
        alias_lower = c.alias_count_lower(q)
        require(data["minimum_A_gap"] >= 6 * q, "hard-core gap check failed")
        require(data["A_max_upper"] < data["K"] // 4, "A carry-margin check failed")
        require(interval_energy * 3 == 2 * data["L"] ** 3 + data["L"], "block boundary energy check failed")
        require(alias_lower == Fraction(2 * data["K"], 3), "Paley alias count mismatch")
        samples.append(
            {
                "q": q,
                "m": data["m"],
                "K": data["K"],
                "L": data["L"],
                "H": data["H"],
                "cardinality": data["R"],
                "minimum_A_gap": data["minimum_A_gap"],
                "A_max_upper": data["A_max_upper"],
                "interval_energy": interval_energy,
                "expected_A_energy_upper": fraction_text(expected_upper),
                "Paley_good_alias_index_lower": fraction_text(alias_lower),
            }
        )
    exponents = {key: fraction_text(value) for key, value in c.exponent_rows().items()}
    require(c.ALIAS_DILATION // 128 == 8, "exact alias-cycle count mismatch")
    require(c.HEIGHT_FACTOR == 2**20, "height constant mismatch")
    return {"samples": samples, "q_exponents": exponents}


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen = frozen_inputs()
    validate_context()
    rows = exact_rows()
    return {
        "artifact_id": "cycle-4-crr-alias-model-barrier-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ANALYTIC_BARRIER_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "This is an elementary logarithmic-alias countermodel to a deduction from generic spacing, real energy, and positive H^(-1) smoothing alone. It is not an actual Farey/rational-net construction; it proves neither a CRR witness nor CRR-U, and it gives no coefficient, cubic, density, prime-interval, saturation, or L-function result.",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "research_stage_review_policy": {
            "lightweight_checks": "source-context transcription, exact integer carry/energy algebra, exact Fourier-moment count, frozen hashes, and replay",
            "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION",
        },
        "source_context": {
            "epistemic_status": "PROVED",
            "actual_GM_rational_example_locator": "LargevaluesDirichlet17.tex, lines 1433-1441",
            "critical_GM_remark_locator": "LargevaluesDirichlet17.tex, lines 2398-2399",
            "source_relation": "The source's rational example and its H^(-1)-scale smoothing motivate the model only; their rational r/s net is not substituted by these aliases.",
        },
        "construction": {
            "epistemic_status": "PROVED",
            "parameterization": "m=floor(q/64), K=q^2, L=64q, C=1024, H=16CKL=2^20 q^3",
            "jittered_A": "a_i=8q*i+r_i with independent r_i in {0,...,2q-1}; choose a realization with E(A)<=3m^2",
            "hard_core": "A has gap >=6q+1 and A subset [0,K/4); W=C(A+K{0,...,L-1}) has gap >=C(6q+1) and lies in [0,H]",
            "cardinality": "q^2/2<=|W|=mL<=q^2",
            "real_energy": {
                "definition": "E_R,1(W)=#{w1,w2,w3,w4 in W: |w1+w2-w3-w4|<=1}",
                "tolerance_reduction": "W subset 1024 Z, so tolerance <=1 is exact equality; this is not modular energy.",
                "no_carry_factorization": "A+A subset [0,K/2) forces separately a1+a2=a3+a4 and l1+l2=l3+l4 in every block equation.",
                "exact_formula": "E_R,1(W)=E(A)*(2L^3+L)/3",
                "scale": "E_R,1(W) asymp q^5",
            },
        },
        "alias_and_smoothing": {
            "epistemic_status": "PROVED",
            "nodes": "u_j=exp(2*pi*j/(C K)), 0<=j<8K; all lie in [3/4,5/4] because y_j<pi/64<1/20",
            "fourier_count": "Parseval sum|Ahat|^2=Km and sum|Ahat|^4=K E_(Z/KZ)(A)<=3Km^2 give >=K/12 good residues; eight cycles give >=2K/3 good node indices.",
            "raw_alias_lower": "For |log(u/u_j)|<=1/(100H), |R_W(u)| >= (9/10)L sqrt(m/2).",
            "positive_smoothing": "The fixed v2 positive kernel H psi1(H(u-u')) psi2(u') has height asymp H and width asymp H^(-1); restricting to a positive core transfers the raw lower bound to F_H(u) >> L^2m.",
            "packet": "A disjoint union U_q of core intervals has measure asymp K/H=asymp q^(-1), integral_U F_H >>q^2, and integral_U F_H^2 >>q^5.",
        },
        "logical_barrier": {
            "epistemic_status": "PROVED",
            "statement": "For every fixed delta>0, the generic conditions listed in claim_boundary cannot by themselves imply a q^(2-delta) first-moment or q^(5-delta) second-moment upper bound on every logarithmic-alias packet.",
            "falsifier": "A proposed generic implication with either fixed-power upper saving, applied to the constructed W and U_q, is refuted for sufficiently large q.",
        },
        "scope_exclusions": [
            "No ordinary Farey nodes r/s or actual CRR-v2 rational net are constructed.",
            "No coefficient sequence b_n or Dirichlet-polynomial large-value condition is supplied.",
            "No positive cubic contribution, Base predicate, CRR witness, or CRR-U conclusion is supplied.",
            "No statement asserts that Guth--Maynard's affine proposition is saturated or improvable.",
        ],
        "exact_replay": rows,
        "replay": {
            "write_command": "python3 proof/build_cycle_4_crr_alias_model_barrier_v1.py --write",
            "check_command": "python3 proof/build_cycle_4_crr_alias_model_barrier_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_4_crr_alias_model_barrier_v1.py",
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
    payload = seal()
    if args.write:
        require(not OUTPUT.exists(), "refusing to overwrite CRR alias-model barrier v1 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "CRR alias-model barrier v1 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "CRR alias-model barrier v1 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
