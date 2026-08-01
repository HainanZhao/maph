#!/usr/bin/env python3
"""Exact directed coprime-Euler geometry screen for frozen Engine-B groups."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "artifacts/engine-b-transport-ledger-v4.json"
W1 = ROOT / "artifacts/w1-full-census-v1.json"
PREREG = ROOT / "docs/cycle-133-engine-b-global-geometry-preregistration.md"
OUT = ROOT / "discovery/engine-b-global-coprime-geometry-v1.json"
TRANSCRIPT = ROOT / "discovery/engine-b-global-coprime-geometry-v1.transcript"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def field_polynomial(d: int) -> str:
    return f"y^2-y+{(1-d)//4}" if d % 4 == 1 else f"y^2-{d}"


def hnf(matrix: list[list[int]]) -> str:
    return f"[{matrix[0][0]},{matrix[0][1]};{matrix[1][0]},{matrix[1][1]}]"


def parse(output: str) -> dict[str, str]:
    values = {}
    for line in output.splitlines():
        if "=" in line:
            key, value = line.strip().split("=", 1)
            values[key] = value
    return values


def screen_pair(source: dict, target: dict) -> tuple[dict, str]:
    if target["finite_norm"] % source["finite_norm"]:
        return {"status": "NORM_OBSTRUCTED"}, ""
    source_hnf, target_hnf = hnf(source["finite_ideal_hnf"]), hnf(target["finite_ideal_hnf"])
    gp = f'''default(parisizemax, 2000000000);
K=bnfinit({field_polynomial(source["d"])},1);
F1={source_hnf}; F2={target_hnf}; Q=idealdiv(K,F2,F1);
print("FIELD_DISC=",K.disc);
print("PRODUCT_OK=",idealhnf(K,idealmul(K,F1,Q))==idealhnf(K,F2));
print("QUOTIENT_NORM=",idealnorm(K,Q));
print("COPRIME_NORM=",idealnorm(K,idealadd(K,F1,Q)));
print("QUOTIENT_FACTOR=",idealfactor(K,Q));
if(idealhnf(K,idealmul(K,F1,Q))==idealhnf(K,F2),
  R1=bnrinit(K,[F1,[1,0]],1); R2=bnrinit(K,[F2,[1,0]],1); M=bnrmap(R2,R1);
  S1=bnrisprincipal(R1,idealhnf(K,{{{source["sign_generator"]}}}),0)[1];
  S2=bnrisprincipal(R2,idealhnf(K,{{{target["sign_generator"]}}}),0)[1];
  print("SOURCE_CYC=",Vec(R1.cyc)); print("TARGET_CYC=",Vec(R2.cyc));
  print("MAP_MATRIX=",M[1]); print("SOURCE_SIGN=",S1); print("TARGET_SIGN=",S2);
  print("MAP_IDENTITY_OK=",bnrmap(M,vector(#R2.cyc))==vector(#R1.cyc));
  print("MAP_SIGN_OK=",bnrmap(M,S2)==S1)
);
'''
    run = subprocess.run(
        ["gp", "-q"], input=gp, text=True, capture_output=True,
        cwd=ROOT, timeout=120, check=False,
    )
    transcript = run.stdout + run.stderr
    if run.returncode:
        return {"status": "TOOL_FAILURE", "returncode": run.returncode}, transcript
    values = parse(run.stdout)
    required = {"FIELD_DISC", "PRODUCT_OK", "QUOTIENT_NORM", "COPRIME_NORM", "QUOTIENT_FACTOR"}
    if not required <= set(values):
        return {"status": "TOOL_FAILURE", "reason": "incomplete GP output"}, transcript
    if int(values["FIELD_DISC"]) != source["field_discriminant"]:
        return {"status": "FIELD_RECONSTRUCTION_FAILURE", "exact": values}, transcript
    if values["PRODUCT_OK"] != "1":
        return {"status": "MODULUS_DIVISIBILITY_OBSTRUCTED", "exact": values}, transcript
    if values["COPRIME_NORM"] != "1":
        return {"status": "SOURCE_PRIME_OBSTRUCTED", "exact": values}, transcript
    map_required = {"SOURCE_CYC", "TARGET_CYC", "MAP_MATRIX", "SOURCE_SIGN", "TARGET_SIGN", "MAP_IDENTITY_OK", "MAP_SIGN_OK"}
    if not map_required <= set(values):
        return {"status": "TOOL_FAILURE", "reason": "incomplete ray-map output", "exact": values}, transcript
    if values["MAP_IDENTITY_OK"] != "1" or values["MAP_SIGN_OK"] != "1":
        return {"status": "RAY_MAP_OBSTRUCTED", "exact": values}, transcript
    return {"status": "GEOMETRICALLY_ELIGIBLE", "exact": values}, transcript


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--closure-id")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    ledger = json.loads(LEDGER.read_text())
    rows = {row["case_id"]: row for row in json.loads(W1.read_text())["records"]}
    groups: dict[str, list[dict]] = {}
    for member in ledger["members"]:
        groups.setdefault(member["closure_id"], []).append(member)
    if len(groups) != 88 or len(ledger["members"]) != 232:
        raise RuntimeError("frozen Engine-B population changed")
    selected = {args.closure_id} if args.closure_id else set(groups)
    if not selected <= set(groups):
        raise RuntimeError("unknown closure id")
    started = time.monotonic()
    output_groups, transcripts = [], []
    for closure_id in sorted(selected):
        members = sorted(groups[closure_id], key=lambda row: row["case_id"])
        pair_records = []
        for source_member in members:
            for target_member in members:
                if source_member["case_id"] == target_member["case_id"]:
                    continue
                source, target = rows[source_member["case_id"]], rows[target_member["case_id"]]
                result, transcript = screen_pair(source, target)
                record = {"source_case_id": source_member["case_id"], "target_case_id": target_member["case_id"], **result}
                pair_records.append(record)
                if transcript:
                    transcripts.append(f"===== {closure_id} {record['source_case_id']} -> {record['target_case_id']} =====\n{transcript}")
        statuses = Counter(row["status"] for row in pair_records)
        output_groups.append({"closure_id": closure_id, "member_case_ids": [row["case_id"] for row in members], "pair_count": len(pair_records), "status_counts": dict(sorted(statuses.items())), "pairs": pair_records})
        print(f"{closure_id}: {len(pair_records)} directions", file=sys.stderr, flush=True)
    if not args.write:
        print(json.dumps(output_groups, indent=2, sort_keys=True))
        return
    if args.closure_id:
        raise RuntimeError("--write requires the full frozen population")
    TRANSCRIPT.write_text("\n".join(transcripts))
    payload = {"schema": "effective-stark-engine-b-global-coprime-geometry-v1", "status": "EXACT_GEOMETRY_EXPORT", "claim_tag": "OBSERVED", "population": {"closures": len(output_groups), "members": len(ledger["members"]), "directions": sum(group["pair_count"] for group in output_groups)}, "runtime_wall_seconds": time.monotonic()-started, "closures": output_groups, "source_hashes": {str(path.relative_to(ROOT)): sha256(path) for path in (LEDGER, W1, PREREG, Path(__file__))}, "transcript": {"path": str(TRANSCRIPT.relative_to(ROOT)), "sha256": sha256(TRANSCRIPT)}}
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    print("ENGINE_B_GLOBAL_COPRIME_GEOMETRY=PASS")


if __name__ == "__main__":
    main()
