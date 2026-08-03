#!/usr/bin/env python3
"""Seal Cycle 188's corrected same-tuple stabilizer transport."""
from __future__ import annotations

import json
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-188-stabilizer-covariance-v1.json"
INPUTS = {
    "instructions": (ROOT / "AGENTS.md", "363495f0dbbe93e244b460c8eafb13247a8fb1f41be24f94c037ae9f6400c6f2"),
    "corrected_packet": (ROOT / "artifacts/cycle-186-normalized-afk-packet-v2.json", "efe2d076814e924c687fb137774fd200e45b8a265f666107b955efb14bfe1a09"),
    "corrected_packet_output": (ROOT / "discovery/cycle-186-normalized-afk-packet-prototype-v2.json", "7f4a2ff7d061189e4aca92acb12e7ae36fb39b03e97e3ed863cdb006dfc20ce8"),
    "preregistration": (ROOT / "docs/cycle-188-stabilizer-covariance-preregistration-v1.md", "a121de917bce388c6961489635df4d928c20c987d58865dc8743016c4a761999"),
    "replay": (ROOT / "proof/verify_cycle_188_stabilizer_covariance.py", "8132f5a4654115d438951d1cbf852ab659dc381bf93374f4db4ef80d227e49b2"),
    "prototype": (ROOT / "discovery/cycle-188-stabilizer-covariance-prototype-v1.json", "36f4fa034f8aa98061e08a56f66630467b23b5d71305d7a705e2628667489505"),
    "multiplier_ledger": (ROOT / "scripts/dimension_six_stabilizer_ledger.py", "594a0d541478f340abe789234335f3ff1b2d874ad8fa3507ad95026c5cc6276b"),
    "heisenberg_descent": (ROOT / "scripts/dimension_six_heisenberg_descent.py", "ccc19fd158cc4714c2d5fcbecbb5c8091c2bdbd748561aed6736482bb2dbe11f"),
    "d6_paper": (ROOT / "paper/sic-stark-dimension-six-boundary-fusion.tex", "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload() -> dict[str, object]:
    runtime = check_runtime("Cycle 188 seal")
    frozen = freeze_inputs(ROOT, INPUTS)
    result = json.loads((ROOT / "discovery/cycle-188-stabilizer-covariance-prototype-v1.json").read_text())
    summary = result["summary"]
    require(
        (
            summary["nonzero_characteristics_checked"],
            summary["transport_relations_checked"],
            summary["corrected_reciprocal_relations_checked"],
            summary["nonzero_L_orbits"],
            summary["self_inverse_nonzero_L_orbits"],
            summary["nonzero_inverse_orbit_pairs"],
            summary["free_multiplicative_rank_after_transport"],
            summary["countermodels_checked"],
        ) == (35, 35, 35, 13, 1, 6, 6, 2),
        "stabilizer covariance census drift",
    )
    require(not summary["stabilizer_covariance_determines_u_01_square"], "countermodel separation drift")
    return {
        "artifact_id": "cycle-188-stabilizer-covariance-v1",
        "cycle": 188,
        "budget_ordinal": "B025",
        "epistemic_status": "PROVED",
        "status": "SEALED_SAME_TUPLE_STABILIZER_COVARIANCE_REDUCES_PACKET_TO_SIX_ORBIT_PAIRS",
        "claim_boundary": result["claim_boundary"],
        "outcome": {"epistemic_status": "PROVED", "statement": "For the canonical d=6 tuple, checked AFK same-tuple covariance under L and corrected even-d quasiperiodicity collapse the 16 finite inverse-pair coordinates to six L-orbit pairs plus one discrete self-inverse orbit. Exact signed assignments with u_(0,1)=1 and 2 still satisfy every admitted relation, so u_(0,1)^2 remains undetermined."},
        "primary_source": result["primary_source"],
        "canonical_stabilizer": result["canonical_stabilizer"],
        "exact_prototype": {"source_output": "discovery/cycle-188-stabilizer-covariance-prototype-v1.json", "transport": result["transport"], "corrected_reciprocal": result["corrected_reciprocal"], "orbits": result["orbits"], "countermodels": result["countermodels"], "summary": summary},
        "gate_outcome": {"d6_interface": "SAME_TUPLE_STABILIZER_COVARIANCE_VALIDATED_ANALYTIC_QSERIES_EVALUATION_REQUIRED", "remaining_bottleneck": "Evaluate or derive an additional analytic relation for the actual modular cocycle, naturally through the sign-reflected 2psi2/2phi1 packet and its boundary continuation; finite covariance leaves six orbit-pair amplitudes free.", "disallowed_pseudo_progress": ["treating finite stabilizer covariance as a cocycle evaluation", "using unsigned standard-representative relations", "replacing cocycle values by multiplier weights", "calling finite countermodels analytic realizations", "inferring a coefficient-to-ray, Stark, fusion, or TCC consequence"]},
        "remaining_target": {"epistemic_status": "CONJECTURED", "statement": "The actual sign-reflected 2psi2/2phi1 boundary packet may supply an analytic relation that fixes one or more of the six remaining stabilizer-orbit amplitudes."},
        "companion_decision": {"identity": "/root/decision_companion_2", "evidence_scope_review": "The cited prototype supports PROVED corrected covariance: 35 signed transports close, 16 inverse-pair parameters reduce to six orbit-pair seeds, and two exact seeds still separate u_(0,1)^2.", "recommendation": "Seal B025; same-tuple covariance is exhausted. A genuine cocycle/q-series evaluation is a distinct analytic engine requiring a new cycle.", "known_flaw": "The six remaining seeds are formal relation-quotient parameters; neither countermodel is realized by the analytic modular cocycle.", "falsifier": "Any source-hypothesis, representative-sign, stabilizer, orbit, transport, countermodel, or replay discrepancy—or an analytic-arbitrariness claim.", "next_action": "Freeze one explicit 2psi2-to-2phi1 continuation identity, domains/branches, and proof criteria; require an exact cross-orbit relation or rigorous enclosure with margin targeting u_(0,1)^2.", "adopted": True, "reason": "The finite same-tuple source theorem is fully enumerated, while any further constraint must come from an analytic evaluation absent from its hypotheses."},
        "preregistration_preflight": {"cycle": 188, "manifest_sha256": sha256(ROOT / "docs/cycle-188-stabilizer-covariance-preregistration-v1.md"), "validator": {"path": "../../tools/preregistration_check.py", "sha256": "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"}},
        "frozen_hashes": frozen,
        "replay": {"preflight_command": "research prereg check docs/cycle-188-stabilizer-covariance-preregistration-v1.md --expected-cycle 188 --allow-head-drift", "prototype_command": "python3 proof/verify_cycle_188_stabilizer_covariance.py --output discovery/cycle-188-stabilizer-covariance-prototype-v1.json", "write_command": "python3 proof/build_cycle_188_stabilizer_covariance_v1.py --write", "check_command": "python3 proof/build_cycle_188_stabilizer_covariance_v1.py --check"},
        "runtime": runtime,
        "sealer": {"path": "proof/build_cycle_188_stabilizer_covariance_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
