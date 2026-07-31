#!/usr/bin/env python3
"""Replay the target-blind exact B2 packet/ray Artin transport."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
EFFECTIVE = ROOT.parent / "effective-stark-sweep"
GP = ROOT / "proof" / "audit_b2_packet_frobenius.gp"

EXPECTED = {
    "RQ-000129": (3, "inverse"),
    "RQ-001280": (3, "inverse"),
    "RQ-001569": (1, "direct"),
    "RQ-001894": (1, "direct"),
    "RQ-007519": (3, "inverse"),
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_blocks(text: str) -> dict[str, dict[str, str]]:
    records: dict[str, dict[str, str]] = {}
    current: dict[str, str] | None = None
    for line in text.splitlines():
        if line.startswith("CASE_ID="):
            case_id = line.split("=", 1)[1]
            current = {"CASE_ID": case_id}
            records[case_id] = current
        elif current is not None and "=" in line:
            key, value = line.split("=", 1)
            current[key] = value
    return records


def main() -> None:
    forbidden_paths = (
        "all-five-phase-gates-v1.json",
        "certified-controls-v1.json",
        "control-phase-audit-v1.json",
    )
    gp_source = GP.read_text(encoding="utf-8")
    for forbidden in forbidden_paths:
        if forbidden in gp_source:
            raise RuntimeError(f"target-bearing input referenced: {forbidden}")

    completed = subprocess.run(
        ["gp", "-q", str(GP)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=600,
    )
    clean_stderr = re.sub(r"\x1b\[[0-9;]*m", "", completed.stderr)
    fatal_stderr = "\n".join(
        line
        for line in clean_stderr.splitlines()
        if line.strip() and "Warning:" not in line
    )
    if (
        completed.returncode != 0
        or fatal_stderr
        or "B2_PACKET_FROBENIUS_AUDIT=PASS" not in completed.stdout
    ):
        raise RuntimeError(completed.stdout + "\n" + completed.stderr)
    records = parse_blocks(completed.stdout)
    if set(records) != set(EXPECTED):
        raise RuntimeError(f"case set changed: {sorted(records)}")

    for case_id, (exponent, orientation) in EXPECTED.items():
        record = records[case_id]
        if int(record["CHI_OF_GAMMA_EXPONENT"]) != exponent:
            raise RuntimeError(f"{case_id}: character exponent changed")
        if record["DEDEKIND_TO_ANALYTIC_ORIENTATION"] != orientation:
            raise RuntimeError(f"{case_id}: transport orientation changed")
        if record["PACKET_FROBENIUS_GATE"] != "PASS":
            raise RuntimeError(f"{case_id}: packet Frobenius gate failed")
        if int(record["GAMMA_EQUALS_FROBENIUS_POWER"]) not in (1, 3):
            raise RuntimeError(f"{case_id}: gamma lost its Frobenius transport")

    q35_config = load(
        EFFECTIVE / "data" / "engine-c-character-selection-cases-v1.json"
    )
    e6_config = load(
        EFFECTIVE / "data" / "engine-c-e6-tranche-01-selection-v1.json"
    )
    exact_routes = [
        row
        for row in q35_config["records"] + e6_config["records"]
        if row["case_id"] in EXPECTED
    ]
    route_counts: dict[str, int] = {}
    source_characters: dict[str, set[str]] = {}
    for row in exact_routes:
        route_counts[row["case_id"]] = route_counts.get(row["case_id"], 0) + 1
        source_characters.setdefault(row["case_id"], set()).add(
            row["source_character"]
        )
    if route_counts != {
        "RQ-001280": 2,
        "RQ-001569": 2,
        "RQ-001894": 2,
        "RQ-007519": 2,
    }:
        raise RuntimeError(f"secondary-route inventory changed: {route_counts}")
    if any(len(values) != 1 for values in source_characters.values()):
        raise RuntimeError("a secondary route changed its source character")

    output = {
        "schema": "dedekind-stark-b2-artin-transport-replay-v1",
        "status": "PASS_EXACT_TRANSPORT_WITH_CONTAINED_EXPOSURE",
        "cases": {
            case_id: {
                "chi_of_constructor_gamma": f"i^{exponent}",
                "dedekind_to_analytic_orientation": orientation,
            }
            for case_id, (exponent, orientation) in EXPECTED.items()
        },
        "checks": {
            "target_bearing_paths_absent_from_gp": True,
            "constructor_gamma_is_primitive_separator_frobenius_power": True,
            "source_ray_character_evaluated_exactly_all_cases": True,
            "nonquarantined_secondary_route_source_characters_agree": True,
            "old_phase_orientation_strings_read_by_replay": False,
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    print("B2_ARTIN_TRANSPORT_AUDIT=PASS", file=sys.stderr)


if __name__ == "__main__":
    main()
