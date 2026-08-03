#!/usr/bin/env python3
"""Seal Cycle 186's finite normalized-AFK packet containment result."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-186-normalized-afk-packet-v1.json"
INPUTS = {
    "instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "prior_transfer": (ROOT / "artifacts/cycle-185-multiplier-weighted-relation-transfer-v1.json", "b4a8926318ea4589c9b38b4464de291557efaeb5bb3dd104c2370a4054fbc269"),
    "prior_transfer_output": (ROOT / "discovery/cycle-185-multiplier-weighted-relation-transfer-prototype-v1.json", "eba8d3e44e935eba20f674dd8a49dc0bac98374f89b5af783fdbd0a4c436b662"),
    "multiplier_ledger": (ROOT / "scripts/dimension_six_stabilizer_ledger.py", "594a0d541478f340abe789234335f3ff1b2d874ad8fa3507ad95026c5cc6276b"),
    "d6_paper": (ROOT / "paper/sic-stark-dimension-six-boundary-fusion.tex", "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7"),
    "preregistration": (ROOT / "docs/cycle-186-normalized-afk-packet-preregistration-v1.md", "1e07a1dfb8b4f2ee263910228a3b80bbdceade1a513545f445bb1fcd32bba2c8"),
    "replay": (ROOT / "proof/verify_cycle_186_normalized_afk_packet.py", "1f92daba285446a216b937c041459b5e7394889b2b8045af66618a133cf341bf"),
    "prototype": (ROOT / "discovery/cycle-186-normalized-afk-packet-prototype-v1.json", "659059b126cc796649708cc977bd5618fb96e40bc31b89bc83359cb16a805f1d"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 186 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads((ROOT / "discovery/cycle-186-normalized-afk-packet-prototype-v1.json").read_text())
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
        "finite packet census drift",
    )
    require(not summary["finite_relation_data_determines_u_01_square"], "countermodel separation drift")
    return {
        "artifact_id": "cycle-186-normalized-afk-packet-v1",
        "cycle": 186,
        "budget_ordinal": "B024",
        "epistemic_status": "PROVED",
        "status": "SEALED_NORMALIZED_AFK_PACKET_FINITE_RELATION_UNDERDETERMINED",
        "claim_boundary": result["claim_boundary"],
        "outcome": {
            "epistemic_status": "PROVED",
            "statement": "Under only the admitted AFK definition, reciprocal theorem, canonical zero relation, and independent Cycle-185 labels, the finite normalized-overlap quotient has 16 free nonzero inverse-pair coordinates. Two exact assignments preserve every admitted relation and every fixed label but give u_(0,1)^2=1 and 4.",
        },
        "primary_source": result["primary_source"],
        "exact_prototype": {
            "source_output": "discovery/cycle-186-normalized-afk-packet-prototype-v1.json",
            "formal_packet": result["formal_packet"],
            "countermodels": result["countermodels"],
            "summary": summary,
        },
        "gate_outcome": {
            "d6_interface": "NORMALIZED_AFK_FINITE_RELATIONS_UNDERDETERMINED_ANALYTIC_SHINTANI_TRANSPORT_REQUIRED",
            "remaining_bottleneck": "Derive and test an exact cross-characteristic A6/Shintani transport identity from the actual modular cocycle or the 2psi2/2phi1 packet; only such additional analytic data could constrain nu_(0,1)^2.",
            "disallowed_pseudo_progress": [
                "claiming the actual analytic modular-cocycle values are arbitrary",
                "replacing the Shintani cocycle by multiplier phases or transfer weights",
                "calling the finite countermodels AFK cocycle realizations",
                "inferring a coefficient-to-ray, Stark, fusion, or TCC consequence",
                "fitting character data, selecting exponents, or using s, d, or ray labels",
            ],
        },
        "remaining_target": {
            "epistemic_status": "CONJECTURED",
            "statement": "A genuine analytic cross-characteristic identity for the source-defined normalized AFK overlaps may impose constraints absent from the finite relation quotient and could then be compared to the sealed transfer algebra.",
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "evidence_scope_review": "The cited output proves underdetermination of the explicitly admitted finite relation quotient: two exact assignments share reciprocal, zero, multiplier, and transfer data while separating u_(0,1)^2.",
            "recommendation": "Seal B024; the finite-quotient question is complete. Additional analytic AFK relations require a distinct method and preregistration.",
            "known_flaw": "Neither assignment realizes an analytic modular cocycle, and the result does not constrain unadmitted functional relations.",
            "falsifier": "A missed admitted relation, invalid inverse/self-inverse census, failed substitution, multiplier/label mismatch, or a broader arbitrariness claim.",
            "next_action": "Open a distinct cycle to derive an exact A6/Shintani transport identity for nu_p from Phi_p and the modular cocycle, preferably through the 2psi2/2phi1 packet, then test whether it eliminates the countermodels or determines nu_(0,1)^2.",
            "adopted": True,
            "reason": "The material gate changes from finite packet derivation to an explicitly analytic transport/evaluation problem; the completed finite quotient is later-relevant evidence.",
        },
        "preregistration_preflight": {
            "cycle": 186,
            "manifest_sha256": sha256(ROOT / "docs/cycle-186-normalized-afk-packet-preregistration-v1.md"),
            "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"},
        },
        "frozen_hashes": frozen,
        "replay": {
            "preflight_command": "research prereg check docs/cycle-186-normalized-afk-packet-preregistration-v1.md --expected-cycle 186 --allow-head-drift",
            "prototype_command": "python3 proof/verify_cycle_186_normalized_afk_packet.py --output discovery/cycle-186-normalized-afk-packet-prototype-v1.json",
            "write_command": "python3 proof/build_cycle_186_normalized_afk_packet_v1.py --write",
            "check_command": "python3 proof/build_cycle_186_normalized_afk_packet_v1.py --check",
        },
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_186_normalized_afk_packet_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
