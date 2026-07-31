#!/usr/bin/env python3
"""Fresh exact conductor/ray-map screen for the frozen B5-025 batch."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "data/census-paper-preregistration-amendment-v13.json"
LEDGER = ROOT / "artifacts/engine-b-transport-ledger-v1.json"
SOURCE_CHECK = ROOT / "artifacts/b5025-source-certificate-integrity-v1.json"
W1 = ROOT / "artifacts/w1-full-census-v1.json"
OUTPUT = ROOT / "artifacts/b5025-transport-geometry-v1.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def gp_screen(source: dict, target: dict) -> tuple[dict[str, str], str]:
    h1 = source["finite_ideal_hnf"]
    h2 = target["finite_ideal_hnf"]
    text = f'''default(parisizemax, 2000000000);
K=bnfinit(y^2-7,1); F1=[{h1[0][0]},{h1[0][1]};{h1[1][0]},{h1[1][1]}]; F2=[{h2[0][0]},{h2[0][1]};{h2[1][0]},{h2[1][1]}];
Q=idealdiv(K,F2,F1); R1=bnrinit(K,[F1,[1,0]],1); R2=bnrinit(K,[F2,[1,0]],1); M=bnrmap(R2,R1);
S1=bnrisprincipal(R1,idealhnf(K,{source['sign_generator']}),0)[1]; S2=bnrisprincipal(R2,idealhnf(K,{target['sign_generator']}),0)[1];
print("TARGET_ID={target['case_id']}"); print("IDEAL_PRODUCT_MATCH=",idealhnf(K,idealmul(K,F1,Q))==idealhnf(K,F2)); print("QUOTIENT_NORM=",idealnorm(K,Q)); print("QUOTIENT_COPRIME_NORM=",idealnorm(K,idealadd(K,F1,Q))); print("QUOTIENT_FACTOR=",idealfactor(K,Q)); print("SOURCE_CYC=",Vec(R1.cyc)); print("TARGET_CYC=",Vec(R2.cyc)); print("MAP_MATRIX=",M[1]); print("SOURCE_SIGN_LOG=",S1); print("TARGET_SIGN_LOG=",S2); print("MAP_IDENTITY=",bnrmap(M,[0])); print("MAP_GENERATOR=",bnrmap(M,[1])); print("MAP_SIGN=",bnrmap(M,[S2]));
'''
    run = subprocess.run(["gp", "-q"], input=text, text=True, cwd=ROOT,
                         capture_output=True, timeout=600)
    if run.returncode:
        raise RuntimeError(run.stdout + run.stderr)
    values = {}
    for line in run.stdout.splitlines():
        line = line.strip()
        if "=" in line:
            key, value = line.split("=", 1)
            values[key] = value
    return values, run.stdout + run.stderr


def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("versioned output already exists")
    prereg = json.loads(PREREG.read_text())
    source_check = json.loads(SOURCE_CHECK.read_text())
    if source_check["claim_tag"] != "VERIFIED_SEALED_SOURCE_CERTIFICATE_INTEGRITY":
        raise RuntimeError("sealed source certificate was not validated")
    ledger = json.loads(LEDGER.read_text())
    w1 = {row["case_id"]: row for row in json.loads(W1.read_text())["records"]}
    group = next(group for group in ledger["members"] if group["case_id"] == "RQ-000190")
    source = w1[group["case_id"]]
    targets = sorted((row for row in ledger["members"] if row["closure_id"] == "B5-025" and row["case_id"] != "RQ-000190"), key=lambda row: (row["finite_norm"], row["case_id"]))
    if len(targets) != 8:
        raise RuntimeError("frozen B5-025 target set drifted")
    records = []
    for target_member in targets:
        target = w1[target_member["case_id"]]
        values, transcript = gp_screen(source, target)
        required = {"TARGET_ID", "IDEAL_PRODUCT_MATCH", "QUOTIENT_NORM", "QUOTIENT_COPRIME_NORM", "QUOTIENT_FACTOR", "SOURCE_CYC", "TARGET_CYC", "MAP_MATRIX", "SOURCE_SIGN_LOG", "TARGET_SIGN_LOG", "MAP_IDENTITY", "MAP_GENERATOR", "MAP_SIGN"}
        if set(values) != required:
            raise RuntimeError(f"incomplete output for {target_member['case_id']}: {values}")
        reusable = (values["IDEAL_PRODUCT_MATCH"] == "1" and values["QUOTIENT_COPRIME_NORM"] == "1" and values["SOURCE_CYC"] == "[6]" and values["TARGET_CYC"] == "[6]" and values["MAP_MATRIX"] == "Mat(1)" and values["SOURCE_SIGN_LOG"] == "3" and values["TARGET_SIGN_LOG"] == "3" and values["MAP_IDENTITY"] == "[0]" and values["MAP_GENERATOR"] == "[1]" and values["MAP_SIGN"] == "[3]")
        records.append({"case_id": target_member["case_id"], "finite_norm": target_member["finite_norm"], "exact": values, "euler_deletion_route_eligible": reusable, "transcript": transcript})
    payload = {"schema": "effective-stark-b5025-transport-geometry-v1", "claim_tag": "PROVED_EXACT_TRANSPORT_GEOMETRY", "source_case_id": "RQ-000190", "target_count": len(records), "eligible_count": sum(row["euler_deletion_route_eligible"] for row in records), "records": records, "claim_boundary": "geometry eligibility only; packet formulas require the separately frozen Cycle-112 source rule", "source_hashes": {str(path.relative_to(ROOT)): sha256(path) for path in (PREREG, LEDGER, SOURCE_CHECK, W1, Path(__file__))}}
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("B5025_TRANSPORT_GEOMETRY=PASS")


if __name__ == "__main__":
    main()
