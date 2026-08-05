"""Seal C65's bounded direct 2x2 step-graphon falsifier search and P2 pause."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.check_cycle_65_step_graphon_packet import audit
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256


H = {
    "prior": ("artifacts/cycle-64-b064-fiber-minimization-v1.json", "141097ac5719461203b118046adf16e9d85655bfcb084a55221f95ad582c66b7"),
    "prereg": ("docs/cycle-65-b065-step-graphon-preregistration-v1.md", "b311968bc0470988092a4cae047b0952f89e831685309813c8968c09959ff51d"),
    "idea": ("discovery/cycle65_step_graphon_idea_selection.md", "b98b5ead16e74f68c5a14bd6837a816d65c0fadd5fd7f09b9967648ad67b3e77"),
    "search_source": ("discovery/cycle65_step_graphon_search.cpp", "1b11ae98ec4fbe2b869ccae746712c919fba6f69e4960382852e352ae28e2564"),
    "exact_source": ("proof/cycle65_step_graphon_exact.cpp", "a942745bca10cab26c0d493ca92acc9beaf57588b98c6063700c4f1fdced7e24"),
    "replay": ("proof/run_cycle_65_step_graphon.sh", "6985b1abf515241fc6b00ea23ff425523ccc224a9e92895f98fe7b06af61f5c5"),
    "audit_source": ("proof/check_cycle_65_step_graphon_packet.py", "b05f51c7efc98db2442c6376c45cfe447d0ed6ca530ba4235c492694e00a10e9"),
    "soundness": ("proof/cycle_65_step_graphon_soundness.md", "c198adaceeb15d73cfe1d097e07567bceb76f7f2d18ac337c458be1e5a19bb76"),
    "test": ("tests/test_cycle_65_step_graphon.py", "02ed6d39fb381f7023d8e88e1403e2a35536ec20e0f201f3b9149654b6ddc4fe"),
    "candidates_650651": ("discovery/out/cycle65-step-graphon/search/candidates-650651.tsv", "893f60567520478a50c919de779d9e76ec81e1004ac8919be459e942efd4df21"),
    "candidates_650652": ("discovery/out/cycle65-step-graphon/search/candidates-650652.tsv", "88afc9c5030ab30dcf718de81cae28ffb92bc77004ec8f9605b753edaa3394e9"),
    "candidates_650653": ("discovery/out/cycle65-step-graphon/search/candidates-650653.tsv", "7409751fa269963124a451b6af4b12ea81402e76ecdb33f0d544bc4410966214"),
    "summary_650651": ("discovery/out/cycle65-step-graphon/search/summary-650651.json", "77f44b89d6654fb16ade074f10c31826040a4980573b553f2a11983b8477899b"),
    "summary_650652": ("discovery/out/cycle65-step-graphon/search/summary-650652.json", "c4fa7dbe6683bcdc1687645b59ceb314a3fa552e922f414d42ef9d36eaaf09af"),
    "summary_650653": ("discovery/out/cycle65-step-graphon/search/summary-650653.json", "0376476e6066d23a41db53569b3d103c5e83bbad0e4df1bb6ef0624dca630848"),
    "exact_rows": ("discovery/out/cycle65-step-graphon/exact/exact-candidates.tsv", "ade2f68267097d06ee6b57c607d2b4cd006b11af50ec8b5d0721b90d082a06dc"),
    "exact_summary": ("discovery/out/cycle65-step-graphon/exact/exact-summary.json", "9b3d07efb1161bd65b9fb9cf55e33a813b69cf074ec117f278ece52beb210104"),
    "packet_audit": ("discovery/out/cycle65-step-graphon/packet-audit.json", "7fa3713dd6e4444e8e8911af41367b1fb38a50997f6cf63ae88ec98642cb8b13"),
    "scaffold": ("proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "validator": ("../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def payload():
    checked = audit()
    return {
        "artifact_id": "cycle-65-b065-step-graphon-v1",
        "budget_ordinal": "B065",
        "cycle": 65,
        "record_type": "BOUNDED_2X2_FALSIFIER_SEARCH_AND_STRATEGIC_PAUSE",
        "recorded_at_utc": "2026-08-05T10:53:53Z",
        "status": "SEALED",
        "epistemic_status": "MIXED",
        "outcome": (
            "PROVED: the normalized denominator-4 grid has 0 negative, 809 "
            "constant-on-effective-support zero, and 2,316 positive rows, and "
            "all 96 denominator-10^9 rounded retained candidates are positive. "
            "OBSERVED: 3,072,000 deterministic search trials found no exact "
            "counterexample or reusable extremal reduction."
        ),
        "claim_boundary": (
            "The five-parameter normalization covers each nonzero 2x2 kernel "
            "up to positive scaling and row/column relabeling; the zero kernel "
            "is trivial. The exact counts concern only the frozen rational rows. "
            "No continuous 2x2 positivity, Zhao comparison, or Sidorenko theorem follows."
        ),
        "audit": checked,
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "companion_advice": (
                "Seal C65, pause Problem 2, and start Problem 3. The 809 coarse-grid "
                "zeros are support degeneracies, not a reusable extremal theorem; "
                "do not extend to a block-size ladder."
            ),
            "decision": (
                "The preregistered hard stop is met. Pause Problem 2 and bank its "
                "unused allocation for Problem 3."
            ),
            "revisit_engine": (
                "Only reopen with a precise triple-neighbor entropy/Finner "
                "inequality and finite weighted-kernel falsifier."
            ),
            "falsifier": "An exact rational kernel with t_H<t_K2^15.",
        },
        "runtime_measurement": {
            "three_searches_parallel_wall_seconds_max": 5.97,
            "search_peak_rss_kib_max": 4352,
            "exact_wall_seconds": 0.04,
            "exact_peak_rss_kib": 4096,
            "aggregate_trial_evaluations": 3072000,
        },
        "frozen_hashes": freeze_inputs(ROOT, {key: (ROOT / path, expected) for key, (path, expected) in H.items()}),
        "runtime": check_runtime("c65"),
        "sealer": {"path": "proof/build_cycle_65_step_graphon_packet.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "full": "bash proof/run_cycle_65_step_graphon.sh",
            "test": "python3 -m unittest tests/test_cycle_65_step_graphon.py",
            "check": "python3 proof/build_cycle_65_step_graphon_packet.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(
        description=__doc__,
        output=ROOT / "artifacts/cycle-65-b065-step-graphon-v1.json",
        payload_factory=payload,
    ))
