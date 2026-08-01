#!/usr/bin/env python3
"""Seal the Cycle 7 signed F4F projection/extremizer reduction v1."""
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
OUTPUT = ROOT / "artifacts/cycle-7-crr-f4f-signed-projection-extremizer-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "crr_v2_artifact": (ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v2.json", "e26be797539eabe53ee765b7067d1c99fe4d440035e27785cf38aa64bc2fc84e"),
    "farey_v2_artifact": (ROOT / "artifacts/cycle-5-crr-farey-log-gram-reduction-v2-averaged-jitter.json", "ce59b777ec02769168d9dc330658a0ab1d46b05cdb7ac5dc8115e248d85f8ce8"),
    "afari_artifact": (ROOT / "artifacts/cycle-6-crr-afari-coefficient-coupling-v1.json", "a9b142f8fd22e4fe9ebd4857af4eb7e764aa20ea379170930f6446231e663266"),
    "cfari_artifact": (ROOT / "artifacts/cycle-6-crr-cfari-phase-equivalence-v1.json", "00ca4e7f794a06d797b24543d174d86ef6d8a3f99a068d14bb693ce894f16dad"),
    "f4f_mellin_artifact": (ROOT / "artifacts/cycle-7-crr-f4f-mellin-farey-reduction-v1.json", "18fefc631e63a622cf780c927cd6aad185d5cc310f9e908c09ccb9de1fefc7a4"),
    "document": (ROOT / "docs/cycle-7-crr-f4f-signed-projection-extremizer-v1.md", "fabe2df4b91d4b38eca3cfb9e2357f430033ae4ad1c671beb341775b463340a2"),
    "conventions": (ROOT / "conventions/crr_f4f_signed_projection_extremizer_v1.py", "62e569e2e63ecd4b02671157866f0b71872264d4367e0ff8d443cde9fae582a1"),
    "tests": (ROOT / "tests/test_cycle_7_crr_f4f_signed_projection_extremizer_v1.py", "a063e0abbcfbac9568f0317681e4335ead39561ff394c4347ce3d3fcf05ffbf5"),
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
    require(runtime == EXPECTED_RUNTIME, "CRR signed F4F projection/extremizer v1 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("crr_f4f_signed_projection_extremizer_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load signed F4F projection/extremizer conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_context() -> dict[str, str]:
    crr = load_json(INPUTS["crr_v2_artifact"][0])
    require(crr.get("artifact_id") == "cycle-4-p1r-crr-u-formalization-v2", "CRR v2 identity mismatch")
    base = crr.get("witness_schema", {}).get("base", {})
    require(base.get("energy_band") == "v^(20-delta(v)) <= E(W) <= v^(20+delta(v))", "Base energy convention mismatch")
    require(base.get("energy_definition") == "ordered quadruples in W^4 with |t1+t2-t3-t4|<=1", "Base energy definition mismatch")
    require(base.get("set") == "finite W subset [0,H], H^(1/100)-separated", "Base row-set convention mismatch")
    farey = load_json(INPUTS["farey_v2_artifact"][0])
    require(farey.get("artifact_id") == "cycle-5-crr-farey-log-gram-reduction-v2-averaged-jitter", "Farey v2 identity mismatch")
    afari = load_json(INPUTS["afari_artifact"][0])
    require(afari.get("f4f_target", {}).get("epistemic_status") == "CONJECTURED", "F4F target status mismatch")
    cfari = load_json(INPUTS["cfari_artifact"][0])
    require("CFARI" in cfari.get("claim_boundary", ""), "CFARI context mismatch")
    prior = load_json(INPUTS["f4f_mellin_artifact"][0])
    require(prior.get("absolute_wiener_no_go", {}).get("epistemic_status") == "PROVED", "prior absolute-Wiener no-go mismatch")
    return {
        "base_energy": base["energy_band"],
        "base_energy_definition": base["energy_definition"],
        "base_set": base["set"],
        "prior_f4f_status": "CONJECTURED",
        "actual_labels": "coprime ordered (r,s) in the frozen Q-shell with true |theta|<=3 jitter",
    }


def exact_rows() -> dict[str, Any]:
    module = load_conventions()
    checked = module.verify_all()
    rows = checked["exact_rows"]
    require(rows["period_strict_lower"] == 24, "period lower bound mismatch")
    require(rows["period_strict_upper"] == 38, "period upper bound mismatch")
    require(rows["energy_existence_upper_constant"] == 2**16, "random-energy existence constant mismatch")
    require(rows["close_pair_q_exponent"] == Fraction(103, 100), "close-pair exponent mismatch")
    require(rows["local_fourth_moment_lower_constant"] == Fraction(1, 20), "local fourth-moment lower constant mismatch")
    return {"scales_at_v8": json_exact(checked["scales"]), "actual_anchor_at_v8": json_exact(checked["actual_anchor"]), "constants": json_exact(rows)}


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen = frozen_inputs()
    context = validate_context()
    rows = exact_rows()
    return {
        "artifact_id": "cycle-7-crr-f4f-signed-projection-extremizer-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_SIGNED_F4F_PROJECTION_AND_ENERGY_ONLY_NO_GO_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "This artifact proves the exact actual-Farey signed pair-sum PSD form, the norm-one unrestricted Fourier-projection boundary including finite homogeneous continuous linear diagnostics, an equal-weight actual-cell phase-lattice extremizer satisfying the CRR cardinality/separation/energy band, and a one-cell inverse lattice lemma. It proves neither Base-admissibility of that extremizer, F4F_eta on Base, AFARI, CFARI, CRR-U, a Base-compatible counterexample, a cubic estimate, a density gain, a short-interval theorem, a full-method saturation theorem, nor an L-function result.",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "research_stage_review_policy": {"lightweight_checks": "exact Fourier/projection algebra, integer scale and random-subset constants, source-artifact checks, replay, and tamper rejection", "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION"},
        "source_context": context,
        "signed_pair_sum_form": {"epistemic_status": "PROVED", "statement": "For nu_W=(sum_(t in W)delta_t)*(sum_(t in W)delta_t), I4_log(W)=<nu_W,K_v nu_W>=integral_(log U_v)|nu_hat_W(x)|^2dx, with K_v(s,s')=J_H(s-s')S_Q(s-s').", "labels": "K_v retains every actual coprime ordered Farey label and true bounded logarithmic jitter", "positivity": "K_v is positive semidefinite despite the signed S_Q expansion."},
        "ambient_projection_no_go": {"epistemic_status": "PROVED", "normalized_operator": "P_(E_v)=(2*pi)^(-1)K_v=F^(-1)M_(1_(log U_v))F on unrestricted L^2(R)", "spectrum": "P_(E_v) is an orthogonal projection with norm exactly one and infinite-dimensional 1-eigenspace.", "finite_diagnostics": "Any finite collection of homogeneous continuous linear functionals leaves a nonzero 1-eigenvector in their common kernel.", "scope": "This is an ambient L^2/finite-rank no-go; atomic self-convolution profiles are a stricter nonlinear class."},
        "phase_lattice_extremizer": {"epistemic_status": "PROVED", "quantifier": "every sufficiently large even v", "actual_label": "r_Q=Q+1, s_Q=5Q/4+1, alpha_Q=r_Q/s_Q, gcd(r_Q,s_Q)=1", "row_set": "W_Q={P_Q a:a in A}, P_Q=2*pi/log(s_Q/r_Q), with A obtained by the sealed random-subset/deletion argument", "properties": "W_Q subset [0,H], |W_Q|=R, W_Q is H^(1/100)-separated, and v^(20-delta(v))<=E(W_Q)<=v^(20+delta(v)) eventually", "local_lower": "integral_(U_v)|R_(W_Q)(u)|^4du>=(1/20)v^20", "conclusion": "F4F_eta fails on the energy/spaced/cardinality class for every fixed eta>0 along an unbounded even sequence; this is not a disproof on the full Base class."},
        "one_cell_inverse": {"epistemic_status": "PROVED", "statement": "If |R_W(alpha)|>=(1-epsilon)|W|, then for 0<lambda<=pi at most pi^2*epsilon*|W|/(2lambda^2) rows lie angular distance more than lambda from one phase-lattice coset modulo 2*pi/|log(alpha)|.", "endpoint": "The phase-lattice extremizer has epsilon=0 at its actual alpha_Q."},
        "remaining_gate": {"epistemic_status": "CONJECTURED", "statement": "A signed F4F advance must exploit nonlinear equal-weight atomic self-convolution realizability and/or the common Base coefficient vector to exclude or control the phase-lattice profiles; generic PSD and finite-dimensional spectral data cannot do so."},
        "crr_u_effect": {"epistemic_status": "PROVED", "statement": "CRR-U remains open. The result sharpens only the energy-only signed F4F boundary."},
        "exact_replay": rows,
        "replay": {"write_command": "python3 proof/build_cycle_7_crr_f4f_signed_projection_extremizer_v1.py --write", "check_command": "python3 proof/build_cycle_7_crr_f4f_signed_projection_extremizer_v1.py --check", "test_command": "python3 -m unittest tests/test_cycle_7_crr_f4f_signed_projection_extremizer_v1.py"},
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
        require(not OUTPUT.exists(), "refusing to overwrite signed F4F projection/extremizer v1 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "signed F4F projection/extremizer v1 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "signed F4F projection/extremizer v1 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
