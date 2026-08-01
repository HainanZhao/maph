#!/usr/bin/env python3
"""Seal/check the unexecuted Cycle 4 CRR finite-analogue probe v1."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
from typing import Any

import mpmath


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-4-p1r-crr-finite-probe-preregistration-v1.json"
EXPECTED_RUNTIME = {
    "implementation": "CPython",
    "python": "3.12.3",
    "mpmath": "1.2.1",
    "optimization_level": 0,
}
INPUTS: dict[str, tuple[Path, str]] = {
    "formalization_v2": (ROOT / "artifacts/cycle-4-p1r-crr-u-formalization-v2.json", "e26be797539eabe53ee765b7067d1c99fe4d440035e27785cf38aa64bc2fc84e"),
    "conventions": (ROOT / "conventions/crr_finite_analogue_probe_v1.py", "489b189e421b2cdfeed7d0bbe532521e56165e3a16cfba4557731f723b42c547"),
    "document": (ROOT / "docs/cycle-4-p1r-crr-finite-probe-preregistration-v1.md", "c6da4e7d84dd8f3251367d57fc28b22c25796fe0d6d382138de2db5058da4959"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_conventions():
    path = INPUTS["conventions"][0]
    spec = importlib.util.spec_from_file_location("crr_finite_analogue_probe_v1", path)
    require(spec is not None and spec.loader is not None, "cannot load finite-probe conventions")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_runtime() -> dict[str, Any]:
    runtime = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "mpmath": mpmath.__version__,
        "optimization_level": sys.flags.optimize,
    }
    require(runtime == EXPECTED_RUNTIME, "finite CRR preregistration requires non-optimized CPython 3.12.3 and mpmath 1.2.1")
    return runtime


def seal() -> dict[str, Any]:
    runtime = check_runtime()
    frozen: dict[str, dict[str, str]] = {}
    for label, (path, expected) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {label}")
        actual = sha256(path)
        require(actual == expected, f"frozen input hash mismatch: {label}")
        frozen[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual}
    prior = json.loads(INPUTS["formalization_v2"][0].read_text(encoding="utf-8"))
    require(prior["artifact_id"] == "cycle-4-p1r-crr-u-formalization-v2", "formalization v2 identity mismatch")
    require(prior["gate"]["formalization"] == "RESEARCH_STAGE_SEALED_LIGHTWEIGHT_CHECKED", "formalization v2 is not lightweight sealed")
    require(prior["gate"]["mathematical_classification"] == "OPEN", "formalization v2 classification mismatch")

    c = load_conventions()
    scales = c.expected_scale_rows()
    rows = c.scheduled_rows()
    require(len(rows) == 160, "expected exactly 160 rows")
    require(len({row["id"] for row in rows}) == 160, "row identifiers must be unique")
    require({row["N"] for row in rows} == set(c.N_VALUES), "N coverage mismatch")
    require({row["family"] for row in rows} == set(c.FAMILY_ORDER), "family coverage mismatch")
    require({row["replicate"] for row in rows} == set(c.REPLICATES), "replicate coverage mismatch")
    require(rows[0]["id"] == "N256-F1-phase-rounded-frame-V1-R0", "first row order mismatch")
    require(rows[-1]["id"] == "N2048-F5-symmetric-positive-trace-spectral-V4-R1", "last row order mismatch")

    return {
        "artifact_id": "cycle-4-p1r-crr-finite-probe-preregistration-v1",
        "epistemic_status": "CONJECTURED",
        "status": "SEALED_DISCOVERY_PREREGISTRATION_UNEXECUTED",
        "claim_boundary": "Frozen 160-row finite-analogue discovery search only. It proves no CRR compatibility/incompatibility statement, extremizer, saturation theorem, density estimate, or short-interval result. No candidate has been evaluated.",
        "runtime": runtime,
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": frozen,
        "predecessor": {
            "artifact_id": prior["artifact_id"],
            "prior_search_status": prior["gate"]["search"],
            "continuing_authorization": "This separate preregistration supplies the formerly missing finite families/ranges/seed/cap/retention details; it does not alter formalization-v2 claims.",
        },
        "research_stage_review_policy": {
            "lightweight_checks": ["exact schedule arithmetic", "input hash pins", "byte replay", "claim-boundary check"],
            "hostile_audit": "NOT_INITIATED; DEFERRED_TO_PAPER_STAGE",
        },
        "execution": {
            "authorized_after_seal": True,
            "executed_by_this_builder": False,
            "future_output_directory": "discovery/",
            "result_classification": "finite_hits_OBSERVED; complex_scores_RECOGNIZED; no_miss_table_implies_universal_negative",
        },
        "finite_surrogate": c.FINITE_SURROGATE,
        "scale_exponents": {label: str(value) for label, value in c.EXPONENTS.items()},
        "exact_scale_rows": {str(key): value for key, value in scales.items()},
        "schedule": {
            "factorization": "4 N values * 5 families * 4 variants * 2 replicates = 160",
            "canonical_order": "N, family, variant, replicate",
            "master_seed": f"0x{c.MASTER_SEED:016X}",
            "rng": "SplitMix64 unsigned 64-bit wraparound; each row uses the next master-stream output as its fresh row seed",
            "rows": rows,
        },
        "family_registry": c.FAMILY_VARIANTS,
        "mutation": {
            "proposals_per_row": c.MUTATIONS_PER_ROW,
            "operation": "one-for-one W swap with forward cyclic collision repair; recompute the family b rule from the same W",
            "acceptance": "16-node/mode-8 proxy increases by at least 2^-40; otherwise reject",
            "post_result_selection": "PROHIBITED",
        },
        "quadrature_and_cubic": {
            "farey_partition": "all reduced fractions in [0,1] of denominator <=Q, midpoint cells, Gauss-Legendre mapped cellwise",
            "proxy_nodes": c.PROXY_QUADRATURE_NODES,
            "final_nodes": c.FINAL_QUADRATURE_NODES,
            "quadrature_relative_disagreement": str(c.QUADRATURE_RELATIVE_DISAGREEMENT),
            "proxy_cubic_mode": c.PROXY_CUBIC_MODE,
            "final_cubic_mode": c.FINAL_CUBIC_MODE,
            "cubic_relative_disagreement": str(c.CUBIC_RELATIVE_DISAGREEMENT),
            "signed_cubic_positive_sign_required": True,
        },
        "retention": {
            "thresholds": c.frozen_thresholds(),
            "retained_hit_margin": str(c.RETAINED_HIT_MARGIN),
            "recognition_ball": "centre=384-bit value; radius=2*max(|384-bit-256-bit|,2^-256*(1+|centre|)); not a rigorous enclosure",
            "failed_row_rule": "Every one of the 160 scheduled rows is retained exactly once. No parameter-changing retry is permitted. After a global cap, the active row is RESOURCE_CAP and all unstarted rows are GLOBAL_CAP_UNREACHED.",
            "failure_codes": ["INIT_INVALID", "COEFFICIENT_BOUND", "SET_CARDINALITY", "SET_DUPLICATE", "SET_DOMAIN", "RESOURCE_CAP", "GLOBAL_CAP_UNREACHED", "NONFINITE", "RECOGNITION_RADIUS", "QUADRATURE_DISAGREEMENT", "CUBIC_PROXY_DISAGREEMENT", "REPLAY_MISMATCH", "NO_RETAINED_HIT"],
            "no_universal_negative_from_misses": True,
        },
        "resources": {
            "aggregate_wall_seconds": c.RESOURCE_WALL_SECONDS,
            "aggregate_wall_minutes": c.RESOURCE_WALL_SECONDS // 60,
            "max_rss_bytes": c.RESOURCE_MAX_RSS_BYTES,
            "max_rss_gib": 1,
        },
        "replay": {
            "write_command": "python3 discovery/build_cycle_4_p1r_crr_finite_probe_preregistration_v1.py --write",
            "check_command": "python3 discovery/build_cycle_4_p1r_crr_finite_probe_preregistration_v1.py --check",
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
        require(not OUTPUT.exists(), "refusing to overwrite finite CRR preregistration artifact")
        with OUTPUT.open("xb") as handle:
            handle.write(render(payload))
    else:
        require(OUTPUT.is_file(), "finite CRR preregistration artifact is absent")
        require(OUTPUT.read_bytes() == render(payload), "finite CRR preregistration artifact mismatch")
    print(json.dumps({"artifact": OUTPUT.name, "rows": len(payload["schedule"]["rows"]), "executed": payload["execution"]["executed_by_this_builder"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
