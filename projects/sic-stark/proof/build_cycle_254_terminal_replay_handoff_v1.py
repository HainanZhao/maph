"""Seal C254/B091 terminal replay and C_FROZEN classification."""
from pathlib import Path

from cycle_seal_v1 import check_runtime, freeze_inputs, require, run_cli, sha256
from verify_cycle_254_terminal_replay_handoff import audit


R = Path(__file__).resolve().parents[1]
O = R / "artifacts/cycle-254-b091-terminal-replay-handoff-v1.json"
I = {
    "c221": (R / "artifacts/cycle-221-b058-tilde-inversion-v1.json", "e81eeaf8df6bf860989682eb6c15f6d0d91598d391031dccec0b72fc739afeb9"),
    "c222": (R / "artifacts/cycle-222-b059-z-label-cocycle-v1.json", "83faa1a1fcad0f31f6cf142c5098069f82401ebf61e2b5244cb6fd0817bb0ae8"),
    "c223": (R / "artifacts/cycle-223-b060-explicit-signed-product-v1.json", "a54c11b4b12530480d449f5a9ae75106d8e1b17f94f2eba4aedfc6fef07db5f1"),
    "c224": (R / "artifacts/cycle-224-b061-shift-cohomology-v1.json", "a24b0573942c5bd869240f7444f6db0542e5a0899d64e1ba1704625c8a5e7a26"),
    "c225": (R / "artifacts/cycle-225-b062-reflection-root-branch-v1.json", "34b7d4943566e57f8c153127449226ec3eae4865f692f17336f6e4f5a3c9c29f"),
    "c226": (R / "artifacts/cycle-226-b063-signed-product-groupoid-v1.json", "c1c3fd23d20a3cd2e40a84dda8e0fade3b1aa873d5c8b66a2b532a1c79fb516c"),
    "c235": (R / "artifacts/cycle-235-b072-meromorphic-loop-holonomy-v1.json", "89064a523f1e26661d2041affc6a2708047bb0b6f412d6a20db9afc6bfc0268a"),
    "c236": (R / "artifacts/cycle-236-b073-ordered-word-dualization-v1.json", "00651344e7ed7610d7af9f14d24cbbfe276701ba5d28e950740645912a63f9ed"),
    "c237": (R / "artifacts/cycle-237-b074-reflection-partner-reachability-v1.json", "4ccc1d28d8bd4c969c185b2cdd45e7fe888a89f02ed1969d470aedf3854da2bf"),
    "c251": (R / "artifacts/cycle-251-b088-residue-dual-cross-sign-v1.json", "d965cc663bf3bb5ba09b904419d16b2dfe8df5df7335d5c0b734087fee37971d"),
    "c252": (R / "artifacts/cycle-252-b089-reciprocal-negative-alpha-v1.json", "8af8806e58bf9ee283acb5fb046a18df20637265fdb298acc514fbf0d12c8f1e"),
    "c253": (R / "artifacts/cycle-253-b090-direct-hyperbolic-continuation-v1.json", "80afd4befd6f125b55300aa522fa2574a9f465c17c277590b75eed4685b61f85"),
    "factor_source": (R / "proof/verify_cycle_228_f3_square_residual_block.py", "3419d8d4f0e81cbfc8c970c3c1de5d16f6c79fa793042291156492796f683987"),
    "c253_replay": (R / "proof/verify_cycle_253_direct_hyperbolic_continuation.py", "04990c39feeb8f269f59a6dd857667a163491055614fa359f089da705a9307bf"),
    "source_paper": (R / "paper/sic-stark-dimension-six-boundary-fusion.tex", "347228e05a87946ca41bb31c118aae069b7fb6002fff4933d030a153cef21cb7"),
    "prereg": (R / "docs/cycle-254-b091-terminal-replay-handoff-preregistration-v1.md", "8ec52270258b5bb2003134bdcbc53e40f4615d14a904dc5dd17fd18369687573"),
    "replay": (R / "proof/verify_cycle_254_terminal_replay_handoff.py", "f89eab102cab33f17e01bca98a642377759f6e8dc338bb564946c0acc9041008"),
    "test": (R / "tests/test_cycle_254_terminal_replay_handoff.py", "e6bfdead9127f1befd7170ec9f9da0e93bbe6ff70ed2eafab21c3ed1cb8b4061"),
    "validator": (R / "../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
    "scaffold": (R / "proof/cycle_seal_v1.py", "92f3dbdf7914973db7bfd6290f826c83e8bf60c1495e2a546d9f76d11751d5e1"),
}


def payload():
    result = audit()
    require(result["epistemic_status"] == "PROVED", "unproved terminal audit")
    require(result["status"] == "C_FROZEN", "unexpected terminal status")
    require(not result["dimension_six_TCC_proved"], "inconsistent closure state")
    require(result["independent_replay"]["C253_obstruction_reproduced"], "independent replay failed")
    require(result["transition_inventory"]["survivor_count"] == 0, "surviving transition ignored")
    require(result["terminal_outcome"]["project_stopped"], "project not stopped")
    return {
        "artifact_id": "cycle-254-b091-terminal-replay-handoff-v1",
        "cycle": 254,
        "budget_ordinal": "B091",
        "epistemic_status": "PROVED",
        "status": "C_FROZEN",
        "claim_boundary": result["claim_boundary"],
        "audit": result,
        "decision": {
            "basis": "An independent implementation reproduced the all-eight continuation/target mismatch, and all twelve sealed relevant transition records fail at least one necessary source, cocycle, state, reflection, or reachability condition.",
            "known_flaw": "The finite inventory cannot exclude a future new source theorem or construction outside the stopped project.",
            "falsifier": "Any independent-replay discrepancy, omitted relevant sealed transition, surviving source-authorized all-eight operator with both required cocycles, or a complete downstream TCC replay.",
            "next_action": "None inside SIC--Stark. Preserve PROGRAM.md, this artifact, and STATUS.md as the handoff; future research requires explicit separate authorization.",
        },
        "frozen_hashes": freeze_inputs(R, I),
        "runtime": check_runtime("C254"),
        "sealer": {"path": "proof/build_cycle_254_terminal_replay_handoff_v1.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=O, payload_factory=payload))
