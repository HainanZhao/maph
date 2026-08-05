"""Seal the C61 exact S3 flat-stratum local-comparison theorem."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from proof.audit_cycle_61_flat_stratum import audit
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

H = {
    "prior_c55": ("artifacts/cycle-55-b055-zhao-deficit-v1.json", "c83b14e71f5b4b4482757f55ec4b018186daf68581d5833e4a6c638379d64c36"),
    "prior_c59": ("artifacts/cycle-59-b059-polya-capped-no-go-v1.json", "fe8e1c34dfe256194bc50156115488ae9fc15e85fead46669629ab86d58e2d2d"),
    "preregistration": ("docs/cycle-61-b061-flat-stratum-preregistration-v1.md", "e073e51ab9a5cd002fb7a4738ead634ab28cb4c3647cc413e0b5ddb118df8781"),
    "idea_selection": ("discovery/cycle61_flat_stratum_idea_selection.md", "add2558034dba31c22a61c9267109e2a32eac4f5af8465c9d25cdc2d7c5b7faf"),
    "c55_polynomials": ("discovery/out/cycle55-zhao-deficit/polynomials.tsv", "14e4a55ece79acff9975b306b3e231faf00e654ea961cf776b12ae3c199d269e"),
    "kernel_evaluator": ("proof/check_cycle_61_flat_stratum.py", "fcfae0d1d6da9f078c0bcaa06b2eb4ea58b01532c06c32aaaaaf422a16bd75ba"),
    "transverse_generator": ("discovery/cycle61_standard_curvature_symbolic.cpp", "33d0f3803b68836693566ac8683c24c9364ecb054f374212e613b879398c7014"),
    "transverse_audit": ("proof/check_cycle_61_transverse.py", "cbe9c54b91b38d8fea304586ddbd48880c366b5a449929f8233df0a3a555459b"),
    "soundness": ("proof/cycle_61_flat_stratum_soundness.md", "c6816d5bd6de9c637fe8677c0755f9d68f2e79257fc57e7e0192bf3bcbcb1194"),
    "audit": ("proof/audit_cycle_61_flat_stratum.py", "347c9938fedfcd814e1a67ce713bf3c05fe341189d54194823d5605bb348856f"),
    "test": ("tests/test_cycle_61_flat_stratum.py", "01cdd29995673016ef110409b31a19ec36d865659da73e16a46dc8b6db4b0e0d"),
    "kernel_summary": ("discovery/out/cycle61-flat-stratum/flat-stratum-summary.json", "7b5df5509ee5c5456eeeee806fc78bd12b85c938adf2c88cd7ec1ba4529392cb"),
    "transverse_raw": ("discovery/out/cycle61-flat-stratum/transverse-curvature.tsv", "b88497cac51e0fec34646d932e6e2d249572ede90d1bc4775122db89d963a986"),
    "transverse_summary": ("discovery/out/cycle61-flat-stratum/transverse-audit.json", "093e02fd998af1262c025c7ad90b0c263e5cffb4714e6ae84353a05414103d29"),
    "scaffold": ("proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "preflight": ("../../tools/preregistration_check.py", "a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}


def payload():
    result = audit()
    return {
        "artifact_id": "cycle-61-b061-flat-stratum-v1",
        "budget_ordinal": "B061",
        "cycle": 61,
        "record_type": "PROVED_FINITE_LOCAL_ENDPOINT_COMPARISON",
        "recorded_at_utc": "2026-08-05T11:20:00Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "Strict local S3 endpoint comparison holds near central bases 111, 121, 212, and 222, off the central subspace.",
        "claim_boundary": "Four specified positive central S3 bases only; not arbitrary S3 functions, finite groups, Zhao's comparison, or Sidorenko.",
        "audit": result,
        "local_theorem": {
            "kernel": "At c=e, the full class-zero Hessian and cubic vanish; the invariant quartic has D=0 and A,B,C positive.",
            "transverse": "Standard and sign Hessians are (c-e)^2 times coefficientwise-positive polynomials; the unique standard cubic is divisible by (c-e)^4.",
            "conclusion": "Finite-polynomial remainder dominance yields a neighborhood in which N(a)>N(P_cl a) for noncentral a.",
        },
        "cycle_decision": {
            "companion_identity": "/root/darwin_cycle25_short",
            "companion_advice": "Seal after representing the full cubic tensor and stating finite-polynomial remainder dominance; then pursue a conjugacy-orbit KKT/exchange minimizer lemma.",
            "next_question": "Can exact KKT conditions at a hypothetical finite-group endpoint minimizer force equality within each conjugacy class by an exchange direction?",
            "falsifier": "A finite group and rational nonnegative a with N(a)<N(P_cl a) refutes the Zhao comparison itself; failure of an exchange identity only rejects that KKT engine.",
        },
        "frozen_hashes": freeze_inputs(ROOT, {k: (ROOT / p, h) for k, (p, h) in H.items()}),
        "runtime": check_runtime("c61"),
        "sealer": {"path": "proof/build_cycle_61_flat_stratum.py", "sha256": sha256(Path(__file__))},
        "replay": {
            "kernel_command": "python3 proof/check_cycle_61_flat_stratum.py",
            "transverse_command": "g++ -O3 -std=c++20 discovery/cycle61_standard_curvature_symbolic.cpp -o /tmp/c61-transverse && /tmp/c61-transverse discovery/out/cycle61-flat-stratum && python3 proof/check_cycle_61_transverse.py",
            "audit_command": "python3 proof/audit_cycle_61_flat_stratum.py",
            "test_command": "python3 -m unittest tests/test_cycle_61_flat_stratum.py",
            "check_command": "python3 proof/build_cycle_61_flat_stratum.py --check",
        },
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=ROOT / "artifacts/cycle-61-b061-flat-stratum-v1.json", payload_factory=payload))
