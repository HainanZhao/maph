#!/usr/bin/env python3
"""Exact ramification and oriented deeper-local action for RQ-000692."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


GP = r'''
K=bnfinit(y^2-5*y+1,1);R=bnrinit(K,[6,[1,0]],1);pK=idealprimedec(K,3)[1];
for(i=0,5,c=bnrconductor(R,[i]);print("CHAR_",i,"_P3_EXP=",idealval(K,c[1],pK)));
beta=Mod(y,y^2-5*y+1);p37=idealhnf(K,4*beta+1);
print("P37_RAY_LOG=",lift(bnrisprincipal(R,p37,0)[1]));
Q=x^12+3*x^11-6*x^10-16*x^9+3*x^8+27*x^6+3*x^4-16*x^3-6*x^2+3*x+1;
L=bnfinit(Q,1);P=idealprimedec(L,3)[1];q=bnfisprincipal(L,P);pi=nfbasistoalg(L,q[2]);A=nfgaloisconj(L);
print("L_CERTIFIED=",bnfcertify(L));print("L_PRIME_COUNT=",#idealprimedec(L,3));print("L_E=",P[3]);print("L_F=",P[4]);print("PI_VAL=",idealval(L,pi,P));print("AUT_COUNT=",#A);
Prel=x^6+(beta-1)*x^5+(1-beta)*x^4+(-4*beta-1)*x^3+(1-beta)*x^2+(beta-1)*x+1;
Pmod=x^6+Mod(8,37)*x^5+Mod(-8,37)*x^4+Mod(-37,37)*x^3+Mod(-8,37)*x^2+Mod(8,37)*x+1;
cycle=vector(6);for(j=0,5,target=Mod(x,Pmod)^(37^j);found=0;for(k=1,#A,if(Mod(Mod(A[k],37),Pmod)==target,found=k));cycle[j+1]=found);
print("FROBENIUS_CYCLE=",cycle);
g=nfgaloisapply(L,A[5],pi);w=nfgaloisapply(L,A[2],pi);w2=nfgaloisapply(L,A[6],pi);ginv=nfgaloisapply(L,A[3],pi);t=nfgaloisapply(L,A[4],pi);
print("G_MINUS_PI_VAL=",idealval(L,g-pi,P));print("G_PLUS_PI_VAL=",idealval(L,g+pi,P));print("W_MINUS_PI_VAL=",idealval(L,w-pi,P));print("W2_MINUS_PI_VAL=",idealval(L,w2-pi,P));print("T_MINUS_PI_VAL=",idealval(L,t-pi,P));print("GINV_MINUS_PI_VAL=",idealval(L,ginv-pi,P));print("GINV_PLUS_PI_VAL=",idealval(L,ginv+pi,P));print("G_MINUS_GINV_VAL=",idealval(L,g-ginv,P));quit();
'''


def exact_data() -> dict[str, str]:
    completed = subprocess.run(["gp", "-q"], input=GP, text=True, capture_output=True, check=True)
    return {key.strip(): value.strip() for key, value in (line.split("=", 1) for line in completed.stdout.splitlines() if "=" in line)}


def build_payload() -> dict[str, object]:
    data = exact_data()
    expected = {
        "CHAR_0_P3_EXP": "0", "CHAR_1_P3_EXP": "2", "CHAR_2_P3_EXP": "2",
        "CHAR_3_P3_EXP": "1", "CHAR_4_P3_EXP": "2", "CHAR_5_P3_EXP": "2",
        "P37_RAY_LOG": "1", "L_CERTIFIED": "1", "L_PRIME_COUNT": "1",
        "L_E": "12", "L_F": "1", "PI_VAL": "1", "AUT_COUNT": "6",
        "FROBENIUS_CYCLE": "[1, 5, 2, 4, 6, 3]", "G_MINUS_PI_VAL": "1",
        "G_PLUS_PI_VAL": "2", "W_MINUS_PI_VAL": "3", "W2_MINUS_PI_VAL": "3",
        "T_MINUS_PI_VAL": "1", "GINV_MINUS_PI_VAL": "1", "GINV_PLUS_PI_VAL": "2",
        "G_MINUS_GINV_VAL": "3",
    }
    if data != expected:
        raise AssertionError({"actual": data, "expected": expected})
    return {
        "schema": "sic-stark-cycle-174-deeper-local-action-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "This exact result constructs only the oriented action on the local truncated ring O_L/P^4 and its ramification filtration. It provides no regulator equality, coefficient map, AFK interface, fusion theorem, or TCC identity.",
        "conductor_crosscheck": {"p3_exponents_for_characters_0_to_5": [0, 2, 2, 1, 2, 2], "upper_filtration": "G^0=C6, G^u=C3 for 0<u<=1, G^u=1 for u>1", "lower_filtration": "G_0=C6, G_1=G_2=C3, G_3=1"},
        "explicit_action": {"uniformizer": "PARI-certified principal generator of P", "frobenius_cycle_indices": [1, 5, 2, 4, 6, 3], "g_index": 5, "g_inverse_index": 3, "wild_indices": [2, 6], "vP_g_minus_pi": 1, "vP_g_plus_pi": 2, "vP_g2_minus_pi": 3, "vP_g_inverse_minus_pi": 1, "vP_g_inverse_plus_pi": 2, "vP_g_minus_g_inverse": 3},
        "orientation_sensitive_quotient": {"quotient": "O_L/P^4", "minimality": "g(pi)=g^-1(pi) mod P^3 but not mod P^4", "first_distinguishing_depth": 4},
        "gate_outcome": {"deeper_local_engine": "ORIENTATION_SENSITIVE_QUOTIENT_CONSTRUCTED", "next_engine": "test whether the oriented O_L/P^4 action and its local pairing can induce finite transport compatible with the two anchors", "disallowed_pseudo_progress": ["calling the truncated local action a regulator equality", "fitting a transport from the convolution defect", "treating local orientation alone as the coefficient-to-ray map"]},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(build_payload(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
