#!/usr/bin/env python3
"""Seal Cycle 107 actual-scale geometric stationary phase."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from cycle_seal_v1 import (
    check_runtime,
    freeze_inputs,
    load_record,
    require,
    run_cli,
    sha256,
    validate_prior,
)


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
OUTPUT = ROOT / "artifacts/cycle-107-actual-scale-phase-v1.json"
INPUTS = {
    "discovery_candidate": (ROOT / "discovery/cycle-107-actual-scale-phase-candidate-v1.md", "98c72c9210eaad48033fa5d20a2925b4577041dfead0ee22c6d0df0b76d7f7db"),
    "preregistration": (ROOT / "docs/cycle-107-actual-scale-phase-preregistration-v1.md", "01253503e31da923bc5bbfd7afae4e295feeded1a561c64f6a99f5731b312e9d"),
    "document": (ROOT / "docs/cycle-107-actual-scale-phase-v1.md", "a8b127ee16e413d90635cb00e449d20b4342d0fdd120cd12dca24002c9e67d90"),
    "conventions": (ROOT / "conventions/actual_scale_phase_v1.py", "8e4b3271d0062e27bfedc6a8efb6c2fdda65b673faef3d76fde05097f6433a3d"),
    "tests": (ROOT / "tests/test_cycle_107_actual_scale_phase_v1.py", "08c372634e56f7e6d63122adc8a230f5741fbb0566bda50dbd68847892f6792f"),
    "seal_scaffold": (ROOT / "proof/cycle_seal_v1.py", "96d404c0e493144d72e593b789062daeaa2bd2481ec8b84641a1e19f9cd646b9"),
    "seal_scaffold_tests": (ROOT / "tests/test_cycle_seal_v1.py", "5ae01d03653e8846b487869af99f9a1a4901e39570111e89495ddd27982f6427"),
    "cycle106": (ROOT / "artifacts/cycle-106-beta-free-saturation-v1.json", "0e681ebf90d531a9564677779016642afbb73cf6c0cc47760b4b17db4b2bf3d1"),
}


def seal() -> dict[str, Any]:
    validate_prior(
        INPUTS["cycle106"][0],
        "SEALED_UNSIGNED_ALL_SCALE_SATURATOR_BETA_PAYLOAD_LOCK",
    )
    theorem = load_record(
        root=ROOT,
        path=INPUTS["conventions"][0],
        module_name="actual_scale_phase_v1",
    )
    require("lcm" in theorem["lambda0"], "actual scale lattice")
    require("Phi_ell=ell*Phi0" in theorem["phase"], "phase homogeneity")
    require("amplitude variation" in theorem["boundary"], "analytic boundary")
    return {
        "artifact_id": "cycle-107-actual-scale-phase-v1",
        "epistemic_status": "PROVED",
        "status": "SEALED_ACTUAL_SCALE_GEOMETRIC_PHASE_RESONANCE_OR_BV_CANCELLATION",
        "claim_boundary": (
            "This artifact proves the actual anchor scale lattice, stationary/phase "
            "homogeneity, and geometric/BV cancellation. It proves no actual amplitude "
            "variation bound, resonance-to-seed theorem, remaining branch closure, "
            "complete moment, density gain, or interval gain."
        ),
        "runtime": check_runtime("Cycle 107"),
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "prior_context": {
            "epistemic_status": "PROVED",
            "cycle106_role": "supply exact rational scale progressions and beta payload lock",
        },
        "actual_phase_theorem": {"epistemic_status": "PROVED", **theorem},
        "e16_interface": {
            "epistemic_status": "PROVED",
            "statement": (
                "a nonsaving scale class must retain near-integral Phi0 together with "
                "c0, beta payload, Poisson modes, base indices, and stationary coordinates"
            ),
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "prove bounded variation for the actual B-process amplitudes and convert "
                "near-integral base phase to a Cycle-67 seed or a smaller resonant class"
            ),
        },
        "containment": {
            "epistemic_status": "OBSERVED",
            "statement": (
                "the first test exposed only SymPy's failure to normalize a complete "
                "cubic root-of-unity sum; exact order reduction fixed the replay helper"
            ),
        },
        "density_effect": {"epistemic_status": "OBSERVED", "status": "NO_PROMOTION"},
        "research_stage_review_policy": {"hostile_audit": "DEFERRED_TO_PAPER_STAGE"},
        "replay": {
            "write_command": "python3 proof/build_cycle_107_actual_scale_phase_v1.py --write",
            "check_command": "python3 proof/build_cycle_107_actual_scale_phase_v1.py --check",
            "test_command": (
                "python3 -m unittest tests/test_cycle_107_actual_scale_phase_v1.py "
                "tests/test_cycle_seal_v1.py"
            ),
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__ or "Cycle 107 sealer", output=OUTPUT, payload_factory=seal))
