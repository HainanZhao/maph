#!/usr/bin/env python3
"""Run generalized W2 on the ten smallest normal closures."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CENSUS = ROOT / "artifacts" / "w1-full-census-v1.json"
C_ANALYSIS = ROOT / "artifacts" / "engine-c-geometry-analysis-v1.json"
GP_SCRIPT = ROOT / "scripts" / "screen_engine_b_two_route.gp"
OUTPUT = ROOT / "artifacts" / "engine-b-two-route-pilot-v1.json"
TRANSCRIPT = ROOT / "artifacts" / "engine-b-two-route-pilot-v1.transcript"


def scalar(lines: list[str], key: str) -> str:
    prefix = f"{key}="
    matches = [line[len(prefix):] for line in lines if line.startswith(prefix)]
    if len(matches) != 1:
        raise RuntimeError(f"expected one {key}, got {len(matches)}")
    return matches[0]


def main() -> None:
    census_data = json.loads(CENSUS.read_text())
    records = census_data["records"]
    by_id = {row["case_id"]: row for row in records}
    c_analysis = json.loads(C_ANALYSIS.read_text())
    queue = [row for row in records if row.get("engine") == "B"]
    queue.extend(by_id[case_id] for case_id in c_analysis["reroute_b_case_ids"])
    queue.sort(key=lambda row: (
        2 * math.prod(row["both_cyc"]),
        row["finite_norm"], row["d"], row["case_id"],
    ))
    selected = queue[:10]
    result = []
    TRANSCRIPT.write_text("")
    for row in selected:
        hnf = row["finite_ideal_hnf"]
        prelude = (
            f'CASE_ID="{row["case_id"]}";\n'
            f'D_VALUE={row["d"]};\n'
            f'H11={hnf[0][0]};H12={hnf[0][1]};'
            f'H21={hnf[1][0]};H22={hnf[1][1]};\n'
        )
        completed = subprocess.run(
            ["gp", "-q"],
            input=(prelude + GP_SCRIPT.read_text()).encode(),
            check=True,
            capture_output=True,
            cwd=ROOT,
        )
        text = completed.stdout.decode()
        with TRANSCRIPT.open("a") as stream:
            stream.write(f"===== {row['case_id']} =====\n{text}")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        result.append({
            "case_id": row["case_id"],
            "d": row["d"],
            "finite_norm": row["finite_norm"],
            "finite_ideal_hnf": hnf,
            "normal_closure_degree": 2 * math.prod(row["both_cyc"]),
            "two_route_ray_subfield_match_count": int(
                scalar(lines, "TWO_ROUTE_RAY_SUBFIELD_MATCH_COUNT")
            ),
        })
    output = {
        "schema": "effective-stark-engine-b-two-route-pilot-v1",
        "source_census_sha256":
            hashlib.sha256(CENSUS.read_bytes()).hexdigest(),
        "c_analysis_sha256":
            hashlib.sha256(C_ANALYSIS.read_bytes()).hexdigest(),
        "screen_sha256": hashlib.sha256(GP_SCRIPT.read_bytes()).hexdigest(),
        "queue_case_count": len(queue),
        "selection": "ten smallest absolute normal-closure degrees",
        "case_count": len(result),
        "cases_with_route2_match": sum(
            row["two_route_ray_subfield_match_count"] > 0 for row in result
        ),
        "records": result,
    }
    OUTPUT.write_text(json.dumps(output, indent=2, sort_keys=True) + "\n")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
