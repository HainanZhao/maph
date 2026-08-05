#!/usr/bin/env python3
"""Seal Cycle 44's outcome-blind non-anchor cone-or-acyclic theorem."""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path

from check_cycle_44_nonanchor import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle44-nonanchor-coupling"
OUTPUT = ROOT / "artifacts/cycle-44-b044-lrc-nonanchor-coupling-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-44-b044-lrc-nonanchor-coupling-preregistration-v1.md", "ec0dbe976dc134c2d32c93bf44df008eef28dafa23c3bede438f1ca5da53cc35"),
    "cycle43_artifact": (ROOT / "artifacts/cycle-43-b043-lrc-moment-h2-coupling-v1.json", "216b40aefe78044c00cc810e016ef904003135208d1e4d821b6a6d94a72126c9"),
    "cycle43_faces": (ROOT / "discovery/out/cycle43-moment-h2-coupling/canonical-coupling.json", "00737a038508ee4220b8ff158552afd976fab8e23194980de26879046566795b"),
    "cycle41_marginals": (ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json", "a1f742592375d035f68d3dcd0ecde65c4ee6e7b78c96fa2a1ed18362e979037e"),
    "idea_selection": (ROOT / "discovery/cycle44_nonanchor_idea_selection.md", "874f9512fde6d3eff37d25a3edb60bc82be5cf72743216e82a1ecf591413a417"),
    "selector": (ROOT / "discovery/lrc_nonanchor_select.py", "fde630c5eb6c759d0bcb4e90d882da0f6e4208c82ef9896526ad6a9b205d2096"),
    "selection": (OUT / "selection.json", "22f517ae6c7eb1f11a65cf14d18ec0a918948cd290af08fdf0d2ef0e711fd1ff"),
    "selection_timing": (OUT / "run-selection.time", "52f0a8844bbf4395a27b30e6a7e98fef619ecae84416fe0993d2625c77fab9d8"),
    "coupling_engine": (ROOT / "discovery/lrc_nonanchor_coupling.py", "1508f00e1eeb66e104b0890dcb5019405c414ac95b13ff80c9e85232f5792945"),
    "coupling_result": (OUT / "coupling.json", "32afe4526846a73f63969d8b1c95142a0bb94075b95273ec61ef31bc5f041eb9"),
    "coupling_timing": (OUT / "run-coupling-optimized.time", "56a5400f33023abe5dc38e08f8f099aed5c9a77fda396d9ea6123de5061dfe45"),
    "independent_replay": (ROOT / "proof/replay_cycle_44_nonanchor_independent.py", "b7e2fca469811e9f4fae98e5908efa7a3d360014ac52ecc377e73265ceb334b1"),
    "independent_result": (OUT / "independent-replay.json", "bbde6e468ea9f5ed77fe3b6566a91a73fc8a9c65157913d4fbe6b3058900f9e7"),
    "independent_timing": (OUT / "run-independent.time", "df2c45531e297f47acc97c14bb6ac531f2c5656e316b9978b1c4c6ef9ecd9501"),
    "soundness": (ROOT / "proof/cycle_44_nonanchor_soundness.md", "cd1d1d37a861b086d48a6b1c315cc06ec7265ce93bdec15ecfea94ee5e8a2eea"),
    "audit": (ROOT / "proof/check_cycle_44_nonanchor.py", "b9f203f50bd4b9c1ea2f11cc84968383f58cc2d085e21c89a76ac3612b1a1bf0"),
    "test": (ROOT / "tests/test_cycle_44_nonanchor.py", "41097226f091b2475ba3e07e24e64a8169a6362fa944d787aa308f38ab04f730"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def counts(values):
    return {str(key): value for key, value in sorted(Counter(values).items())}


def payload():
    checked = audit()
    selection = json.loads((OUT / "selection.json").read_text(encoding="utf-8"))
    result = json.loads((OUT / "coupling.json").read_text(encoding="utf-8"))
    replay = json.loads((OUT / "independent-replay.json").read_text(encoding="utf-8"))
    return {
        "artifact_id": "cycle-44-b044-lrc-nonanchor-coupling-v1",
        "budget_ordinal": "B044",
        "cycle": 44,
        "record_type": "PROVED_OUTCOME_BLIND_NONANCHOR_CONE_OR_ACYCLIC_FILLING",
        "recorded_at_utc": "2026-08-04T22:42:17Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "Cycle 43's shared face assignment extends rationally on all 2,000 frozen outcome-blind non-anchor interfaces: 1,528 by explicit distinguished-vertex cones and 472 by exact GF(2)-H2-zero rational-boundary existence. Every one of the 29 positive-H2 interfaces is an explicit cone.",
        "claim_boundary": "This is a deterministic stratified holdout, not all four-type multisets. It proves neither a universal cone-or-acyclic theorem nor a natural chain homotopy, the full degree-four functional, a leaf certificate, or LRC(13).",
        "selection": {"hash_candidates": selection["hash_counter_candidates"], "deduplicated_pool": selection["deduplicated_candidate_pool"], "preselection_strata": selection["preselection_strata"], "preliminary_interfaces": selection["preliminary_interfaces"], "preliminary_structural_complexes": selection["preliminary_structural_complexes"], "selected_interfaces": selection["selected_interfaces"], "h2_bin_counts": selection["h2_bin_counts"], "repeat_partition_counts": selection["repeat_partition_counts"], "density_bin_counts": selection["density_bin_counts"]},
        "construction": {"shared_face_classes": result["face_classes"], "shared_pair_classes": result["pair_classes"], "face_coefficients": result["face_coefficients"], "cycle_coefficients": sum(len(row["cycle"]) for row in result["interface_records"]), "cone_coefficients": sum(len(row["fill"]) for row in result["interface_records"]), "canonical_fills": result["canonical_fills"], "canonical_failures": result["canonical_failures"], "explicit_cones": result["cone_explained"], "h2_zero_existence_fills": result["h2_zero_existence_fills"], "elimination_only_fills": result["elimination_only_fills"], "maximum_cone_support": result["maximum_fill_nonzero"], "maximum_coefficient_bits": result["maximum_coefficient_bits"], "coherent_escalation_required": result["coherent_escalation_required"]},
        "finite_dichotomy": {"epistemic_status": "PROVED_ON_FROZEN_HOLDOUT", "h2_dimension_counts": counts(row["h2_gf2"] for row in result["interface_records"]), "route_counts": counts(row["route"] for row in result["interface_records"]), "positive_h2_interfaces": sum(bool(row["h2_gf2"]) for row in result["interface_records"]), "positive_h2_without_cone": 0, "interpretation": "Positive ambient H2 did not obstruct the actual cycle because every positive-H2 selected case has a direct cone. This motivates but does not prove a defect-supported chain homotopy."},
        "selected_family_coherence": {"epistemic_status": "PROVED", "argument": "Degree-four variables decompose by unordered type multiset after globally fixing faces. Distinct selected multisets have disjoint interior variables; repeated-type fills can be averaged over their stabilizer because boundary and allowed support are equivariant."},
        "independent_replay": {"status": replay["status"], "route": "reverse candidate and raw-pattern enumeration, lowest-bit GF(2) pivots, full selector reconstruction, and exhaustive serialized face/cycle/cone validation", "candidate_pool": replay["candidate_pool"], "selected_interfaces": replay["selected_interfaces"], "selected_structural_complexes": replay["selected_structural_complexes"], "face_coefficients_checked": replay["face_coefficients_checked"], "cycle_coefficients_checked": replay["cycle_coefficients_checked"], "cone_coefficients_checked": replay["cone_coefficients_checked"], "controls": replay["controls"]},
        "contained_resource_cap": {"status": "NO_RESULT_PROMOTED", "description": "The first implementation crossed the original 3,600-second wall cap while constructing unnecessary explicit fills on H2-zero rows. It was left to terminate naturally and was superseded within Cycle 44 by the exact universal-coefficient existence route; it does not support the theorem."},
        "audit": checked,
        "cycle_decision": {"companion_identity": "/root/darwin_cycle25_short", "outcome": "SEAL_FINITE_HOLDOUT_AND_OPEN_GLOBAL_CHAIN_HOMOTOPY_DESIGN", "scope_review": "The companion agreed to seal the finite result and identified global compatibility as the immediate bridge. The primary resolved that selected-family compatibility algebraically by direct-sum decomposition and stabilizer averaging, so another compatibility census would not be a genuinely new engine.", "strongest_flaw": "The holdout is tiny relative to all type multisets, and deterministic face selection is not naturality.", "companion_proposal": "Audit any overlap obstruction among local degree-four fills after faces are fixed.", "primary_decision": "Do not spend a cycle rediscovering an automatic direct-sum fact. Open a distinct design cycle for a parameterized chain homotopy/discrete-Morse contraction with rank-three-corner defect, paired with an abstract countermodel as falsifier.", "next_action": "Preregister the smallest falsifiable global chain-homotopy prototype: define its state space, owner-selection invariant, rank-three defect, and countermodel condition before exhaustive execution.", "falsifier": "An allowed actual structural interface where the matching cycles, changes a frozen marginal, or leaves a non-conical nonzero residual refutes the proposed homotopy family."},
        "resources": {"worker_cpus": [0, 1, 2], "reserved_cpu": 3, "aggregate_wall_cap_seconds": 14400, "selection_wall_seconds": selection["wall_seconds"], "optimized_coupling_wall_seconds": result["wall_seconds"], "independent_wall_seconds": replay["wall_seconds"], "validated_wall_seconds": selection["wall_seconds"] + result["wall_seconds"] + replay["wall_seconds"], "optimized_peak_rss_kib": 1274424, "independent_peak_rss_kib": 1220100, "temporary_disk_cap_bytes": 5368709120},
        "runtime": check_runtime("Cycle 44 outcome-blind non-anchor cone-or-acyclic filling"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {"selector_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_nonanchor_select.py", "coupling_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_nonanchor_coupling.py", "independent_command": "taskset -c 0-2 .venv/bin/python proof/replay_cycle_44_nonanchor_independent.py", "audit_command": ".venv/bin/python proof/check_cycle_44_nonanchor.py", "test_command": ".venv/bin/python -m unittest tests.test_cycle_44_nonanchor -v", "check_command": ".venv/bin/python proof/build_cycle_44_lrc_nonanchor.py --check"},
        "sealer": {"path": "proof/build_cycle_44_lrc_nonanchor.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
