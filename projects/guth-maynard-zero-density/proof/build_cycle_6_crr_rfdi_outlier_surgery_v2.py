#!/usr/bin/env python3
"""Seal the versioned correction for the CRR RFDI outlier-surgery theorem."""
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
OUTPUT = ROOT / "artifacts/cycle-6-crr-rfdi-outlier-surgery-v2.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "v1_artifact": (ROOT / "artifacts/cycle-6-crr-rfdi-outlier-surgery-v1.json", "0bd2843123957ed045b1feae389467030066f572f65914032955fc4cb90bc351"),
    "v1_current_conventions": (ROOT / "conventions/crr_rfdi_outlier_surgery_v1.py", "4e4c69fa2b1cfc477102056ae29293711022f7173d3e6fc971d61d41f2c9d7a7"),
    "v1_current_document": (ROOT / "docs/cycle-6-crr-rfdi-outlier-surgery-v1.md", "fd8b50aa9dca59ff42c461dd2ac778f31fca643b4fe6b68553c3f940ae3e8d96"),
    "v1_current_builder": (ROOT / "proof/build_cycle_6_crr_rfdi_outlier_surgery_v1.py", "a2be6e1a40c48c0dfe04c33e26bd32605a7e411c7d9ac63752fcdab28090ad53"),
    "v1_tests": (ROOT / "tests/test_cycle_6_crr_rfdi_outlier_surgery_v1.py", "38396a2ad382ed4c985d51cc28197a270957826811e955b83a6808a219b739dd"),
    "crr_v2_artifact": (ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v2.json", "e26be797539eabe53ee765b7067d1c99fe4d440035e27785cf38aa64bc2fc84e"),
    "crr_v2_conventions": (ROOT / "conventions/crr_formalization_v2.py", "0d960b76a4ad03cce43727159cf846696dbee732184df44b2ee0503b9ae18ce8"),
    "gm_source_tex": (ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex", "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
    "farey_log_v2_artifact": (ROOT / "artifacts/cycle-5-crr-farey-log-gram-reduction-v2-averaged-jitter.json", "ce59b777ec02769168d9dc330658a0ab1d46b05cdb7ac5dc8115e248d85f8ce8"),
    "row_deletion_artifact": (ROOT / "artifacts/cycle-6-crr-row-deletion-inverse-v1.json", "9b0d74235c587d8624879626703efc9577020ebb8770defe022108914c35e832"),
    "conventions": (ROOT / "conventions/crr_rfdi_outlier_surgery_v2.py", ""),
    "document": (ROOT / "docs/cycle-6-crr-rfdi-outlier-surgery-v2-correction.md", ""),
    "tests": (ROOT / "tests/test_cycle_6_crr_rfdi_outlier_surgery_v2.py", ""),
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
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"expected JSON object: {path}")
    return data


def load_module(label: str, module_name: str):
    path = INPUTS[label][0]
    spec = importlib.util.spec_from_file_location(module_name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {label}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def runtime_metadata() -> dict[str, Any]:
    result = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(result == EXPECTED_RUNTIME, "RFDI outlier surgery v2 requires non-optimized CPython 3.12.3")
    return result


def frozen_inputs() -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing input: {label}")
        actual = sha256(path)
        if expected:
            require(actual == expected, f"frozen input hash mismatch: {label}")
        result[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    return result


def validate_context() -> dict[str, str]:
    v1 = load_json(INPUTS["v1_artifact"][0])
    sealed = v1.get("frozen_hashes", {})
    require(sealed.get("conventions", {}).get("sha256") == "6e9183c18458904a2f90d4f2100c8723640c03f6a6e17418291e78930699d328", "v1 sealed conventions hash mismatch")
    require(sealed.get("document", {}).get("sha256") == "2e199ab232334f9faceeca9a2690debf21d745e6c191fba6d482c4a17a9685c2", "v1 sealed document hash mismatch")
    require(v1.get("sealer", {}).get("sha256") == "a3dac8b689b27ed28e25158ed2fd258c486af94f694092d1525361cd955f0bbd", "v1 sealed builder hash mismatch")
    crr = load_json(INPUTS["crr_v2_artifact"][0])
    base = crr.get("witness_schema", {}).get("base", {})
    rational = crr.get("witness_schema", {}).get("rational_mass", {})
    require(base.get("set") == "finite W subset [0,H], H^(1/100)-separated", "Base set anchor mismatch")
    require(base.get("energy_definition") == "ordered quadruples in W^4 with |t1+t2-t3-t4|<=1", "Base energy anchor mismatch")
    require(rational.get("threshold") == "measure({u in Q_v:Rtilde_W(u)>=v^(6-delta(v))}) >= v^(-4-delta(v))", "RationalMass anchor mismatch")
    conventions = load_module("crr_v2_conventions", "crr_formalization_v2_for_outlier_surgery_v2")
    require(conventions.SMOOTH_FUNCTIONS["psi1"] == "psi1(x)=eta(1-x^2)/eta(1)", "psi1 formula mismatch")
    require(conventions.SMOOTH_FUNCTIONS["psi2"] == "psi2(u)=eta(1-4*(u-1)^2)/eta(1)", "psi2 formula mismatch")
    source = INPUTS["gm_source_tex"][0].read_text(encoding="utf-8")
    require("(M_W)_{t,n}=w(n/N)n^{it}" in source, "actual matrix source anchor mismatch")
    farey = load_json(INPUTS["farey_log_v2_artifact"][0])
    require(farey.get("averaged_actual_farey_bundle", {}).get("labeled_identity") == "C_theta(sk,rk)=R_W((r/s)*exp(theta/H))", "Farey identity mismatch")
    deletion = load_json(INPUTS["row_deletion_artifact"][0])
    require(deletion.get("row_deletion_leverage", {}).get("consequence") == "mu_top(W)>=DelCov(W)", "row-deletion anchor mismatch")
    return {
        "v1_artifact": v1["artifact_id"],
        "v1_input_status": "v1 post-seal convention/document/builder hashes are pinned separately in this correction and intentionally differ from v1's sealed hashes",
        "base_set": base["set"],
        "base_energy_definition": base["energy_definition"],
        "rationalmass_threshold": rational["threshold"],
        "actual_farey_identity": farey["averaged_actual_farey_bundle"]["labeled_identity"],
        "row_deletion": deletion["row_deletion_leverage"]["consequence"],
    }


def exact_rows() -> dict[str, Any]:
    conventions = load_module("conventions", "crr_rfdi_outlier_surgery_v2")
    verified = conventions.verify_all()
    require(verified["large_v_mean_value_coarse_tail_at_v64"] == Fraction(81, 128), "v2 mean-value tail mismatch")
    require("ell+r+2s<2" in verified["selection_rows"]["failure"], "v2 budget row mismatch")
    return json_exact(verified)


def seal() -> dict[str, Any]:
    conventions = load_module("conventions", "crr_rfdi_outlier_surgery_v2_for_seal")
    return {
        "artifact_id": "cycle-6-crr-rfdi-outlier-surgery-v2",
        "epistemic_status": "PROVED",
        "status": "SEALED_VERSIONED_CORRECTION_CONDITIONAL_ACTUAL_LOG_FAREY_RFDI_OUTLIER_OBSTRUCTION",
        "claim_boundary": "This is a versioned correction/reseal of a conditional actual-log/Farey outlier theorem. It does not construct its core, refute RFDI, prove a full Base common witness or pointwise coefficient condition, prove AFARI/FARI/CFARI/CRR-U, a cubic estimate, a density gain, a short-interval theorem, a saturation theorem, or an L-function result.",
        "runtime": runtime_metadata(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "research_stage_review_policy": {
            "lightweight_checks": "exact algebra, elementary integral/harmonic estimates, source/convention anchors, replay, and tamper rejection",
            "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION",
        },
        "correction": {
            "epistemic_status": "PROVED",
            "v1_artifact_sha256": "0bd2843123957ed045b1feae389467030066f572f65914032955fc4cb90bc351",
            "v1_sealed_input_hashes": {
                "conventions": "6e9183c18458904a2f90d4f2100c8723640c03f6a6e17418291e78930699d328",
                "document": "2e199ab232334f9faceeca9a2690debf21d745e6c191fba6d482c4a17a9685c2",
                "builder": "a3dac8b689b27ed28e25158ed2fd258c486af94f694092d1525361cd955f0bbd",
            },
            "post_seal_mutation": "v1 convention/document/builder were edited after v1 sealing; their current hashes are frozen as v1_current_* inputs above, while the v1 artifact bytes remain unchanged.",
            "mathematical_effect": "v2 makes no stronger unconditional theorem claim. It independently re-seals the conditional theorem, spelling out normalized-bump use and the ell+r+2s budget consequence.",
            "disposition": "v1 is retained as an immutable but nonreplayable post-mutation record; v2 is the replayable versioned correction.",
        },
        "context": validate_context(),
        "conditional_theorem": {
            "epistemic_status": "PROVED_CONDITIONAL_ON_A_CONJECTURED_CORE",
            "core": "A has R-1 rows in [0,H/4], an interior frozen energy band, a fixed top spectral gap and Lambda>=v^(12-ell*delta(v)), and RationalMass surplus F_A>=(1+epsilon)v^(12-2delta(v)) on the required rational set.",
            "preservation": "For a selected actual tau in [3H/4,H], one common W=A union {tau} retains frozen separation, cardinality, energy, RationalMass, and actual Farey labels.",
            "selection": "The actual-log coupling is selected by the elementary C_v mean-value bound, without inspecting the enlarged target eigenvector or Farey outcome.",
            "failure": "DelCov(W)<=8g^(-2)v^(-4+ell*delta(v))<v^(-2s*delta(v)) for every fixed g,ell,r,s with ell+r+2s<2 and sufficiently large v.",
            "scope": "The result blocks only a set-only RFDI inference from scalar/hereditary inputs; it does not show that the full Base coefficient/pointwise condition survives surgery.",
        },
        "exact_rows": json_exact(conventions.verify_all()),
        "falsifiers": {
            "correction": "A mismatch between the preserved v1 artifact, its sealed hashes, or the explicitly pinned post-seal inputs refutes the correction ledger.",
            "preservation": "A failure of the pair-sum energy identity or smoothing Cauchy bound refutes scalar/RationalMass preservation.",
            "selection": "A sign/orientation error in the actual-log coupling, mean-value estimate, or block gap argument refutes the conditional theorem.",
            "scope": "An incompatibility theorem ruling out the listed core would redirect the program but would not refute this conditional implication.",
        },
        "replay": {
            "write_command": "python3 proof/build_cycle_6_crr_rfdi_outlier_surgery_v2.py --write",
            "check_command": "python3 proof/build_cycle_6_crr_rfdi_outlier_surgery_v2.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_6_crr_rfdi_outlier_surgery_v2.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite RFDI outlier surgery v2 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "RFDI outlier surgery v2 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "RFDI outlier surgery v2 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
