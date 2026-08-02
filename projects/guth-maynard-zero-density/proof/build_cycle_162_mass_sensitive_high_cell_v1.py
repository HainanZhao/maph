#!/usr/bin/env python3
"""Seal Cycle 162 mass-sensitive high-cell extraction."""
from __future__ import annotations
from fractions import Fraction
from pathlib import Path
from typing import Any
from cycle_seal_v1 import check_runtime, freeze_inputs, load_record, require, run_cli, sha256, validate_prior

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-162-mass-sensitive-high-cell-v1.json"
INPUTS = {
 "preregistration": (ROOT / "docs/cycle-162-mass-sensitive-high-cell-preregistration-v1.md", "0b6263b24e2c6972d0a07f3f725d8e12232db2b1574f74699d96bbf38700c0b1"),
 "document": (ROOT / "docs/cycle-162-mass-sensitive-high-cell-v1.md", "61bb9001eb39058d23e2fd5cd8750543f76d8acd7a6df35f1508a01bbe483584"),
 "conventions": (ROOT / "conventions/mass_sensitive_high_cell_v1.py", "014407dab7fba3cd543b019844db04f59bf22ec2d874b91caddc015db4ea55cd"),
 "tests": (ROOT / "tests/test_cycle_162_mass_sensitive_high_cell_v1.py", "0e35320f7b4fc5c94199cea03f384cefb57be98c42a81bc66c48de358035c0c1"),
 "cycle161": (ROOT / "artifacts/cycle-161-high-cell-refinement-v1.json", "9765ae4ffd580711089301078ea295a85e50d236e40415a3a9542f875e7229ff"),
 "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
 "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
}

def seal() -> dict[str, Any]:
 validate_prior(INPUTS["cycle161"][0], "SEALED_PHASE_ALIGNED_FOUR_CYCLE_OR_LABELLED_STAR_DEGENERACY_BANKED")
 theorem = load_record(root=ROOT, path=INPUTS["conventions"][0], module_name="mass_sensitive_high_cell_v1")
 module = __import__("conventions.mass_sensitive_high_cell_v1", fromlist=["refined_high_l1_square_lower", "oriented_star_square_lower"])
 retained = module.refined_high_l1_square_lower(Fraction(576))
 star = module.oriented_star_square_lower(certificate_l1_square=Fraction(64), tau=Fraction(1,4))
 require(retained == 1 and star == 1, "exact B and orientation loss ledger")
 require("does not prove" in theorem["boundary"], "boundary")
 return {"artifact_id":"cycle-162-mass-sensitive-high-cell-v1", "epistemic_status":"PROVED", "status":"SEALED_GLOBAL_ALIGNED_FOUR_CYCLE_MASS_OR_WEIGHTED_HIGH_DEGREE_STAR_INVERSE_BANKED", "claim_boundary":"This artifact conditionally extracts global four-cycle mass or literal weighted star-edge mass from Cycle-89 excess. It does not prove excess, coordinate pullback, rational web, moment, density, or intervals.", "runtime":check_runtime("Cycle 162"), "sealer":{"path":str(SELF.relative_to(ROOT)),"sha256":sha256(SELF)}, "frozen_hashes":freeze_inputs(ROOT, INPUTS), "mass_sensitive_high_cell":{"epistemic_status":"PROVED",**theorem}, "sample":{"epistemic_status":"PROVED","refined_high_l1_square":str(retained),"oriented_star_square":str(star)}, "remaining_target":{"epistemic_status":"CONJECTURED","statement":"pull back one globally massed labelled output through the actual (d,q) coordinate map, or construct an admissible labelled obstruction"}, "density_effect":{"epistemic_status":"OBSERVED","status":"NO_PROMOTION"}, "research_stage_review_policy":{"hostile_audit":"DEFERRED_TO_PAPER_STAGE"}, "replay":{"write_command":"python3 proof/build_cycle_162_mass_sensitive_high_cell_v1.py --write","check_command":"python3 proof/build_cycle_162_mass_sensitive_high_cell_v1.py --check","test_command":"python3 -m unittest tests/test_cycle_162_mass_sensitive_high_cell_v1.py tests/test_cycle_seal_v1.py"}}

if __name__ == "__main__":
 raise SystemExit(run_cli(description=__doc__ or "Cycle 162 sealer", output=OUTPUT, payload_factory=seal))
