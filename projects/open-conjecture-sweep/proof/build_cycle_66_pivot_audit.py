"""Seal C66's user-directed cross-conjecture leverage decision."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.check_cycle_66_pivot_audit import audit
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256


H = {
    "c64": ("artifacts/cycle-64-b064-fiber-minimization-v1.json", "141097ac5719461203b118046adf16e9d85655bfcb084a55221f95ad582c66b7"),
    "c65": ("artifacts/cycle-65-b065-step-graphon-v2.json", "19c914fd1179c89475050ad2c0e47342ea6c9835e8615dc298e842bc5eb8785c"),
    "prereg": ("docs/cycle-66-b066-s3-pivot-audit-preregistration-v1.md", "b7b255316f6dd9b110cebb3f393c390d5dc7c8b3ca59ec5816e717a7e2d8fabd"),
    "idea": ("discovery/cycle66_pivot_idea_selection.md", "2d008a1b102bb9c347111889ddf000b77cb8a320d6204b2243f716710b4a4158"),
    "prior_eligibility": ("discovery/problem2_eligibility_audit.md", "196c30a07951a091fefd10d1d2550e111d614664f3aea7fc70eebe9b70fc3250"),
    "audit_document": ("discovery/cycle66_pivot_audit.md", "443617233cb8bb00c3cc1d632938b26d28530fcee8a359d5edfe4025af622a80"),
    "audit_source": ("proof/check_cycle_66_pivot_audit.py", "09efb32cac4a04d2ad923ef98de03eb6e9fb41deaaea1bf391c235a6092b76c6"),
    "test": ("tests/test_cycle_66_pivot_audit.py", "bd072d45377fa9df1990b612ff92fdab320b215575a12010995f54025a769687"),
    "audit_result": ("discovery/out/cycle66-pivot-audit/packet-audit.json", "f7c8493deee441f85e4d166ec82eac8bd9199190a3cdc262a23cd61fc18822b2"),
    "scaffold": ("proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "validator": ("../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def payload():
    checked = audit()
    return {
        "artifact_id": "cycle-66-b066-s3-pivot-audit-v1",
        "budget_ordinal": "B066",
        "cycle": 66,
        "record_type": "BOUNDED_NOVELTY_AUDIT_AND_CROSS_CONJECTURE_PIVOT",
        "recorded_at_utc": "2026-08-05T11:02:41Z",
        "status": "SEALED",
        "epistemic_status": "OBSERVED",
        "outcome": (
            "PROVED: C63-C64 reduce the exact fixed-S3 instance of Zhao's "
            "conjugacy-averaging comparison for K5,5-C10 to four boundary "
            "families and at most 156 algebraic pairs per outer fiber. "
            "OBSERVED: a bounded primary-source search found no prior fixed-S3 "
            "theorem or semialgebraic reduction. The finding warrants a bounded "
            "pivot to exact boundary positivity."
        ),
        "claim_boundary": checked["claim_boundary"],
        "audit": checked,
        "primary_sources": {
            "zhao_theorem_1_3": "https://arxiv.org/html/2606.15368v1",
            "lee_schuelke_theorem_1_3": "https://arxiv.org/abs/1910.08454",
            "lovasz_local_sidorenko": "https://arxiv.org/abs/1004.3026",
        },
        "cycle_decision": {
            "user_direction": "Pivot when a banked finding materially advances an open problem or conjecture.",
            "companion_identity": "/root/darwin_cycle25_short",
            "companion_advice": (
                "Pivot only to the fixed-S3 Zhao comparison: the local-stability "
                "finding is subsumed by Lovasz, while C64 is a genuine exact "
                "nonabelian reduction. Keep scalability to all S_n explicit."
            ),
            "decision": "Open C67 on exact positivity of C64's four fiber endpoint families.",
            "rejected": "Larger groups, larger step graphons, another Polya ladder, and immediate unscoped CAD.",
            "falsifier": "One exact feasible boundary tuple with negative Zhao deficit.",
        },
        "frozen_hashes": freeze_inputs(ROOT, {key: (ROOT / path, expected) for key, (path, expected) in H.items()}),
        "runtime": check_runtime("c66"),
        "sealer": {"path": "proof/build_cycle_66_pivot_audit.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "audit": "python3 proof/check_cycle_66_pivot_audit.py",
            "test": "python3 -m unittest tests/test_cycle_66_pivot_audit.py",
            "check": "python3 proof/build_cycle_66_pivot_audit.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(
        description=__doc__,
        output=ROOT / "artifacts/cycle-66-b066-s3-pivot-audit-v1.json",
        payload_factory=payload,
    ))
