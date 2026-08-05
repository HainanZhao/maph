"""Seal C81's durable LEM-method boundary."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256

OUTPUT = ROOT / "artifacts/cycle-81-b081-lem-method-boundary-v1.json"
HASHES = {
    "preregistration": ("docs/cycle-81-b081-lem-dominance-preregistration-v1.md", "dc19fc7c776799d6ba8b5520c83c77c6e3dd3359fb5cdfe87a5b46c3ffd4fecf"),
    "chain_split": ("discovery/cycle81_chain_split.cpp", "c3d15f9a9f399a34027f31e9f169b3fafcabeeea2485818dc6278b0b95a8e5f5"),
    "xyz_search": ("discovery/cycle81_xyz_model.py", "77b6e02656ab95214cb064d61de7164ab290e97f2f341534f45a9717f6965718"),
    "lem_checker": ("proof/check_cycle81_lem_witness.py", "2c8e6dcd19238f788a99d64c288fd5d4a2517c8dbcee547f39b972b88ec96fe6"),
    "xyz_checker": ("proof/check_cycle81_xyz_witness.py", "a0af35fc2d5c6f3c19e350a35bdb36e56029651733d71e8d6810da6b513a822f"),
    "reduction": ("proof/cycle81_shortest_cycle_reduction.md", "5abbd28119860beb0e1b524b2c2814806595eeb1c481ab6331fb7f1a03314cfd"),
    "boundary": ("proof/cycle81_method_boundary.md", "c364db77b60d32eef32ab365da2015f1c6f46168a471014e33551ed64d6dfa75"),
    "scaffold": ("proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "validator": ("../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}

def audit() -> dict:
    xyz = json.loads(subprocess.check_output([sys.executable, str(ROOT / HASHES["xyz_checker"][0])], text=True))
    lem = json.loads(subprocess.check_output([sys.executable, str(ROOT / HASHES["lem_checker"][0])], text=True))
    require(xyz["status"] == "PASS" and xyz["full_has_4_cycle"] and not xyz["restricted_has_4_cycle"], "XYZ witness mismatch")
    require(lem["status"] == "PASS" and lem["extensions"] == 1431, "LEM witness mismatch")
    return {"xyz": xyz, "lem": lem}

def payload() -> dict:
    return {"artifact_id":"cycle-81-b081-lem-method-boundary-v1","budget_ordinal":"B081","cycle":81,"record_type":"METHOD_BOUNDARY","recorded_at_utc":"2026-08-05T20:15:00Z","status":"SEALED","epistemic_status":"PROVED","outcome":"Dominance-only and common-pivot XYZ-only bridges cannot prove the LEM spectrum assertion; equal directed girth is proved, but Question 14 remains open.","claim_boundary":"This does not refute or prove Gupta Question 14. The XYZ witness is not a uniform linear-extension distribution; sampled chain splits are bounded regression evidence only.","cycle_decision":{"companion_identity":"/root/oracle_c81_gate_review (Oracle)","companion_advice":"Close C81; retain LEM only for an order-15-or-larger inverse modular realization, and do not enlarge the census.","decision":"Seal the later-relevant method falsifier and strategic transition; open a distinct inverse-realization cycle rather than continue C81.","falsifier":"A proof that the XYZ witness is a uniform linear-extension distribution, or a valid C81 split mismatch."},"audit":audit(),"frozen_hashes":freeze_inputs(ROOT,{k:(ROOT/p,h) for k,(p,h) in HASHES.items()}),"runtime":check_runtime("c81"),"sealer":{"path":"proof/build_cycle_81_lem_method_boundary.py","sha256":sha256(Path(__file__))},"replay":{"audit":"python3 proof/check_cycle81_xyz_witness.py && python3 proof/check_cycle81_lem_witness.py","check":"python3 proof/build_cycle_81_lem_method_boundary.py --check"}}

if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
