#!/usr/bin/env python3
"""Seal Cycle 15 prime phase-transition and rank-one semiprime reduction."""
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
OUTPUT = ROOT / "artifacts/cycle-15-prime-phase-transition-rank-one-v1.json"
EXPECTED_RUNTIME = {"implementation": "CPython", "python": "3.12.3", "optimization_level": 0}
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-15-prime-phase-transition-rank-one-preregistration-v1.md", "4633801097fc0303856b6165e64cb57a0caa083adfc8f8df5d5383f100afee89"),
    "document": (ROOT / "docs/cycle-15-prime-phase-transition-rank-one-v1.md", "768dda84d3259040ce80a7a71c515068d51e03fe88c48bc22b6726638484a411"),
    "conventions": (ROOT / "conventions/prime_phase_transition_rank_one_v1.py", "6d3136958072d8cfb1fea919e7b1d16bea82aa44978166087566ef2c0ddb3660"),
    "tests": (ROOT / "tests/test_cycle_15_prime_phase_transition_rank_one_v1.py", "c7dac0bbf7eec9ef939389e3d5f4fdaec28bb88353b51185868266e92203ffbd"),
    "gm_source": (ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex", "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"),
    "cycle14_artifact": (ROOT / "artifacts/cycle-14-prime-atom-fractional-moment-v1.json", "8cd7f58a5972031553708e9efc1f0d8f4a613a232ffbcecc85bb659d085b5152"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_json(value: Any) -> Any:
    if isinstance(value, Fraction):
        return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    if isinstance(value, list):
        return [exact_json(item) for item in value]
    if isinstance(value, dict):
        return {str(key): exact_json(item) for key, item in value.items()}
    return value


def check_runtime() -> dict[str, Any]:
    runtime = {"implementation": platform.python_implementation(), "python": platform.python_version(), "optimization_level": sys.flags.optimize}
    require(runtime == EXPECTED_RUNTIME, "Cycle 15 requires non-optimized CPython 3.12.3")
    return runtime


def frozen_inputs() -> dict[str, dict[str, str]]:
    result = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        result[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    return result


def load_rows() -> dict[str, object]:
    path = INPUTS["conventions"][0]
    spec = importlib.util.spec_from_file_location("prime_phase_transition_rank_one_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load Cycle 15 conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.verify_all()
    require(rows["phase_transition"]["p_star"] == Fraction(24, 5), "phase transition mismatch")
    require(rows["rank_one_gm_translation"]["required_saving"] == Fraction(4, 25), "rank-one saving mismatch")
    return rows


def validate_source() -> dict[str, str]:
    source = INPUTS["gm_source"][0].read_text(encoding="utf-8")
    for needle in ("N^2V^{-2}+N^{18/5}V^{-4}+TN^{12/5}V^{-4}", "|b_n| \\le 1"):
        require(needle in source, f"missing GM theorem anchor: {needle}")
    cycle14 = json.loads(INPUTS["cycle14_artifact"][0].read_text(encoding="utf-8"))
    require(cycle14.get("artifact_id") == "cycle-14-prime-atom-fractional-moment-v1", "Cycle 14 artifact mismatch")
    return {"gm_large_values": "Theorem 1.1, TeX lines 68--77", "prime_count_scale": "already checked PNT baseline; only m=X^(1-o(1)) is used"}


def seal() -> dict[str, Any]:
    rows = load_rows()
    return {
        "artifact_id": "cycle-15-prime-phase-transition-rank-one-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_PRIME_PHASE_TRANSITION_RANK_ONE_SEMIPRIME_TARGET_OPEN",
        "claim_boundary": "This artifact proves sharp lower mechanisms and an exact reduction to a rank-one semiprime coefficient class. It does not prove the restricted rank-one large-value estimate, selection of the prime component on zero rows, a density gain, or an interval improvement.",
        "runtime": check_runtime(),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen_inputs(),
        "source_context": {"epistemic_status": "PROVED", **validate_source()},
        "two_extremizer_lower_theorem": {
            "epistemic_status": "PROVED",
            "coherent_spike": "For aligned unimodular coefficients, integral |P|^p >=c_p m^p.",
            "random_bulk": "For some deterministic Steinhaus coefficient vector, integral |P|^p >=H m^(p/2) for p>=4.",
            "phase_transition": "At H=X^(12/5), the exponents p and 12/5+p/2 meet uniquely at p=24/5.",
            "sharpness": "Any uniform order-24/5 upper at exponent X^(24/5+o(1)) is power-sharp against both mechanisms.",
        },
        "rank_one_semiprime_reduction": {
            "epistemic_status": "PROVED",
            "identity": "P_a^2 has diagonal coefficients a_p^2 and off-diagonal coefficients 2a_pa_q, a symmetric rank-one tensor.",
            "dyadic_cost": "two colours and constant threshold loss",
            "generic_gm_exponents_in_X": ["6/5", "8/5", "8/5"],
            "target_count_exponent_in_X": "36/25",
            "required_saving_in_X": "4/25",
            "required_saving_in_v": "4/5",
        },
        "principal_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Improve both tied GM terms to X^(36/25+o(1)) for the symmetric rank-one semiprime coefficient class at N=X^2, T=N^(6/5), V=N^(7/10).",
            "global_fractional_moment": "SUFFICIENT_NOT_NECESSARY",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "exact_replay": exact_json(rows),
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_15_prime_phase_transition_rank_one_v1.py --write",
            "check_command": "python3 proof/build_cycle_15_prime_phase_transition_rank_one_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_15_prime_phase_transition_rank_one_v1.py",
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
        require(not OUTPUT.exists(), "refusing to overwrite Cycle 15 artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "Cycle 15 artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "Cycle 15 artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "status": payload["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
