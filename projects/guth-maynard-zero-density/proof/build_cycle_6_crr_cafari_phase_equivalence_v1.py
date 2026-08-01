#!/usr/bin/env python3
"""Seal the Cycle 6 CRR CFARI/AFARI phase-equivalence reduction v1."""
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
OUTPUT = ROOT / "artifacts/cycle-6-crr-cfari-phase-equivalence-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "crr_v2_artifact": (ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v2.json", "e26be797539eabe53ee765b7067d1c99fe4d440035e27785cf38aa64bc2fc84e"),
    "afari_coupling_artifact": (ROOT / "artifacts/cycle-6-crr-afari-coefficient-coupling-v1.json", "a9b142f8fd22e4fe9ebd4857af4eb7e764aa20ea379170930f6446231e663266"),
    "farey_log_v2_artifact": (ROOT / "artifacts/cycle-5-crr-farey-log-gram-reduction-v2-averaged-jitter.json", "ce59b777ec02769168d9dc330658a0ab1d46b05cdb7ac5dc8115e248d85f8ce8"),
    "gm_source_tex": (ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex", "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
    "document": (ROOT / "docs/cycle-6-crr-cfari-phase-equivalence-v1.md", "569a2bea4ad16b2ecab8b40a8ab7578ab3010cbb2c0a4baf8dac727afcb5ad03"),
    "conventions": (ROOT / "conventions/crr_cafari_phase_equivalence_v1.py", "62fbe5603f3c5f5024b7745d7196cef3d02f88e6a941f8d141974c74c65ee64e"),
    "tests": (ROOT / "tests/test_cycle_6_crr_cafari_phase_equivalence_v1.py", "f1185e174fd715eb595f445329e1eb2b331475025f6a30022832e576e1f051a0"),
}
SOURCE_FRAGMENTS = (
    "Using a simple orthogonality argument,  it has long been known that for any $T \\ge N$",
    "Thus we wish to improve upon the bound $\\|M\\|\\lessapprox T^{1/2}$ which follows from the Mean Value Theorem",
    "(M_W)_{t,n}=w(n/N)n^{it}",
)


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


def affine_text(value: tuple[Fraction, Fraction]) -> str:
    constant, slack = value
    if slack == 0:
        return fraction_text(constant)
    sign = "+" if slack > 0 else "-"
    return f"{fraction_text(constant)}{sign}{fraction_text(abs(slack))}*delta"


def check_runtime() -> dict[str, Any]:
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "CRR CFARI phase-equivalence v1 requires non-optimized CPython 3.12.3")
    return runtime


def frozen_inputs() -> dict[str, dict[str, str]]:
    frozen: dict[str, dict[str, str]] = {}
    for label, (path, expected_hash) in INPUTS.items():
        require(expected_hash != "AUTO", f"unfrozen input hash: {label}")
        require(path.is_file(), f"missing frozen input: {label}")
        actual_hash = sha256(path)
        require(actual_hash == expected_hash, f"frozen input hash mismatch: {label}")
        frozen[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual_hash}
    return frozen


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"expected JSON object: {path}")
    return data


def load_conventions():
    path = INPUTS["conventions"][0]
    spec = importlib.util.spec_from_file_location("crr_cafari_phase_equivalence_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load CFARI phase-equivalence conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_context() -> dict[str, str]:
    source = INPUTS["gm_source_tex"][0].read_text(encoding="utf-8")
    for fragment in SOURCE_FRAGMENTS:
        require(fragment in source, f"mean-value source fragment missing: {fragment}")
    crr = load_json(INPUTS["crr_v2_artifact"][0])
    require(crr.get("artifact_id") == "cycle-4-p1r-crr-u-formalization-v2", "CRR v2 artifact identity mismatch")
    base = crr.get("witness_schema", {}).get("base", {})
    require(base.get("set") == "finite W subset [0,H], H^(1/100)-separated", "Base separation convention mismatch")
    require(base.get("cardinality") == "v^(8-delta(v)) <= |W| <= v^(8+delta(v))", "Base cardinality convention mismatch")
    require(base.get("pointwise") == "|D_v(t)| >= v^(7-delta(v)) for every t in W", "Base pointwise convention mismatch")
    afari = load_json(INPUTS["afari_coupling_artifact"][0])
    require(afari.get("artifact_id") == "cycle-6-crr-afari-coefficient-coupling-v1", "AFARI coupling artifact identity mismatch")
    bridge = afari.get("coefficient_phase_bridge", {})
    require(bridge.get("rayleigh_lower") == "a^*(M_W*M_W^*)a=||M_W^*a||_2^2>=v^(20-4*delta(v))", "phase-Rayleigh lower convention mismatch")
    farey = load_json(INPUTS["farey_log_v2_artifact"][0])
    require(farey.get("artifact_id") == "cycle-5-crr-farey-log-gram-reduction-v2-averaged-jitter", "Farey v2 identity mismatch")
    lower = farey.get("averaged_actual_farey_lower", {})
    upper = farey.get("raw_rl2_global_upper", {})
    require(lower.get("ray_multiplicity_lower") == "#K_(r,s)>=L/(20Q)=v^6/20", "ray lower convention mismatch")
    require(upper.get("ray_multiplicity_upper") == "#K_(r,s)<=9L/(5Q)<=2L/Q", "ray upper convention mismatch")
    return {
        "mean_value_anchor": "LargevaluesDirichlet17.tex, lines 217-225 and 320-333",
        "base_set": base["set"],
        "base_cardinality": base["cardinality"],
        "phase_lower": bridge["rayleigh_lower"],
        "ray_comparison": "(L/(20Q))*Mcal<=A<=(2L/Q)*Mcal",
    }


def exact_rows() -> dict[str, Any]:
    conventions = load_conventions()
    checked = conventions.verify_all()
    rows = checked["affine_rows"]
    rendered = {key: affine_text(value) if isinstance(value, tuple) else value for key, value in rows.items()}
    expected = {
        "base_phase_rayleigh_lower": "20-4*delta",
        "sampled_mean_value_phase_upper": "20+1*delta",
        "sampled_mean_value_extra_factor": "C*(1+log(2L))",
        "afaris_A_to_Mcal": "20",
        "Mcal_to_afaris_A": "26",
        "cfari_to_Mcal_before_absorption": "20-1*delta",
        "afari_to_cafari_before_absorption": "40-1*delta",
    }
    require(rendered == expected, "CFARI phase-equivalence exponent rows mismatch")
    scales = checked["scales"]
    require(scales["H"] == scales["L"] * scales["v"] ** 2, "mean-value scale identity mismatch")
    return {"scales_at_v8": json_exact(scales), "affine_rows": rendered, "fixed_power_maps": checked["fixed_power_maps"]}


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen = frozen_inputs()
    context = validate_context()
    rows = exact_rows()
    return {
        "artifact_id": "cycle-6-crr-cfari-phase-equivalence-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_CFARI_AFARI_PHASE_EQUIVALENCE_LIGHTWEIGHT_CHECKED",
        "claim_boundary": "This artifact proves the sampled mean-value enclosure for the Base phase factor, fixed-power CFARI/AFARI equivalence, and tensor/Schur identities. It proves neither CFARI, AFARI, F4F, CRR-U, a witness, a cubic estimate, a density gain, a short-interval theorem, a full-method saturation theorem, or an L-function result.",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "research_stage_review_policy": {"lightweight_checks": "primary-source anchors, exact scale algebra, finite-dimensional kernel identities, replay, and tamper rejection", "hostile_audit": "DEFERRED_TO_PAPER_STAGE_BY_USER_DIRECTION"},
        "source_context": context,
        "phase_scale_enclosure": {
            "epistemic_status": "PROVED",
            "lower": "a^*G_W*a>=v^(20-4*delta(v))",
            "upper": "a^*G_W*a<=C*v^(20+delta(v))*(1+log(2L))",
            "mean_value_translation": "1-separated sampling plus the classical coefficient-l2 Dirichlet mean-value estimate yields ||M_W||_op^2<=C(H+L)(1+log(2L))",
            "scope": "every Base-admissible common pair; no RationalMass, energy, or PositiveCubic hypothesis enters the upper bound",
            "power_scale": "a^*G_W*a=v^(20+o(1)) uniformly on the Base class",
        },
        "fixed_power_equivalence": {
            "epistemic_status": "PROVED",
            "cfari_to_afari": "CFARI_eta implies AFARI_(eta/2) eventually, using the Base phase lower and A<=(2L/Q)Mcal",
            "afari_to_cafari": "AFARI_eta implies CFARI_(eta/2) eventually, using Mcal<=(20Q/L)A and the sampled phase upper",
            "equivalence": "exists fixed eta>0 CFARI_eta if and only if exists fixed eta>0 AFARI_eta",
            "consequence": "CFARI is a phase-sensitive reformulation, not an independent fixed-power gate beyond AFARI",
        },
        "tensor_and_schur": {
            "epistemic_status": "PROVED",
            "tensor_identity": "(a^*G_W*a)(1^*K_F*1)=||(M_W^*a) tensor (F_W*1)||_2^2",
            "four_linear_structure": "the G pair and K_F pair are independent before a new mixed estimate is introduced",
            "schur_identity": "(G_W circ K_F)_(t,t')=sum_(n,(r,s),theta)w(n/L)^2*(n*(r/s)*exp(theta/H))^(i(t-t'))",
            "scope": "the Schur kernel is PSD but it is a diagonal mixed object, not the tensor product above",
        },
        "extra_energy_gate": {
            "epistemic_status": "CONJECTURED",
            "statement": "F4F_zeta: integral_(U_v)|R_W(u)|^4du<=v^(20-zeta) for a fixed zeta>0 and every Base-admissible W",
            "proved_conditional_effect": "F4F_zeta implies CFARI_(zeta/3) eventually through actual-Farey Cauchy plus the sampled phase upper",
            "scope": "the least currently isolated non-tautological energy/Farey condition in this Cauchy chain; not claimed logically weakest among all arguments",
            "positive_cubic_boundary": "No proved bridge connects the frozen PositiveCubic predicate to the Base phase or the mixed Schur kernel.",
        },
        "literature_boundary": {
            "epistemic_status": "OBSERVED",
            "boca_radziwill": "The additive complete-Farey matrix e(n*a/q), n<=N, N asymp Q^2 is not the logarithmic-jitter K_F on arbitrary real W subset [0,Q^3]; its eigenvalue-moment result supplies no all-ones or mixed G_W/K_F bound here.",
            "ramare": "The same additive uniform-weight Farey setting is studied; no direct log-node transfer is asserted.",
            "not_an_imported_theorem": True,
        },
        "crr_u_effect": {"epistemic_status": "PROVED", "statement": "The truth status of CRR-U does not advance. A proof of either fixed-saving target would still imply CRR-U through the averaged-jitter reduction."},
        "exact_replay": rows,
        "replay": {"write_command": "python3 proof/build_cycle_6_crr_cafari_phase_equivalence_v1.py --write", "check_command": "python3 proof/build_cycle_6_crr_cafari_phase_equivalence_v1.py --check", "test_command": "python3 -m unittest tests/test_cycle_6_crr_cafari_phase_equivalence_v1.py"},
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
        require(not OUTPUT.exists(), "refusing to overwrite CFARI phase-equivalence v1 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "CFARI phase-equivalence v1 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "CFARI phase-equivalence v1 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
