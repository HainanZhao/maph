"""Seal C86's all-inclusion Hall transport boundary."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


OUTPUT = ROOT / "artifacts/cycle-86-b086-frankl-all-inclusion-hall-boundary-v1.json"
HASHES = {
    "preregistration": ("docs/cycle-86-b086-frankl-all-inclusion-hall-preregistration-v1.md", "b82e71a9aa659931f73d5c21b743527f55b3ab77afb4340f1ad3fb73c3c3ab4b"),
    "idea_selection": ("discovery/cycle86_frankl_hall_selection.md", "d1e753fcb1210cf3d9c001a7b6a47cd6a149ca873da31a17b6f8d9198a08c1b2"),
    "source_audit": ("discovery/cycle86_frankl_source_audit.md", "b580436ee2040d5ba36f16c21892b29fd60abdd6131701e969997a9b7b7e9584"),
    "checker": ("proof/check_cycle86_frankl_all_inclusion_hall.py", "b1d2536e8e1d36e83f1c2a7c5ddc666b78fb970aa995b5be8271f9a52fc8045f"),
    "boundary": ("proof/cycle86_all_inclusion_hall_boundary.md", "164e8068e991fc12435adf8183b8b2f4a2d463c7d3eba7b813eb11cdb32135a4"),
    "test": ("tests/test_cycle86_frankl_all_inclusion_hall.py", "5253bf84ab9db5151a76a75b7fccbeb5d68e34165a5c6af4d459e22c9981b0dd"),
    "prior_c85": ("artifacts/cycle-85-b085-sidorenko-c5-kernel-boundary-v1.json", "3fb242906c97496c6a5e32cd373880a4b487db231aaa81b827df8ecc1e61e131"),
    "scaffold": ("proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "validator": ("../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def audit() -> dict:
    result = json.loads(subprocess.check_output([sys.executable, str(ROOT / HASHES["checker"][0])], text=True))
    require(result["status"] == "PASS" and result["family_masks"] == 65536, "census failure")
    require(result["retained_dimension_three"] == 2034 and result["all_optimal_hall_failures"] == 0, "four-point control drift")
    require(result["verifier_disagreements"] == 0, "matching/Hall verifier disagreement")
    controls = result["source_controls"]
    require(controls["example_319"]["optimal_1_hall_witness"] == [[0, 2, 4, 6], [3, 5, 7]], "Example 3.19 drift")
    require(controls["example_320"]["all_inclusion_matching"] == [False] * 5, "Example 3.20 no longer falsifies transport")
    require(all(witness is not None for witness in controls["example_320"]["hall_witnesses"]), "missing Example 3.20 Hall witness")
    return result


def payload() -> dict:
    return {
        "artifact_id": "cycle-86-b086-frankl-all-inclusion-hall-boundary-v1",
        "budget_ordinal": "B086",
        "cycle": 86,
        "record_type": "METHOD_BOUNDARY",
        "recorded_at_utc": "2026-08-06T00:56:24Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "All 2,034 declared four-point dimension-three controls have an optimal all-inclusion Hall matching, but Colbert's stated five-point Example 3.20 has every element optimal and abundant while every such matching fails. The proposed transport mechanism is therefore false.",
        "claim_boundary": "This refutes only the all-inclusion Hall transport mechanism. It neither refutes height-four Frankl nor excludes weighted, non-inclusion, or rank-layer transports.",
        "cycle_decision": {
            "companion_identity": "/root/oracle_c86_portfolio (Oracle)",
            "companion_advice": "Test the all-inclusion transport on the complete four-point gate and mandatory source controls; any all-optimal Hall failure ends the mechanism without an enlarged census.",
            "decision": "Seal the exact method boundary because Example 3.20 is the preregistered adverse control and falsifies all-inclusion transport for every optimal element.",
            "falsifier": "A Hall-deficient left subset for each optimal element in a retained family or named source control, or disagreement between matching and exhaustive Hall verification.",
        },
        "audit": audit(),
        "frozen_hashes": freeze_inputs(ROOT, {key: (ROOT / path, digest) for key, (path, digest) in HASHES.items()}),
        "runtime": check_runtime("c86"),
        "sealer": {"path": "proof/build_cycle_86_frankl_all_inclusion_hall_boundary.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "audit": "python3 proof/check_cycle86_frankl_all_inclusion_hall.py",
            "test": "python3 -c \"import runpy; ns=runpy.run_path('tests/test_cycle86_frankl_all_inclusion_hall.py'); ns['test_c86_four_point_control_and_source_falsifier']()\"",
            "check": "python3 proof/build_cycle_86_frankl_all_inclusion_hall_boundary.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
