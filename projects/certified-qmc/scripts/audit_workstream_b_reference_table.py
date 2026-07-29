#!/usr/bin/env python3
"""Certify every dimension in the frozen vector-only UNSW prefix."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.certificate import build_certificate, canonical_sha256


TARGETS = ROOT / "data" / "phase0-targets.json"
INVENTORY = ROOT / "data" / "workstream-b-table-inventory.json"
OUTPUT = ROOT / "certificates" / "workstream-b-unsw-prefix-reference-table.json"


def main() -> None:
    target_data = json.loads(TARGETS.read_text())
    inventory = json.loads(INVENTORY.read_text())
    target = target_data["targets"][0]
    frozen = inventory["frozen_audit_set"][0]

    if target["id"] != frozen["id"]:
        raise RuntimeError("target and schema inventory IDs disagree")
    if frozen["merit_column_present"]:
        raise RuntimeError("reference-table path requires a vector-only source")
    if target["full_table_vendored"]:
        raise RuntimeError("this script is scoped to the frozen prefix")

    modulus = int(target["modulus"])
    generator = [int(value) for value in target["vendored_prefix"]]
    rows = []
    for dimension in range(1, len(generator) + 1):
        weights = [
            Fraction(1, index * index)
            for index in range(1, dimension + 1)
        ]
        core = build_certificate(
            modulus,
            generator[:dimension],
            weights,
        )
        rows.append(
            {
                "dimension": dimension,
                "generator_component": generator[dimension - 1],
                "core_certificate": core,
            }
        )

    payload = {
        "schema": "certified-qmc-workstream-b-reference-table-v1",
        "tag": "VERIFIED_REFERENCE_TABLE_PREFIX",
        "classification_track": "CERTIFIED_REFERENCE_MERIT_ONLY",
        "published_merit_values_present": False,
        "external_merit_subtractions_performed": False,
        "target": {
            "id": target["id"],
            "source": target["source"],
            "url": target["url"],
            "index_url": target["index_url"],
            "upstream_sha256": target["upstream_sha256"],
            "upstream_bytes": target["upstream_bytes"],
            "upstream_lines": target["upstream_lines"],
            "modulus": modulus,
            "weight_model": target["weight_model"],
            "scope": "vendored 16-component prefix",
            "full_upstream_table_certified": False,
        },
        "normalization": {
            "convention": "DKS2013-eq5.13-beta0-product-B2",
            "kernel": "B2(x)=x^2-x+1/6",
            "weights": "gamma_j=1/j^2",
        },
        "dimensions": list(range(1, len(generator) + 1)),
        "rows": rows,
        "claim_boundary": (
            "exact squared worst-case merits for the frozen prefix only; "
            "not an audit of the unvendored 3600-component source and not "
            "an integration-error claim"
        ),
    }
    payload["table_sha256"] = canonical_sha256(payload)
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(OUTPUT)


if __name__ == "__main__":
    main()
