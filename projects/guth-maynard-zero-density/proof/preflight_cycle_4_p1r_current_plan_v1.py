#!/usr/bin/env python3
"""Report replaceable, current-Plan P1R operational eligibility."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text).lower()


def evaluate(plan_path: Path) -> dict[str, Any]:
    """Return an OBSERVED current-state report; never a historical proof input."""
    text = plan_path.read_text(encoding="utf-8")
    value = normalized(text)
    required = {
        "p1r_active": "| p1r | active |",
        "fs_branch": "p1r-fs: fixed-splice obstruction",
        "crr_branch": "p1r-crr: critical rational/random compatibility",
        "crr_pre_search": "before any search, a versioned preregistration must freeze:",
        "no_p2_selection": "no p2a/p2b/p2c route is presently selected.",
    }
    present = {label: clause in value for label, clause in required.items()}
    eligible = all(present.values())
    return {
        "artifact_id": "cycle-4-p1r-current-plan-preflight-v1",
        "epistemic_status": "OBSERVED",
        "status": "ELIGIBLE_CURRENT_PLAN" if eligible else "INELIGIBLE_CURRENT_PLAN",
        "claim_boundary": "Mutable operational Plan eligibility only; not a proof, not a preregistration identity, and replaceable after every Plan revision.",
        "plan_path": str(plan_path),
        "required_clauses": present,
        "historical_replay_dependency": "EXCLUDED",
        "discovery_authorization": "PROHIBITED_PENDING_CRR_FORMALIZATION",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, default=ROOT / "PLAN.md")
    args = parser.parse_args()
    if not args.plan.is_file():
        raise RuntimeError(f"current Plan is absent: {args.plan}")
    print(json.dumps(evaluate(args.plan), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
