#!/usr/bin/env python3
"""Seal Cycle 166's exact fibre-resolved multiplier-torsor result."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts" / "cycle-166-fibre-torsor-v1.json"
FROZEN_INPUTS = {
    "project_instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "cycle_165_obstruction": (ROOT / "artifacts/cycle-165-section-equivariance-v1.json", "0e485ac41f8a5b71c6f22e128be3071b3f9d75b18b52dce7ed626a38f9dd8405"),
    "preregistration": (ROOT / "docs/cycle-166-fibre-torsor-preregistration-v1.md", "b461465675743d9bfc6bede5e3d79022978e8cfd8825763d0e9fc79bc64621e3"),
    "decision_record": (ROOT / "docs/cycle-166-fibre-torsor-v1.md", "c6757bbdd35a7ee34a13aa47dd8357004f50860ad519ce7ddb7e1cc54bb925e3"),
    "working_ledger": (ROOT / "discovery/cycle-166-fibre-torsor-working-ledger.md", "89d39eb675de4b0d81bb53bec9e02a235f22828355dc990c42161ec5fe094f3f"),
    "torsor_replay": (ROOT / "proof/verify_cycle_166_fibre_torsor.py", "0bc7df3652113925349b5c102a4c2abe6ed85d510fc401486b465f24272edbb5"),
    "torsor_output": (ROOT / "discovery/cycle-166-fibre-torsor-prototype-v1.json", "d21c50ffa317f4b1f8faa8d78c13e006b1d97e6725cda07d01ee50029d6b9a53"),
    "test": (ROOT / "tests/test_cycle_166_fibre_torsor.py", "0ef892e684ec053d28ef2accc217b13751c3802f76eaec8ad0275287f22d5781"),
    "sealing_scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 166 fibre-torsor seal")
    frozen_hashes = freeze_inputs(ROOT, FROZEN_INPUTS)
    prototype = json.loads(
        (ROOT / "discovery/cycle-166-fibre-torsor-prototype-v1.json").read_text()
    )
    summary = prototype["summary"]
    require(summary["base_rows_checked"] == 36, "wrong base row count")
    require(summary["torsor_states_checked"] == 216, "wrong torsor state count")
    require(summary["orbit_count"] == 14, "wrong orbit count")
    for name in (
        "phase_differences_all_divisible_by_8",
        "all_multiplier_square_identities_match",
        "all_t_orbit_holonomies_zero",
        "lifted_third_return_identity",
        "graph_intertwining",
    ):
        require(summary[name] is True, f"failed finite invariant: {name}")
    require(summary["orientation_anchors"] == {"3,4": 2, "3,5": 1}, "anchor drift")
    return {
        "artifact_id": "cycle-166-fibre-torsor-v1",
        "cycle": 166,
        "budget_ordinal": "B004",
        "epistemic_status": "PROVED",
        "status": "SEALED_FIBRE_RESOLVED_MULTIPLIER_TORSOR",
        "claim_boundary": (
            "This exact finite result constructs a phase-derived fibre-resolved C6 transport torsor. "
            "It defines no additive coefficient-to-logarithm operation, analytic continuation, finite part, "
            "AFK-interface identification, Stark identity, fusion theorem, or TCC identity."
        ),
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": "The frozen phase law yields an anchor-preserving C6 torsor transport over all 36 characteristics: its 14 orbit holonomies vanish, its lifted Shintani third return is the identity on all 216 states, and its normalized graph exactly intertwines transport.",
        },
        "exact_prototype": {
            "base_rows_checked": summary["base_rows_checked"],
            "torsor_states_checked": summary["torsor_states_checked"],
            "orbit_count": summary["orbit_count"],
            "phase_differences_all_divisible_by_8": summary["phase_differences_all_divisible_by_8"],
            "all_multiplier_square_identities_match": summary["all_multiplier_square_identities_match"],
            "all_t_orbit_holonomies_zero": summary["all_t_orbit_holonomies_zero"],
            "lifted_third_return_identity": summary["lifted_third_return_identity"],
            "graph_intertwining": summary["graph_intertwining"],
            "orientation_anchors": summary["orientation_anchors"],
            "source_output": "discovery/cycle-166-fibre-torsor-prototype-v1.json",
        },
        "gate_outcome": {
            "d6_interface": "FIBRE_RESOLVED_MULTIPLIER_TORSOR_SEALED_ADDITIVE_CONVOLUTION_REQUIRED",
            "surviving_construction": "phase-derived C6 torsor transport retaining the fibre coordinate and both orientation anchors",
            "remaining_bottleneck": "An independently specified additive coefficient operation must be defined and checked; graph transport alone is not such an operation.",
            "disallowed_pseudo_progress": [
                "calling the defining graph transport an additive coefficient-to-logarithm operation",
                "choosing a coboundary or product only after inspecting the graph defect",
                "claiming AFK, Stark, fusion, or TCC compatibility from finite transport alone",
            ],
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "Cycle 167/B005: preregister an independent translation-invariant bilinear C6-twisted convolution family on the sealed torsor and test exact graph/product and transport compatibility, or falsify that named class."
        },
        "preregistration_preflight": {
            "cycle": 166,
            "manifest_sha256": sha256(ROOT / "docs/cycle-166-fibre-torsor-preregistration-v1.md"),
            "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"},
        },
        "mentor_checkpoint": {
            "identity": "/root/decision_companion_2",
            "recommendation": "Seal Cycle 166/B004 as PROVED only for the convention-pinned finite phase-derived fibre-resolved C6 torsor, then continue the interface gate.",
            "known_flaw": "Finite transport and graph intertwining are not an additive coefficient-to-logarithm operation.",
            "falsifier": "Any replay discrepancy, phase/multiplier mismatch, nonzero holonomy, failed third return, moved anchor, or broader interpretation invalidates the seal.",
            "next_action": "Preregister an independently specified additive/convolution operation family on the torsor with exact log-compatibility or a named-class falsifier.",
            "resolution": "ADOPTED",
        },
        "frozen_hashes": frozen_hashes,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-166-fibre-torsor-preregistration-v1.md --expected-cycle 166 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_166_fibre_torsor.py --output discovery/cycle-166-fibre-torsor-prototype-v1.json",
            "test_command": "python3 -m unittest tests.test_cycle_166_fibre_torsor -v",
            "write_command": "python3 proof/build_cycle_166_fibre_torsor_v1.py --write",
            "check_command": "python3 proof/build_cycle_166_fibre_torsor_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_166_fibre_torsor_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
