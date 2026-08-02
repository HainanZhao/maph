#!/usr/bin/env python3
"""Seal Cycle 117 weighted weak-turnover closure."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-117-weighted-weak-sector-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-117-weighted-weak-preregistration-v1.md", "4450465a0c13a5793f2e7d71d8cbc7dd4ed773f7dd9565414234bbb65f65aebc"),
    "document": (ROOT / "docs/cycle-117-weighted-weak-sector-v1.md", "84043849844c0b69e5ef23082238e3e36e4cbdebea6cd909058cca252b3679d8"),
    "conventions": (ROOT / "conventions/weighted_weak_sector_v1.py", "04f139db22f6d4fbbfc933e33148c0b60fe8f3428d0803ad581befb638b804cf"),
    "tests": (ROOT / "tests/test_cycle_117_weighted_weak_sector_v1.py", "0514697c9676b3bf26288a94b957c811e789464be129c54c25fa5837d7520bf6"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle114": (ROOT / "artifacts/cycle-114-coupled-anchor-scale-v1.json", "bec19431e36affe22633ce2095db8537205b5dcd2525e29abb7a0ab79271d596"),
    "cycle116": (ROOT / "artifacts/cycle-116-projective-tolerance-v1.json", "f40fb40708fb27d857f3c116dc8c1b7d76cb2291a4ad965e81f5cafe09a62dd2"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle114"][0], "SEALED_ALL_SMOOTH_STRONG_CORES_WEIGHTED_X13_30_WEAK_SIMPLE_OPEN")
    validate_prior(INPUTS["cycle116"][0], "SEALED_WEAK_TRANSITION_ENERGY_CAP_MODE_EXPONENT_7_25_AGGREGATE_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="weighted_weak_sector_v1")
    require("D^2/(KQ)" in theorem["mode_count"], "ellipse count")
    require("1/25" in theorem["exponent"], "uniform margin")
    require("simple-root" in theorem["boundary"], "remaining branch")
    return {
        "artifact_id": "cycle-117-weighted-weak-sector-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_SMOOTH_WEAK_SECTOR_X59_150_SIMPLE_ROOT_OPEN",
        "claim_boundary": (
            "This artifact sums the registered smooth weak-turnover sector with exponent "
            "at most 59/150, a 1/25 margin below the smooth strong benchmark. Simple roots, "
            "nonsmooth variants, full moment assembly, density, and intervals remain open."
        ),
        "runtime": check_runtime("Cycle 117"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "weighted_weak_theorem": {"epistemic_status": "PROVED", **theorem},
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "aggregate the quantitative simple-root output and assemble the lower-band signed moment",
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_117_weighted_weak_sector_v1.py --write",
            "check_command": "python3 proof/build_cycle_117_weighted_weak_sector_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_117_weighted_weak_sector_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 117 sealer", output=OUTPUT, payload_factory=seal))
