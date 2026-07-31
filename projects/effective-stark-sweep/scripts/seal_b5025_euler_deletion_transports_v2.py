#!/usr/bin/env python3
"""Corrected B5-025 Euler-deletion transport batch sealer."""

from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
GEOMETRY = ROOT / "artifacts/b5025-transport-geometry-v1.json"
SOURCE = ROOT / "artifacts/b5025-source-certificate-integrity-v1.json"
PREREG = ROOT / "data/census-paper-preregistration-amendment-v13.json"
PROOF = ROOT / "docs/cycle-113-b5025-euler-deletion-batch-proof.md"
CORRECTION = ROOT / "docs/cycle-114-b5025-factor-extraction-correction.md"
W1 = ROOT / "artifacts/w1-full-census-v1.json"
OUTPUT = ROOT / "artifacts/b5025-euler-deletion-transports-v2.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def factor_logs(target: dict) -> list[dict[str, int]]:
    h = target["finite_ideal_hnf"]
    text = f'''default(parisizemax,2000000000);
K=bnfinit(y^2-7,1); F1=[7,0;0,1]; F2=[{h[0][0]},{h[0][1]};{h[1][0]},{h[1][1]}]; Q=idealdiv(K,F2,F1); R=bnrinit(K,[F1,[1,0]],1); F=idealfactor(K,Q);
for(i=1,matsize(F)[1],{{print("FACTOR_",i,"_EXP=",F[i,2]);print("FACTOR_",i,"_LOG=",bnrisprincipal(R,F[i,1],0)[1]);}});
'''
    run = subprocess.run(["gp", "-q"], input=text, text=True, cwd=ROOT,
                         capture_output=True, check=True, timeout=600)
    values: dict[str, int] = {}
    for line in run.stdout.splitlines():
        if "=" in line:
            key, value = line.strip().split("=", 1)
            values[key] = int(value)
    result = []
    for index in range(1, 1 + len(values) // 2):
        result.append({"exponent": values[f"FACTOR_{index}_EXP"], "source_ray_log": values[f"FACTOR_{index}_LOG"]})
    if not result:
        raise RuntimeError(f"no exact factors emitted for {target['case_id']}")
    return result


def terms(factors: list[dict[str, int]]) -> list[dict[str, int]]:
    logs = [factor["source_ray_log"] for factor in factors]
    return [{"source_label_shift": (-sum(logs[i] for i in subset)) % 6,
             "exponent": -1 if len(subset) % 2 else 1}
            for size in range(len(logs) + 1)
            for subset in itertools.combinations(range(len(logs)), size)]


def main() -> None:
    if OUTPUT.exists():
        raise RuntimeError("versioned output already exists")
    geometry = json.loads(GEOMETRY.read_text())
    if json.loads(SOURCE.read_text())["claim_tag"] != "VERIFIED_SEALED_SOURCE_CERTIFICATE_INTEGRITY":
        raise RuntimeError("source integrity gate absent")
    w1 = {row["case_id"]: row for row in json.loads(W1.read_text())["records"]}
    eligible = [row for row in geometry["records"] if row["euler_deletion_route_eligible"]]
    expected_ids = ["RQ-000195", "RQ-000200", "RQ-000205", "RQ-000213"]
    if [row["case_id"] for row in eligible] != expected_ids:
        raise RuntimeError("eligible batch changed")
    expected_factor_counts = dict(zip(expected_ids, (1, 1, 1, 2)))
    records = []
    for row in eligible:
        factors = factor_logs(w1[row["case_id"]])
        if len(factors) != expected_factor_counts[row["case_id"]]:
            raise RuntimeError(f"unexpected factor count for {row['case_id']}")
        records.append({"case_id": row["case_id"], "source_case_id": "RQ-000190", "closure_id": "B5-025", "factors": factors, "artin_labelled_formula_terms": terms(factors), "packet_relation": "Euler-deletion subset product of certified RQ-000190 entries", "orientation": "positive product/quotient at frozen split embedding", "claim_tag": "PROVED_EXACT_MEMBER_TRANSPORT"})
    payload = {"schema": "effective-stark-b5025-euler-deletion-transports-v2", "claim_tag": "PROVED_EXACT_MEMBER_TRANSPORT_BATCH", "supersedes": "artifacts/b5025-euler-deletion-transports-v1.json", "record_count": len(records), "records": records, "claim_boundary": "only four identity-labelled, source-coprime B5-025 targets are promoted", "source_hashes": {str(path.relative_to(ROOT)): sha256(path) for path in (GEOMETRY, SOURCE, PREREG, PROOF, CORRECTION, W1, Path(__file__))}}
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("B5025_EULER_DELETION_TRANSPORTS_V2=PASS")


if __name__ == "__main__":
    main()
