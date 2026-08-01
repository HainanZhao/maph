#!/usr/bin/env python3
"""Seal the Objective-2 EO-LF4 saturation completion audit v1."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-8-crr-objective2-energy-only-saturation-audit-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "crr_v2_artifact": (ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v2.json", "e26be797539eabe53ee765b7067d1c99fe4d440035e27785cf38aa64bc2fc84e"),
    "afari_artifact": (ROOT / "artifacts/cycle-6-crr-afari-coefficient-coupling-v1.json", "a9b142f8fd22e4fe9ebd4857af4eb7e764aa20ea379170930f6446231e663266"),
    "afari_test_correction": (ROOT / "artifacts/cycle-6-crr-afari-coefficient-coupling-v1-test-correction.json", "31da90127f321d91bf7b6a2d4373ae1bbff638d7a4fcc4cc9a0fb6ae1c788815"),
    "f4f_mellin_artifact": (ROOT / "artifacts/cycle-7-crr-f4f-mellin-farey-reduction-v1.json", "18fefc631e63a622cf780c927cd6aad185d5cc310f9e908c09ccb9de1fefc7a4"),
    "signed_extremizer_artifact": (ROOT / "artifacts/cycle-7-crr-f4f-signed-projection-extremizer-v1.json", "9616ef55eec03f2f11ba2b625fd9e8cbd3c4ad581900a8a441ce9ed130d05796"),
    "signed_extremizer_test_correction": (ROOT / "artifacts/cycle-7-crr-f4f-signed-projection-extremizer-v1-test-correction.json", "e7ba78e6f17de27862f69ca6cc61ada2c3724477d0e6757c2f98982719dbf638"),
    "phase_lattice_artifact": (ROOT / "artifacts/cycle-7-crr-phase-lattice-base-saturation-v1.json", "3207a7764470d5512d20778e739e0e0bdc31535c0b2ac68b8366707304678534"),
    "phase_lattice_test_correction": (ROOT / "artifacts/cycle-7-crr-phase-lattice-base-saturation-v1-test-correction.json", "9ad5dac78854c26ada7034a87eda981eca4700bdbf1e85dc42761e44fe706843"),
    "gm_source_tex": (ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex", "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
    "document": (ROOT / "docs/cycle-8-crr-objective-2-energy-only-saturation-audit-v1.md", "c5d70e76808f62589290f5098d813c933d177c0eb714acd756c6ff2bfd3c8f34"),
    "conventions": (ROOT / "conventions/crr_objective2_energy_only_saturation_v1.py", "7d435f56ca1a9ce7ec9b97760fb62bc11f1944e470e669575a5a0089e4de0ac1"),
    "tests": (ROOT / "tests/test_cycle_8_crr_objective2_energy_only_saturation_audit_v1.py", "18a9f8b9943f6e2aaf1184382fa62d17512a22e7f532f4374636877d1fd0dd26"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_runtime() -> dict[str, Any]:
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "Objective-2 EO-LF4 saturation audit requires non-optimized CPython 3.12.3")
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
    spec = importlib.util.spec_from_file_location("crr_objective2_energy_only_saturation_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Objective-2 EO-LF4 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_context() -> dict[str, str]:
    source = INPUTS["gm_source_tex"][0].read_text(encoding="utf-8")
    for fragment in ("\\begin{lmm}[$L^4$ bound] \\label{RL4}", "\\int_{v \\asymp 1} |R(v)|^4 dv \\lessapprox E(W)", "$A \\lessapprox B$ to mean that for any $\\epsilon > 0$, there is a constant"):
        require(fragment in source, f"GM RL4 source fragment missing: {fragment}")

    crr = load_json(INPUTS["crr_v2_artifact"][0])
    require(crr.get("artifact_id") == "cycle-4-p1r-crr-u-formalization-v2", "CRR v2 identity mismatch")
    base = crr.get("witness_schema", {}).get("base", {})
    require(base.get("set") == "finite W subset [0,H], H^(1/100)-separated", "CRR set convention mismatch")
    require(base.get("energy_band") == "v^(20-delta(v)) <= E(W) <= v^(20+delta(v))", "CRR energy-band convention mismatch")
    require(base.get("energy_definition") == "ordered quadruples in W^4 with |t1+t2-t3-t4|<=1", "CRR energy definition mismatch")

    afari = load_json(INPUTS["afari_artifact"][0])
    require(afari.get("energy_restricted_upper", {}).get("source_bound") == "integral_(1/2)^(3/2)|R_W(u)|^4du<=H^(o(1))*E(W)", "RL4 transfer context mismatch")
    require(afari.get("f4f_target", {}).get("epistemic_status") == "CONJECTURED", "Base F4F status mismatch")
    afari_correction = load_json(INPUTS["afari_test_correction"][0])
    require(afari_correction.get("correction", {}).get("mathematical_change") == "none", "AFARI correction scope mismatch")

    mellin = load_json(INPUTS["f4f_mellin_artifact"][0])
    require(mellin.get("absolute_wiener_no_go", {}).get("epistemic_status") == "PROVED", "absolute-Wiener context mismatch")
    signed = load_json(INPUTS["signed_extremizer_artifact"][0])
    extremizer = signed.get("phase_lattice_extremizer", {})
    require(extremizer.get("epistemic_status") == "PROVED", "phase-lattice extremizer status mismatch")
    require("(1/20)v^20" in extremizer.get("local_lower", ""), "phase-lattice local lower mismatch")
    require("not a disproof on the full Base class" in extremizer.get("conclusion", ""), "phase-lattice Base boundary mismatch")
    signed_correction = load_json(INPUTS["signed_extremizer_test_correction"][0])
    require(signed_correction.get("correction", {}).get("mathematical_change") == "none", "signed-extremizer correction scope mismatch")

    phase = load_json(INPUTS["phase_lattice_artifact"][0])
    bridge = phase.get("base_saturation_efficiency", {})
    require(bridge.get("epistemic_status") == "PROVED", "phase-lattice bridge status mismatch")
    require("lambda_(P,A)*Xi_(P,A)" in bridge.get("base_equivalence", ""), "exact Base bridge mismatch")
    require(phase.get("remaining_gate", {}).get("epistemic_status") == "CONJECTURED", "phase-lattice gate status mismatch")
    phase_correction = load_json(INPUTS["phase_lattice_test_correction"][0])
    require(phase_correction.get("correction", {}).get("mathematical_change") == "none", "phase-lattice correction scope mismatch")

    return {
        "source_rl4": "LargevaluesDirichlet17.tex lines 1266-1302; lessapprox is defined at lines 288-291",
        "critical_class": "W subset [0,H], |W|=R, H^(1/100)-separated, full v^(20+/-delta) energy band",
        "actual_geometry": "coprime reduced Farey labels with true |theta|<=3 logarithmic jitter",
        "energy_only_extremizer": "every sufficiently large even v has a phase-lattice W with I_v(W)>=(1/20)v^20",
        "base_boundary": "the energy-only W is not shown Base-admissible",
        "exact_missing_bridge": "Gamma>=V_- iff lambda*Xi>=m*V_-^2/(L-1)",
    }


def exact_rows() -> dict[str, Any]:
    module = load_conventions()
    checked = module.verify_all()
    rows = checked["extremizer_rows"]
    require(rows["central_exponent"] == 20, "sharp central exponent mismatch")
    require(str(rows["local_lower_constant"]) == "1/20", "local extremizer constant mismatch")
    allocation = module.epsilon_absorption(1.0)
    require(allocation["source_eta"] == 1.0 / 24.0, "epsilon allocation mismatch")
    require(allocation["H_to_v_exponent_loss"] == 0.5, "H-to-v conversion mismatch")
    require(allocation["delta_cap"] == 0.5, "delta allocation mismatch")
    return {
        "scales_at_v8": checked["scales"],
        "extremizer_rows_at_v8": {key: str(value) for key, value in rows.items()},
        "base_bridge_at_v8": checked["base_bridge"],
        "epsilon_absorption_at_1": allocation,
    }


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen = frozen_inputs()
    context = validate_context()
    rows = exact_rows()
    return {
        "artifact_id": "cycle-8-crr-objective2-energy-only-saturation-audit-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_OBJECTIVE2_EO_LF4_SCOPED_SATURATION_AUDIT_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "This artifact proves that Objective 2 is satisfied only for the explicitly defined EO-LF4 actual-log-Farey energy-only Guth--Maynard subarchitecture. It does not prove full-method or full-CRR saturation, Base F4F, AFARI, CFARI, CRR-U, a density gain, a short-interval theorem, or an L-function result.",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "research_stage_review_policy": {"lightweight_checks": "source hypothesis anchor, sealed-artifact reconciliation, exact scale/epsilon algebra, corrected-replay selection, and tamper rejection", "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION"},
        "source_context": context,
        "objective_2_assessment": {
            "epistemic_status": "PROVED",
            "status": "SATISFIED_FOR_EO_LF4_SCOPED_GM_SUBARCHITECTURE",
            "reason": "EO-LF4 is a precisely defined actual-log-Farey subarchitecture of the critical Guth--Maynard CRR route, and the same class/function have a uniform exponent-20 upper bound and an actual-label extremizing sequence at exponent 20.",
            "full_method_boundary": "This is not a full-method saturation theorem: the common Base coefficient, RationalMass, PositiveCubic, and all-cell ray-bundle conditions are excluded from EO-LF4.",
            "plan_interpretation": "It may discharge PLAN Objective 2 only under its literal precisely-defined-architecture alternative; it must never be reported as a full Guth--Maynard saturation theorem.",
        },
        "eolf4_architecture": {
            "epistemic_status": "PROVED",
            "name": "EO-LF4 = energy-only actual-log-Farey local fourth-moment architecture",
            "scales": "H=v^12, L=v^10, Q=v^4, R=v^8=Q^2, delta(v)=1/sqrt(log v)",
            "row_class": "finite W subset [0,H], |W|=R, H^(1/100)-separated, v^(20-delta(v))<=E(W)<=v^(20+delta(v))",
            "energy": "E(W)=#{(t1,t2,t3,t4) in W^4: |t1+t2-t3-t4|<=1}",
            "actual_union": "U_v=union_(coprime Q<=r,s<2Q, 3/4<=r/s<=5/4){(r/s)exp(theta/H): |theta|<=3}",
            "functional": "I_v(W)=integral_(U_v)|sum_(t in W)u^(it)|^4du",
            "allowed_upper_step": "checked GM raw-R Lemma RL4 followed by U_v subset [1/2,3/2]",
            "excluded_inputs": "one common coefficient b, Base pointwise values, RationalMass, PositiveCubic, ray-bundle aggregation, and any separately selected jitter",
        },
        "sharp_eolf4_theorem": {
            "epistemic_status": "PROVED",
            "upper_quantifier": "For every fixed epsilon>0, there are C_epsilon and v_epsilon such that for every even v>=v_epsilon and every EO-LF4-admissible W, I_v(W)<=C_epsilon*v^(20+epsilon).",
            "upper_derivation": "RL4 gives integral_(1/2)^(3/2)|R_W|^4<=C_eta H^eta E(W); choose eta=epsilon/24, so H^eta=v^(epsilon/2), and eventually delta(v)<=epsilon/2.",
            "lower_quantifier": "For every sufficiently large even v, there exists an EO-LF4-admissible equal-weight actual-Farey phase-lattice W_v.",
            "lower_bound": "I_v(W_v)>=(1/20)*R^4/H=(1/20)*Q^5=(1/20)*v^20.",
            "extremizer": "W_v=P_Q A with P_Q=2*pi/log((5Q/4+1)/(Q+1)); A is the sealed random-subset/deletion integer set and alpha_Q=(Q+1)/(5Q/4+1) is an actual reduced Farey label.",
            "sharpness": "If M_v=sup_(W in EO-LF4) I_v(W), then limsup_(v->infinity, v even) log(M_v)/log(v)=20. Hence no fixed eta>0 gives I_v(W)<=v^(20-eta) uniformly on EO-LF4.",
        },
        "why_not_scalar_only": {
            "epistemic_status": "PROVED",
            "statement": "The lower side is realized by an equal-weight atomic self-convolution on an actual Farey cell, not by the earlier scalar profile calibration. It therefore supplies an extremizing sequence in the nonlinear row-set class.",
        },
        "bundle_boundary": {
            "epistemic_status": "PROVED",
            "statement": "This theorem does not establish sharp exponent 26 for the ray-weighted bundle A_v(W). The extremizer is coherent on one actual cell and does not supply the all-cell RationalMass lower at v^26.",
        },
        "missing_base_full_crr_gate": {
            "epistemic_status": "CONJECTURED",
            "name": "PL-BASE-BRIDGE",
            "exact_equivalence": "For W_(P,A)=P*A, Gamma_(P,A)>=V_-=v^(7-delta(v)) iff lambda_(P,A)*Xi_(P,A)>=|A|*v^(14-2delta(v))/(L-1).",
            "missing_fact": "Neither a capped coefficient vector attaining this condition nor a fixed-power exclusion for the EO-LF4 phase-lattice extremizers is sealed.",
            "full_crr_additions": "Even a Base lift would still require RationalMass and PositiveCubic for the same common pair (b,W) before it could be a full CRR-compatible extremizer.",
            "allowed_resolutions": "Construct the common capped Base vector, or prove an actual distinct-phase quotient/Xi upper bound excluding it; retain all conclusions at their resulting scope.",
        },
        "explicit_exclusions": {
            "epistemic_status": "PROVED",
            "items": [
                "no Base-admissibility or disproof of Base-restricted F4F_eta",
                "no RationalMass, PositiveCubic, AFARI, CFARI, or CRR-U conclusion",
                "no sharp v^26 ray-bundle extremizer",
                "no full Guth--Maynard saturation theorem",
                "no zero-density, short-interval, or L-function theorem",
            ],
        },
        "falsifiers": {
            "epistemic_status": "PROVED",
            "eolf4": "Failure of RL4 applicability, the actual-cell/jitter inclusion, the phase-lattice energy/separation/cardinality construction, or the v^20 lower invalidates the scoped theorem.",
            "scope": "A proof of PL-BASE-BRIDGE changes only the stronger Base/full-CRR branch; it is not needed for EO-LF4 sharpness.",
        },
        "exact_replay": rows,
        "replay": {
            "write_command": "python3 proof/build_cycle_8_crr_objective2_energy_only_saturation_audit_v1.py --write",
            "check_command": "python3 proof/build_cycle_8_crr_objective2_energy_only_saturation_audit_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_8_crr_objective2_energy_only_saturation_audit_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Objective-2 EO-LF4 audit artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Objective-2 EO-LF4 audit artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Objective-2 EO-LF4 audit artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
