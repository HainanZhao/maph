#!/usr/bin/env python3
"""Check C66's literature/logic pivot packet against sealed prior claims."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery" / "out" / "cycle66-pivot-audit"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def audit() -> dict[str, object]:
    c64 = load(ROOT / "artifacts" / "cycle-64-b064-fiber-minimization-v1.json")
    c65 = load(ROOT / "artifacts" / "cycle-65-b065-step-graphon-v2.json")
    text = (ROOT / "discovery" / "cycle66_pivot_audit.md").read_text(encoding="utf-8")
    assert c64["audit"]["exact_reduction"]["resultant_u_degree"] == 26
    assert c64["audit"]["exact_reduction"]["maximum_isolated_pairs"] == 156
    assert c65["cycle_decision"]["decision"].startswith("The preregistered hard stop")
    for required in (
        "https://arxiv.org/html/2606.15368v1",
        "https://arxiv.org/abs/1910.08454",
        "https://arxiv.org/abs/1004.3026",
        "fixed-`S3` Zhao comparison",
        "boundary positivity",
        "does not imply the Möbius graph is",
    ):
        assert required in text
    result = {
        "status": "PASS",
        "epistemic_status": "OBSERVED",
        "logical_interface": {
            "epistemic_status": "PROVED",
            "fixed_group": "S3",
            "target_graph": "K5,5-C10",
            "source_theorem": "Zhao Theorem 1.3",
            "universal_group_hypothesis_required_for_sidorenko": True,
            "fixed_s3_implies_sidorenko": False,
        },
        "banked_reduction": {
            "epistemic_status": "PROVED",
            "resultant_u_degree": 26,
            "maximum_isolated_pairs_per_fiber": 156,
            "remaining_outer_dimension": 3,
        },
        "novelty": {
            "epistemic_status": "CONJECTURED",
            "bounded_primary_search_found_exact_overlap": False,
        },
        "decision": "Pivot to a bounded fixed-S3 boundary-positivity closure engine.",
        "claim_boundary": (
            "The audit supports a scoped pivot, not a novelty priority claim, "
            "fixed-S3 sign theorem, universal Zhao comparison, or Sidorenko theorem."
        ),
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "packet-audit.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return result


def main() -> int:
    print(json.dumps(audit(), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
