#!/usr/bin/env python3
"""Rank canonical dimensions by actual unconditional theorem coverage.

The local order-ray quotient is computed directly in O_d/d O_d.  PARI
supplies the maximal-order ray field at the multiplier modulus d*f and
the exact Shintani index.  Comparing ray orders determines whether the
natural maximal-order-to-order-ray map is an isomorphism.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path
import subprocess

from analyze_canonical_order_character_obstruction import LocalRayQuotient


ROOT = Path(__file__).resolve().parents[1]
GP_SCRIPT = ROOT / "scripts/screen_higher_dimension_theorem_coverage.gp"


def parse_value(value: str) -> object:
    stripped = value.strip()
    if stripped.startswith("["):
        return ast.literal_eval(stripped)
    return int(stripped)


def maximal_order_records() -> list[dict[str, object]]:
    process = subprocess.run(
        ["gp", "-q", str(GP_SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    records: list[dict[str, object]] = []
    for line in process.stdout.splitlines():
        if not line.startswith("DIMENSION="):
            continue
        record: dict[str, object] = {}
        for field in line.split("|"):
            key, value = field.split("=", 1)
            record[key.lower()] = parse_value(value)
        records.append(record)
    return records


def classification(record: dict[str, object]) -> tuple[str, list[str]]:
    reasons: list[str] = []
    dimension = int(record["dimension"])
    isomorphic = bool(record["order_to_maximal_ray_isomorphism"])
    shintani_index = int(record["shintani_index"])
    local_exponent = int(record["local_one_place_ray_kernel_exponent"])
    ray_order = int(record["order_ray_order"])

    if dimension in (4, 5, 7, 8):
        return "proved-control", ["existing unconditional benchmark"]
    if dimension == 6:
        return (
            "analytic-theorem-boundary",
            [
                "one primitive order-six scalar remains",
                "conductor lowering and current Stark theorems do not "
                "separate it",
            ],
        )
    if isomorphic and shintani_index == 2:
        reasons.extend(
            [
                "order ray field equals the multiplier-modulus ray field",
                "one-place field is quadratic over its maximal "
                "absolutely abelian subfield",
            ]
        )
        if ray_order <= 16:
            return "best-candidate", reasons
        return "shintani-covered-large", reasons
    if shintani_index == 2:
        reasons.extend(
            [
                "maximal multiplier ray field passes Shintani's index-two test",
                "order/maximal ray map has a nontrivial kernel",
            ]
        )
        return "conductor-lowering-needed", reasons
    if local_exponent <= 6:
        reasons.append("small nonquadratic character exponent")
        return "open-small-packet", reasons
    reasons.append("large primitive character packet")
    return "defer", reasons


def main() -> None:
    records = maximal_order_records()
    combined: list[dict[str, object]] = []
    for record in records:
        dimension = int(record["dimension"])
        if dimension == 4:
            local: dict[str, object] = {
                "dimension": 4,
                "residue_unit_group_order": 12,
                "local_one_place_ray_kernel_order": 2,
                "local_one_place_ray_kernel_exponent": 2,
                "element_order_distribution": {"1": 1, "2": 1},
                "sign_class_nontrivial": True,
            }
        else:
            local = LocalRayQuotient(dimension).quotient_data()
        order_class_number = int(record["order_class_number"])
        order_ray_order = (
            int(local["local_one_place_ray_kernel_order"])
            * order_class_number
        )
        maximal_ray_order = int(record["maximal_one_ray_order"])
        record.update(local)
        record["order_ray_order"] = order_ray_order
        record["order_to_maximal_ray_isomorphism"] = (
            order_ray_order == maximal_ray_order
        )
        category, reasons = classification(record)
        record["classification"] = category
        record["classification_reasons"] = reasons
        combined.append(record)

    result = {
        "schema": "sic-stark-higher-dimension-theorem-coverage-v2",
        "audited_dimensions": [
            int(record["dimension"]) for record in combined
        ],
        "criterion": (
            "Prefer an isomorphic order/maximal ray bridge and "
            "Shintani index [H:H intersection Q_ab]=2."
        ),
        "closed_dimensions": [4, 5, 7, 8],
        "next_exact_tcc_target": 9,
        "next_analytic_theorem_target": 6,
        "records": combined,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
