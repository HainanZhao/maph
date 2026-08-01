#!/usr/bin/env python3
"""Corrected D12 order-ray lowering ledger from the AFK/Kopp fixed point.

For Q=<1,-3,-1>, the RM fixed point is rho=y+1=(3+sqrt(13))/2.
With b=O_K and m=12 O_K, Kopp's correspondence has alpha=12, so the
principal representative attached to (p,q)/12 is gamma=q*rho-p_tilde.
This replaces the invalid exploratory v1 use of the stabilizer eigenunit.
"""

from __future__ import annotations

import ast
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "discovery" / "tcc-sweep-d12-conductor-lowering-corrected-v2.json"

GP = r'''\ Exact D12 conductor lowering from rho=(3+sqrt(13))/2=y+1.
K=bnfinit(y^2-y-3,1);
if(bnfcertify(K)!=1,error("base bnf certification failed"));
rho=Mod(y+1,y^2-y-3);
finite=idealhnf(K,12);
audit(p,q)={
  my(pt=p);
  while(subst(lift(q*rho-pt),y,(1-sqrt(13))/2)<=0,pt-=12);
  my(gamma=q*rho-pt, gamma_ideal=idealhnf(K,gamma));
  my(common=idealadd(K,finite,gamma_ideal));
  my(reduced_modulus=idealdiv(K,finite,common));
  my(reduced_ideal=idealdiv(K,gamma_ideal,common));
  my(ray=bnrinit(K,[reduced_modulus,[1,0]],1));
  my(ray_log=bnrisprincipal(ray,reduced_ideal,0));
  my(sign_log=bnrisprincipal(ray,idealhnf(K,11),0));
  print("ROW=",[p,q,pt,norm(gamma),idealnorm(K,common),
    idealnorm(K,reduced_modulus),[reduced_modulus[1,1],reduced_modulus[1,2],reduced_modulus[2,1],reduced_modulus[2,2]],
    Vec(ray.cyc),Vec(ray_log),Vec(sign_log)]);
};
for(p=0,11,for(q=0,11,if(p||q,audit(p,q))));
print("PARI_VERSION=",version());
quit;
'''


def positive_lift(p: int, q: int) -> int:
    ptilde = p
    while True:
        # q*(3-sqrt(13))/2-ptilde > 0 iff
        # 3q-2ptilde-q*sqrt(13)>0.
        left = 3 * q - 2 * ptilde
        if q == 0:
            if left > 0:
                return ptilde
        elif left > 0 and left * left > 13 * q * q:
            return ptilde
        ptilde -= 12


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def main() -> None:
    started = time.monotonic()
    run = subprocess.run(["gp", "-q"], input=GP, text=True,
                         capture_output=True, check=True)
    records = []
    version = None
    for line in run.stdout.splitlines():
        if line.startswith("ROW="):
            values = ast.literal_eval(line.removeprefix("ROW="))
            p, q, ptilde, gamma_norm, common_norm, reduced_norm, hnf, cyc, log, sign = values
            if ptilde != positive_lift(p, q):
                raise AssertionError((p, q, ptilde, positive_lift(p, q)))
            if gamma_norm != ptilde * ptilde - 3 * ptilde * q - q * q:
                raise AssertionError((p, q, ptilde, gamma_norm))
            records.append({"characteristic": [p, q], "positive_lift": ptilde,
                            "norm_q_rho_minus_ptilde": gamma_norm,
                            "common_ideal_norm": common_norm,
                            "reduced_finite_modulus_norm": reduced_norm,
                            "reduced_finite_modulus_hnf": hnf,
                            "reduced_ray_cyc": cyc, "reduced_ideal_ray_log": log,
                            "reduced_sign_log": sign})
        elif line.startswith("PARI_VERSION="):
            version = line.removeprefix("PARI_VERSION=")
    if len(records) != 143 or version is None:
        raise AssertionError((len(records), version))
    if any(row["common_ideal_norm"] * row["reduced_finite_modulus_norm"] != 144 for row in records):
        raise AssertionError("ideal quotient norm check failed")
    payload = {"schema": "tcc-sweep-d12-conductor-lowering-corrected-v2",
               "claim_tag": "EXPLORATORY",
               "claim_boundary": "Exact maximal-order lowering arithmetic using the AFK/Kopp fixed-point representative only; no AFK phase, signed reconstruction, minor, or TCC claim.",
               "correction_of": "tcc-sweep-d12-conductor-lowering-v1.json",
               "candidate": {"d": 12, "r": 1, "form": "<1,-3,-1>", "rho": "y+1, y^2-y-3=0", "alpha": 12, "form_conductor": 1},
               "mathematical_route": {"reference": "Kopp arXiv:2411.06763, thm:correspondence and prop:changemodzeta", "representative": "gamma=alpha*(q/d*rho-p/d)=q*rho-p_tilde"},
               "nonzero_characteristic_count": len(records),
               "full_modulus_rows": sum(row["reduced_finite_modulus_norm"] == 144 for row in records),
               "lowered_modulus_rows": sum(row["reduced_finite_modulus_norm"] != 144 for row in records),
               "reduced_modulus_norm_histogram": {str(v): sum(row["reduced_finite_modulus_norm"] == v for row in records) for v in sorted({row["reduced_finite_modulus_norm"] for row in records})},
               "distinct_reduced_finite_modulus_hnf_count": len({tuple(row["reduced_finite_modulus_hnf"]) for row in records}),
               "records": records,
               "replay": {"command": "python3 discovery/audit_tcc_sweep_d12_conductor_lowering_corrected_v2.py", "python_version": sys.version.split()[0], "pari_version": version, "wall_seconds": time.monotonic()-started},
               "source_hashes": {"audit_script": digest(Path(__file__))}, "gp_stderr": run.stderr}
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    print("TCC_SWEEP_D12_CONDUCTOR_LOWERING_CORRECTED_V2=PASS")


if __name__ == "__main__":
    main()
