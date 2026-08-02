#!/usr/bin/env python3
"""Seal Cycle 113 general weighted split theorem and Cycle-112 containment."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-113-irrational-weighted-split-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-113-irrational-weighted-preregistration-v1.md", "2e71a15c0e646035fae06b34312f6dcef8e3310938a9a8649f300f3e94598bac"),
    "document": (ROOT / "docs/cycle-113-irrational-weighted-split-v1.md", "fd42559fbfb3f99ce5b10c0d2724c6273bf581e7ff1829323791341eac0a40db"),
    "conventions": (ROOT / "conventions/irrational_weighted_split_v1.py", "a9bf727f1a9006cb9142c77ac01bc8254eab85b56b5b6f3c80717ff9679fdb05"),
    "discovery_script": (ROOT / "discovery/run_cycle_113_irrational_weighted_falsifier_v1.py", "1040dae8bbef6ba4a0f0568246295bdc07f091d612e5205a2b3749f9c795d8c1"),
    "discovery_output": (ROOT / "discovery/cycle-113-irrational-weighted-falsifier-v1.json", "f7a12782639cc6912bfbd9819f9b662a1c077ec524c47a8d1f8578209cbefdca"),
    "tests": (ROOT / "tests/test_cycle_113_irrational_weighted_split_v1.py", "0a251e87af1daf5110d74f81a9b204a4daa6fe65d91b18ac4c62482e3610f4d4"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle104": (ROOT / "artifacts/cycle-104-radical-alias-separation-v1.json", "be9acdb96e8d8708ccdc1625e273f9fd092ad505125b058f6162ceae0715ed5b"),
    "cycle112": (ROOT / "artifacts/cycle-112-full-triple-b-symbol-v1.json", "e6f890eaae72a99c53dbd07cea7bd69d050f4df5c93d40e27245f71503f6954c"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle104"][0], "SEALED_SINGLE_RADICAL_RATIONAL_CLASSIFICATION_AND_NORM_SECTOR")
    validate_prior(INPUTS["cycle112"][0], "SEALED_SMOOTH_PERFECT_POWER_STRONG_BRANCH_X3_5_ARITHMETIC_MULTIPLICITY")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="irrational_weighted_split_v1")
    require("(d*N*R)^o(1)" in theorem["split_sum"], "general split bound")
    require("Cycle 112" in theorem["correction"], "correction scope")
    require("anchor-scale" in theorem["aggregate"], "remaining coupled lock")
    return {
        "artifact_id": "cycle-113-irrational-weighted-split-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_GENERAL_STRONG_SPLIT_SUBPOWER_ANCHOR_SCALE_AGGREGATE_OPEN",
        "claim_boundary": (
            "This artifact proves subpower normalized split weight for every compact reduced label, "
            "including irrational large-degree cores. It corrects Cycle 112 by withholding its "
            "X^(3/5) aggregate: pointwise anchor absorption does not sum the support window."
        ),
        "runtime": check_runtime("Cycle 113"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "weighted_split_theorem": {"epistemic_status": "PROVED", **theorem},
        "correction": {
            "epistemic_status": "PROVED",
            "affected_artifact": "cycle-112-full-triple-b-symbol-v1",
            "survives": "full-symbol identity, cutoff coordinates, and pointwise anchor absorption",
            "withheld": "X^(3/5+o(1)) aggregate closure",
        },
        "falsifier": {
            "epistemic_status": "OBSERVED", "proof_role": "none", "rows": 522053,
            "maximum": 0.9868365652513905, "witness": [7, 3, 4],
            "scaled_growth_witness": [119, 44, 75, 0.7392321714655499],
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "bound the coupled anchor-scale-label tail, then weak and simple-root branches",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_113_irrational_weighted_split_v1.py --write",
            "check_command": "python3 proof/build_cycle_113_irrational_weighted_split_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_113_irrational_weighted_split_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 113 sealer", output=OUTPUT, payload_factory=seal))
