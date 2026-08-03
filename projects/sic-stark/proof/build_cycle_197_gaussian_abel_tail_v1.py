#!/usr/bin/env python3
"""Seal Cycle 197/B034's scoped Gaussian-Abel tail falsifier."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-197-b034-gaussian-abel-tail-v1.json"
INPUTS = {
    "prior_contour_geometry": (ROOT / "artifacts/cycle-196-b033-endpoint-contour-geometry-v1.json", "086d85549c39c385724c5f3709236b783e6c0ba568b758467b9c5e445774b26f"),
    "preregistration": (ROOT / "docs/cycle-197-b034-gaussian-abel-tail-preregistration-v1.md", "2665a96367a21f0f7dded6c541e31b8a4c637d36fa46091f392cd313c6d5ba3a"),
    "prior_replay": (ROOT / "proof/verify_cycle_196_endpoint_contour_geometry.py", "aa8a98e94b19738040ae7ead70615b53c9e16a760fd67383b9d61de3a3107577"),
    "replay": (ROOT / "proof/verify_cycle_197_gaussian_abel_tail.py", "88d56fc6b9351b205f1e43dcd08374e028709b7add02470f0e6eebb975bdeca1"),
    "regression_test": (ROOT / "tests/test_cycle_197_gaussian_abel_tail.py", "9baf9d78a7d87b894f1bb0d3aa017d13141d02fc29b94b56c2645ab77405bf96"),
    "prototype": (ROOT / "discovery/cycle-197-b034-gaussian-abel-tail-prototype-v1.json", "e626ddae200dc1cdc5b011e27e8e6000f7881c0b6694d07f928e6bfe4253e2e2"),
    "beta_fourier": (ROOT / "scripts/dimension_six_beta_fourier.py", "d47242027af1851ea29b60b8e8c362f42fa5a1634fd0b375e39233b4d87f7a6e"),
    "beta_kernel_match": (ROOT / "scripts/dimension_six_beta_kernel_match.py", "6210819200882c83ebaed4fc74c9cce220a0d09748a8343a8b02a609d1289e27"),
    "d6_paper": (ROOT / "paper/sic-stark-dimension-six-boundary-fusion.tex", "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 197 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads((ROOT / "discovery/cycle-197-b034-gaussian-abel-tail-prototype-v1.json").read_text())
    ledger, asymptotic = result["component_ledger"], result["gaussian_asymptotic"]
    require(ledger["component_count"] == 36 and ledger["nonzero_frequency_count"] == 30 and ledger["zero_frequency_count"] == 6, "frequency census drift")
    require(ledger["all_30_nonzero_components_have_positive_gaussian_laplace_exponent"], "Gaussian exponent drift")
    require(asymptotic["fixed_gaussian_abel_limit_for_nonzero_alpha"] == "DOES_NOT_EXIST_AS_A_FINITE_RAW_LIMIT", "tail conclusion drift")
    return {
        "artifact_id": "cycle-197-b034-gaussian-abel-tail-v1", "cycle": 197, "budget_ordinal": "B034", "epistemic_status": "PROVED", "status": "SEALED_GAUSSIAN_ABEL_RAW_ENDPOINT_LIMIT_FALSIFIED",
        "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "For the single frozen even scalar Gaussian cutoff on the central contour, all 30 nonzero real endpoint components have a nonzero-tail Laplace scale exp(B^2 alpha^2/(4 epsilon)); it has no finite raw limit. The six zero components do not supply a uniform 36-component prescription."},
        "endpoint_constants": result["endpoint_constants"], "component_ledger": ledger, "gaussian_asymptotic": asymptotic, "gate_outcome": result["gate_outcome"], "next_target": result["next_unresolved_boundary"],
        "companion_decision": {"identity": "/root/decision_companion_2", "recommendation": "Seal B034/C197 as PROVED only for failure of the prescribed scalar even-Gaussian Abel family on the 30 nonzero endpoint frequencies.", "known_flaw": "The saddle growth excludes neither contour tilts nor analytic-frequency, hyperfunction, Fresnel, or canonically subtracted distributional boundary values.", "falsifier": "Any tail-asymptotic, nonzero constant, sign/B-factor, frequency census, Gaussian saddle calculation, cancellation analysis, or replay discrepancy.", "next_action": "Open a new cycle defining a source-derived analytic-frequency/hyperfunction continuation on a fixed exponential-type test space, with contour sectors and boundary-value uniqueness frozen before evaluation.", "adopted": True, "reason": "The all-36 preregistered ledger gives the exact scoped Gaussian failure while the claim boundary keeps every alternative endpoint rule open."},
        "preregistration_preflight": {"cycle": 197, "manifest_sha256": sha256(ROOT / "docs/cycle-197-b034-gaussian-abel-tail-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-197-b034-gaussian-abel-tail-preregistration-v1.md --expected-cycle 197 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_197_gaussian_abel_tail.py --output discovery/cycle-197-b034-gaussian-abel-tail-prototype-v1.json", "test_command": "python3 -m unittest tests/test_cycle_197_gaussian_abel_tail.py tests/test_cycle_196_endpoint_contour_geometry.py", "write_command": "python3 proof/build_cycle_197_gaussian_abel_tail_v1.py --write", "check_command": "python3 proof/build_cycle_197_gaussian_abel_tail_v1.py --check"},
        "runtime": runtime, "sealer": {"path": "proof/build_cycle_197_gaussian_abel_tail_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
