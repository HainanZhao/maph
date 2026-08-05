"""Seal Cycle 31's exact no-go for the 1,390-atom convolution quotient."""
from __future__ import annotations

from pathlib import Path

from check_cycle_31_convolution_quotient import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle31-convolution-quotient"
OUTPUT = ROOT / "artifacts/cycle-31-b031-lrc-convolution-quotient-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-31-b031-lrc-convolution-quotient-preregistration-v1.md", "19a59c399ce6065d0d0280083677c5c1eeb5671f6b09256182c3dcb761983675"),
    "prior_artifact": (ROOT / "artifacts/cycle-30-b030-lrc-crt-synchronization-v1.json", "13a617a6322b0ed1a2bfd9d1d51a3a09ea6da76c716e6b0f0d9791c5064ec674"),
    "idea_selection": (ROOT / "discovery/cycle31_convolution_quotient_idea_selection.md", "807b94a4257b485794bdad5442c1cd04b4d4166a36bcc6863b96b69619ca4370"),
    "primary_engine": (ROOT / "discovery/lrc_convolution_quotient.py", "46cad8aba1e110fb237a8fe2aa870955b80f938cb0639909fb265c4f1c8974d3"),
    "independent_replay": (ROOT / "proof/replay_cycle_31_convolution_quotient_independent.py", "4d05eb6abea5a48f16ff369bb2a2f8c1e47e92cc47bdcb1de9939604b42ad24d"),
    "audit": (ROOT / "proof/check_cycle_31_convolution_quotient.py", "fe141c064f91eae6e9a3c57a9db7d35b5f648463762a5fc0fdde127680ae050d"),
    "soundness": (ROOT / "proof/cycle_31_convolution_quotient_soundness.md", "62146000f37dbdf6f4c5ddc8cd52d53a293223fc9cb12348ea6ed0eceaf035ef"),
    "test": (ROOT / "tests/test_cycle_31_convolution_quotient.py", "1b59d12bec6deed486f9c457ebd6fd14653d8aab8ddc445606916a352a4cd5b3"),
    "primary_result": (OUT / "result.json", "56bb4ab23e91ed728799c7882c46d8f4d17d44d2b771c651430846fd87ee929d"),
    "independent_result": (OUT / "independent-replay.json", "c7299a0bcb5df4aacc29311c992d9bcb91f50d77e36e197c1c76935bff74a01f"),
    "primary_timing": (ROOT / "discovery/out/cycle31-convolution-quotient.time", "fc15f4a91764a8b8c141626897121ec64e5b7f67070ce71e21c9c17fde1cc2b5"),
    "independent_timing": (OUT / "independent-replay.time", "5868c29f851ad2563f245f9b00bcfebf75d3deeadb7adce6c2cecd98c7a89477"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def payload() -> dict[str, object]:
    checked = audit()
    return {
        "artifact_id": "cycle-31-b031-lrc-convolution-quotient-v1",
        "budget_ordinal": "B031",
        "cycle": 31,
        "record_type": "PROVED_STRUCTURAL_NO_GO",
        "recorded_at_utc": "2026-08-04T14:24:59Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "The sealed 1,390-atom p199 partition is not an additive convolution quotient: the first targeted pair A={±1}, B={±198} splits the six-point atom containing ±199.",
        "claim_boundary": "This exact witness rejects only the Cycle-30 1,390-atom partition as an additive convolution quotient. It does not reject the 1,394-orbit negation refinement, other CRT/association schemes, polynomial calculus, the named leaf, or LRC(13).",
        "audit": checked,
        "finite_result": {
            "epistemic_status": "PROVED",
            "singleton_profiles_passed": 2780,
            "first_pair_profile": 198,
            "target_evaluations": 395,
            "left_atom": [1, 2785],
            "right_atom": [198, 2588],
            "target_atom": [199, 597, 995, 1791, 2189, 2587],
            "four_sums": [197, 199, 2587, 2589],
            "splitting_values": {"199": 1, "597": 0},
            "independent_replay": "PASS",
        },
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "outcome": "SEALED_FOR_DISTINCT_OWNERSHIP_POLYNOMIAL_QUESTION",
            "scope_review": "The witness is decisive only for the four extra mergers beyond negation; it is not a general convolution or CRT no-go.",
            "strongest_flaw": "Refining both six-point atoms into negation pairs removes this witness but supplies no new compression beyond known even symmetry.",
            "independent_ideas": ["use the 1,394 negation quotient only as verified preprocessing", "attempt bounded-degree coordinate-specific Nullstellensatz on exact rank-three ownership blockers", "deprioritize alternate association schemes unless their stabilizer exceeds negation"],
            "falsifier": "For the next engine, an exact legal ownership assignment or independently failed finite-field certificate identity invalidates a claimed refutation; a cap is only bounded failure.",
            "next_action": "Open a distinct cycle for a monomial-count benchmark and bounded-degree Nullstellensatz prototype on base 4 / leaf 78, using only verified negation-pair deduplication.",
        },
        "resources": {"worker_cpus": [0, 1, 2], "reserved_cpu": 3, "aggregate_wall_seconds": 4.9, "largest_peak_rss_kib": 79104, "memory_max_bytes": 2147483648, "temporary_disk_cap_bytes": 5368709120},
        "runtime": check_runtime("Cycle 31 convolution quotient no-go"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {
            "primary_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_convolution_quotient.py",
            "independent_command": "taskset -c 0-2 .venv/bin/python proof/replay_cycle_31_convolution_quotient_independent.py",
            "audit_command": ".venv/bin/python proof/check_cycle_31_convolution_quotient.py",
            "test_command": ".venv/bin/python -m unittest tests.test_cycle_31_convolution_quotient -v",
            "check_command": ".venv/bin/python proof/build_cycle_31_lrc_convolution_quotient.py --check",
        },
        "sealer": {"path": "proof/build_cycle_31_lrc_convolution_quotient.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
