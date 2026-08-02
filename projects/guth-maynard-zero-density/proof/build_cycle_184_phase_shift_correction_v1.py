#!/usr/bin/env python3
"""Seal Cycle 184's positive-exponential slope correction."""
from __future__ import annotations
from pathlib import Path
import sys
from typing import Any
from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
if str(REPOSITORY_ROOT) not in sys.path: sys.path.insert(0, str(REPOSITORY_ROOT))
from tools.preregistration_check import validate_preregistration  # noqa: E402

SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-184-phase-shift-correction-v1.json"
TOOL_HASH = "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"
INPUTS = {
 "preregistration":(ROOT/"docs/cycle-184-phase-shift-correction-preregistration-v1.md","a7cc179cd5a73bcba641b55c35043de2bc575738504783ea3ecce2a22258fa60"),
 "document":(ROOT/"docs/cycle-184-phase-shift-correction-v1.md","34ebde2f4e1cb34462eeddb12fa5896ad3b724e739f044897f14c0b4d0c70655"),
 "conventions":(ROOT/"conventions/cycle_184_phase_shift_correction_v1.py","7bd4f0a032d60b5983177983579f34c15747ccbfe5f45be92c5f22a636868864"),
 "tests":(ROOT/"tests/test_cycle_184_phase_shift_correction_v1.py","457f73efa12a9519d6c9fc97a80f697d047d632d139bed1accd6baaa84c6bcb2"),
 "affected_artifact":(ROOT/"artifacts/cycle-184-ray-box-determinant-orbit-v1.json","02a9c3e61166c6a265dd5f14dd80043daf8f6de5063594161cb435b68a340e25"),
 "sealing_scaffold":(ROOT/"proof/cycle_seal_v1.py","96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
}
def exact(v: object) -> object:
 from fractions import Fraction
 if isinstance(v,Fraction): return str(v.numerator) if v.denominator==1 else f"{v.numerator}/{v.denominator}"
 if isinstance(v,dict): return {str(k):exact(x) for k,x in v.items()}
 if isinstance(v,(tuple,list)): return [exact(x) for x in v]
 return v
def seal() -> dict[str,Any]:
 require(sha256(REPOSITORY_ROOT/"tools/preregistration_check.py")==TOOL_HASH,"validator hash")
 checked=validate_preregistration(INPUTS["preregistration"][0],expected_cycle=184,enforce_manifest_head=False)
 module=__import__("conventions.cycle_184_phase_shift_correction_v1",fromlist=["theorem_record"])
 theorem=module.theorem_record()
 return {"artifact_id":"cycle-184-phase-shift-correction-v1","epistemic_status":"PROVED","status":"SEALED_CORRECTION_SHIFTED_SLOPES_NONRATIONAL_TWO_RAY_DEFORMATION","claim_boundary":"This corrects C184's deformation convention only; it proves no critical-box bound, recurrence, density gain, or interval result.","affected_artifact":{"path":"artifacts/cycle-184-ray-box-determinant-orbit-v1.json","sha256":INPUTS["affected_artifact"][1],"disposition":"immutable; LCM algebra unaffected, deformation wording superseded by shifted slopes."},"runtime":check_runtime("Cycle 184 correction"),"sealer":{"path":str(SELF.relative_to(ROOT)),"sha256":sha256(SELF)},"frozen_hashes":freeze_inputs(ROOT,INPUTS),"preregistration_preflight":{"cycle":checked["cycle"],"manifest_sha256":checked["manifest_sha256"],"input_hashes":checked["input_hashes"],"parameters":checked["parameters"]},"corrected_result":exact(theorem),"density_effect":{"epistemic_status":"OBSERVED","status":"NO_PROMOTION"},"replay":{"check_command":"python3 proof/build_cycle_184_phase_shift_correction_v1.py --check","write_command":"python3 proof/build_cycle_184_phase_shift_correction_v1.py --write","test_command":"python3 -m unittest tests/test_cycle_184_phase_shift_correction_v1.py"}}
if __name__ == "__main__": raise SystemExit(run_cli(description=__doc__ or "C184 correction",output=OUTPUT,payload_factory=seal))
