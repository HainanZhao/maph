#!/usr/bin/env python3
"""Exact conductor-lowering ledger for the exploratory D12 bridge.

For gamma=q*beta-p_tilde, remove the common ideal divisor with (12),
then take the ray label at the reduced one-place modulus.  This is the
maximal-order reduction pattern of Kopp, Prop. `prop:stark3`; it does not
identify AFK phases or prove TCC, and the post-hoc D12 choice remains
exploratory.
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
OUTPUT = ROOT / "discovery" / "tcc-sweep-d12-conductor-lowering-v1.json"

GP = r'''\ Exact D12 characteristic-dependent finite conductor lowering.
K=bnfinit(y^2-y-3,1);
if(bnfcertify(K)!=1,error("base bnf certification failed"));
beta=Mod(4+3*y,y^2-y-3);
finite=idealhnf(K,12);
audit(p,q)={
  my(pt=p);
  while(subst(lift(q*beta-pt),y,(1-sqrt(13))/2)<=0,pt-=12);
  my(gamma=q*beta-pt, gamma_ideal=idealhnf(K,gamma));
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


def exact_positive_lift(p: int, q: int) -> int:
    ptilde = p
    while True:
        left = 11 * q - 2 * ptilde
        if left > 0 and left * left > 117 * q * q:
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
            p, q, ptilde, gamma_norm, common_norm, reduced_norm, reduced_hnf, cyc, log, sign = values
            if ptilde != exact_positive_lift(p, q):
                raise AssertionError((p, q, ptilde, exact_positive_lift(p, q)))
            records.append({
                "characteristic": [p, q],
                "positive_lift": ptilde,
                "norm_q_beta_minus_ptilde": gamma_norm,
                "common_ideal_norm": common_norm,
                "reduced_finite_modulus_norm": reduced_norm,
                "reduced_finite_modulus_hnf": reduced_hnf,
                "reduced_ray_cyc": cyc,
                "reduced_ideal_ray_log": log,
                "reduced_sign_log": sign,
            })
        elif line.startswith("PARI_VERSION="):
            version = line.removeprefix("PARI_VERSION=")
    if len(records) != 143 or version is None:
        raise AssertionError((len(records), version, run.stdout[-1000:]))
    if any(row["common_ideal_norm"] * row["reduced_finite_modulus_norm"] != 144 for row in records):
        raise AssertionError("ideal quotient norm check failed")
    payload = {
        "schema": "tcc-sweep-d12-conductor-lowering-v1",
        "claim_tag": "EXPLORATORY",
        "claim_boundary": (
            "Exact maximal-order arithmetic ledger only. It performs the "
            "characteristic-dependent conductor lowering required before ray "
            "logs are meaningful, but supplies neither the AFK phase comparison, "
            "the signed reconstruction, nor a TCC conclusion."
        ),
        "candidate": {
            "d": 12, "r": 1, "field": "Q(sqrt(13))",
            "form_conductor": 1, "beta": "4+3y, y^2-y-3=0",
            "full_one_place_modulus": "(12) infinity_2",
        },
        "mathematical_route": {
            "reference": "Kopp arXiv:2411.06763, Proposition prop:stark3 and its change-of-modulus step",
            "formula": "common=(12)+(gamma); reduced_modulus=(12)/common; reduced_ideal=(gamma)/common",
            "positive_lift_check": "(11q-2p_tilde)>0 and (11q-2p_tilde)^2>117q^2",
        },
        "nonzero_characteristic_count": len(records),
        "full_modulus_rows": sum(row["reduced_finite_modulus_norm"] == 144 for row in records),
        "lowered_modulus_rows": sum(row["reduced_finite_modulus_norm"] != 144 for row in records),
        "reduced_modulus_norm_histogram": {
            str(value): sum(row["reduced_finite_modulus_norm"] == value for row in records)
            for value in sorted({row["reduced_finite_modulus_norm"] for row in records})
        },
        "distinct_reduced_finite_modulus_hnf_count": len({tuple(row["reduced_finite_modulus_hnf"]) for row in records}),
        "records": records,
        "replay": {
            "command": "python3 discovery/audit_tcc_sweep_d12_conductor_lowering.py",
            "python_version": sys.version.split()[0], "pari_version": version,
            "wall_seconds": time.monotonic() - started,
        },
        "source_hashes": {"audit_script": digest(Path(__file__))},
        "gp_stderr": run.stderr,
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print("TCC_SWEEP_D12_CONDUCTOR_LOWERING=PASS")


if __name__ == "__main__":
    main()
