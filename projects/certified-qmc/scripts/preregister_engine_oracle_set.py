#!/usr/bin/env python3
"""Emit the value-blind engine-oracle selection freeze."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "engine-oracle-set-v1.json"
FROZEN_AT = "2026-07-29T08:15:52Z"
FAMILIES = ("unsw-fixed-29102", "unsw-extensible-39102")


def table_id(family: str, modulus: int, power: int) -> str:
    return f"{family}-n{modulus}-j{power}"


def add_table_entry(
    entries: list[dict],
    seen: set[tuple[str, int, int, int]],
    family: str,
    modulus: int,
    dimension: int,
    power: int,
    stratum: str,
) -> None:
    key = (family, modulus, dimension, power)
    if key in seen:
        return
    seen.add(key)
    entries.append(
        {
            "source_id": family,
            "table_id": table_id(family, modulus, power),
            "N": modulus,
            "dimension": dimension,
            "weight_power": power,
            "selection_stratum": stratum,
        }
    )


def main() -> None:
    entries: list[dict] = []
    seen: set[tuple[str, int, int, int]] = set()

    # Complete low-N prefixes exercise embedded-construction and running
    # product invariants without selecting on an observed merit.
    for family in FAMILIES:
        for dimension in range(1, 65):
            add_table_entry(
                entries,
                seen,
                family,
                1024,
                dimension,
                2,
                "full-prefix-n1024-d1-64",
            )

    # Cross-scale anchors include forced d=1, practical middle prefixes,
    # and the maximal published prefix at every remaining N.
    for family in FAMILIES:
        for exponent in range(11, 21):
            modulus = 1 << exponent
            for dimension in (1, 16, 64, 256, 1024, 3600):
                add_table_entry(
                    entries,
                    seen,
                    family,
                    modulus,
                    dimension,
                    2,
                    "cross-scale-j2",
                )

    # Complete the N=1024 extreme-dimension anchors.
    for family in FAMILIES:
        for dimension in (256, 1024, 3600):
            add_table_entry(
                entries,
                seen,
                family,
                1024,
                dimension,
                2,
                "n1024-extreme-d",
            )

    # Every nonduplicated usability-grid result covers the two alternate
    # profiles. The j^-2 members are already structurally represented.
    for family in FAMILIES:
        for modulus in (1024, 32768, 1048576):
            for dimension in (16, 64, 256):
                for power in (1, 3):
                    add_table_entry(
                        entries,
                        seen,
                        family,
                        modulus,
                        dimension,
                        power,
                        "alternate-weight-profile",
                    )

    adversarial = [
        {
            "case_id": "ordinary-n32",
            "N": 32,
            "prefix": [1, 7],
            "weights": ["1", "1/4", "1/9"],
            "candidates": [1, 5],
            "purpose": "ordinary separated comparison",
        },
        {
            "case_id": "sign-tie-n32",
            "N": 32,
            "prefix": [1, 7],
            "weights": ["1", "1/4", "1/9"],
            "candidates": [5, 27],
            "purpose": "exact z versus N-z symmetry tie",
        },
        {
            "case_id": "tiny-weight-n32",
            "N": 32,
            "prefix": [1, 7],
            "weights": ["1", "1/4", "1/100000000000000000000000000000"],
            "candidates": [1, 5],
            "purpose": "near-degenerate tiny new-coordinate weight",
        },
        {
            "case_id": "zero-weight-n64",
            "N": 64,
            "prefix": [1, 5, 13],
            "weights": ["1", "1/4", "1/9", "0"],
            "candidates": [1, 5],
            "purpose": "all-candidate exact tie at zero new weight",
        },
        {
            "case_id": "tiny-weight-n64",
            "N": 64,
            "prefix": [1, 5, 13],
            "weights": [
                "1",
                "1/4",
                "1/9",
                "1/100000000000000000000000000000000000000000000000000",
            ],
            "candidates": [1, 5],
            "purpose": "deep precision escalation stress",
        },
        {
            "case_id": "sign-tie-n64",
            "N": 64,
            "prefix": [1, 5, 13],
            "weights": ["1", "1/4", "1/9", "1/16"],
            "candidates": [5, 59],
            "purpose": "higher-stage exact sign symmetry tie",
        },
        {
            "case_id": "denominator-stress-n64",
            "N": 64,
            "prefix": [1, 5, 13],
            "weights": ["1", "1/6", "1/35", "1/143"],
            "candidates": [1, 5],
            "purpose": "non-factorial coprime denominator stress",
        },
        {
            "case_id": "quotient-competitors-n64",
            "N": 64,
            "prefix": [1, 5, 13],
            "weights": ["1", "1/4", "1/9", "1/16"],
            "candidates": [5, 25],
            "purpose": "same-valuation quotient competitors",
        },
    ]

    if len(entries) != 290:
        raise ArithmeticError(f"expected 290 table entries, got {len(entries)}")
    payload = {
        "schema": "certified-qmc-engine-oracle-preregistration-v1",
        "frozen_at_utc": FROZEN_AT,
        "selection_status": "PREREGISTERED_BEFORE_VALUE_EXTRACTION",
        "claim_boundary": (
            "Software-conformance oracle selected by input structure; "
            "not a representative sample of lattice-rule quality."
        ),
        "artifact_priority": [
            "exact/enclosure evaluator and independent verifier",
            "curated engine oracle/conformance set",
            "supplementary exhaustive fidelity grid",
        ],
        "dependencies": {
            "fidelity_spec": "data/cycles-016-017-fidelity-spec-v2.json",
            "usability_preregistration": (
                "data/cycle-018-usability-preregistration.json"
            ),
            "interpretive_amendment": (
                "docs/artifact-emphasis-amendment.md"
            ),
        },
        "selection_counts": {
            "table_merits": len(entries),
            "adversarial_decision_cases": len(adversarial),
            "total_oracle_cases": len(entries) + len(adversarial),
        },
        "table_merits": entries,
        "adversarial_decision_cases": adversarial,
        "extraction_gate": (
            "Extract only after the supplying fidelity/usability dataset "
            "is sealed and its independent audit passes."
        ),
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["selection_sha256"] = sha256(canonical.encode()).hexdigest()
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(OUTPUT.relative_to(ROOT))
    print(payload["selection_sha256"])
    print(json.dumps(payload["selection_counts"], sort_keys=True))


if __name__ == "__main__":
    main()
