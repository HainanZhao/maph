#!/usr/bin/env python3
"""Verify that research is active without an external sequencing gate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    original = json.loads(
        (ROOT / "data" / "sequencing-gate-v1.json").read_text()
    )
    amendment = json.loads(
        (ROOT / "data" / "sequencing-gate-v2.json").read_text()
    )
    active = json.loads(
        (ROOT / "data" / "research-activation-v3.json").read_text()
    )
    checks = {
        "original_preserved_closed": not original["activated"],
        "intermediate_amendment_preserved": amendment["activated"],
        "research_activated": active["activated"],
        "no_external_gate": active["verdict"]
        == "RESEARCH_ACTIVE_NO_EXTERNAL_SEQUENCING_GATE",
        "paper_metadata_administrative": active["administrative_metadata"][
            "paper_identifiers"
        ]
        == "TRACKED_SEPARATELY_NOT_A_RESEARCH_GATE",
        "correspondence_administrative": active["administrative_metadata"][
            "kopp_correspondence"
        ]
        == "TRACKED_SEPARATELY_NOT_A_RESEARCH_GATE",
        "history_superseded": set(active["supersedes_active_use_of"])
        == {
            "data/sequencing-gate-v1.json",
            "data/sequencing-gate-v2.json",
        },
        "intermediate_identifiers_not_invented": all(
            amendment["prerequisites"][paper][field] is None
            for paper in ("paper_I", "paper_II")
            for field in ("artifact_doi", "arxiv_id")
        ),
        "intermediate_letter_not_claimed_sent": amendment["prerequisites"][
            "kopp_correspondence"
        ]["sent_at_utc"]
        is None,
    }
    failed = [name for name, passed in checks.items() if not passed]
    print(f"CHECK_COUNT={len(checks)}")
    print(f"FAILED_CHECK_COUNT={len(failed)}")
    print(f"ACTIVATION_AUTHORIZED={int(not failed)}")
    print(f"VERDICT={active['verdict'] if not failed else 'ACTIVATION_AUDIT_FAILED'}")
    if failed:
        print(f"FAILED={failed}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
