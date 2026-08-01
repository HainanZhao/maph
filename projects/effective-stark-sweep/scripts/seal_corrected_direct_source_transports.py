#!/usr/bin/env python3
"""Seal corrected label-aware Euler-deletion transports from three sources."""

from __future__ import annotations

import hashlib
import itertools
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GEOMETRY = ROOT / "artifacts/engine-b-global-coprime-geometry-audit-v1.json"
PREREG = ROOT / "docs/cycle-135-corrected-direct-source-transport-preregistration.md"
PROOF = ROOT / "docs/cycle-136-corrected-direct-source-transport-proof.md"
W1 = ROOT / "artifacts/w1-full-census-v1.json"
OUT = ROOT / "artifacts/corrected-direct-source-transports-v1.json"
SOURCES = {
    "B5-021": ("RQ-002057", "data/q57-norm27-case-v1.json", "artifacts/rq57-norm27-w3-arb-certificate-v1.transcript", "scripts/certify_rq57_norm27_packet.py", "RQ57_NORM27_PACKET_IDENTITY_VERIFIED=1"),
    "B5-033": ("RQ-002955", "data/rq002955-case-v1.json", "artifacts/rq002955-w3-arb-certificate-v1.transcript", "scripts/certify_rq002955_packet.py", "RQ002955_PACKET_IDENTITY_VERIFIED=1"),
    "B5-086": ("RQ-001107", "data/q33-p11-order10-case-v1.json", "artifacts/rq001107-w3-arb-certificate-v1.transcript", "scripts/certify_rq001107_packet.py", "RQ001107_PACKET_IDENTITY_VERIFIED=1"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def poly(d: int) -> str:
    return f"y^2-y+{(1-d)//4}" if d % 4 == 1 else f"y^2-{d}"


def hnf(value: list[list[int]]) -> str:
    return f"[{value[0][0]},{value[0][1]};{value[1][0]},{value[1][1]}]"


def gp_factors(source: dict, target: dict) -> tuple[int, list[dict[str, int]]]:
    text = f'''default(parisizemax,2000000000);
K=bnfinit({poly(source["d"])},1); F1={hnf(source["finite_ideal_hnf"])}; F2={hnf(target["finite_ideal_hnf"])};
Q=idealdiv(K,F2,F1); R1=bnrinit(K,[F1,[1,0]],1); R2=bnrinit(K,[F2,[1,0]],1); M=bnrmap(R2,R1);
S1=bnrisprincipal(R1,idealhnf(K,{{{source["sign_generator"]}}}),0)[1]; S2=bnrisprincipal(R2,idealhnf(K,{{{target["sign_generator"]}}}),0)[1]; F=idealfactor(K,Q);
print("MAP=",M[1]); print("IDENTITY_OK=",bnrmap(M,vector(#R2.cyc))==vector(#R1.cyc)); print("SIGN_OK=",bnrmap(M,S2)==S1);
for(i=1,matsize(F)[1],{{print("E",i,"=",F[i,2]);print("L",i,"=",bnrisprincipal(R1,F[i,1],0)[1]);}});
'''
    run = subprocess.run(["gp", "-q"], input=text, text=True, cwd=ROOT, capture_output=True, check=False, timeout=120)
    if run.returncode:
        raise RuntimeError(run.stdout + run.stderr)
    values = {line.split("=", 1)[0]: line.split("=", 1)[1] for line in run.stdout.splitlines() if "=" in line}
    if values.get("IDENTITY_OK") != "1" or values.get("SIGN_OK") != "1":
        raise RuntimeError(f"ray-map gate failed for {target['case_id']}: {values}")
    match = re.fullmatch(r"Mat\((-?\d+)\)", values["MAP"])
    if not match:
        raise RuntimeError(f"noncyclic map matrix: {values['MAP']}")
    factors = [{"exponent": int(values[f"E{i}"]), "source_ray_log": int(values[f"L{i}"])} for i in range(1, 1 + sum(key.startswith("E") for key in values))]
    if not factors:
        raise RuntimeError(f"empty quotient factorization for {target['case_id']}")
    return int(match.group(1)), factors


def main() -> None:
    if OUT.exists():
        raise RuntimeError("versioned output already exists")
    geometry = json.loads(GEOMETRY.read_text())
    if geometry["status"] != "PASS_EXACT_GEOMETRY_CLASSIFICATION":
        raise RuntimeError("corrected geometry audit missing")
    rows = {row["case_id"]: row for row in json.loads(W1.read_text())["records"]}
    correction = geometry["integral_basis_correction"]["affected_closures"]
    records = []
    source_paths = []
    for closure_id, (source_id, data_path, transcript_path, program_path, token) in SOURCES.items():
        source_paths.extend(ROOT / path for path in (data_path, transcript_path, program_path))
        data = json.loads((ROOT / data_path).read_text())
        if data["verdict"] != "VERIFIED" or data["identification"]["claim_tag"] != "VERIFIED" or token not in (ROOT / transcript_path).read_text():
            raise RuntimeError(f"sealed source integrity failed: {source_id}")
        target_ids = correction[closure_id]["eligible_target_case_ids"]
        if correction[closure_id]["source_case_id"] != source_id:
            raise RuntimeError(f"corrected source changed: {closure_id}")
        source = rows[source_id]
        modulus = source["one_cyc"][0]
        for target_id in target_ids:
            coefficient, factors = gp_factors(source, rows[target_id])
            terms = []
            for size in range(len(factors) + 1):
                for subset in itertools.combinations(range(len(factors)), size):
                    terms.append({"target_label_coefficient_to_source": coefficient, "source_label_shift": (-sum(factors[index]["source_ray_log"] for index in subset)) % modulus, "exponent": -1 if size % 2 else 1})
            records.append({"case_id": target_id, "source_case_id": source_id, "closure_id": closure_id, "ray_map_generator_coefficient": coefficient, "factors": factors, "artin_labelled_formula_terms": terms, "packet_relation": f"label-aware Euler-deletion subset product of sealed {source_id} entries", "orientation": "positive product/quotient at frozen split embedding", "claim_tag": "PROVED_EXACT_MEMBER_TRANSPORT"})
    expected = ["RQ-002079", "RQ-002964", "RQ-002983", "RQ-001115", "RQ-001125", "RQ-001132", "RQ-001133", "RQ-001149", "RQ-001164", "RQ-001172"]
    if sorted(row["case_id"] for row in records) != sorted(expected):
        raise RuntimeError("frozen corrected target set drifted")
    payload = {"schema": "effective-stark-corrected-direct-source-transports-v1", "claim_tag": "PROVED_EXACT_MEMBER_TRANSPORT_BATCH", "record_count": len(records), "records": records, "claim_boundary": "only the ten integral-basis-corrected direct source-coprime targets are promoted; all other Engine-B members retain their current status", "source_hashes": {str(path.relative_to(ROOT)): sha256(path) for path in (GEOMETRY, PREREG, PROOF, W1, *source_paths, Path(__file__))}}
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("CORRECTED_DIRECT_SOURCE_TRANSPORTS=PASS")


if __name__ == "__main__":
    main()
