#!/usr/bin/env python3
"""Seal Cycle 45's Morse projection theorem and local-axiom falsifiers."""
from __future__ import annotations

import json
from pathlib import Path

from check_cycle_45_morse import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle45-critical-projection"
OUTPUT = ROOT / "artifacts/cycle-45-b045-lrc-critical-projection-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-45-b045-lrc-critical-projection-preregistration-v1.md", "e0cae514468762e4be5aa02f74c199800bba0f7740285ab567af9b0303690c59"),
    "cycle44_artifact": (ROOT / "artifacts/cycle-44-b044-lrc-nonanchor-coupling-v1.json", "9599f64027d120467c1bba556a8e5fdd6c7868f3c655e88fa165af2887418a72"),
    "cycle43_faces": (ROOT / "discovery/out/cycle43-moment-h2-coupling/canonical-coupling.json", "00737a038508ee4220b8ff158552afd976fab8e23194980de26879046566795b"),
    "cycle44_coupling": (ROOT / "discovery/out/cycle44-nonanchor-coupling/coupling.json", "32afe4526846a73f63969d8b1c95142a0bb94075b95273ec61ef31bc5f041eb9"),
    "cycle41_closure": (ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json", "a1f742592375d035f68d3dcd0ecde65c4ee6e7b78c96fa2a1ed18362e979037e"),
    "idea_selection": (ROOT / "discovery/cycle45_chain_homotopy_idea_selection.md", "51bd73402a94879758bfb233dbb344ca658b353a1b6be56c1cfa60aad4760fb8"),
    "generic_operator": (ROOT / "discovery/lrc_morse_critical_projection.py", "669991dedd193fa7d27aef1fa47995bac5fe59b2e5fb5858c7eafd0509326bb2"),
    "actual_engine": (ROOT / "discovery/lrc_morse_actual.py", "303b0f3c70f4af019bf0274d76e05b1df1e6ab5e4ed548a2ca358d8015ed31fa"),
    "actual_result": (OUT / "actual-corpus-layered.json", "814b7159834c6930a89a84b450d7a273b4465ba101a38140060a0a536dafdb64"),
    "actual_timing": (OUT / "run-actual-layered.time", "0146809183e7ba03d6d7d1f3c01a2a3bfbda78f2a7f5c49229762c3c5755d98d"),
    "abstract_engine": (ROOT / "discovery/lrc_morse_abstract.py", "55be8e0f7eb04e569256d7f105b0058ddcf159a9df4cf0ccba0e98649cdac491"),
    "abstract_result": (OUT / "abstract-models.json", "27f78885d0718e8237929c13d5f4e44c812a350cfc969e801939de63ed5fe0b8"),
    "abstract_timing": (OUT / "run-abstract-layered.time", "8afa21e2461ac005a22d51097932fe4f84679f0b564eac6d2cb084d411bec7ce"),
    "signature_engine": (ROOT / "discovery/lrc_morse_signature_abstract.py", "cbe36e4f3618777fe9b93f4b10700bace4f4571b2929fe607eac0d7e7b3620a6"),
    "signature_result": (OUT / "signature-abstract-models.json", "92f9426404ac3fb8207355aea0b53e22d084c5d9ad367fccff676efbed50cc9f"),
    "signature_timing": (OUT / "run-signature-abstract.time", "1b67b80a767e039dc452a1bbcd5e7eae6bf81174a972afd429864b0df321466e"),
    "independent_replay": (ROOT / "proof/replay_cycle_45_morse_independent.py", "61aae6413cebf09501576e6b0dd9dcf24d5aa690db1604c3a38b99bb60fadcf9"),
    "independent_result": (OUT / "independent-actual-replay.json", "152a4c497c1b0a9ed61a00490b90d2ea63a79a585663c2c96aa1a35349284488"),
    "independent_timing": (OUT / "run-independent-actual.time", "7e2f5749b457dd2242adb19c66293c785f232897ff73e64c1679a36c4de778bb"),
    "soundness": (ROOT / "proof/cycle_45_morse_soundness.md", "2b171e12a4b09c11dea9d1e7fbf5268e524ef8e3b4558b814e5e20af722d1be5"),
    "audit": (ROOT / "proof/check_cycle_45_morse.py", "ca93a52bbe474189bcf949c252d2a1f9431994bb53a805bc5f939e82abfb4cc3"),
    "test": (ROOT / "tests/test_cycle_45_morse.py", "9c64f8e4c1d43154b5221b5c9caac88cbd5c6a86bccc5d5ab9ce4fcbe52899cb"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "preregistration_validator": (ROOT / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def payload():
    checked = audit()
    actual = json.loads((OUT / "actual-corpus-layered.json").read_text())
    abstract = json.loads((OUT / "abstract-models.json").read_text())
    signature = json.loads((OUT / "signature-abstract-models.json").read_text())
    independent = json.loads((OUT / "independent-actual-replay.json").read_text())
    return {
        "artifact_id": "cycle-45-b045-lrc-critical-projection-v1",
        "budget_ordinal": "B045",
        "cycle": 45,
        "record_type": "PROVED_MORSE_PROJECTION_AND_LOCAL_AXIOM_FALSIFIERS",
        "recorded_at_utc": "2026-08-05T00:31:00Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "The stagewise distinguished-owner matching gives a finite acyclic Morse flow and an exact chain homotopy dh+hd=I-pi. On all 5,954 frozen actual interfaces the first schedule leaves 470 residuals and the extended schedule leaves 457, all rational boundaries. Exact arbitrary and signature-realizable abstract searches produce respectively 2,647 and 649 nonboundary residual models, proving that local blocker/signature geometry cannot explain the actual vanishing; the missing state is global p199 type and marginal closure.",
        "claim_boundary": "The generic homotopy identity and frozen finite classifications are proved. This does not prove annihilation on every actual type multiset, characterize p199 realizability, construct the full degree-four functional or a leaf certificate, or prove LRC(13).",
        "generic_theorem": {
            "statement": "For a finite simplicial complex, greedy pairing by an ordered sequence of vertices is acyclic. With V on matched lower cells and Phi=I+dV+Vd, the stabilized projection pi satisfies dh+hd=I-pi and is a chain map.",
            "coefficient_ring": "Z incidences; instantiated over Q",
            "proof_route": "single-stage insertion monotonicity, stagewise patchwork induction, and finite gradient-path stabilization",
        },
        "actual_corpus": {
            "interfaces": actual["actual_interfaces"],
            "allowed_simplices_weighted": actual["aggregate_allowed_simplices"],
            "matching_cycles": actual["matching_cycles"],
            "initial_zero": actual["zero_projections"],
            "initial_nonzero": actual["nonzero_projections"],
            "extended_zero": actual["extended_zero_projections"],
            "extended_nonzero": actual["extended_nonzero_projections"],
            "maximum_projection_support": actual["maximum_projection_nonzero"],
            "maximum_extended_steps": actual["maximum_extended_flow_steps"],
            "nonboundary_residuals": actual["nonboundary_projections"],
            "classification": "All 3,954 Cycle 43 rows and all 1,528 explicit Cycle 44 cones project to zero initially. Of 472 Cycle 44 GF(2)-H2-zero noncones, 2 project to zero and 470 remain; the extended schedule kills 13 more.",
        },
        "local_axiom_falsifiers": {
            "arbitrary_models": {"deduplicated": abstract["deduplicated_models"], "face_admissible": abstract["admissible_face_models"], "initial_nonboundary": abstract["nonboundary_projection_models"], "extended_nonboundary": abstract["extended_nonboundary_projection_models"], "rank3_free_nonboundary": abstract["rank3_free_nonboundary_projection_models"]},
            "signature_realizable_models": {"deduplicated": signature["deduplicated_signature_models"], "face_admissible": signature["admissible_face_models"], "initial_nonboundary": signature["nonboundary_projection_models"], "extended_nonboundary": signature["extended_nonboundary_projection_models"]},
            "implication": "Local signature-intersection realizability is necessary but insufficient; the next engine must expose global p199 type/marginal closure relations.",
        },
        "independent_replay": {"status": independent["status"], "route": "direct local-signature deletions, reverse enumeration, and DFS acyclicity", "interfaces": independent["actual_interfaces"], "allowed_simplices_weighted": independent["aggregate_allowed_simplices"], "initial_nonzero": independent["initial_nonzero_projections"], "extended_nonzero": independent["extended_nonzero_projections"]},
        "control": {"basis_controls": checked["basis_controls"], "raw_two_owner_descriptors": checked["raw_two_owner_control_count"], "raw_exhaustive_status": checked["raw_control_status"], "interpretation": "The raw count exceeded the frozen 2,000,000-model cap before execution; no empirical universal claim is inferred."},
        "audit": checked,
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "outcome": "SEAL_NARROW_BOUNDARY_AND_OPEN_GLOBAL_RELATIVE_CHAIN_QUOTIENT",
            "strongest_flaw": "The 457 actual nonzero projections are known boundaries but have no local canonical explanation.",
            "companion_proposal": "Construct the exact relative-chain/Cech map from the 457 residual projections to pair-intersection H1 modulo Cycle 41 global singleton/binary closure relations.",
            "primary_decision": "Adopt that proposal as a genuinely new global engine. Do not spend another cycle tuning local Morse schedules.",
            "next_action": "Preregister the relative-chain quotient, its global relation matrix, and a dual obstruction falsifier before executable work.",
            "falsifier": "A residual and exact dual class that annihilates every imported global closure relation but pairs nontrivially refutes the proposed quotient bridge.",
        },
        "resources": {
            "worker_cpus": [0, 1, 2], "reserved_cpu": 3,
            "actual_wall_seconds": actual["wall_seconds"], "actual_peak_rss_kib": 1178248,
            "independent_wall_seconds": independent["wall_seconds"], "independent_peak_rss_kib": 224436,
            "abstract_wall_seconds": abstract["wall_seconds"], "abstract_peak_rss_kib": 254448,
            "signature_wall_seconds": signature["wall_seconds"], "signature_peak_rss_kib": 233352,
            "temporary_disk_cap_bytes": 5368709120,
        },
        "runtime": check_runtime("Cycle 45 Morse critical projection"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {
            "actual_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_morse_actual.py",
            "abstract_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_morse_abstract.py",
            "signature_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_morse_signature_abstract.py",
            "independent_command": "taskset -c 0-2 .venv/bin/python proof/replay_cycle_45_morse_independent.py",
            "audit_command": ".venv/bin/python proof/check_cycle_45_morse.py",
            "test_command": ".venv/bin/python -m unittest tests.test_cycle_45_morse -v",
            "check_command": ".venv/bin/python proof/build_cycle_45_lrc_morse.py --check",
        },
        "sealer": {"path": "proof/build_cycle_45_lrc_morse.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
