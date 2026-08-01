#!/usr/bin/env python3
"""Read-only exact replay of the complete sealed Cycle-1 Route B."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
CHECKS = (
    ("proof/replay_baseline_route_b.py", "--check", "artifacts/cycle-1-route-b-baseline.json"),
    ("proof/replay_bottleneck_cell_route_b_v2.py", "--check", "artifacts/cycle-1-route-b-v2-bottleneck-cell.json"),
    ("proof/replay_theorem_1_2_case_split_route_b_v3.py", "--check", "artifacts/cycle-1-route-b-v3-theorem-1-2-case-split.json"),
)


def verify() -> dict[str, object]:
    for command in CHECKS:
        subprocess.run((sys.executable, *command), cwd=ROOT, check=True,
                       capture_output=True, text=True)
    return {
        "artifact_id": "cycle1-route-b-readonly-replay-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "Exact read-only replay of Cycle-1 Route B arithmetic only, conditional on its frozen published analytic inputs.",
        "status": "PASS",
        "checks": [list(command) for command in CHECKS],
    }


if __name__ == "__main__":
    print(json.dumps(verify(), sort_keys=True))
