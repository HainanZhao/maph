#!/usr/bin/env python3
"""Inventory exact Stark normalization e-values for C-eligible packets."""

from __future__ import annotations

from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "artifacts/engine-c-geometry-analysis-v1.json"
GEOMETRY_TRANSCRIPT = (
    ROOT / "artifacts/engine-c-geometry-full-v1.transcript"
)
CENSUS = ROOT / "artifacts/frozen-ideal-census-v1.json"
GP_SCRIPT = ROOT / "scripts/screen_engine_c_e_values.gp"
OUTPUT = ROOT / "artifacts/engine-c-e-inventory-v1.json"
TRANSCRIPT = ROOT / "artifacts/engine-c-e-inventory-v1.transcript"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_eligible_packets():
    analysis = json.loads(ANALYSIS.read_text())
    eligible = set(analysis["complete_c_case_ids"])
    records = []
    for block in GEOMETRY_TRANSCRIPT.read_text().split("===== ")[1:]:
        lines = block.splitlines()
        header = re.fullmatch(
            r"(RQ-\d+) PACKET (\d+) =====", lines[0]
        )
        if not header or header.group(1) not in eligible:
            continue
        case_id = header.group(1)
        packet_index = int(header.group(2))
        polynomial = re.search(
            rf"^PACKET_{packet_index}_ABSOLUTE_POLYNOMIAL=(.*)$",
            block,
            re.MULTILINE,
        )
        passed = re.search(
            rf"^PACKET_{packet_index}_C_GEOMETRY_PASS=(\d+)$",
            block,
            re.MULTILINE,
        )
        if polynomial is None or passed is None:
            raise RuntimeError(f"{case_id}/{packet_index}: parse failure")
        if passed.group(1) != "1":
            raise RuntimeError(
                f"{case_id}/{packet_index}: incomplete eligible case"
            )
        records.append({
            "case_id": case_id,
            "packet_index": packet_index,
            "absolute_polynomial": polynomial.group(1),
        })
    if len(eligible) != 728 or len(records) != 1163:
        raise RuntimeError(
            f"eligible count changed: {len(eligible)} cases, "
            f"{len(records)} packets"
        )
    return eligible, records


def scalar(text: str, key: str) -> str:
    values = re.findall(rf"^{re.escape(key)}=(.*)$", text, re.MULTILINE)
    if len(values) != 1:
        raise RuntimeError(f"expected one {key}, got {len(values)}")
    return values[0]


def run_field(record, discriminants, script):
    prelude = (
        f'CASE_ID="{record["case_id"]}";'
        f'PACKET_INDEX={record["packet_index"]};'
        f'D_VALUE={discriminants[record["case_id"]]};'
        f'SOURCE_POLYNOMIAL={record["absolute_polynomial"]};\n'
    )
    completed = subprocess.run(
        ["gp", "-q"],
        input=prelude + script,
        text=True,
        capture_output=True,
        cwd=ROOT,
        timeout=600,
    )
    text = completed.stdout
    if "ENGINE_C_E_INVENTORY_VERIFIED=1" not in text:
        raise RuntimeError(
            f"{record['case_id']}/{record['packet_index']} failed:\n"
            f"stdout:\n{text}\nstderr:\n{completed.stderr}"
        )
    routes = []
    route_count = int(scalar(text, "ROUTE_COUNT"))
    for route in range(1, route_count + 1):
        routes.append({
            "cm_base": scalar(text, f"ROUTE_{route}_CM_BASE"),
            "character_field": scalar(
                text, f"ROUTE_{route}_CHARACTER_FIELD"
            ),
            "e": int(scalar(text, f"ROUTE_{route}_E")),
            "bnfcertify": int(
                scalar(text, f"ROUTE_{route}_BNFCERTIFY")
            ),
        })
    e_values = sorted(route["e"] for route in routes)
    if len(routes) != 2 or any(route["bnfcertify"] != 1 for route in routes):
        raise RuntimeError("route count or bnfcertify changed")
    return {
        **record,
        "routes": routes,
        "e_pair": e_values,
        "minimum_e": min(e_values),
        "transcript": text,
    }


def main():
    eligible, occurrences = parse_eligible_packets()
    census = json.loads(CENSUS.read_text())
    discriminants = {
        row["case_id"]: row["field_discriminant"]
        for row in census["cases"]
    }
    by_polynomial = defaultdict(list)
    for record in occurrences:
        by_polynomial[record["absolute_polynomial"]].append(record)
    if len(by_polynomial) != 393:
        raise RuntimeError(
            f"expected 393 eligible packet fields, got {len(by_polynomial)}"
        )
    representatives = [
        values[0] for _, values in sorted(by_polynomial.items())
    ]
    script = GP_SCRIPT.read_text()
    completed_fields = []
    with ThreadPoolExecutor(max_workers=4) as executor:
        future_map = {
            executor.submit(
                run_field, record, discriminants, script
            ): record
            for record in representatives
        }
        for completed, future in enumerate(
            as_completed(future_map), start=1
        ):
            completed_fields.append(future.result())
            if completed % 25 == 0 or completed == len(future_map):
                print(
                    f"{completed}/{len(future_map)} packet fields",
                    flush=True,
                )
    completed_fields.sort(key=lambda item: item["absolute_polynomial"])

    transcript_parts = []
    field_records = []
    field_by_polynomial = {}
    for index, result in enumerate(completed_fields, start=1):
        occurrences_for_field = by_polynomial[
            result["absolute_polynomial"]
        ]
        field_record = {
            key: value for key, value in result.items()
            if key != "transcript"
        }
        field_record["field_index"] = index
        field_record["occurrence_count"] = len(occurrences_for_field)
        field_record["occurrences"] = [
            {
                "case_id": item["case_id"],
                "packet_index": item["packet_index"],
            }
            for item in occurrences_for_field
        ]
        field_records.append(field_record)
        field_by_polynomial[result["absolute_polynomial"]] = field_record
        transcript_parts.append(
            f"===== FIELD {index}/393 "
            f"{result['case_id']} PACKET {result['packet_index']} =====\n"
            f"{result['transcript']}"
        )
    TRANSCRIPT.write_text("\n".join(transcript_parts))

    field_minimum_histogram = Counter(
        record["minimum_e"] for record in field_records
    )
    occurrence_minimum_histogram = Counter()
    route_field_histogram = Counter()
    route_occurrence_histogram = Counter()
    e_pair_field_histogram = Counter()
    e_pair_occurrence_histogram = Counter()
    cases_to_minima = defaultdict(list)
    for occurrence in occurrences:
        field = field_by_polynomial[occurrence["absolute_polynomial"]]
        multiplicity = 1
        occurrence_minimum_histogram[field["minimum_e"]] += multiplicity
        e_pair = tuple(field["e_pair"])
        e_pair_occurrence_histogram[e_pair] += multiplicity
        for e_value in field["e_pair"]:
            route_occurrence_histogram[e_value] += multiplicity
        cases_to_minima[occurrence["case_id"]].append(field["minimum_e"])
    for field in field_records:
        e_pair_field_histogram[tuple(field["e_pair"])] += 1
        for e_value in field["e_pair"]:
            route_field_histogram[e_value] += 1

    banked_fields = sum(
        count for e_value, count in field_minimum_histogram.items()
        if e_value in (2, 4)
    )
    banked_occurrences = sum(
        count for e_value, count in occurrence_minimum_histogram.items()
        if e_value in (2, 4)
    )
    case_staging = {
        "BANKED_GENERAL_E_2_4": sorted(
            case_id for case_id, minima in cases_to_minima.items()
            if all(value in (2, 4) for value in minima)
        ),
        "BLOCKED_GENERAL_E_GT_4": sorted(
            case_id for case_id, minima in cases_to_minima.items()
            if any(value not in (2, 4) for value in minima)
        ),
    }
    if sum(len(values) for values in case_staging.values()) != 728:
        raise RuntimeError("case staging does not cover 728 cases")

    output = {
        "schema": "effective-stark-engine-c-e-inventory-v1",
        "claim_tag": "VERIFIED_EXACT_INVENTORY",
        "scope": {
            "eligible_case_count": len(eligible),
            "eligible_packet_occurrence_count": len(occurrences),
            "distinct_packet_field_count": len(field_records),
            "routes_per_packet_field": 2,
        },
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (
                ANALYSIS, GEOMETRY_TRANSCRIPT, CENSUS, GP_SCRIPT
            )
        },
        "field_minimum_e_histogram": {
            str(key): value
            for key, value in sorted(field_minimum_histogram.items())
        },
        "occurrence_minimum_e_histogram": {
            str(key): value
            for key, value in sorted(
                occurrence_minimum_histogram.items()
            )
        },
        "route_e_histogram_distinct_fields": {
            str(key): value
            for key, value in sorted(route_field_histogram.items())
        },
        "route_e_histogram_occurrences": {
            str(key): value
            for key, value in sorted(route_occurrence_histogram.items())
        },
        "e_pair_histogram_distinct_fields": {
            ",".join(map(str, key)): value
            for key, value in sorted(e_pair_field_histogram.items())
        },
        "e_pair_histogram_occurrences": {
            ",".join(map(str, key)): value
            for key, value in sorted(
                e_pair_occurrence_histogram.items()
            )
        },
        "banked_e_2_4_field_count": banked_fields,
        "banked_e_2_4_occurrence_count": banked_occurrences,
        "banked_e_2_4_dominates_fields": (
            banked_fields * 2 > len(field_records)
        ),
        "banked_e_2_4_dominates_occurrences": (
            banked_occurrences * 2 > len(occurrences)
        ),
        "case_staging": {
            key: {
                "case_count": len(value),
                "case_ids": value,
            }
            for key, value in case_staging.items()
        },
        "field_records": field_records,
    }
    OUTPUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "field_minimum_e_histogram":
            output["field_minimum_e_histogram"],
        "occurrence_minimum_e_histogram":
            output["occurrence_minimum_e_histogram"],
        "case_staging": {
            key: value["case_count"]
            for key, value in output["case_staging"].items()
        },
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
