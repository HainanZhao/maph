#!/usr/bin/env python3
"""Seal Cycle 211/B048's two-cusp source-section result."""
from __future__ import annotations

from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_211_cusp_asymptotic_flat_sections import run as cusp_run


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-211-b048-cusp-asymptotic-flat-sections-v1.json"
INPUTS = {
    "prior_logarithmic_connection": (ROOT / "artifacts/cycle-210-b047-logarithmic-projective-connection-v1.json", "8175697f8616ac3912ab4eeba80a77a03c0eeef3b97000aa26aa7630f522844d"),
    "prior_projective_packet": (ROOT / "artifacts/cycle-206-b043-projective-line-interface-v1.json", "a1ce1e2a0e0d9b42032dd984d9f7f7161f90e080bdf22d38650c097adfa90c8d"),
    "preregistration": (ROOT / "docs/cycle-211-b048-cusp-asymptotic-flat-sections-preregistration-v1.md", "42904756d03bda923b92dcdf72becadc3d4d94809430d86ffc210c7d0351a8f6"),
    "replay": (ROOT / "proof/verify_cycle_211_cusp_asymptotic_flat_sections.py", "0cef852e1ebf2db3b2fec48e4bc197ca79e3be9bbd14cd09a09ca73ab99d589d"),
    "regression_test": (ROOT / "tests/test_cycle_211_cusp_asymptotic_flat_sections.py", "e213a3aa8b7857a0620a0db4922f62a62ae894e8ee651db420d158cc80267a79"),
    "prototype": (ROOT / "discovery/cycle-211-b048-cusp-asymptotic-flat-sections-prototype-v1.json", "8137176a94d65d20d7d9e9283519b1489c5b3a6726b8c642e8bccbbe77f9959a"),
    "cycle206_replay": (ROOT / "proof/verify_cycle_206_projective_line_interface.py", "8e7769231af66c146f3e5b187bea6b4fe23f9c00c3359f2a606110e98019145a"),
    "stabilizer_ledger": (ROOT / "scripts/dimension_six_stabilizer_ledger.py", "594a0d541478f340abe789234335f3ff1b2d874ad8fa3507ad95026c5cc6276b"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 211 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = cusp_run()
    extrema = result["exponent_extrema"]
    sections = result["cusp_sections"]
    symmetry = result["a6_preservation_audit"]
    nonselection = result["nonselection_audit"]
    require(extrema["record_count"] == 36, "exponent census drift")
    require(extrema["maximum"] == {"exponent": 20, "unique_label": [0, 5]}, "infinity cusp drift")
    require(extrema["minimum"] == {"exponent": -25, "unique_label": [5, 0]}, "zero cusp drift")
    require(sections["record_count"] == 6, "h-channel cusp census drift")
    require(symmetry["all_cusp_lines_projectively_preserved"], "cusp symmetry drift")
    require(nonselection["distinct_projective_lines"], "cusp line distinction drift")
    require(nonselection["selection_status"] == "OPEN_REQUIRES_ADDITIONAL_SOURCE_ORIENTATION_OR_BOUNDARY_THEOREM", "scope drift")
    return {
        "artifact_id": "cycle-211-b048-cusp-asymptotic-flat-sections-v1",
        "cycle": 211,
        "budget_ordinal": "B048",
        "epistemic_status": "PROVED",
        "status": "SEALED_TWO_SOURCE_CUSP_SECTIONS_NO_DECLARED_SELECTOR",
        "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "The source packet has two, not one, all-h cusp projective sections: [e_(0,5)] and [e_(5,0)]. Both are A6/multiplier preserved, and the declared source rules select neither."},
        "exponent_extrema": extrema,
        "cusp_sections": sections,
        "a6_preservation_audit": symmetry,
        "nonselection_audit": nonselection,
        "gate_outcome": result["gate_outcome"],
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "C211 proves the two distinct all-h cusp limits [e_(0,5)] and [e_(5,0)] and their A6/multiplier stability; it shows only that the currently declared rules contain no selector, not that no source selector exists.",
            "recommendation": "Seal C211 with that narrow two-candidates/no-declared-selector boundary, then open a new orientation cycle.",
            "known_flaw": "Preservation of both lines does not exclude an arithmetic-Frobenius, attracting-endpoint, place, or analytic boundary theorem that canonically chooses one.",
            "falsifier": "Any exponent-extremum, cusp-limit, h-independence, A6 label, multiplier-phase, line-distinctness, or claimed completeness-of-source-rules discrepancy invalidates the seal.",
            "next_action": "Preregister an orientation theorem linking the pinned p37 Frobenius/A6 contraction and real embedding to t->0 or t->infinity, then test whether it selects exactly one cusp without C198 target data.",
            "adopted": True,
            "reason": "The exact source packet establishes precisely two candidates and finite symmetry preserves both; a new orientation theorem is a genuinely distinct engine.",
        },
        "preregistration_preflight": {"cycle": 211, "manifest_sha256": sha256(ROOT / "docs/cycle-211-b048-cusp-asymptotic-flat-sections-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-211-b048-cusp-asymptotic-flat-sections-preregistration-v1.md --expected-cycle 211 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_211_cusp_asymptotic_flat_sections.py --output discovery/cycle-211-b048-cusp-asymptotic-flat-sections-prototype-v1.json",
            "test_command": "python3 -m unittest tests/test_cycle_211_cusp_asymptotic_flat_sections.py",
            "write_command": "python3 proof/build_cycle_211_cusp_asymptotic_flat_sections_v1.py --write",
            "check_command": "python3 proof/build_cycle_211_cusp_asymptotic_flat_sections_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_211_cusp_asymptotic_flat_sections_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
