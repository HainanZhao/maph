#!/usr/bin/env python3
"""Exact local 3-adic data extraction for the pinned d=6 ray field."""
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
GP=r'''K=bnfinit(y^2-5*y+1,1);L=bnfinit(x^12+3*x^11-6*x^10-16*x^9+3*x^8+27*x^6+3*x^4-16*x^3-6*x^2+3*x+1,1);pK=idealprimedec(K,3)[1];pL=idealprimedec(L,3)[1];R=bnrinit(K,[6,[1,0]],1);C=bnrconductor(R);print("K_E=",pK[3]);print("K_F=",pK[4]);print("L_E=",pL[3]);print("L_F=",pL[4]);print("RAY_CYC=",R.cyc);print("RAY_ORDER=",R.no);print("CONDUCTOR_NORM=",idealnorm(K,C[1]));print("CONDUCTOR_INFINITY=",C[2]);quit();'''
def build_payload():
 out=subprocess.run(["gp","-q"],input=GP,text=True,capture_output=True,check=True).stdout.splitlines();d={k:v for k,v in (line.split("=",1) for line in out if "=" in line)}
 d={k.strip():v.strip() for k,v in d.items()};expected={"K_E":"2","K_F":"1","L_E":"12","L_F":"1","RAY_CYC":"[6]","RAY_ORDER":"6","CONDUCTOR_NORM":"36","CONDUCTOR_INFINITY":"[1, 0]"}
 if d!=expected:raise AssertionError((d,expected))
 return {"schema":"sic-stark-cycle-172-local-filtration-prototype-v1","epistemic_status":"PROVED","claim_boundary":"This exact result extracts only local decomposition and first principal-unit quotient data at 3 for the pinned ray field. It defines no local Artin module, regulator equality, coefficient map, AFK interface, Stark identity, fusion theorem, or TCC identity.","summary":{"base_prime_e":2,"base_prime_f":1,"ray_prime_e":12,"ray_prime_f":1,"relative_ramification_e":6,"ray_group":"C6","wild_subgroup":"C3=<g^2>","first_principal_unit_quotient_order":3},"gate_outcome":{"local_filtration_data":"EXTRACTED","scope":"first local graded quotient only"}}
def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=Path);a=p.parse_args();s=json.dumps(build_payload(),indent=2,sort_keys=True)+"\n";a.output.write_text(s) if a.output else print(s,end="")
if __name__=="__main__":main()
