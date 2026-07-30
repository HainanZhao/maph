#!/usr/bin/env python3
"""Byte-deterministic generic Engine-C replays for the two hard controls."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
CONFIG = ROOT / "data/engine-c-reproduction-gate-cases-v1.json"
GENERIC_RUNNER = ROOT / "scripts/run_generic_engine_c_character_selection.py"
GP_SOURCE = ROOT / "scripts/generic_engine_c_character_selection.gp"
RQ_CASE = ROOT / "data/rq000458-dual-case-v1.json"
Q6_CASE = ROOT / "data/q6-norm8-case-v1.json"
OUTPUT = ROOT / "artifacts/engine-c-reproduction-gate-v1.json"
TRANSCRIPT = ROOT / "artifacts/engine-c-reproduction-gate-v1.transcript"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_generic_runner():
    spec = importlib.util.spec_from_file_location(
        "generic_engine_c_runner", GENERIC_RUNNER
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load generic selector")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def canonical_bytes(records: list[dict]) -> bytes:
    return (
        json.dumps(records, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")


def execute_once(config: dict, generic) -> tuple[list[dict], str]:
    source = GP_SOURCE.read_text(encoding="utf-8")
    results: list[dict] = []
    transcripts: list[str] = []
    for index, record in enumerate(config["records"], start=1):
        result, transcript = generic.run(
            record, config["coefficient_limit"], source
        )
        for key in (
            "expected_selected_character",
            "expected_e",
            "expected_stark_s_size",
            "theorem_scope",
        ):
            result[key.removeprefix("expected_")] = record[key]
        if (
            result["selected_cm_character"]
            != record["expected_selected_character"]
        ):
            raise RuntimeError(
                f"{record['case_id']}/{record['route_id']}: "
                "selected-character mismatch"
            )
        if (
            result["character_field_roots_of_unity_e"]
            != record["expected_e"]
        ):
            raise RuntimeError(
                f"{record['case_id']}/{record['route_id']}: e mismatch"
            )
        if result["stark_s_size"] != record["expected_stark_s_size"]:
            raise RuntimeError(
                f"{record['case_id']}/{record['route_id']}: |S| mismatch"
            )
        if (
            record["theorem_scope"] == "STARK_1980_GLOBAL_UNIT"
            and not result["global_unit_clause_applies"]
        ):
            raise RuntimeError("global-unit route unexpectedly out of scope")
        if (
            record["theorem_scope"] == "STARK_1980_GLOBAL_UNIT"
            and not result["relative_abelian_certified"]
        ):
            raise RuntimeError("theorem route failed relative-abelian gate")
        if (
            record["theorem_scope"] == "ALGEBRAIC_ONLY_S_SIZE_2"
            and result["global_unit_clause_applies"]
        ):
            raise RuntimeError("algebraic-only boundary unexpectedly moved")
        if not result["relative_abelian_certified"]:
            raise RuntimeError("ray-class round-trip abelian gate failed")
        results.append(result)
        transcripts.append(
            f"===== {index}/{len(config['records'])} "
            f"{record['case_id']} {record['route_id']} =====\n"
            f"{transcript}"
        )
    return results, "\n".join(transcripts)


def verify_banked_cases(records: list[dict]) -> None:
    rq = json.loads(RQ_CASE.read_text(encoding="utf-8"))
    q6 = json.loads(Q6_CASE.read_text(encoding="utf-8"))
    rq_rows = [r for r in records if r["case_id"] == "RQ-000458"]
    q6_rows = [r for r in records if r["case_id"] == "RQ-000129"]
    if len(rq_rows) != 2 or len(q6_rows) != 2:
        raise RuntimeError("hard-control route count changed")
    primary = next(r for r in rq_rows if r["route_id"] == "Qsqrt(-42)")
    fixed_label = next(
        record["banked_fixed_ray_character"]
        for record in json.loads(CONFIG.read_text(encoding="utf-8"))[
            "records"
        ]
        if record["case_id"] == "RQ-000458"
        and record["route_id"] == "Qsqrt(-42)"
    )
    if fixed_label != str(rq["engine_c"]["primary_character"]):
        raise RuntimeError("RQ-000458 fixed-ray bank label changed")
    if primary["source_separator_coefficient"] != primary[
        "selected_separator_coefficient"
    ]:
        raise RuntimeError("RQ-000458 reconstructed-basis character mismatch")
    q6_primary = next(r for r in q6_rows if r["route_id"] == "Qsqrt(-2)")
    normalized_generic = "".join(
        q6_primary["character_field_polynomial"].split()
    )
    normalized_banked = "".join(
        q6["selected_cm_route"]["character_field_polynomial"].split()
    )
    if normalized_generic != normalized_banked:
        raise RuntimeError("Q(sqrt6) primary field disagrees with bank")
    if (
        q6_primary["character_field_roots_of_unity_e"]
        != q6["selected_cm_route"]["roots_of_unity_e"]
    ):
        raise RuntimeError("Q(sqrt6) primary e disagrees with bank")


def main() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    generic = load_generic_runner()
    first, first_transcript = execute_once(config, generic)
    second, second_transcript = execute_once(config, generic)
    first_bytes = canonical_bytes(first)
    second_bytes = canonical_bytes(second)
    if first_bytes != second_bytes:
        raise RuntimeError("generic replay records are not byte-identical")
    if first_transcript.encode() != second_transcript.encode():
        raise RuntimeError("generic replay transcripts are not byte-identical")
    verify_banked_cases(first)
    TRANSCRIPT.write_text(first_transcript, encoding="utf-8")
    q6_secondary = next(
        row
        for row in first
        if row["case_id"] == "RQ-000129"
        and row["route_id"] == "Qsqrt(-3)"
    )
    payload = {
        "schema": "effective-stark-engine-c-reproduction-gate-v1",
        "claim_tag": "VERIFIED_EXACT_REPRODUCTION_GATE",
        "generic_pipeline_execution_count": 2,
        "byte_identical_record_replay": True,
        "byte_identical_transcript_replay": True,
        "rq000458_c_side_reproduced": True,
        "q6_algebraic_half_reproduced": True,
        "q6_secondary_scope": {
            "stark_s_size": q6_secondary["stark_s_size"],
            "promotion": "HALTED_OUTSIDE_GLOBAL_UNIT_CLAUSE",
        },
        "records": first,
        "source_hashes": {
            str(path.relative_to(ROOT)): sha(path)
            for path in (
                CONFIG,
                GP_SOURCE,
                GENERIC_RUNNER,
                RQ_CASE,
                Q6_CASE,
                SELF,
            )
        },
        "transcript": {
            "path": str(TRANSCRIPT.relative_to(ROOT)),
            "sha256": sha(TRANSCRIPT),
        },
        "gate_effect": (
            "The generic exact algebraic pipeline reproduces both hard "
            "controls. This does not remove the Q(sqrt(6)) |S|=2 analytic "
            "scope boundary."
        ),
    }
    serialized = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    OUTPUT.write_text(serialized, encoding="utf-8")
    print("ROUTE_COUNT=4")
    print("GENERIC_EXECUTION_COUNT=2")
    print("BYTE_IDENTICAL_RECORD_REPLAY=1")
    print("BYTE_IDENTICAL_TRANSCRIPT_REPLAY=1")
    print("RQ000458_C_SIDE_REPRODUCED=1")
    print("Q6_ALGEBRAIC_HALF_REPRODUCED=1")
    print(
        "OUTPUT_SHA256="
        + hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    )


if __name__ == "__main__":
    main()
