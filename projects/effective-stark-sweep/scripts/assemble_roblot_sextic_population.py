#!/usr/bin/env python3
"""Propagate deduplicated exact sextic gates to all frozen kernels."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTES = ROOT / "artifacts" / "roblot-sextic-route-inventory-v1.json"
FIELDS = ROOT / "artifacts" / "roblot-sextic-field-inventory-v1.json"
THREECLASS = ROOT / "artifacts" / "roblot-sextic-3class-v1.json"
OUTPUT = ROOT / "artifacts" / "roblot-sextic-population-v1.json"
EXPECTED_CONTROLS = {
    "RQ-000021": (True, False),
    "RQ-000190": (True, False),
    "RQ-000419": (True, False),
    "RQ-002057": (False, True),
    "RQ-002955": (True, False),
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    routes = load(ROUTES)
    fields = load(FIELDS)
    threeclass = load(THREECLASS)
    if routes["status"] != "COMPLETE_EXACT_ROUTE_INVENTORY":
        raise RuntimeError("route inventory is incomplete")
    if fields["status"] != "DEDUPLICATED_FIELD_GATE_SWEEP_COMPLETE":
        raise RuntimeError("field inventory is incomplete")
    if (
        threeclass["status"]
        != "COMPLETE_EXACT_3CLASS_OBSTRUCTION_POPULATION"
    ):
        raise RuntimeError("3-class obstruction population is incomplete")

    field_by_key = {
        record["field_key"]: record for record in fields["records"]
    }
    threeclass_keys = {
        record["field_key"]
        for record in threeclass["records"]
        if record["population"] == "RESIDUAL_FIELD"
    }
    records = []
    for route in routes["records"]:
        if route["status"] != "EXACT_ROUTE_COMPLETE":
            raise RuntimeError("route failure cannot be propagated")
        key = route["field_key"]
        local_pass = route["A3"] and route["S_equals_S_extension"]
        field = field_by_key.get(key)
        if field is None:
            if local_pass:
                raise RuntimeError(
                    f"{route['case_id']}: missing required field screen"
                )
            field_gates = {
                "A1": None,
                "A2": None,
                "class_number_prime_to_3": None,
                "no_wild_prime_above_3": None,
            }
            status = "EXACT_LOCAL_NONAPPLICABILITY"
            class_number_provenance = (
                "NOT_NEEDED_AFTER_EXACT_LOCAL_FAILURE"
            )
        else:
            field_gates = {
                "A1": field["A1"],
                "A2": field["A2"],
                "no_wild_prime_above_3": field[
                    "no_wild_prime_above_3"
                ],
            }
            if field["status"] == "EXACT_FIELD_GATES_COMPLETE":
                field_gates["class_number_prime_to_3"] = field[
                    "class_number_prime_to_3"
                ]
                class_number_provenance = field[
                    "class_number_gate_provenance"
                ]
            elif (
                field["status"] == "NEEDS_STRONG_3_CLASS_CERTIFICATE"
                and key in threeclass_keys
            ):
                field_gates["class_number_prime_to_3"] = False
                class_number_provenance = (
                    "EXACT_UNRAMIFIED_CYCLIC_CUBIC_PROVES_3_DIVIDES"
                )
            else:
                raise RuntimeError(f"{key}: unresolved field gate")
            status = "EXACT_SCREEN_COMPLETE"

        applicable = bool(
            local_pass
            and field_gates["A1"]
            and field_gates["A2"]
            and field_gates["class_number_prime_to_3"]
            and field_gates["no_wild_prime_above_3"]
        )
        records.append(
            {
                "case_id": route["case_id"],
                "kernel_index": route["kernel_index"],
                "inventory_offset": route["inventory_offset"],
                "field_key": key,
                "status": status,
                "applicable": applicable,
                "A1": field_gates["A1"],
                "A2": field_gates["A2"],
                "A3": route["A3"],
                "S_equals_S_extension": route[
                    "S_equals_S_extension"
                ],
                "class_number_prime_to_3": field_gates[
                    "class_number_prime_to_3"
                ],
                "class_number_gate_provenance": (
                    class_number_provenance
                ),
                "no_wild_prime_above_3": field_gates[
                    "no_wild_prime_above_3"
                ],
                "A3_local_rows": route["A3_local_rows"],
                "primitive_conductor": route["primitive_conductor"],
                "primitive_character": route["primitive_character"],
                "primitive_kernel_hnf": route[
                    "primitive_kernel_hnf"
                ],
            }
        )

    controls = {}
    by_case = {}
    for record in records:
        by_case.setdefault(record["case_id"], record)
    for case_id, (expected_applicable, expected_wild) in (
        EXPECTED_CONTROLS.items()
    ):
        record = by_case[case_id]
        passed = (
            record["applicable"] == expected_applicable
            and record["no_wild_prime_above_3"] != expected_wild
        )
        if not passed:
            raise RuntimeError(f"{case_id}: control disagreement")
        controls[case_id] = {
            "expected_applicable": expected_applicable,
            "expected_wild_above_3": expected_wild,
            "passed": True,
        }

    exact_decisions = [
        record
        for record in records
        if record["status"]
        in {"EXACT_SCREEN_COMPLETE", "EXACT_LOCAL_NONAPPLICABILITY"}
    ]
    applicable = [record for record in records if record["applicable"]]
    payload = {
        "schema": "effective-stark-roblot-sextic-population-v1",
        "claim_tag": "PROVED",
        "status": "COMPLETE_EXACT_POPULATION_SCREEN",
        "claim_boundary": {
            "screened": "Roblot 2013 Theorem 7.1 hypotheses only",
            "eligibility_is_not_a_stark_identity": True,
            "local_short_circuit": (
                "field-level gates are not computed when exact A3 or "
                "S equality failure already proves nonapplicability"
            ),
        },
        "source_hashes": {
            "artifacts/roblot-sextic-route-inventory-v1.json": (
                sha256(ROUTES)
            ),
            "artifacts/roblot-sextic-field-inventory-v1.json": (
                sha256(FIELDS)
            ),
            "artifacts/roblot-sextic-3class-v1.json": (
                sha256(THREECLASS)
            ),
        },
        "counts": {
            "inventory_kernels": len(records),
            "exact_applicability_decisions": len(exact_decisions),
            "exact_full_field_screens": sum(
                record["status"] == "EXACT_SCREEN_COMPLETE"
                for record in records
            ),
            "exact_local_nonapplicability": sum(
                record["status"] == "EXACT_LOCAL_NONAPPLICABILITY"
                for record in records
            ),
            "applicable_kernels": len(applicable),
            "applicable_rows": len(
                {record["case_id"] for record in applicable}
            ),
            "nonapplicable_kernels": len(records) - len(applicable),
            "incomplete_kernels": len(records) - len(exact_decisions),
        },
        "frozen_control_replay": controls,
        "records": records,
    }
    OUTPUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
