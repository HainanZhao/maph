#!/usr/bin/env python3
"""Seal energy-only restricted-log-Farey F4F sharpness, version 1."""
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
OUTPUT = ROOT / "artifacts/cycle-7-crr-energy-only-f4f-sharpness-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "crr_v2_artifact": (ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v2.json", "e26be797539eabe53ee765b7067d1c99fe4d440035e27785cf38aa64bc2fc84e"),
    "farey_v2_artifact": (ROOT / "artifacts/cycle-5-crr-farey-log-gram-reduction-v2-averaged-jitter.json", "ce59b777ec02769168d9dc330658a0ab1d46b05cdb7ac5dc8115e248d85f8ce8"),
    "afari_coupling_artifact": (ROOT / "artifacts/cycle-6-crr-afari-coefficient-coupling-v1.json", "a9b142f8fd22e4fe9ebd4857af4eb7e764aa20ea379170930f6446231e663266"),
    "signed_extremizer_artifact": (ROOT / "artifacts/cycle-7-crr-f4f-signed-projection-extremizer-v1.json", "9616ef55eec03f2f11ba2b625fd9e8cbd3c4ad581900a8a441ce9ed130d05796"),
    "signed_extremizer_test_correction": (ROOT / "artifacts/cycle-7-crr-f4f-signed-projection-extremizer-v1-test-correction.json", "e7ba78e6f17de27862f69ca6cc61ada2c3724477d0e6757c2f98982719dbf638"),
    "phase_lattice_base_artifact": (ROOT / "artifacts/cycle-7-crr-phase-lattice-base-saturation-v1.json", "3207a7764470d5512d20778e739e0e0bdc31535c0b2ac68b8366707304678534"),
    "gm_source_tex": (ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex", "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
    "conventions": (ROOT / "conventions/crr_energy_only_f4f_sharpness_v1.py", ""),
    "document": (ROOT / "docs/cycle-7-crr-energy-only-f4f-sharpness-v1.md", ""),
    "tests": (ROOT / "tests/test_cycle_7_crr_energy_only_f4f_sharpness_v1.py", ""),
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


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def load_conventions():
    path = INPUTS["conventions"][0]
    spec = importlib.util.spec_from_file_location("crr_energy_only_f4f_sharpness_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load energy-only F4F sharpness conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def runtime_metadata() -> dict[str, Any]:
    result = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(result == EXPECTED_RUNTIME, "energy-only F4F sharpness v1 requires non-optimized CPython 3.12.3")
    return result


def frozen_inputs() -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        if expected:
            require(actual == expected, f"frozen input hash mismatch: {label}")
        result[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    return result


def validate_context() -> dict[str, str]:
    crr = load_json(INPUTS["crr_v2_artifact"][0])
    base = crr.get("witness_schema", {}).get("base", {})
    require(base.get("set") == "finite W subset [0,H], H^(1/100)-separated", "Base set convention mismatch")
    require(base.get("cardinality") == "v^(8-delta(v)) <= |W| <= v^(8+delta(v))", "Base cardinality convention mismatch")
    require(base.get("energy_band") == "v^(20-delta(v)) <= E(W) <= v^(20+delta(v))", "Base energy convention mismatch")
    require(base.get("energy_definition") == "ordered quadruples in W^4 with |t1+t2-t3-t4|<=1", "Base energy definition mismatch")
    farey = load_json(INPUTS["farey_v2_artifact"][0])
    require(farey.get("averaged_actual_farey_bundle", {}).get("actual_nodes") == "coprime Q<=r,s<2Q, 3/4<=r/s<=5/4; no generic logarithmic-alias substitution", "actual Farey labels mismatch")
    require(farey.get("averaged_actual_farey_bundle", {}).get("labeled_identity") == "C_theta(sk,rk)=R_W((r/s)*exp(theta/H))", "actual Farey identity mismatch")
    afari = load_json(INPUTS["afari_coupling_artifact"][0])
    upper = afari.get("energy_restricted_upper", {})
    require(upper.get("epistemic_status") == "PROVED", "energy-restricted upper status mismatch")
    require(upper.get("source_bound") == "integral_(1/2)^(3/2)|R_W(u)|^4du<=H^(o(1))*E(W)", "RL4 predecessor bound mismatch")
    signed = load_json(INPUTS["signed_extremizer_artifact"][0])
    extremizer = signed.get("phase_lattice_extremizer", {})
    require(extremizer.get("epistemic_status") == "PROVED", "phase-lattice extremizer status mismatch")
    require(extremizer.get("quantifier") == "every sufficiently large even v", "phase-lattice quantifier mismatch")
    require(extremizer.get("local_lower") == "integral_(U_v)|R_(W_Q)(u)|^4du>=(1/20)v^20", "phase-lattice lower mismatch")
    correction = load_json(INPUTS["signed_extremizer_test_correction"][0])
    require(correction.get("preserved_v1", {}).get("artifact_sha256") == INPUTS["signed_extremizer_artifact"][1], "signed-extremizer correction link mismatch")
    phase = load_json(INPUTS["phase_lattice_base_artifact"][0])
    require(phase.get("remaining_gate", {}).get("epistemic_status") == "CONJECTURED", "common-coefficient gate status mismatch")
    require("one common capped vector" in phase.get("remaining_gate", {}).get("statement", ""), "common-coefficient gate label mismatch")
    source = INPUTS["gm_source_tex"][0].read_text(encoding="utf-8")
    require(r"\begin{lmm}[$L^4$ bound] \label{RL4}" in source, "GM RL4 source anchor mismatch")
    return {
        "energy_only_base_subset": "separation, cardinality, and energy only; no coefficient/pointwise Base antecedent",
        "actual_farey_labels": farey["averaged_actual_farey_bundle"]["actual_nodes"],
        "global_rl4": upper["source_bound"],
        "phase_lattice_lower": extremizer["local_lower"],
        "common_coefficient_gate": phase["remaining_gate"]["statement"],
    }


def exact_rows() -> dict[str, Any]:
    module = load_conventions()
    checked = module.verify_all()
    require(checked["central_exponent"] == 20, "central exponent mismatch")
    require(checked["log_lower_constant"] == Fraction(1, 30), "log lower constant mismatch")
    require("limsup" in checked["sharpness_rows"]["limsup"], "sharpness limsup row mismatch")
    return json_exact(checked)


def seal() -> dict[str, Any]:
    module = load_conventions()
    return {
        "artifact_id": "cycle-7-crr-energy-only-f4f-sharpness-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ENERGY_ONLY_RESTRICTED_LOG_FAREY_F4F_CENTRAL_EXPONENT_SHARPNESS_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "This artifact proves central exponent 20 is sharp for the explicitly defined energy-only restricted-log-Farey fourth-moment architecture. It does not prove Base-admissibility of the phase lattice, a common capped coefficient/pointwise Base condition, RationalMass, PositiveCubic, F4F_eta on Base, AFARI, CFARI, CRR-U, a density gain, a short-interval theorem, a full-method saturation theorem, or an L-function result.",
        "runtime": runtime_metadata(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "research_stage_review_policy": {
            "lightweight_checks": "pinned predecessor claims, exact scale/log-measure bookkeeping, source-anchor checks, replay, and tamper rejection",
            "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION",
        },
        "context": validate_context(),
        "architecture": {
            "epistemic_status": "PROVED",
            "definition": "EO_v consists only of actual-Farey row sets W satisfying frozen [0,H] containment, H^(1/100) separation, cardinality band, and tolerance-one energy band; J_v(W)=integral_(log U_v)|sum_t exp(i t x)|^4dx.",
            "actuality": "U_v uses the actual reduced coprime Q-shell and true -3<=theta<=3 logarithmic jitter; no generic log-packet or alias union is substituted.",
            "excluded": "No common coefficient b, pointwise Base value, RationalMass, or PositiveCubic condition is present.",
        },
        "global_upper": {
            "epistemic_status": "PROVED",
            "predecessor": "checked GM RL4 as frozen in cycle-6-crr-afari-coefficient-coupling-v1",
            "statement": "For every W in EO_v, J_v(W)<=2H^(o(1))E(W)<=v^(20+o(1)).",
            "hypotheses_checked": "W is H^(1/100)-separated in [0,H], and U_v subset [1/2,3/2].",
        },
        "actual_phase_lattice_lower": {
            "epistemic_status": "PROVED",
            "predecessor": "cycle-7-crr-f4f-signed-projection-extremizer-v1 with its immutable test correction",
            "quantifier": "every sufficiently large even v",
            "actual_label": "r_Q=Q+1, s_Q=5Q/4+1, alpha_Q=r_Q/s_Q, P_Q=2*pi/log(s_Q/r_Q)",
            "row_set": "W_v={P_Q a:a in A} lies in EO_v by the pinned random-subset/deletion construction.",
            "du_lower": "integral_(U_v)|R_(W_v)(u)|^4du>=(1/20)v^20",
            "log_lower": "J_v(W_v)>=(1/30)v^20, using du/u>=(2/3)du on U_v.",
        },
        "sharpness_theorem": {
            "epistemic_status": "PROVED",
            "supremum": "S_v=sup_(W in EO_v)J_v(W)",
            "statement": "limsup_(v->infinity, v even) log(S_v)/log(v)=20.",
            "fixed_power_consequence": "For every fixed eta>0, EO-F4F_eta: J_v(W)<=v^(20-eta) for all sufficiently large v and W in EO_v is false.",
            "scope": "This is sharpness only for the energy-only architecture, not for the full Base class.",
        },
        "full_base_common_coefficient_boundary": {
            "epistemic_status": "CONJECTURED",
            "statement": "The full Base/common-coefficient Guth--Maynard problem remains open. The phase-lattice predecessor leaves open a fixed-power distinct-phase quotient/efficiency bound or construction of one common capped vector satisfying its exact Base product condition.",
            "non_implication": "Energy-only phase-lattice saturation neither constructs a Base-admissible coefficient nor excludes one.",
        },
        "exact_replay": exact_rows(),
        "falsifiers": {
            "upper": "Failure of the pinned RL4 source bound under the checked separation/interval hypotheses refutes the global-upper half.",
            "lower": "Failure of the actual-label phase-lattice EO_v membership or its true-jitter lower bound refutes the lower half.",
            "normalization": "Failure of dx=du/u or of the [1/2,3/2] measure comparison refutes the conversion to J_v.",
            "scope": "A Base exclusion or Base-compatible coefficient construction affects the open common-coefficient gate, not this energy-only theorem.",
        },
        "replay": {
            "write_command": "python3 proof/build_cycle_7_crr_energy_only_f4f_sharpness_v1.py --write",
            "check_command": "python3 proof/build_cycle_7_crr_energy_only_f4f_sharpness_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_7_crr_energy_only_f4f_sharpness_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite energy-only F4F sharpness artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "energy-only F4F sharpness artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "energy-only F4F sharpness artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
