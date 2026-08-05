"""Seal Cycle 20's proved CRT two-diagonal bad-time interface."""

from __future__ import annotations

from pathlib import Path

from check_cycle_20_crt_diagonal import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle20-crt-diagonal"
OUTPUT = ROOT / "artifacts/cycle-20-b020-lrc-crt-diagonal-v1.json"
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-20-b020-lrc-crt-diagonal-preregistration-v1.md", "bf31a9e9bbe9059deb2f503bcce4609c37beb1f4ab523e3b9d95df32d9c08c90"),
    "prior_artifact": (ROOT / "artifacts/cycle-19-b019-lrc-symbolic-antichain-v1.json", "024d4bcc0d9dde79450182aff1ff3c2997325b96577d34c83dd3a15532f566b0"),
    "soundness": (ROOT / "proof/cycle_20_crt_diagonal_soundness.md", "5e6532e7d4f9937ead48d43870f15ed3e3851809231479ca4a689756ca13ea89"),
    "executed_source": (ROOT / "discovery/lrc_crt_diagonal.cpp", "1ca417537073cff88feea8233027856c13fbec2491628a48989ee79ea71a4975"),
    "executed_binary": (OUT / "lrc_crt_diagonal", "291668e0c5bb253c328ec7839aae6102b7b59413f11214eefcb625074efeeeb1"),
    "audit": (ROOT / "proof/check_cycle_20_crt_diagonal.py", "615be7ebf7324695dbb3c77e9e437d425fd48c1a3abc557056ccfd29fbfa2bac"),
    "test": (ROOT / "tests/test_cycle_20_crt_diagonal.py", "da6c60948af97fb13de5192cd364096a6f45b76b384fbf4f4473680ec30cbd04"),
    "p11_summary": (OUT / "p11-c4-summary.tsv", "2738fd2545a55eab2784edf42b64fbd3f5745fe7dfc9b0d07bbcca5bcd3e691c"),
    "p47_summary": (OUT / "p47-c7-summary.tsv", "2e87f2cb1e469803a5e6c6047aa5994bb643241eff2bcade931f17d0df3e0662"),
    "p199_summary": (OUT / "p199-c14-summary.tsv", "397b286e919704a913c498a687e08423bd3feca5a8272af38ce485a86b1ca094"),
    "p11_mismatches": (OUT / "p11-c4-mismatches.tsv", "e1802ae7e3d05b7eb4abb56728469caac8b8984afae7a8ece8da8ca893fed82c"),
    "p47_mismatches": (OUT / "p47-c7-mismatches.tsv", "e1802ae7e3d05b7eb4abb56728469caac8b8984afae7a8ece8da8ca893fed82c"),
    "p199_mismatches": (OUT / "p199-c14-mismatches.tsv", "e1802ae7e3d05b7eb4abb56728469caac8b8984afae7a8ece8da8ca893fed82c"),
    "p11_timing": (OUT / "p11-c4.time", "d0d93ac2bfa5688a346226521b96c2797b6047d0a02f32304747d11a7ec1750d"),
    "p47_timing": (OUT / "p47-c7.time", "7edcb6f14d8d0b6c05af339c036f98371dbf75addcaa9545c8ecbbf12b10127f"),
    "p199_timing": (OUT / "p199-c14.time", "d943a747c0d13dcfef12de4c8067b624f9c9fc8fa596cde7c270c18e046e983d"),
    "audit_timing": (OUT / "audit.time", "a7bba2c577d1d335f804d9f4ff0e5b5d827aad9743927495e40ec4ebdd109502"),
    "audit_output": (OUT / "audit.json", "5932c96762ef2dc2e379c92c6035be3b0b7dca39cb1d6580856770adb6dfc7da"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def payload() -> dict:
    runtime = check_runtime("Cycle 20 CRT diagonal")
    frozen = freeze_inputs(ROOT, INPUTS)
    summary = audit()
    return {
        "artifact_id": "cycle-20-b020-lrc-crt-diagonal-v1",
        "budget_ordinal": "B020",
        "cycle": 20,
        "record_type": "PROVED_LOCAL_INTERFACE",
        "recorded_at_utc": "2026-08-03T23:36:27Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "For every coprime positive p,c, the denominator-q=pc bad-time predicate is exactly the union of two coupled CRT diagonals: j=0, or j=c-1 with x_p nonzero. The complete frozen H11, p47, and p199 executable controls produced zero disagreements in 7,871,973 ordered pairs.",
        "claim_boundary": "The theorem factorizes one bad-time predicate only. It does not make the two diagonals independently selectable, factorize simultaneous coverage or gcd properness, close a leaf or base, empty F_1 or J, or prove LRC(13). The finite controls validate the executable implementation and are not the proof of the general theorem.",
        "theorem": {
            "epistemic_status": "PROVED",
            "hypotheses": "p,c are positive and coprime; q=pc; x, x_p, x_c and j are canonical residues in their stated ranges.",
            "statement": "Writing x=x_p+p*j, c*min(x,q-x)<q iff j=0 or (j=c-1 and x_p!=0), and j=p^{-1}(x_c-x_p) mod c.",
            "strict_boundary": "At j=c-1 and x_p=0, q-x=p, so the strict inequality is false.",
        },
        "complete_controls": {
            "epistemic_status": "OBSERVED",
            **summary,
            "independence": "The C++ generator and Python audit use separate implementations and different direct-threshold expressions; the Python audit re-enumerates every row.",
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "scope_review": "The identity is proved, with strong independent observed confirmation, but has exactly one-time scope and does not factor any global union, leaf CSP, gcd condition, F_1, J, or LRC.",
            "recommendation": "Seal Cycle 20 and open Cycle 21 for a genuinely distinct global coverage construction.",
            "strongest_flaw": "Multiplication couples p- and c-residues of both time and speed; treating local diagonals as independently selectable edges would silently relax the cover predicate.",
            "falsifier": "Any direct pair disagreement refutes the local identity; for the next engine, one fixed leaf whose direct outcome differs from the coupled-incidence formulation kills that formulation.",
            "independent_ideas": ["coupled two-diagonal permutation-graph incidence with Hall deficiency", "Fourier or character bound on graph unions", "finite-state transfer across c=14 fibers"],
            "next_action": "Prove exact graph-union equivalence first, retain gcd patterns, then test Hall or matching deficiency on complete controls before p199 targets.",
        },
        "resources": {
            "ordered_pair_comparisons": 7871973,
            "control_worker_cpus": [0, 1, 2],
            "reserved_cpu": 3,
            "control_aggregate_wall_seconds": 1,
            "largest_control_wall_seconds": 0.49,
            "audit_wall_seconds": 5.26,
            "peak_rss_kib": 16256,
            "output_corpus_bytes": 22534,
            "temporary_disk_cap_bytes": 1073741824,
        },
        "runtime": runtime,
        "frozen_hashes": frozen,
        "replay": {
            "compile_command": "g++ -std=c++20 -O3 -DNDEBUG -Wall -Wextra -pedantic discovery/lrc_crt_diagonal.cpp -o discovery/out/cycle20-crt-diagonal/lrc_crt_diagonal",
            "run_command": "Run the three frozen (p,c) domains on CPUs 0-2 as specified in the preregistration, writing the named summary, mismatch, and timing files.",
            "audit_command": "python3 proof/check_cycle_20_crt_diagonal.py",
            "check_command": "python3 proof/build_cycle_20_lrc_crt_diagonal.py --check",
            "test_command": "python3 -m unittest tests.test_cycle_20_crt_diagonal -v",
        },
        "sealer": {"path": "proof/build_cycle_20_lrc_crt_diagonal.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
