#!/usr/bin/env python3
"""Read-only exact replay of the complete sealed Cycle-1 Route A."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify() -> dict[str, object]:
    baseline = load_module("cycle1_route_a_baseline", "proof/replay_baseline_route_a.py")
    expected_baseline = json.loads((ROOT / "artifacts/baseline-route-a-v3.json").read_text())
    computed_baseline = baseline.compute_certificate()
    computed_baseline["frozen_source"] = baseline.FROZEN_SOURCE
    computed_baseline["supersedes"] = {
        "artifact": "artifacts/baseline-route-a-v2.json",
        "mathematical_certificate_sha256": baseline.PREVIOUS_MATHEMATICAL_CERTIFICATE_SHA256,
        "change": "adds the exact §13.1 zero-density bottleneck-cell evaluation",
    }
    baseline_digest = baseline.canonical_sha256(computed_baseline)
    assert baseline_digest == expected_baseline["mathematical_certificate_sha256"]
    assert computed_baseline == {key: value for key, value in expected_baseline.items() if key not in {"mathematical_certificate_sha256", "replay"}}

    case = load_module("cycle1_route_a_case_split", "proof/replay_theorem_1_2_case_split_route_a_v4.py")
    expected_case = json.loads((ROOT / "artifacts/theorem-1-2-case-split-route-a-v4.json").read_text())
    computed_case = case.theorem_1_2_case_split()
    computed_case.update({
        "artifact_version": case.VERSION,
        "route": case.ROUTE,
        "arithmetic": "exact fractions.Fraction only",
        "frozen_source": case.FROZEN_SOURCE,
    })
    case_digest = case.canonical_sha256(computed_case)
    assert case_digest == expected_case["mathematical_certificate_sha256"]
    assert computed_case == {key: value for key, value in expected_case.items() if key not in {"mathematical_certificate_sha256", "replay"}}
    return {
        "artifact_id": "cycle1-route-a-readonly-replay-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "Exact read-only replay of Cycle-1 Route A arithmetic only, conditional on its frozen published analytic inputs.",
        "status": "PASS",
        "baseline_mathematical_sha256": baseline_digest,
        "case_split_mathematical_sha256": case_digest,
    }


if __name__ == "__main__":
    print(json.dumps(verify(), sort_keys=True))
