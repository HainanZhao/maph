#!/usr/bin/env python3
"""Execute an exact, closure-batched Engine-B W2 tranche.

The normal closure, rather than a census occurrence, is the unit of work.
For each requested canonical representative this driver:

1. reruns the corrected two-route screen in a fresh PARI process;
2. requires every abelian imaginary route to reconstruct the frozen
   normal closure;
3. selects the matching route with the shortest divisor table; and
4. emits the complete exact Shintani divisor/exponent table for that
   route.

This script deliberately does not attempt W3.  A W2 closure certificate
must not be mistaken for an identified Stark packet.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "artifacts" / "post-theorem-bulk-plan-v1.json"
B_SOURCE = ROOT / "artifacts" / "engine-b-two-route-analysis-v1.json"
SCREEN = ROOT / "scripts" / "screen_engine_b_two_route.gp"
DIVISORS = ROOT / "scripts" / "compute_imaginary_divisor_exponent.gp"
ARTIFACTS = ROOT / "artifacts"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def scalar(lines: list[str], key: str) -> str:
    prefix = f"{key}="
    values = [line[len(prefix):] for line in lines if line.startswith(prefix)]
    if len(values) != 1:
        raise RuntimeError(f"expected exactly one {key}, got {len(values)}")
    return values[0]


def run_gp(prelude: str, script: Path, timeout: int) -> str:
    completed = subprocess.run(
        ["gp", "-q"],
        input=(prelude + script.read_text()).encode(),
        capture_output=True,
        cwd=ROOT,
        timeout=timeout,
    )
    if completed.returncode:
        raise RuntimeError(
            f"{script.name}: GP exit {completed.returncode}\n"
            f"stdout:\n{completed.stdout.decode(errors='replace')}\n"
            f"stderr:\n{completed.stderr.decode(errors='replace')}"
        )
    return completed.stdout.decode(errors="replace")


def parse_matrix(text: str) -> list[list[int]]:
    match = re.fullmatch(
        r"\[\s*(-?\d+)\s*,\s*(-?\d+)\s*;\s*"
        r"(-?\d+)\s*,\s*(-?\d+)\s*\]",
        text,
    )
    if not match:
        raise RuntimeError(f"cannot parse 2x2 HNF matrix: {text}")
    a, b, c, d = (int(value) for value in match.groups())
    return [[a, b], [c, d]]


def parse_quadratic(text: str) -> tuple[int, int]:
    compact = text.replace(" ", "")
    match = re.fullmatch(r"x\^2(?P<linear>[+-]x)?(?P<const>[+-]\d+)?", compact)
    if not match:
        raise RuntimeError(f"cannot parse monic quadratic: {text}")
    linear = {"-x": -1, "+x": 1, None: 0}[match.group("linear")]
    constant = int(match.group("const") or 0)
    return linear, constant


def route_records(lines: list[str]) -> list[dict]:
    count = int(scalar(lines, "ROUTE1_ABELIAN_IMAGINARY_BASE_COUNT"))
    routes = []
    for index in range(1, count + 1):
        match = int(
            scalar(
                lines,
                f"ROUTE2_BASE_{index}_RAY_SUBFIELD_ABSOLUTE_MATCH",
            )
        )
        routes.append(
            {
                "route_index": index,
                "base_polynomial": scalar(
                    lines, f"ROUTE2_BASE_{index}_POLYNOMIAL"
                ),
                "conductor_hnf": parse_matrix(
                    scalar(lines, f"ROUTE2_BASE_{index}_CONDUCTOR")
                ),
                "divisor_count": int(
                    scalar(lines, f"ROUTE2_BASE_{index}_DIVISOR_COUNT")
                ),
                "ray_order": int(
                    scalar(lines, f"ROUTE2_BASE_{index}_RAY_ORDER")
                ),
                "subfield_relative_degree": int(
                    scalar(
                        lines,
                        f"ROUTE2_BASE_{index}_SUBFIELD_RELATIVE_DEGREE",
                    )
                ),
                "normal_closure_match": bool(match),
            }
        )
    return routes


def execute_closure(
    plan_item: dict,
    census_record: dict,
    timeout: int,
    run_timestamp: str,
) -> dict:
    case_id = plan_item["canonical_representative"]
    input_hnf = census_record["finite_ideal_hnf"]
    screen_prelude = (
        f'CASE_ID="{case_id}";\n'
        f'D_VALUE={census_record["d"]};\n'
        f"H11={input_hnf[0][0]};H12={input_hnf[0][1]};"
        f"H21={input_hnf[1][0]};H22={input_hnf[1][1]};\n"
    )
    screen_text = run_gp(screen_prelude, SCREEN, timeout)
    screen_lines = [
        line.strip() for line in screen_text.splitlines() if line.strip()
    ]
    if scalar(screen_lines, "ENGINE_B_TWO_ROUTE_SCREEN_COMPLETE") != "1":
        raise RuntimeError(f"{case_id}: incomplete two-route screen")
    measured_closure = scalar(
        screen_lines, "NORMAL_CLOSURE_ABSOLUTE_FIELD"
    )
    if measured_closure != plan_item["normal_closure_absolute_field"]:
        raise RuntimeError(f"{case_id}: frozen normal closure changed")
    routes = route_records(screen_lines)
    if not routes or not all(route["normal_closure_match"] for route in routes):
        raise RuntimeError(f"{case_id}: two-route disagreement")
    match_count = int(
        scalar(screen_lines, "TWO_ROUTE_RAY_SUBFIELD_MATCH_COUNT")
    )
    if match_count != len(routes):
        raise RuntimeError(
            f"{case_id}: {match_count} matches for {len(routes)} routes"
        )

    selected = min(
        routes,
        key=lambda route: (
            route["divisor_count"],
            route["ray_order"],
            route["route_index"],
        ),
    )
    base_a, base_b = parse_quadratic(selected["base_polynomial"])
    conductor = selected["conductor_hnf"]
    divisor_prelude = (
        f'CASE_ID="{case_id}";\n'
        f'ROUTE_LABEL="route-{selected["route_index"]}-minimum-divisors";\n'
        f"BASE_A={base_a};BASE_B={base_b};\n"
        f"H11={conductor[0][0]};H12={conductor[0][1]};"
        f"H21={conductor[1][0]};H22={conductor[1][1]};\n"
    )
    divisor_text = run_gp(divisor_prelude, DIVISORS, timeout)
    divisor_lines = [
        line.strip() for line in divisor_text.splitlines() if line.strip()
    ]
    if scalar(
        divisor_lines, "GENERIC_IMAGINARY_DIVISOR_TABLE_VERIFIED"
    ) != "1":
        raise RuntimeError(f"{case_id}: incomplete divisor audit")
    measured_divisor_count = int(
        scalar(divisor_lines, "SHINTANI_DIVISOR_COUNT")
    )
    if measured_divisor_count != selected["divisor_count"]:
        raise RuntimeError(
            f"{case_id}: route screen/divisor table count mismatch"
        )

    stem = case_id.lower().replace("-", "")
    transcript = ARTIFACTS / f"{stem}-b-closure-w2-v1.transcript"
    transcript.write_text(
        "===== EXACT TWO-ROUTE RECONSTRUCTION =====\n"
        + screen_text
        + "\n===== PRINTED SHINTANI DIVISOR TABLE =====\n"
        + divisor_text
    )
    certificate = {
        "schema": "effective-stark-engine-b-closure-w2-v1",
        "claim_tag": "VERIFIED_W2",
        "run_timestamp_utc": run_timestamp,
        "canonical_representative": case_id,
        "closure_index": plan_item["closure_index"],
        "member_case_ids": plan_item["case_ids"],
        "member_occurrence_count": plan_item["occurrence_count"],
        "real_quadratic_field_d": census_record["d"],
        "finite_ideal_hnf": input_hnf,
        "finite_norm": census_record["finite_norm"],
        "normal_closure_degree": plan_item["normal_closure_degree"],
        "normal_closure_absolute_field": measured_closure,
        "two_route": {
            "abelian_imaginary_route_count": len(routes),
            "matching_route_count": match_count,
            "all_routes_reconstruct_identical_closure": True,
            "routes": routes,
        },
        "selected_divisor_route": {
            **selected,
            "selection_rule": (
                "minimum divisor count, then ray order, then route index"
            ),
            "safe_exponent": int(
                scalar(divisor_lines, "SHINTANI_SAFE_EXPONENT")
            ),
            "clearing_exponents": scalar(
                divisor_lines, "SHINTANI_CLEARING_EXPONENTS"
            ),
            "distribution_indices": scalar(
                divisor_lines, "SHINTANI_DISTRIBUTION_INDICES"
            ),
            "w_values": scalar(divisor_lines, "SHINTANI_W_VALUES"),
            "base_class_number": int(
                scalar(divisor_lines, "BASE_CLASS_NUMBER")
            ),
            "base_roots_of_unity": int(
                scalar(divisor_lines, "BASE_ROOTS_OF_UNITY")
            ),
            "base_bnfcertify": int(
                scalar(divisor_lines, "BASE_BNFCERTIFY")
            ),
        },
        "w3": {
            "state": "PENDING",
            "claim": (
                "No packet identification or analytic equality is claimed "
                "by this W2 certificate."
            ),
            "required_gate": (
                "exact packet plus Arb enclosure at >=100x Voutier margin "
                "and explicit d<=2 fallback"
            ),
        },
        "source_hashes": {
            str(path.relative_to(ROOT)): sha256(path)
            for path in (PLAN, B_SOURCE, SCREEN, DIVISORS)
        },
        "transcript": {
            "path": str(transcript.relative_to(ROOT)),
            "sha256": sha256(transcript),
        },
    }
    certificate_path = ARTIFACTS / f"{stem}-b-closure-w2-v1.json"
    certificate_path.write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    )
    return {
        "case_id": case_id,
        "closure_index": plan_item["closure_index"],
        "member_occurrence_count": plan_item["occurrence_count"],
        "selected_base": selected["base_polynomial"],
        "divisor_count": measured_divisor_count,
        "safe_exponent": certificate["selected_divisor_route"][
            "safe_exponent"
        ],
        "classification": "VERIFIED_W2",
        "w3": "PENDING",
        "certificate_path": str(certificate_path.relative_to(ROOT)),
        "certificate_sha256": sha256(certificate_path),
        "transcript_path": str(transcript.relative_to(ROOT)),
        "transcript_sha256": sha256(transcript),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-id", action="append", required=True)
    parser.add_argument("--timeout", type=int, default=3600)
    parser.add_argument(
        "--output-stem", default="engine-b-closure-tranche-01-v1"
    )
    arguments = parser.parse_args()

    plan = json.loads(PLAN.read_text())
    b_source = json.loads(B_SOURCE.read_text())
    by_case = {row["case_id"]: row for row in b_source["records"]}
    by_canonical = {
        row["canonical_representative"]: row
        for row in plan["engine_b"]["remaining_closures"]
    }
    requested = arguments.case_id
    if len(requested) != len(set(requested)):
        raise RuntimeError("duplicate --case-id")
    missing = sorted(set(requested) - set(by_canonical))
    if missing:
        raise RuntimeError(
            f"not remaining canonical representatives: {missing}"
        )

    run_timestamp = datetime.now(timezone.utc).isoformat()
    records = []
    for index, case_id in enumerate(requested, start=1):
        print(f"{index}/{len(requested)} {case_id}", flush=True)
        records.append(
            execute_closure(
                by_canonical[case_id],
                by_case[case_id],
                arguments.timeout,
                run_timestamp,
            )
        )

    output = {
        "schema": "effective-stark-engine-b-closure-tranche-v1",
        "claim_tag": "VERIFIED_W2_TRANCHE",
        "run_timestamp_utc": run_timestamp,
        "selection": (
            "explicit bounded tranche of remaining canonical normal-closure "
            "representatives; no member-occurrence transport in this run"
        ),
        "closure_count": len(records),
        "member_occurrence_count": sum(
            row["member_occurrence_count"] for row in records
        ),
        "w3_verified_count": 0,
        "w3_pending_count": len(records),
        "records": records,
    }
    output_path = ARTIFACTS / f"{arguments.output_stem}.json"
    output_path.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
