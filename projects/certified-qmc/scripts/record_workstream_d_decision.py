#!/usr/bin/env python3
"""Record the prospectively human-selected Workstream-D disposition."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.certificate import canonical_sha256


BRIEF = ROOT / "docs" / "workstream-d-decision-brief.md"
DEFAULT_OUTPUT = ROOT / "data" / "workstream-d-decision.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--decision",
        choices=(
            "internal-pricing-stack",
            "public-benchmark",
            "defer-workstream-d",
        ),
        required=True,
    )
    parser.add_argument(
        "--human-response",
        required=True,
        help="verbatim or faithful concise record of the human direction",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise ValueError(
            "Workstream-D decision already exists; amend prospectively "
            "with a new version rather than overwriting it"
        )
    payload = {
        "schema": "certified-qmc-workstream-d-human-decision-v1",
        "recorded_at_utc": utc_now(),
        "human_decision": args.decision,
        "human_response": args.human_response,
        "decision_brief": {
            "path": str(BRIEF.relative_to(ROOT)),
            "sha256": sha256(BRIEF.read_bytes()).hexdigest(),
        },
        "workstream_d_scoping_authorized": (
            args.decision != "defer-workstream-d"
        ),
        "boundary": (
            "This records the required human disposition. It does not "
            "certify an application, authorize a broader claim, or "
            "change any Cycles 013-019 arithmetic artifact."
        ),
    }
    payload["decision_sha256"] = canonical_sha256(payload)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(output)


if __name__ == "__main__":
    main()
