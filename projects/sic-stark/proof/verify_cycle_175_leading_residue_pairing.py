#!/usr/bin/env python3
"""Exact leading wild residue and frozen local pairing for RQ-000692."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


GP = r'''
Q=x^12+3*x^11-6*x^10-16*x^9+3*x^8+27*x^6+3*x^4-16*x^3-6*x^2+3*x+1;
L=bnfinit(Q,1);P=idealprimedec(L,3)[1];pi=nfbasistoalg(L,bnfisprincipal(L,P)[2]);A=nfgaloisconj(L);M=nfmodprinit(L,P);
g=nfgaloisapply(L,A[5],pi);gi=nfgaloisapply(L,A[3],pi);h=nfgaloisapply(L,A[2],pi);h2=nfgaloisapply(L,A[6],pi);
c=(h-pi)/pi^3;c2=(h2-pi)/pi^3;delta=(g-gi)/pi^3;
print("L_CERTIFIED=",bnfcertify(L));print("P_COUNT=",#idealprimedec(L,3));print("P_E=",P[3]);print("P_F=",P[4]);print("PI_VAL=",idealval(L,pi,P));print("AUT_COUNT=",#A);
print("C_H=",nfmodpr(L,c,M));print("C_H2=",nfmodpr(L,c2,M));print("DELTA=",nfmodpr(L,delta,M));print("G_C_H=",nfmodpr(L,nfgaloisapply(L,A[5],c),M));print("H_C_H=",nfmodpr(L,nfgaloisapply(L,A[2],c),M));quit();
'''


def exact_data() -> dict[str, str]:
    completed = subprocess.run(["gp", "-q"], input=GP, text=True, capture_output=True, check=True)
    return {key.strip(): value.strip() for key, value in (line.split("=", 1) for line in completed.stdout.splitlines() if "=" in line)}


def build_payload() -> dict[str, object]:
    data = exact_data()
    expected = {"L_CERTIFIED": "1", "P_COUNT": "1", "P_E": "12", "P_F": "1", "PI_VAL": "1", "AUT_COUNT": "6", "C_H": "2", "C_H2": "1", "DELTA": "1", "G_C_H": "2", "H_C_H": "2"}
    if data != expected:
        raise AssertionError({"actual": data, "expected": expected})
    c_h = 2
    pairing = [[(a * b * c_h) % 3 for b in range(3)] for a in range(3)]
    if pairing != [[0, 0, 0], [0, 2, 1], [0, 1, 2]]:
        raise AssertionError(pairing)
    return {
        "schema": "sic-stark-cycle-175-leading-residue-pairing-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "This exact result constructs only a normalized wild leading-residue character and its frozen finite F3 pairing with Artin exponents. It proves no regulator equality, coefficient map, AFK interface, fusion theorem, transport operation, or TCC identity.",
        "leading_residue": {"wild_generator": "h=g^2", "c_h": 2, "c_h_squared": 1, "generator_law": "c_(h^2)=2*c_h in F3", "oriented_difference_delta": 1, "delta_relation": "delta=-c_h in F3", "g_action_on_c_h": 2, "h_action_on_c_h": 2},
        "pairing": {"definition": "B(a,b)=(a mod 3)(b mod 3)c_h in F3", "matrix_a_rows_b_columns": pairing, "anchor_g1": {"ray_label": "(3,5)->g^1", "value": 2}, "anchor_g2": {"ray_label": "(3,4)->g^2", "value": 1}, "anchors_distinct_nonzero": True},
        "gate_outcome": {"local_pairing": "ORIENTATION_SENSITIVE_ANCHOR_DISTINGUISHING", "next_engine": "test whether this fixed local pairing can define a transport compatible with the full 36-row torsor without fitting the defect", "disallowed_pseudo_progress": ["changing the uniformizer or residue normalization", "changing the pairing after anchor inspection", "calling a local pairing an AFK or coefficient interface"]},
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
