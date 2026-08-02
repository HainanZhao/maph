#!/usr/bin/env python3
"""Seal Cycle 169's normalized equivariant-coboundary obstruction."""
from __future__ import annotations
import json
from pathlib import Path
from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-169-equivariant-coboundary-v1.json"
FROZEN_INPUTS = {
 "project_instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
 "cycle_168_falsifier": (ROOT / "artifacts/cycle-168-carry-cocycle-v1.json", "5bd68acba19ae45f14db099e3d72f1256f90ed0973ab625d2332276bc60c2bae"),
 "preregistration": (ROOT / "docs/cycle-169-equivariant-coboundary-preregistration-v1.md", "c4ffb9f60933c2b8b12b2e6eaa5540935d79c8fc98449cf7aed3e0319ba8b753"),
 "replay": (ROOT / "proof/verify_cycle_169_equivariant_coboundary.py", "80c9395830b48e24e72aaaafcf8dcf42e6185cdf65c5d68ff12de1e49e9dd7a3"),
 "output": (ROOT / "discovery/cycle-169-equivariant-coboundary-prototype-v1.json", "27e5ef8b288b98ad80dcedb109fcb4aa812ca673ad83ea507dfcfaf9233e8c25"),
 "test": (ROOT / "tests/test_cycle_169_equivariant_coboundary.py", "f163970a91d4331dcd56a15d5a60e863a7f9342f30ef063c2171542cdb99fc19"),
 "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"), }
def payload():
 runtime = check_runtime("Cycle 169 equivariant-coboundary seal"); frozen_hashes = freeze_inputs(ROOT, FROZEN_INPUTS)
 prototype = json.loads((ROOT / "discovery/cycle-169-equivariant-coboundary-prototype-v1.json").read_text()); summary = prototype["summary"]
 require((summary["states"], summary["defect_equations"], summary["total_equations"]) == (36,1296,1335), "system size drift")
 require(summary["f2_inconsistent"] and summary["f3_inconsistent"] and not summary["normalized_t_invariant_coboundary_exists"], "obstruction drift")
 return {"artifact_id":"cycle-169-equivariant-coboundary-v1","cycle":169,"budget_ordinal":"B007","epistemic_status":"PROVED","status":"SEALED_NORMALIZED_EQUIVARIANT_COBOUNDARY_OBSTRUCTION","claim_boundary":"This exact finite result proves nontriviality only in the normalized T-invariant C6 action-groupoid coboundary quotient of the frozen Cycle-166 graph defect. It does not rule out projective equivariance, larger groupoids, higher fibres, or analytic coefficient operations.","outcome":{"epistemic_status":"PROVED","statement":"The 1,335-equation normalized T-invariant system is inconsistent over both F2 and F3, hence has no C6 solution."},"exact_prototype":{**summary,"source_output":"discovery/cycle-169-equivariant-coboundary-prototype-v1.json"},"gate_outcome":{"d6_interface":"NORMALIZED_EQUIVARIANT_COHOMOLOGY_OBSTRUCTION_PROJECTIVE_EXTENSION_REQUIRED","remaining_bottleneck":"Test a projectively T-equivariant central extension with an independently frozen character twist.","disallowed_pseudo_progress":["treating ordinary graph coboundarity as equivariant closure","claiming a TCC no-go","reusing the T-invariant quotient under new notation"]},"remaining_target":{"epistemic_status":"CONJECTURED","statement":"Cycle 170/B008: preregister a projectively T-equivariant central-extension engine with a frozen character twist and test whether it kills the defect class."},"preregistration_preflight":{"cycle":169,"manifest_sha256":sha256(ROOT / "docs/cycle-169-equivariant-coboundary-preregistration-v1.md"),"validator":{"path":"../../tools/preregistration_check.py","sha256":"a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},"frozen_hashes":frozen_hashes,"replay":{"preflight_command":"research prereg check docs/cycle-169-equivariant-coboundary-preregistration-v1.md --expected-cycle 169 --allow-head-drift","prototype_command":"python3 proof/verify_cycle_169_equivariant_coboundary.py --output discovery/cycle-169-equivariant-coboundary-prototype-v1.json","test_command":"python3 -m unittest tests.test_cycle_169_equivariant_coboundary -v","write_command":"python3 proof/build_cycle_169_equivariant_coboundary_v1.py --write","check_command":"python3 proof/build_cycle_169_equivariant_coboundary_v1.py --check"},"runtime":runtime,"sealer":{"path":"proof/build_cycle_169_equivariant_coboundary_v1.py","sha256":sha256(Path(__file__))}}
if __name__ == "__main__": raise SystemExit(run_cli(description=__doc__,output=OUTPUT,payload_factory=payload))
