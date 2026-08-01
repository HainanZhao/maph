#!/usr/bin/env python3
"""Seal the Cycle 7 CRR phase-lattice Base-saturation reduction v1."""
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
OUTPUT = ROOT / "artifacts/cycle-7-crr-phase-lattice-base-saturation-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "crr_v2_artifact": (ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v2.json", "e26be797539eabe53ee765b7067d1c99fe4d440035e27785cf38aa64bc2fc84e"),
    "spectral_phase_lift_artifact": (ROOT / "artifacts/cycle-6-crr-spectral-phase-lift-v1.json", "165aff6e15a9c2177b1a69d7a2ce32ff9ba3b2d651aba6683d9f5ecca21403e4"),
    "phase_flatness_artifact": (ROOT / "artifacts/cycle-6-crr-phase-flatness-v1.json", "28990f2c703e0f8bfba8e25fb40ecc3d8231392e564653a01fcf5330a52b83ff"),
    "cfari_artifact": (ROOT / "artifacts/cycle-6-crr-cfari-phase-equivalence-v1.json", "00ca4e7f794a06d797b24543d174d86ef6d8a3f99a068d14bb693ce894f16dad"),
    "signed_extremizer_artifact": (ROOT / "artifacts/cycle-7-crr-f4f-signed-projection-extremizer-v1.json", "9616ef55eec03f2f11ba2b625fd9e8cbd3c4ad581900a8a441ce9ed130d05796"),
    "document": (ROOT / "docs/cycle-7-crr-phase-lattice-base-saturation-v1.md", "f6203aa929c354efcd65bce00f5b33864f2ebaccce99af6bf3770298fd364f81"),
    "conventions": (ROOT / "conventions/crr_phase_lattice_base_saturation_v1.py", "02d64afcb324858982042cd946ab66111d489eab65b45a9057ac57034e6ec8ef"),
    "tests": (ROOT / "tests/test_cycle_7_crr_phase_lattice_base_saturation_v1.py", "614f84fce97194c14ac10b3d2f938a69a3b8c4006f0949e2b4446732720693f6"),
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
    require(runtime == EXPECTED_RUNTIME, "CRR phase-lattice Base-saturation v1 requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("crr_phase_lattice_base_saturation_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load phase-lattice Base-saturation conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_context() -> dict[str, str]:
    crr = load_json(INPUTS["crr_v2_artifact"][0])
    require(crr.get("artifact_id") == "cycle-4-p1r-crr-u-formalization-v2", "CRR v2 identity mismatch")
    base = crr.get("witness_schema", {}).get("base", {})
    require(base.get("cardinality") == "v^(8-delta(v)) <= |W| <= v^(8+delta(v))", "Base cardinality convention mismatch")
    require(base.get("pointwise") == "|D_v(t)| >= v^(7-delta(v)) for every t in W", "Base pointwise convention mismatch")
    require(base.get("set") == "finite W subset [0,H], H^(1/100)-separated", "Base set convention mismatch")
    phase_lift = load_json(INPUTS["spectral_phase_lift_artifact"][0])
    require(phase_lift.get("artifact_id") == "cycle-6-crr-spectral-phase-lift-v1", "spectral phase-lift identity mismatch")
    flatness = load_json(INPUTS["phase_flatness_artifact"][0])
    require(flatness.get("phase_flatness_lemma", {}).get("epistemic_status") == "PROVED", "phase-flatness context mismatch")
    cfari = load_json(INPUTS["cfari_artifact"][0])
    require(cfari.get("phase_scale_enclosure", {}).get("epistemic_status") == "PROVED", "sampled mean-value context mismatch")
    extremizer = load_json(INPUTS["signed_extremizer_artifact"][0])
    require(extremizer.get("phase_lattice_extremizer", {}).get("epistemic_status") == "PROVED", "signed-extremizer context mismatch")
    return {
        "base_cardinality": base["cardinality"],
        "base_pointwise": base["pointwise"],
        "base_set": base["set"],
        "phase_lift": "exact capped max-min program on one common W",
        "mean_value": "lambda<=C(H+L)(1+log(2L)) for the separated actual matrix",
        "signed_extremizer_boundary": "energy/cardinality/separation do not supply Base coefficients",
    }


def exact_rows() -> dict[str, Any]:
    module = load_conventions()
    checked = module.verify_all()
    rows = checked["exact_rows"]
    require(rows["max_exact_alias_class_size"] == 4, "alias-class bound mismatch")
    require(rows["beta_lower"] == Fraction(6, 5), "anchor beta lower bound mismatch")
    require(rows["base_product_main_exponent"] == 12, "Base product exponent mismatch")
    require(rows["base_product_delta_loss"] == 3, "Base product delta loss mismatch")
    return {"scales_at_v8": json_exact(checked["scales"]), "actual_anchor_at_v8": json_exact(checked["actual_anchor"]), "constants": json_exact(rows)}


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen = frozen_inputs()
    context = validate_context()
    rows = exact_rows()
    return {
        "artifact_id": "cycle-7-crr-phase-lattice-base-saturation-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_PHASE_LATTICE_BASE_SATURATION_REDUCTION_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "This artifact proves an exact actual-rational phase-alias quotient, constant alias-class bounds, and the exact capped Base-saturation functional for phase lattices. It proves neither a fixed-power distinct-phase norm/efficiency bound, a full phase-lattice Base exclusion, a Base-compatible phase-lattice witness, RationalMass, PositiveCubic, F4F, AFARI, CFARI, CRR-U, a density gain, a short-interval theorem, a full-method saturation theorem, nor an L-function result.",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "research_stage_review_policy": {"lightweight_checks": "exact phase-alias algebra, cap/scale bookkeeping, source-artifact checks, replay, and tamper rejection", "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION"},
        "source_context": context,
        "phase_lattice_rephasing": {"epistemic_status": "PROVED", "statement": "For W_(tau_0,A)={tau_0+P_Q a}, b_n -> b_n*n^(i*tau_0) preserves the cap and reduces the common coefficient problem exactly to D_b(P_Q a)=sum_n w_n b_n z_n^a."},
        "exact_alias_quotient": {"epistemic_status": "PROVED", "alias_relation": "z_n=z_m iff n/m=(s_Q/r_Q)^k for some integer k", "class_bound": "Every exact alias class in I_L has at most four columns because (6/5)^4>2.", "capped_program": "Gamma_(P_Q,A)=max_(|q_C|<=omega_C)min_(a in A)|sum_C q_C z_C^a|, omega_C=sum_(n in C)w_n", "operator_bound": "M_(A,P)=Mbar_(A,P)B and lambda_(P,A)<=4||Mbar_(A,P)||_op^2", "conclusion": "Exact rational aliases offer only constant factors; the unresolved problem is the distinct-phase quotient."},
        "base_saturation_efficiency": {"epistemic_status": "PROVED", "definition": "Xi_(P,A)=m*Gamma_(P,A)^2/(N_L*lambda_(P,A)), where m=|A| and N_L=L-1", "range": "0<=Xi_(P,A)<=1", "exact_identity": "Gamma_(P,A)^2=N_L*lambda_(P,A)*Xi_(P,A)/m", "base_equivalence": "The common capped Base pointwise condition is equivalent to lambda_(P,A)*Xi_(P,A)>=m*v^(14-2delta(v))/N_L."},
        "base_necessary_saturation": {"epistemic_status": "PROVED", "lower_product": "Base cardinality plus pointwise values force lambda_(P,A)*Xi_(P,A)>=v^(12-3delta(v)).", "mean_value_upper": "lambda_(P,A)<=C(H+L)(1+log(2L))<=2C v^12(1+log(2L)) for a phase lattice in [0,H].", "consequences": "Every Base-compatible phase lattice has lambda_(P,A)>=v^(12-3delta(v)) and Xi_(P,A)>=v^(-3delta(v))/(2C(1+log(2L)))=v^(-o(1)).", "fixed_power_exclusion": "For any fixed kappa>0, lambda<=v^(12-kappa) or Xi<=v^(-kappa) eventually excludes Base on that phase lattice."},
        "leading_vector_link": {"epistemic_status": "PROVED", "statement": "The sealed phase-rounded leading-vector certificate gives Xi_(P,A)>=rho*phi^2; the phase-flatness gate gives Xi_(P,A)>=rho*((1-kappa_0)^2/(1+kappa_0^2))*mu_top when chi_ph<=kappa_0<1."},
        "remaining_gate": {"epistemic_status": "CONJECTURED", "statement": "Prove a fixed-power bound for the distinct-phase quotient norm or Xi to exclude Base, or construct one common capped vector satisfying the exact product condition together with the row-set/energy conditions to witness Base compatibility."},
        "crr_u_effect": {"epistemic_status": "PROVED", "statement": "CRR-U remains open. This is a sharp phase-lattice/Base coupling reduction only."},
        "exact_replay": rows,
        "replay": {"write_command": "python3 proof/build_cycle_7_crr_phase_lattice_base_saturation_v1.py --write", "check_command": "python3 proof/build_cycle_7_crr_phase_lattice_base_saturation_v1.py --check", "test_command": "python3 -m unittest tests/test_cycle_7_crr_phase_lattice_base_saturation_v1.py"},
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
        require(not OUTPUT.exists(), "refusing to overwrite phase-lattice Base-saturation v1 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "phase-lattice Base-saturation v1 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "phase-lattice Base-saturation v1 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
