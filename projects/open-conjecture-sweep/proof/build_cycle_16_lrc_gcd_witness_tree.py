"""Seal Cycle 16's exact gcd-witness tree and sparse template census."""

from __future__ import annotations

from pathlib import Path

from check_cycle_16_gcd_witness_tree import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256
from lrc_gcd_witness_tree import CNFS, CORES, CORE_PROOFS, OUT, PROOFS, read_table

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-16-b016-lrc-gcd-witness-tree-v1.json"
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-16-b016-lrc-gcd-witness-tree-preregistration-v1.md", "15594bbddef448561236192ae677512c623b558d3e8304f095347be135304a81"),
    "engine": (ROOT / "discovery/lrc_gcd_witness_tree.py", "9f84ad656a29aa60aaca88129a4b16e3ab527c3143b238dc0ff0ec4c14e466d3"),
    "soundness": (ROOT / "proof/cycle_16_gcd_witness_tree_soundness.md", "1d9ae2038b6b496efd029b5b388a8d53671aced37424efab9e979784ae286902"),
    "audit": (ROOT / "proof/check_cycle_16_gcd_witness_tree.py", "af670bfa393b8780b4025461751b1e2949c800a1f1fab99ac1f47eb580665ec2"),
    "test": (ROOT / "tests/test_cycle_16_gcd_witness_tree.py", "666c9832e5d39858a6b239874ec5531880f078d940d2ce5804fb4e3741eed5ef"),
    "leaf_table": (OUT / "leaves.tsv", "c0993bba6bacd7808990039f3f76d4df8b52e1794947a0f95e6ccae03eccae0f"),
    "tree_result": (OUT / "tree.result", "6304e6de8ea58dfaa3fc92ce8717d7488f075542c06b76694b810e6f781b36e5"),
    "core_table": (OUT / "cores.tsv", "9d58b2d8e57c06d41b2ed126bf062b0b051a006986f79b0f1136a73a84313365"),
    "core_result": (OUT / "cores.result", "bfb9d68d88867fb0e957560474eae4e49a23b3bca3e021ecc96e1a8d87c84886"),
    "validation_table": (OUT / "validation/results.tsv", "1ed27a2851e7065d76d0bf71c8a034cb9fbeb06e130d071964fcc13451f3ed4a"),
    "validation_result": (OUT / "validation/validation.result", "79b018d192528747ccf644f801784510b8b6183e13fa8edaf191faa64bb8fa6f"),
    "census_certificates": (OUT / "census/certificates.tsv", "3f8db7fc50ad892f9a2882b55119cb6c1c3efc85d57844e49a0b6ea1a0e98382"),
    "census_summary": (OUT / "census/summary.tsv", "e269fbd6599066eab21037d528bb0dd251a2fa05be3a6268512b8db8e1929a42"),
    "census_result": (OUT / "census/census.result", "ab415ac398835edd3518e5c8fa32a6abff965c8c359ed8593593d9d120e12faa"),
    "tree_timing": (ROOT / "discovery/out/cycle16-tree.time", "a5466015b9ed90ddce4f6ecfff23285d22009fc1161acbee763eeb7eb4e62433"),
    "core_timing": (ROOT / "discovery/out/cycle16-cores.time", "38ca377488e00d7428eb9eae4e6718f44e3ea812daa78a0d2cf191687e69b093"),
    "census_timing": (ROOT / "discovery/out/cycle16-census.time", "e2cf01481deff209864c5e75944062f56679087622d1f59f33c9c587ac41be68"),
    "audit_timing": (ROOT / "discovery/out/cycle16-audit.time", "a5d153bbc8a21dcbee3a414820b18ba45973a04aa6d515eca7acc72dfc31a406"),
    "proof_replay_timing": (ROOT / "discovery/out/cycle16-proof-replay.time", "2fee083460592c09369db0edb7481433f5a55a2f8f3f7cc272f80581be93880e"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def payload() -> dict:
    runtime = check_runtime("Cycle 16 gcd-witness tree")
    frozen = freeze_inputs(ROOT, INPUTS)
    summary = audit(False)
    leaves = []
    for row in read_table(OUT / "leaves.tsv"):
        ordinal = int(row["ordinal"])
        cnf = CNFS / f"{ordinal:04d}.cnf"
        proof = PROOFS / f"{ordinal:04d}.drat"
        if sha256(cnf) != row["cnf_sha256"] or sha256(proof) != row["proof_sha256"]:
            raise RuntimeError("leaf evidence hash mismatch")
        leaves.append({
            "ordinal": ordinal,
            "pair_mod_2": [int(row["i"]), int(row["j"])],
            "pair_mod_7": [int(row["u"]), int(row["v"])],
            "unit_clauses": int(row["units"]),
            "status": "CERTIFIED_UNSAT",
            "cnf_path": str(cnf.relative_to(ROOT)),
            "cnf_sha256": row["cnf_sha256"],
            "proof_path": str(proof.relative_to(ROOT)),
            "proof_sha256": row["proof_sha256"],
            "proof_bytes": int(row["proof_bytes"]),
        })
    cores = []
    for row in read_table(OUT / "cores.tsv"):
        ordinal = int(row["ordinal"])
        cnf = CORES / f"{ordinal:04d}.cnf"
        proof = CORE_PROOFS / f"{ordinal:04d}.drat"
        if sha256(cnf) != row["core_sha256"] or sha256(proof) != row["proof_sha256"]:
            raise RuntimeError("core evidence hash mismatch")
        cores.append({
            "leaf_ordinal": ordinal,
            "pair_mod_2": [int(row["i"]), int(row["j"])],
            "pair_mod_7": [int(row["u"]), int(row["v"])],
            "clauses": int(row["clauses"]),
            "discriminating_clauses": int(row["discriminating_clauses"]),
            "status": "CERTIFIED_UNSAT_SUBSET",
            "cnf_path": str(cnf.relative_to(ROOT)),
            "cnf_sha256": row["core_sha256"],
            "proof_path": str(proof.relative_to(ROOT)),
            "proof_sha256": row["proof_sha256"],
        })
    return {
        "artifact_id": "cycle-16-b016-lrc-gcd-witness-tree-v1",
        "budget_ordinal": "B016",
        "cycle": 16,
        "record_type": "CERTIFIED_FINITE_RESULT",
        "recorded_at_utc": "2026-08-03T21:28:02Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "The 78^2 canonical first-two-nondivisibility leaves form a disjoint exhaustive partition of the gcd-admissible assignments for frozen base 7, and all 6,084 residual CNFs have independently replayed checked UNSAT proofs. All 608 cores in the smallest proof-size decile are certified residual subsets; the selected 27-clause core is one 26-literal coverage clause plus its 26 negated units, a direct cover-deficit contradiction. Its exact typed image is certified for the corresponding leaves of held-out bases 4 and 3. Across all 608,400 frozen base/leaf tests, this exact one-clause template matches 34,398 residuals and completes no base.",
        "claim_boundary": "This proves only the full canonical leaf tree for frozen base 7 and the 34,398 named exact template embeddings. It does not certify full leaf trees for bases 4 or 3, any unmatched base/leaf residual, every frozen base, F_1 emptiness, J(13,199) emptiness, or LRC(13). The 5.653846 percent match rate is a finite census, not an extrapolation.",
        "partition_theorem": {
            "epistemic_status": "PROVED",
            "coordinates": 13,
            "canonical_pairs_per_prime": 78,
            "leaves": summary["leaves"],
            "certified_unsat": summary["leaves"],
            "caps": 0,
            "errors": 0,
            "independent_full_proof_replay": "PASS: 6084/6084",
        },
        "core_result": {
            "epistemic_status": "PROVED",
            "certified_decile_cores": summary["cores"],
            "selected_leaf_ordinal": 74,
            "selected_pair_mod_2": [0, 1],
            "selected_pair_mod_7": [9, 12],
            "selected_clauses": summary["selected_clauses"],
            "selected_discriminating_clauses": 1,
            "direct_form": "one 26-literal positive coverage clause and its 26 negative unit clauses",
            "heldout_exact_matches": summary["validation_matches"],
        },
        "template_census": {
            "epistemic_status": "PROVED",
            "frozen_bases": 100,
            "leaf_tests": summary["census_tests"],
            "exact_matches": summary["census_matches"],
            "match_fraction": "34398/608400 = 0.05653846153846153",
            "complete_bases": summary["complete_bases"],
            "minimum_matches_per_base": 0,
            "maximum_matches_per_base": 702,
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "scope_review": "The 608,400-test replay eliminates exactly 34,398 named base/leaf residuals; it does not eliminate unmatched leaves, complete another base, or prove F_1, J, or LRC(13).",
            "recommendation": "Seal Cycle 16 and move to a genuinely broader analytic signature family.",
            "strongest_flaw": "The local signature is sparse: zero complete bases and a 0-to-702 match range.",
            "falsifier": "Any partition overlap/gap, residual mismatch, rejected proof, invalid typed map, false containment, or census reconstruction mismatch invalidates the affected claim.",
            "independent_ideas": ["typed time-deficit signatures", "finite Hall/set-cover certificates", "CRT composition as fallback"],
            "next_action": "New Cycle 17: freeze a finite analytic signature grammar and seek certificate-checked union coverage of canonical leaves.",
        },
        "resources": {
            "aggregate_wall_seconds": 616.43,
            "aggregate_wall_cap_seconds": 3600,
            "peak_rss_kib": 81536,
            "corpus_bytes": 1731925027,
            "temporary_disk_cap_bytes": 21474836480,
            "worker_cpus": [0, 1, 2],
            "reserved_cpu": 3,
        },
        "leaf_certificate_manifest": leaves,
        "core_certificate_manifest": cores,
        "runtime": runtime,
        "frozen_hashes": frozen,
        "replay": {
            "audit_command": "python3 proof/check_cycle_16_gcd_witness_tree.py",
            "full_proof_replay_command": "taskset -c 0-2 python3 proof/check_cycle_16_gcd_witness_tree.py --proofs",
            "check_command": "python3 proof/build_cycle_16_lrc_gcd_witness_tree.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_16_gcd_witness_tree.py -v",
        },
        "sealer": {"path": "proof/build_cycle_16_lrc_gcd_witness_tree.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
