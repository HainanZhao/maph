#!/usr/bin/env python3
"""Seal the Cycle 7 CRR F4F Mellin--Farey reduction v1."""
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
OUTPUT = ROOT / "artifacts/cycle-7-crr-f4f-mellin-farey-reduction-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "crr_v2_artifact": (ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v2.json", "e26be797539eabe53ee765b7067d1c99fe4d440035e27785cf38aa64bc2fc84e"),
    "farey_v2_artifact": (ROOT / "artifacts/cycle-5-crr-farey-log-gram-reduction-v2-averaged-jitter.json", "ce59b777ec02769168d9dc330658a0ab1d46b05cdb7ac5dc8115e248d85f8ce8"),
    "afari_artifact": (ROOT / "artifacts/cycle-6-crr-afari-coefficient-coupling-v1.json", "a9b142f8fd22e4fe9ebd4857af4eb7e764aa20ea379170930f6446231e663266"),
    "cfari_artifact": (ROOT / "artifacts/cycle-6-crr-cfari-phase-equivalence-v1.json", "00ca4e7f794a06d797b24543d174d86ef6d8a3f99a068d14bb693ce894f16dad"),
    "document": (ROOT / "docs/cycle-7-crr-f4f-mellin-farey-reduction-v1.md", "c65439916cab0f10f36c8a2b637f2c204783171367271f01669e41dcee038394"),
    "conventions": (ROOT / "conventions/crr_f4f_mellin_farey_v1.py", "b61f2c0ec7c9adbb8a0f14e03e172396c9262b2cd24deb89653966f82d059719"),
    "tests": (ROOT / "tests/test_cycle_7_crr_f4f_mellin_farey_reduction_v1.py", "0e4ff76eb80aeb91ff3252c554a92aae8a92e2def6967aef8c6ccf3ac019819d"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def json_exact(value: Any) -> Any:
    if isinstance(value, Fraction):
        return fraction_text(value)
    if isinstance(value, tuple):
        return [json_exact(item) for item in value]
    if isinstance(value, list):
        return [json_exact(item) for item in value]
    if isinstance(value, dict):
        return {str(key): json_exact(item) for key, item in value.items()}
    return value


def check_runtime() -> dict[str, Any]:
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "CRR F4F Mellin--Farey v1 requires non-optimized CPython 3.12.3")
    return runtime


def frozen_inputs() -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for label, (path, expected) in INPUTS.items():
        require(expected != "AUTO", f"unfrozen input hash: {label}")
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        result[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    return result


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def load_conventions():
    path = INPUTS["conventions"][0]
    spec = importlib.util.spec_from_file_location("crr_f4f_mellin_farey_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load F4F Mellin--Farey conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_context() -> dict[str, str]:
    crr = load_json(INPUTS["crr_v2_artifact"][0])
    require(crr.get("artifact_id") == "cycle-4-p1r-crr-u-formalization-v2", "CRR v2 identity mismatch")
    base = crr.get("witness_schema", {}).get("base", {})
    require(base.get("energy_band") == "v^(20-delta(v)) <= E(W) <= v^(20+delta(v))", "Base energy convention mismatch")
    farey = load_json(INPUTS["farey_v2_artifact"][0])
    require(farey.get("artifact_id") == "cycle-5-crr-farey-log-gram-reduction-v2-averaged-jitter", "Farey v2 identity mismatch")
    lower = farey.get("averaged_actual_farey_lower", {})
    require(lower.get("lower_bound") == "A_v(W)>=(15/8)*v^(26-3*delta(v))", "Farey lower convention mismatch")
    afari = load_json(INPUTS["afari_artifact"][0])
    require(afari.get("f4f_target", {}).get("epistemic_status") == "CONJECTURED", "F4F status convention mismatch")
    cfari = load_json(INPUTS["cfari_artifact"][0])
    require("CFARI" in cfari.get("claim_boundary", ""), "CFARI context mismatch")
    return {"base_energy": base["energy_band"], "farey_lower": lower["lower_bound"], "f4f_prior_status": "CONJECTURED", "actual_labels": "coprime ordered (r,s) in the frozen Q-shell"}


def exact_rows() -> dict[str, Any]:
    module = load_conventions()
    checked = module.verify_all()
    rows = checked["exact_rows"]
    require(rows["log_jitter_kernel_at_zero"] == 6, "jitter zero constant mismatch")
    require(rows["log_jitter_high_band_lower_numerator"] == Fraction(1, 2), "high-band jitter lower mismatch")
    require(rows["wiener_no_go_lower"] == Fraction(1, 1000), "Wiener no-go constant mismatch")
    return {"scales_at_v8": json_exact(checked["scales"]), "constants": json_exact(rows)}


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen = frozen_inputs()
    context = validate_context()
    rows = exact_rows()
    return {
        "artifact_id": "cycle-7-crr-f4f-mellin-farey-reduction-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_F4F_MELLIN_FAREY_REDUCTION_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "This artifact proves exact logarithmic Farey Fourier and fourth-moment identities, a conditional Wiener sufficient condition, low-frequency continuum scope, and a high-frequency no-go for the absolute energy-bin route. It proves neither F4F_eta, AFARI_eta, CFARI_eta, CRR-U, a Base-compatible counterexample, a cubic estimate, a density gain, a short-interval theorem, a full-method saturation theorem, nor an L-function result.",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "research_stage_review_policy": {"lightweight_checks": "exact Fourier/Mobius algebra, scale/constants bookkeeping, source-artifact checks, replay, and tamper rejection", "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION"},
        "source_context": context,
        "exact_log_farey_expansion": {"epistemic_status": "PROVED", "kernel": "mu_hat_v(tau)=J_H(tau)S_Q(tau), J_H(tau)=2*sin(3*tau/H)/tau", "fourth_moment": "I4_log(W)=sum_(t1,t2,t3,t4 in W)mu_hat_v(t1+t2-t3-t4)", "labels": "the sum S_Q keeps each original coprime ordered pair (r,s)"},
        "energy_bin_reduction": {"epistemic_status": "PROVED", "bound": "integral_(U_v)|R_W|^4du<=(3/2)E(W)W_Q", "wiener_norm": "W_Q=sum_(|m|<=2H+2)sup_(|tau-m|<=1)|J_H(tau)S_Q(tau)|", "conditional_effect": "W_Q<=v^(-kappa) implies F4F_(kappa/2) eventually, hence AFARI and CRR-U"},
        "continuum_scope": {"epistemic_status": "PROVED", "estimate": "S_Q(tau)=Q^2 I(tau)/zeta(2)+O(Q+Q(1+|tau|)log(2Q)), I(tau)<<1/(1+|tau|)", "valid_uniform_decay_range": "(1+|tau|)^2 log(2Q)<<Q", "low_frequency_wiener": "sum_low B_m<<Q^(-1)log(2Q)", "boundary": "this is the elementary continuum/Mobius method's breakdown scale, not a theorem locating all discrete large values"},
        "mobius_dirichlet_square": {"epistemic_status": "PROVED", "statement": "S_(phi,Q)(tau)=sum_d mu(d)|sum_n phi(dn/Q)n^(i tau)|^2 for a smooth core phi supported in [1,9/8]", "scope": "identifies the high-frequency object; it does not by itself upper-bound the full sharp shell"},
        "absolute_wiener_no_go": {"epistemic_status": "PROVED", "statement": "W_Q>=1/1000 for all sufficiently large Q", "mechanism": "Farey log separation plus the Montgomery--Vaughan Hilbert mean-value lower on [H/10,9H/10], where |J_H|>=1/(2H)", "conclusion": "No fixed-power W_Q upper bound exists, so the absolute Fourier-bin/Cauchy energy route cannot prove F4F."},
        "crr_u_effect": {"epistemic_status": "PROVED", "statement": "CRR-U remains open. A fixed-saving F4F theorem would still imply AFARI and CRR-U, but this reduction only rules out one absolute-energy proof route."},
        "exact_replay": rows,
        "replay": {"write_command": "python3 proof/build_cycle_7_crr_f4f_mellin_farey_reduction_v1.py --write", "check_command": "python3 proof/build_cycle_7_crr_f4f_mellin_farey_reduction_v1.py --check", "test_command": "python3 -m unittest tests/test_cycle_7_crr_f4f_mellin_farey_reduction_v1.py"},
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
        require(not OUTPUT.exists(), "refusing to overwrite F4F Mellin--Farey v1 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "F4F Mellin--Farey v1 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "F4F Mellin--Farey v1 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
