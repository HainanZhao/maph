"""Seal Cycle 43's exact selected canonical moment-H2 coupling theorem."""
from __future__ import annotations

import json
from pathlib import Path

from check_cycle_43_moment_h2 import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle43-moment-h2-coupling"
OUTPUT = ROOT / "artifacts/cycle-43-b043-lrc-moment-h2-coupling-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-43-b043-lrc-moment-h2-coupling-preregistration-v1.md", "26447bc7ff648b64b1cf098270db421b411b6aef110a2e032653b309db99a2e0"),
    "cycle42_artifact": (ROOT / "artifacts/cycle-42-b042-lrc-h2-horn-v1.json", "6c0140e4f3bd5f11faec264a92dea81d4905eb2320e5e5596fb2c4fbac416487"),
    "idea_selection": (ROOT / "discovery/cycle43_moment_h2_idea_selection.md", "b2d46943de9fddf9a4b6a6d8c472deb4981426ea8370938a36ffd050943d29e1"),
    "engine": (ROOT / "discovery/lrc_moment_h2_coupling.py", "935e34313e50b324933c79a343a6f23747c66bb3845ea4ddbf9a9c1cefdb4870"),
    "result": (OUT / "canonical-coupling.json", "00737a038508ee4220b8ff158552afd976fab8e23194980de26879046566795b"),
    "timing": (OUT / "run-canonical.time", "9de8babc94a6ac11f7b59bfc9f9511cdbc684de5cdbfa643172ef72f852cf283"),
    "independent_replay": (ROOT / "proof/replay_cycle_43_moment_h2_independent.py", "2e7290cbfa174ec4d717e158ceeb6844197661933ac544c10c650a65ae358c4e"),
    "independent_result": (OUT / "independent-replay.json", "fc6ff80de946df8b4d49c4214ec8918a525361eb1d9f50bacb56af8b02b06262"),
    "independent_timing": (OUT / "run-independent.time", "c5ace49c039ef9e83c41d90d23c535ceb00ac9bace611c42e6bb4d56a0ffaeb5"),
    "soundness": (ROOT / "proof/cycle_43_moment_h2_soundness.md", "4b67f8a42452fc6a74d7b66fc7cbb09d86b9d70d3048d59bb7f79b3b96c9fca6"),
    "audit": (ROOT / "proof/check_cycle_43_moment_h2.py", "ee2cb7b35265fe97e056a2954e87cb35f80b3b45f0aea281d6ed27e6328a52cc"),
    "test": (ROOT / "tests/test_cycle_43_moment_h2.py", "55be0a9443787ad28e8132b58e9b7849a93bf9ca40f8ba3802da1a2b4281be6f"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def payload():
    checked = audit()
    result = json.loads((OUT / "canonical-coupling.json").read_text(encoding="utf-8"))
    replay = json.loads((OUT / "independent-replay.json").read_text(encoding="utf-8"))
    face_distribution = CounterLike(len(row["coefficients"]) for row in result["face_tensors"])
    fill_distribution = CounterLike(len(row["fill"]) for row in result["interface_records"])
    return {
        "artifact_id": "cycle-43-b043-lrc-moment-h2-coupling-v1",
        "budget_ordinal": "B043",
        "cycle": 43,
        "record_type": "PROVED_SELECTED_CANONICAL_MOMENT_H2_FILLING",
        "recorded_at_utc": "2026-08-04T20:48:34Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "One globally shared repeated-type-symmetric Cycle 41 face assignment produces an exact integral tetrahedral filling on all 3,954 Cycle 42 selected interfaces, despite nonzero ambient H2 on 3,893 of them.",
        "claim_boundary": "This is the frozen three-anchor family only. Deterministic lowest-pivot canonicality is not naturality. The result is not all quadruples, a full degree-four functional, a complete rank-three-multiplier layer, a leaf certificate, or LRC(13).",
        "construction": {"raw_interfaces": result["raw_interfaces"], "structural_complexes": result["structural_complexes"], "unordered_shared_faces": result["unordered_face_classes"], "oriented_shared_pairs": result["oriented_pair_classes"], "face_coefficients": result["canonical_face_nonzero"], "cycle_coefficients": sum(len(row["cycle"]) for row in result["interface_records"]), "fill_coefficients": sum(len(row["fill"]) for row in result["interface_records"]), "canonical_fills": result["canonical_fills"], "canonical_failures": result["canonical_failures"], "maximum_fill_support": result["maximum_fill_nonzero"], "maximum_coefficient_bits": max(result["maximum_face_bits"], result["maximum_fill_bits"]), "coherent_escalation_required": result["coherent_escalation_required"]},
        "sparse_pattern": {"epistemic_status": "OBSERVED_WITHIN_PROVED_CENSUS", "face_support_distribution": face_distribution, "fill_support_distribution": fill_distribution, "interpretation": "The twelve seven-term cases are signed cube-with-one-corner faces with corresponding seven-term cone fills; this suggests but does not prove a contraction mechanism."},
        "independent_replay": {"status": replay["status"], "route": "direct type/signature membership in reverse order plus exhaustive serialized face, marginal, cycle, and fill checks", "face_coefficients_checked": replay["face_coefficients_checked"], "cycle_coefficients_checked": replay["cycle_coefficients_checked"], "fill_coefficients_checked": replay["fill_coefficients_checked"], "controls": replay["controls"]},
        "audit": checked,
        "cycle_decision": {"companion_identity": "/root/darwin_cycle25_short", "outcome": "SEAL_SELECTED_FILLING_AND_OPEN_STRATIFIED_NONANCHOR_HOLDOUT", "scope_review": "Every actual selected class fills, but the anchors were chosen from Cycle 41's H1 boundary and cannot establish a natural chain contraction.", "strongest_flaw": "Anchor bias and deterministic, non-natural face selection; selected fills do not span the full rank-three-literal layer.", "next_action": "Open Cycle 44 for a preregistered stratified non-anchor coupling holdout across support profiles, deletion patterns, density, and repeated-type regimes, while recording whether each fill is explained by an explicit cone part.", "falsifier": "An exact non-anchor canonical moment cycle with a dual H2 cochain of nonzero pairing refutes the selected canonical extension pattern."},
        "resources": {"worker_cpus": [0, 1, 2], "reserved_cpu": 3, "cycle_wall_upper_bound_seconds": 1200, "principal_wall_seconds": result["wall_seconds"], "independent_wall_seconds": replay["wall_seconds"], "peak_rss_kib": 1222488, "temporary_disk_cap_bytes": 5368709120},
        "runtime": check_runtime("Cycle 43 selected canonical moment-H2 coupling"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {"primary_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_moment_h2_coupling.py", "independent_command": "taskset -c 0-2 .venv/bin/python proof/replay_cycle_43_moment_h2_independent.py", "audit_command": ".venv/bin/python proof/check_cycle_43_moment_h2.py", "test_command": ".venv/bin/python -m unittest tests.test_cycle_43_moment_h2 -v", "check_command": ".venv/bin/python proof/build_cycle_43_lrc_moment_h2.py --check"},
        "sealer": {"path": "proof/build_cycle_43_lrc_moment_h2.py", "sha256": sha256(Path(__file__))},
    }


def CounterLike(values):
    counts = {}
    for value in values:
        counts[str(value)] = counts.get(str(value), 0) + 1
    return counts


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
