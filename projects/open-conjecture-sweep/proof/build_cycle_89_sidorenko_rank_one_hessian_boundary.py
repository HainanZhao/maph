"""Seal C89's stationary rank-one Hessian method boundary."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


OUTPUT = ROOT / "artifacts/cycle-89-b089-sidorenko-rank-one-hessian-boundary-v1.json"
PYTHON = ROOT / ".venv/bin/python"
HASHES = {
    "preregistration": ("docs/cycle-89-b089-sidorenko-rank-one-escape-preregistration-v1.md", "46cdb77b9bc9fd43fef3b6753906ca6aa71933d8a3199fcec0237307650dc329"),
    "idea_selection": ("discovery/cycle89_sidorenko_rank_one_escape_selection.md", "456030d0d893b7f3dc8be1abdfb504b0180b827da12ca215e426c8d31372199b"),
    "source_audit": ("discovery/cycle89_sidorenko_rank_one_escape_source_audit.md", "a502b3dd66e056aed5e423dd8031d25f1872fc6550053bcd49617604b3865a0b"),
    "finite_checker": ("proof/check_cycle89_rank_one_escape.py", "4ecafb11e0fa3dfe512484b4cece78c1e1ae9336c0592de27c23dc06f2b41e3d"),
    "orbit_checker": ("proof/check_cycle89_rank_one_symbolic.py", "57527c6340cf8c94e4c7838f5912626b55caeb1447bfada83ec890c08509b8e3"),
    "coefficient_replay": ("proof/check_cycle89_rank_one_symbolic_replay.py", "078d75bc961e1d0a2f8707b7106d49e0c7539c8896cd8f8bc6af166e5cd75979"),
    "boundary": ("proof/cycle89_rank_one_escape_boundary.md", "e1c3fdf1e32a539c5ef345a5e9990c5eff18e2862b7e7ad3e31f404e35fd5d02"),
    "derivation": ("proof/cycle89_rank_one_symbolic.md", "a47323468e1428fdca8c25368bb1ad9bdb9b106fd710f4ec867e4b09e4d3b347"),
    "finite_test": ("tests/test_cycle89_rank_one_escape.py", "b35a2e8c4dcce3b344b941e4a82efa0c56a1908b3d4efcad36ebdb3a0e7c2a78"),
    "symbolic_test": ("tests/test_cycle89_rank_one_symbolic.py", "6b030f06a7dc4835c5bfa1fb3ce8d0bb27eb9bc1e4141075a5659d068a8e674f"),
    "prior_c85": ("artifacts/cycle-85-b085-sidorenko-c5-kernel-boundary-v1.json", "3fb242906c97496c6a5e32cd373880a4b487db231aaa81b827df8ecc1e61e131"),
    "scaffold": ("proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "validator": ("../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def run(path: str) -> dict:
    return json.loads(subprocess.check_output([str(PYTHON), str(ROOT / path)], text=True))


def audit() -> dict:
    finite, orbits, replay = (run(HASHES[key][0]) for key in ("finite_checker", "orbit_checker", "coefficient_replay"))
    require(finite["status"] == "PSD_CONTROL_PASS" and finite["tangent_dimension"] == 7, "finite C89 control drift")
    require(finite["negative_principal_minors"] == [] and finite["density"] == "1/4", "finite C89 PSD/density drift")
    require(orbits["status"] == "PASS" and orbits["ordered_pair_orbits"] == {"shared_left": 30, "shared_right": 30, "disjoint": 150}, "orbit count drift")
    require(replay["status"] == "COEFFICIENTWISE_REPLAY_PASS", "formula replay failed")
    require([row["mismatch_count"] for row in replay["controls"]] == [0, 0], "coefficient mismatch")
    return {"finite_control": {"status": finite["status"], "density": finite["density"], "tangent_dimension": finite["tangent_dimension"], "negative_principal_minors": 0},
            "edge_pair_orbits": orbits["ordered_pair_orbits"],
            "independent_coefficient_replay": {"status": replay["status"], "controls": [row["name"] for row in replay["controls"]], "mismatch_counts": [row["mismatch_count"] for row in replay["controls"]]}}


def payload() -> dict:
    return {"artifact_id": "cycle-89-b089-sidorenko-rank-one-hessian-boundary-v1", "budget_ordinal": "B089", "cycle": 89,
            "record_type": "PROVED_SCOPED_THEOREM_AND_METHOD_BOUNDARY", "recorded_at_utc": "2026-08-06T03:10:00Z", "status": "SEALED", "epistemic_status": "PROVED",
            "outcome": "For K_{5,5}\\C_{10}, every bounded stationary density-tangent direction at a positive rank-one bigraphon has nonnegative deficit Hessian. The exact 30/30/150 edge-pair Gram decomposition and two independent rational finite-step coefficient replays pass.",
            "claim_boundary": "This is conditional second-variation positivity only. It proves no local minimum, feasible-neighborhood positivity, higher-order control, global Sidorenko inequality, counterexample, or novelty claim.",
            "cycle_decision": {"companion_identity": "/root/oracle_c88_retry (Oracle)", "companion_advice": "Seal after the explicit density-term, hypotheses, L=0, and source-overlap audit; do not add grids, higher-order expansions, or general regular extensions.", "decision": "Seal the scoped stationary-Hessian theorem and its method boundary, then return to portfolio discovery.", "falsifier": "A legal bounded rank-one tangent direction with negative Hessian, an orbit-count error, a coefficient replay mismatch, or an exact-overlap source changing the novelty classification."},
            "audit": audit(), "frozen_hashes": freeze_inputs(ROOT, {key: (ROOT / path, digest) for key, (path, digest) in HASHES.items()}), "runtime": check_runtime("c89"),
            "sealer": {"path": "proof/build_cycle_89_sidorenko_rank_one_hessian_boundary.py", "sha256": sha256(Path(__file__))},
            "replay": {"finite": ".venv/bin/python proof/check_cycle89_rank_one_escape.py", "orbits": ".venv/bin/python proof/check_cycle89_rank_one_symbolic.py", "coefficient_replay": ".venv/bin/python proof/check_cycle89_rank_one_symbolic_replay.py", "tests": ".venv/bin/python -c \"import runpy; runpy.run_path('tests/test_cycle89_rank_one_symbolic.py')['test_c89_rank_one_symbolic_replay'](); runpy.run_path('tests/test_cycle89_rank_one_escape.py')['test_c89_rank_one_escape_control']()\"", "check": ".venv/bin/python proof/build_cycle_89_sidorenko_rank_one_hessian_boundary.py --check"}}


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
