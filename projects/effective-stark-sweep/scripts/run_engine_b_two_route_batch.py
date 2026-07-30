#!/usr/bin/env python3
"""Run generalized W2 over a degree-bounded Engine-B queue.

Each case is a fresh PARI process.  A tool crash or timeout is a
TOOL_BLOCKED record, never a mathematical verdict.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "artifacts" / "w1-full-census-v1.json"
C_ANALYSIS = ROOT / "artifacts" / "engine-c-geometry-analysis-v1.json"
GP_SCRIPT = ROOT / "scripts" / "screen_engine_b_two_route.gp"


def scalar(lines: list[str], key: str) -> int:
    prefix = f"{key}="
    values = [line[len(prefix):] for line in lines if line.startswith(prefix)]
    if len(values) != 1:
        raise RuntimeError(f"expected one {key}, got {len(values)}")
    return int(values[0])


def queue() -> list[dict]:
    census = json.loads(CENSUS.read_text())
    records = census["records"]
    by_id = {row["case_id"]: row for row in records}
    result = [row for row in records if row.get("engine") == "B"]
    c_analysis = json.loads(C_ANALYSIS.read_text())
    result.extend(by_id[case_id] for case_id in c_analysis["reroute_b_case_ids"])
    result.sort(key=lambda row: (
        2 * math.prod(row["both_cyc"]),
        row["finite_norm"],
        row["d"],
        row["case_id"],
    ))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-degree", type=int, default=0)
    parser.add_argument("--max-degree", type=int, default=24)
    parser.add_argument("--timeout", type=int, default=3600)
    parser.add_argument("--output-stem", default="engine-b-two-route-degree24-v1")
    arguments = parser.parse_args()
    output = ROOT / "artifacts" / f"{arguments.output_stem}.json"
    transcript = ROOT / "artifacts" / f"{arguments.output_stem}.transcript"

    selected = [
        row for row in queue()
        if (
            arguments.min_degree
            < 2 * math.prod(row["both_cyc"])
            <= arguments.max_degree
        )
    ]
    records: list[dict] = []
    transcript.write_text("")
    for index, row in enumerate(selected, start=1):
        hnf = row["finite_ideal_hnf"]
        prelude = (
            f'CASE_ID="{row["case_id"]}";\n'
            f'D_VALUE={row["d"]};\n'
            f'H11={hnf[0][0]};H12={hnf[0][1]};'
            f'H21={hnf[1][0]};H22={hnf[1][1]};\n'
        )
        degree = 2 * math.prod(row["both_cyc"])
        record = {
            "case_id": row["case_id"],
            "d": row["d"],
            "finite_norm": row["finite_norm"],
            "finite_ideal_hnf": hnf,
            "normal_closure_degree": degree,
        }
        try:
            completed = subprocess.run(
                ["gp", "-q"],
                input=(prelude + GP_SCRIPT.read_text()).encode(),
                capture_output=True,
                cwd=ROOT,
                timeout=arguments.timeout,
            )
        except subprocess.TimeoutExpired as error:
            text = (error.stdout or b"").decode(errors="replace")
            record.update({
                "classification": "TOOL_BLOCKED",
                "tool_reason": "TIMEOUT",
            })
        else:
            text = completed.stdout.decode(errors="replace")
            if completed.returncode:
                record.update({
                    "classification": "TOOL_BLOCKED",
                    "tool_reason": f"GP_EXIT_{completed.returncode}",
                })
            else:
                lines = [
                    line.strip() for line in text.splitlines() if line.strip()
                ]
                base_count = scalar(
                    lines, "ROUTE1_ABELIAN_IMAGINARY_BASE_COUNT"
                )
                match_count = scalar(
                    lines, "TWO_ROUTE_RAY_SUBFIELD_MATCH_COUNT"
                )
                classification = (
                    "TWO_ROUTE_PASS"
                    if match_count
                    else (
                        "NO_ABELIAN_IMAGINARY_BASE"
                        if base_count == 0
                        else "TWO_ROUTE_MISMATCH"
                    )
                )
                record.update({
                    "route1_abelian_imaginary_base_count": base_count,
                    "two_route_ray_subfield_match_count": match_count,
                    "classification": classification,
                })
        records.append(record)
        with transcript.open("a") as stream:
            stream.write(
                f"===== {index}/{len(selected)} {row['case_id']} "
                f"{record['classification']} =====\n{text}\n"
            )
        print(
            f"{index}/{len(selected)} {row['case_id']} "
            f"{record['classification']}",
            flush=True,
        )

    counts: dict[str, int] = {}
    for record in records:
        key = record["classification"]
        counts[key] = counts.get(key, 0) + 1
    payload = {
        "schema": "effective-stark-engine-b-two-route-batch-v1",
        "claim_tag": "VERIFIED_W2_SCREEN",
        "source_census_sha256": hashlib.sha256(CENSUS.read_bytes()).hexdigest(),
        "c_analysis_sha256":
            hashlib.sha256(C_ANALYSIS.read_bytes()).hexdigest(),
        "screen_sha256": hashlib.sha256(GP_SCRIPT.read_bytes()).hexdigest(),
        "selection": (
            f"{arguments.min_degree} < normal_closure_degree "
            f"<= {arguments.max_degree}"
        ),
        "case_count": len(records),
        "classification_counts": counts,
        "records": records,
    }
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "case_count": len(records),
        "classification_counts": counts,
        "output": str(output),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
