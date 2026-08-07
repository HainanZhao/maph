#!/usr/bin/env python3
"""Standard-library full replay for C104's four-bit dihedral gate."""
from __future__ import annotations
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[1]

def main() -> None:
    with tempfile.TemporaryDirectory() as directory:
        result=Path(directory)/"result.json"
        subprocess.run([sys.executable,"proof/cycle104_book_ramsey_dihedral_cayley.py","--output",str(result)],cwd=ROOT,check=True)
        check=json.loads(subprocess.check_output([sys.executable,"proof/check_cycle104_book_ramsey_dihedral_cayley.py",str(result)],cwd=ROOT,text=True))
        data=json.loads(result.read_text())
    assert len(data["q7"])==16 and data["q7_hits"]==[] and data["q23"]==[]
    assert all(row["route_agrees"] for row in data["q7"])
    candidates=[row for row in data["q7"] if row["row_ok"]]
    assert candidates==[{"mask":3,"degree":7,"route_agrees":True,"row_ok":True,"offdiagonal_square_distribution":{"-12":7,"-8":42,"8":42},"square_ok":False,"hit":False},{"mask":14,"degree":7,"route_agrees":True,"row_ok":True,"offdiagonal_square_distribution":{"-12":49,"12":42},"square_ok":False,"hit":False}]
    assert check=={"q7_rows":16,"q7_hits":[],"q23_rows":0,"status":"PASS"}
    print(json.dumps({"status":"PASS","q7_rows":16,"q7_hits":[],"q23_rows":0},sort_keys=True))

if __name__=="__main__": main()
