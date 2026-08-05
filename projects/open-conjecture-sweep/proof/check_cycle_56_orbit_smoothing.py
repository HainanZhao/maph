from __future__ import annotations
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/"discovery/out/cycle56-orbit-smoothing"
def rows(n):
 with (OUT/n).open() as f:return list(csv.DictReader(f,delimiter="\t"))
def audit():
 a=json.loads((OUT/"summary.json").read_text());b=json.loads((OUT/"independent-summary.json").read_text());x,y=rows("rows.tsv"),rows("independent-rows.tsv")
 assert a==b=={"status":"PASS","rows":1458,"negative_rows":0};assert sorted(tuple(z.items()) for z in x)==sorted(tuple(z.items()) for z in y);assert all(int(z["sign"])>=0 for z in x)
 return {"status":"PASS","epistemic_status":"PROVED","functions":729,"rows":1458,"negative_rows":0,"claim_boundary":"Frozen ternary S3 one-orbit smoothing packet only; no universal orbitwise smoothing or Zhao conclusion."}
if __name__=="__main__":print(json.dumps(audit(),sort_keys=True))
