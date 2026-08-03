#!/usr/bin/env python3
"""Issue the Cycle 186 even-d representative-convention correction."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-186-normalized-afk-packet-v2.json"
INPUTS = {
    "instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "superseded_artifact": (ROOT / "artifacts/cycle-186-normalized-afk-packet-v1.json", "b569fc23d0044480c0d53739764272cc6a7a92a5452afc13bff379653f674e31"),
    "original_preregistration": (ROOT / "docs/cycle-186-normalized-afk-packet-preregistration-v1.md", "1e07a1dfb8b4f2ee263910228a3b80bbdceade1a513545f445bb1fcd32bba2c8"),
    "superseded_replay": (ROOT / "proof/verify_cycle_186_normalized_afk_packet.py", "1f92daba285446a216b937c041459b5e7394889b2b8045af66618a133cf341bf"),
    "corrected_replay": (ROOT / "proof/verify_cycle_186_normalized_afk_packet_v2.py", "c0fad0d986c4666eb89062c91d6e2c58dd40e9a11988cab7addbd332586cbded"),
    "corrected_prototype": (ROOT / "discovery/cycle-186-normalized-afk-packet-prototype-v2.json", "7f4a2ff7d061189e4aca92acb12e7ae36fb39b03e97e3ed863cdb006dfc20ce8"),
    "prior_transfer": (ROOT / "artifacts/cycle-185-multiplier-weighted-relation-transfer-v1.json", "b4a8926318ea4589c9b38b4464de291557efaeb5bb3dd104c2370a4054fbc269"),
    "prior_transfer_output": (ROOT / "discovery/cycle-185-multiplier-weighted-relation-transfer-prototype-v1.json", "eba8d3e44e935eba20f674dd8a49dc0bac98374f89b5af783fdbd0a4c436b662"),
    "multiplier_ledger": (ROOT / "scripts/dimension_six_stabilizer_ledger.py", "594a0d541478f340abe789234335f3ff1b2d874ad8fa3507ad95026c5cc6276b"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 186 v2 correction")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads((ROOT / "discovery/cycle-186-normalized-afk-packet-prototype-v2.json").read_text())
    summary = result["summary"]
    require(
        (
            summary["packet_characteristics_checked"],
            summary["nonzero_characteristics_checked"],
            summary["self_inverse_nonzero_count"],
            summary["free_inverse_pair_count"],
            summary["free_multiplicative_rank"],
            summary["multiplier_records_checked"],
            summary["transfer_label_count"],
            summary["countermodels_checked"],
        ) == (36, 35, 3, 16, 16, 36, 11, 2),
        "corrected finite packet census drift",
    )
    require(not summary["finite_relation_data_determines_u_01_square"], "corrected countermodel separation drift")
    return {
        "artifact_id": "cycle-186-normalized-afk-packet-v2",
        "cycle": 186,
        "budget_ordinal": "B024",
        "epistemic_status": "PROVED",
        "status": "CORRECTED_NORMALIZED_AFK_PACKET_FINITE_RELATION_UNDERDETERMINED",
        "supersedes": {"artifact_id": "cycle-186-normalized-afk-packet-v1", "status": "SUPERSEDED_BY_EVEN_D_REPRESENTATIVE_CONVENTION_CORRECTION"},
        "claim_boundary": result["claim_boundary"],
        "correction": result["correction"],
        "outcome": {"epistemic_status": "PROVED", "statement": "With the AFK even-d standard-representative sign restored, the admitted finite quotient still has 16 free nonzero inverse-pair coordinates. Two exact signed assignments preserve every corrected relation and the independent Cycle-185 labels while giving u_(0,1)^2=1 and 4."},
        "primary_source": result["primary_source"],
        "exact_prototype": {"source_output": "discovery/cycle-186-normalized-afk-packet-prototype-v2.json", "formal_packet": result["formal_packet"], "countermodels": result["countermodels"], "summary": summary},
        "gate_outcome": {"d6_interface": "CORRECTED_NORMALIZED_AFK_FINITE_RELATIONS_UNDERDETERMINED_ANALYTIC_SHINTANI_TRANSPORT_REQUIRED", "remaining_bottleneck": "Derive and test an exact cross-characteristic A6/Shintani transport identity from the actual modular cocycle or the 2psi2/2phi1 packet; only additional analytic data could constrain nu_(0,1)^2.", "disallowed_pseudo_progress": ["using unsigned standard-representative reciprocal relations in even d", "claiming analytic modular-cocycle values are arbitrary", "replacing the Shintani cocycle by multiplier phases or transfer weights", "calling finite countermodels AFK cocycle realizations", "inferring a coefficient-to-ray, Stark, fusion, or TCC consequence"]},
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "A genuine analytic cross-characteristic identity for the source-defined normalized AFK overlaps may impose constraints absent from the corrected finite relation quotient and could then be compared to the sealed transfer algebra."},
        "companion_decision": {"identity": "/root/decision_companion_2", "evidence_scope_review": "B024 v1 materially omitted the even-d standard-representative sign; its finite underdetermination conclusion is plausible only after an exact signed rerun.", "recommendation": "Issue immutable Cycle 186 v2, mark v1 superseded, contain B025's failed premise, and restart analytic covariance only from the corrected artifact.", "known_flaw": "The corrected 16-coordinate conclusion would fail if the periodicity sign, representative convention, coefficient field, or signed witnesses are wrong.", "falsifier": "Any error in the sign derivation, signed orbit census, or corrected countermodel substitution.", "next_action": "Freeze and replay every signed standard-representative relation, rerun multiplier/transfer agreement, then restart analytic transport from this corrected artifact.", "adopted": True},
        "preregistration_preflight": {"original_cycle": 186, "original_manifest_sha256": sha256(ROOT / "docs/cycle-186-normalized-afk-packet-preregistration-v1.md"), "correction_basis": "No retroactive manifest change: v2 records the post-seal convention correction triggered by source quasiperiodicity."},
        "frozen_hashes": frozen,
        "replay": {"corrected_prototype_command": "python3 proof/verify_cycle_186_normalized_afk_packet_v2.py --output discovery/cycle-186-normalized-afk-packet-prototype-v2.json", "write_command": "python3 proof/build_cycle_186_normalized_afk_packet_v2.py --write", "check_command": "python3 proof/build_cycle_186_normalized_afk_packet_v2.py --check"},
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_186_normalized_afk_packet_v2.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
