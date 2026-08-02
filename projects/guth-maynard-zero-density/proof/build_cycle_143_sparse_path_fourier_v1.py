#!/usr/bin/env python3
"""Seal Cycle 143 sparse-path Fourier compiler."""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path
from typing import Any

from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-143-sparse-path-fourier-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-143-sparse-path-fourier-preregistration-v1.md", "f895d37d0f4a2a3e16b8489345c86b91378e43be44e5cce2dfc93b3d63b74dfe"),
    "document": (ROOT / "docs/cycle-143-sparse-path-fourier-v1.md", "94619f1c2621c226eff8a364cab562131a051038d4fe38ba3f1efab3fa827fea"),
    "conventions": (ROOT / "conventions/sparse_path_fourier_v1.py", "53c1f25178bd683c67d19c7901c4339ed5a636c638847a0fbfa972bb7200f739"),
    "tests": (ROOT / "tests/test_cycle_143_sparse_path_fourier_v1.py", "91aea72513279d99a1513487ec18af33b15be6f8464e6ff548db1827c57d70a3"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle136": (ROOT / "artifacts/cycle-136-common-multiplier-scalar-v1.json", "d3af0383df6754f59fb0515c0f0811e116c772b441868d1ad41c13360cfcf52f"),
    "cycle142": (ROOT / "artifacts/cycle-142-changing-color-walk-v1.json", "7533463448df762879b9113901489f584b8ae76d47ca9b51a046b9ab984aab76"),
}


def seal() -> dict[str, Any]:
    validate_prior(INPUTS["cycle136"][0], "SEALED_PAIRED_NORM_SCALAR_DICHOTOMY_EXCEPTIONAL_MULTIPLIER_AVERAGE_OPEN")
    validate_prior(INPUTS["cycle142"][0], "SEALED_RECURRENCE_LOG_DEPTH_SATURATION_SPARSE_COMPONENT_NORM_OPEN")
    theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="sparse_path_fourier_v1")
    module = __import__("conventions.sparse_path_fourier_v1", fromlist=["scalar_threshold"])
    threshold = module.scalar_threshold(Fraction(1, 5), Fraction(7, 10))
    require(threshold["kappa_threshold"] == Fraction(-1, 10), "scalar threshold")
    require("unchanged" in theorem["self_duality"], "path self-duality")
    require("M_0" in theorem["moment_expansion"], "zeroth signed moment")
    require("not bounded" in theorem["boundary"], "actual moments open")
    return {
        "artifact_id": "cycle-143-sparse-path-fourier-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_SPARSE_PATH_NORM_SELF_DUAL_SIGNED_MOMENT_HIERARCHY_OPEN",
        "claim_boundary": (
            "This artifact proves norm self-duality only for arbitrary-weight "
            "logarithmic path layering and identifies the signed moment hierarchy. "
            "It proves no bound for the actual coefficients, paired norm, endpoint, "
            "moment theorem, density, or prime intervals."
        ),
        "runtime": check_runtime("Cycle 143"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "sparse_path_fourier_theorem": {"epistemic_status": "PROVED", **theorem},
        "sample_threshold_ledger": {
            "epistemic_status": "PROVED",
            "rho": "1/5",
            "tau": "7/10",
            **{key: str(value) for key, value in threshold.items()},
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "derive cancellation in M_0(d),M_1(d),... from the actual signed "
                "tail coefficients and quantify the first uniform moment saving"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_143_sparse_path_fourier_v1.py --write",
            "check_command": "python3 proof/build_cycle_143_sparse_path_fourier_v1.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_143_sparse_path_fourier_v1.py tests/test_cycle_seal_v1.py",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 143 sealer", output=OUTPUT, payload_factory=seal))
