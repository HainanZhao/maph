"""Seal Cycle 11's certified 100-orbit first-lift exclusion."""

from __future__ import annotations

from pathlib import Path
import re
import subprocess

from check_cycle_11_certificates import bases, read_table, structural_check
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/cycle-11-b011-lrc-certified-sat-v1.json"
INPUTS: dict[str, tuple[Path, str]] = {
    "preregistration": (ROOT / "docs/cycle-11-b011-lrc-certified-sat-preregistration-v1.md", "e0ca8bc712093a45333f58623ea153798bbf257f6764c850dcfbe63887fe8359"),
    "encoding_soundness": (ROOT / "proof/cycle_11_sat_encoding_soundness.md", "dc83624b8949bd11b5aa8e89766be8e0d948258f81b57394048fbd64ec56b5ea"),
    "runner": (ROOT / "discovery/lrc_certified_sat.py", "dafdd9c83ae027ef9f1a589d8cc5817ecaafdf70caaa292b9c0b81981dc8ab93"),
    "independent_audit": (ROOT / "proof/check_cycle_11_certificates.py", "b6de322c0f556c7bb806d98f119d40d8dbc444b1f35e4cfc631264c7487e0b53"),
    "extended_checker": (ROOT / "proof/check_cycle_11_cap_proofs.sh", "ddaa0ba95aa271d51c2e955f560f5459e1abcd69f6865487e63627c98ce780a4"),
    "cadical_source": (ROOT / "discovery/vendor/cadical-f13d74439a5b5c963ac5b02d05ce93a8098018b8.tar.gz", "ffeab40171153fb3064c7ccc0278f5d7e1772ebdf2da85a3bf19a3f5be7cf4b0"),
    "drat_trim_source": (ROOT / "discovery/vendor/drat-trim-2e5e29cb0019d5cfd547d4208dca1b3ec290349f.tar.gz", "2ac28cd9e38e050b4f78fbff0efd4a1aa2349d157aef08c9b1fb6c7139949108"),
    "cadical_binary": (ROOT / "discovery/out/cycle11-tools/cadical-f13d74439a5b5c963ac5b02d05ce93a8098018b8/build/cadical", "2bcd58f5b0468eaacc00a9d6c7549fe17a9b11000307fcc23e3033d9703034c6"),
    "drat_trim_binary": (ROOT / "discovery/out/cycle11-tools/drat-trim-2e5e29cb0019d5cfd547d4208dca1b3ec290349f/drat-trim", "a48ebed7b4b6b373d3ddbeb3368dae7622a9e17bab7fe6eb751ab996757f9fbe"),
    "control_table": (ROOT / "discovery/out/cycle11-certified-sat/controls.tsv", "edf11f0e4534979d932b4d4f725ab62c15254f85eabc17c47565202058e66ccd"),
    "p199_table": (ROOT / "discovery/out/cycle11-certified-sat/p199.tsv", "f3c71d5c82876f07ccd0a3d67c3685d5497cbb3a6f9cbd7eddd529eceb917052"),
    "initial_summary": (ROOT / "discovery/out/cycle11-certified-sat/summary.txt", "f49525577db11c7c0de02f7320607e6b9ba264b9d2ba5fc590d6c6b5e10881c8"),
    "initial_timing": (ROOT / "discovery/out/cycle11-run.time", "d6577b72dc00b48e41b8164184ed8670492700103a32b141ef1be0f9e60a84d8"),
    "extension_result": (ROOT / "discovery/out/cycle11-cap-recheck.result", "aa7c6b9938dea78b1506c88945de62fa08af8668d9121e2aa9d918988f468b94"),
    "extension_timing": (ROOT / "discovery/out/cycle11-cap-recheck.time", "0d65ed83e81db3386a80cd5956f51104c1c6655d506b62483e2e5105c048db6f"),
    "independent_replay_result": (ROOT / "discovery/out/cycle11-independent-replay.result", "c7fe218def87c5c70bfc58818432e180e98a4c0bad4a5985f9b6fa5188f6fcfe"),
    "independent_replay_timing": (ROOT / "discovery/out/cycle11-independent-replay.time", "171cac7581c5cd1be0e78144eb656cc478e51df51e359924efe6be57afa1c40b"),
    "final_result": (ROOT / "discovery/out/cycle11-final.result", "b848490fc1fcdd6e601efa3f27fd8666e18eafbfaa77da003b225924b24553d5"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
    "regression_test": (ROOT / "tests/test_cycle_11_lrc_certified_sat.py", "04e3a0f45e0dff165dc3929780bc4664a8c1bb774f88b917434cfb85d3a6c438"),
}


def elapsed_seconds(path: Path) -> float:
    match = re.search(r"Elapsed \(wall clock\).*?: (?:(\d+):)?(\d+):(\d+\.\d+)", path.read_text())
    if not match:
        raise RuntimeError(f"missing elapsed time: {path}")
    hours = int(match.group(1) or 0)
    return 3600 * hours + 60 * int(match.group(2)) + float(match.group(3))


def peak_rss_kib(path: Path) -> int:
    match = re.search(r"Maximum resident set size \(kbytes\): (\d+)", path.read_text())
    if not match:
        raise RuntimeError(f"missing peak RSS: {path}")
    return int(match.group(1))


def payload() -> dict:
    runtime = check_runtime("Cycle 11 certified SAT")
    frozen = freeze_inputs(ROOT, INPUTS)
    jobs = structural_check()
    if len(jobs) != 393:
        raise RuntimeError("unexpected certificate corpus size")
    if (ROOT / "discovery/out/cycle11-cap-recheck.result").read_text().strip() != "PASS rows=000,002 proofs=VERIFIED":
        raise RuntimeError("extended proof result mismatch")
    if (ROOT / "discovery/out/cycle11-independent-replay.result").read_text().strip() != "PASS structure=393 h11_truth_rows=15360 proofs=393 wall_seconds=710.676757":
        raise RuntimeError("independent replay result mismatch")
    by_family = bases()
    controls = read_table(ROOT / "discovery/out/cycle11-certified-sat/controls.tsv")
    frontier = read_table(ROOT / "discovery/out/cycle11-certified-sat/p199.tsv")
    manifest = []
    for row in controls + frontier:
        family = row["family"]
        index = int(row["index"])
        manifest.append({
            "family": family,
            "index": index,
            "base": list(by_family[family][index]),
            "cnf_path": f"discovery/out/cycle11-certified-sat/{family}/{index:03d}.cnf",
            "cnf_sha256": row["cnf_sha256"],
            "proof_path": f"discovery/out/cycle11-certified-sat/{family}/{index:03d}.drat",
            "proof_sha256": row["proof_sha256"],
            "final_status": "CERTIFIED_UNSAT",
            "verification": "extended drat-trim replay" if family == "p199" and index in (0, 2) else "initial and independent drat-trim replay",
        })
    times = [
        ROOT / "discovery/out/cycle11-run.time",
        ROOT / "discovery/out/cycle11-cap-recheck.time",
        ROOT / "discovery/out/cycle11-independent-replay.time",
    ]
    aggregate_wall = sum(elapsed_seconds(path) for path in times)
    if aggregate_wall > 3600:
        raise RuntimeError("aggregate wall cap exceeded")
    return {
        "artifact_id": "cycle-11-b011-lrc-certified-sat-v1",
        "budget_ordinal": "B011",
        "cycle": 11,
        "record_type": "CERTIFIED_FINITE_RESULT",
        "recorded_at_utc": "2026-08-03T18:18:07Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "The exact first-lift CNF is unsatisfiable for all 100 frozen stratified p199 base orbits. Therefore none of those 100 bases belongs to F_1(13,199,14). All 293 H11/p47 controls are also certified UNSAT.",
        "claim_boundary": "This is a certified finite exclusion of exactly 100 named base orbits from a 4,748,938-orbit census. It does not establish F_1(13,199,14)=empty, J(13,199)=empty, LRC(13), a density estimate, or a universal structural rule.",
        "encoding_theorem": {
            "epistemic_status": "PROVED",
            "statement": "For a fixed base, the emitted CNF is satisfiable iff its frozen fiber contains a Definition-2.1-improper first lift.",
            "independent_checks": ["all 393 CNFs reconstructed as clause multisets", "all 15,360 H11 base-digit assignments truth-table checked against the direct predicate"],
        },
        "proved_controls": {"epistemic_status": "PROVED", "h11_certified_unsat": 240, "p47_certified_unsat": 53, "certified_unsat": 293},
        "p199_finite_result": {
            "epistemic_status": "PROVED",
            "sample_orbits": 100,
            "certified_unsat": 100,
            "initially_verified": 98,
            "verifier_only_extension": 2,
            "sample": "the exact fixed Cycle-8 10-by-10 stratified completed-base sample",
        },
        "independent_replay": {"structure_instances": 393, "h11_truth_rows": 15_360, "proofs_checked": 393, "result": "PASS", "wall_seconds": elapsed_seconds(times[2])},
        "containment": {
            "epistemic_status": "OBSERVED",
            "event": "The initial Python timeout killed two checker wrappers but left their child checkers orphaned; those already-timed-out children were terminated without touching the unrelated CPU-3 process. Process-group cleanup was added before any future invocation.",
            "effect_on_claim": "None: the two proof files were preserved and later VERIFIED, and the complete corpus passed a fresh independent replay.",
        },
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "adopted": True,
            "primary_ideas": ["verifier-only completion", "checked-core invariant", "CRT prototype", "stop Problem 1"],
            "companion_independent_ideas": ["verifier-only completion", "core-template/interpolation engine", "small exact CRT preflight"],
            "recommendation": "Complete rows 0/2 in live Cycle 11, seal, then open Cycle 12 for reusable checked core templates rather than a raw full census.",
            "strongest_flaw": "DRAT certifies CNF UNSAT only; a common encoding error must be excluded independently.",
            "falsifier": "Any CNF/direct-predicate disagreement, proof-instance hash mismatch, DRAT rejection, or checked SAT witness invalidates the corresponding exclusion.",
            "next_action": "New Cycle 12: cluster certified UNSAT cores, formulate base-orbit invariant templates, and test a small exact checker before any broad census.",
        },
        "resources": {
            "aggregate_wall_seconds": aggregate_wall,
            "aggregate_wall_cap_seconds": 3600,
            "peak_rss_kib": max(peak_rss_kib(path) for path in times),
            "corpus_and_tools_bytes": 2_888_765_340,
            "temporary_disk_cap_bytes": 107_374_182_400,
            "worker_cpus": [0, 1, 2],
            "reserved_cpu": 3,
        },
        "certificate_manifest": manifest,
        "runtime": {
            **runtime,
            "cadical": subprocess.run([str(INPUTS["cadical_binary"][0]), "--version"], check=True, capture_output=True, text=True).stdout.strip(),
            "drat_trim_source_commit": "2e5e29cb0019d5cfd547d4208dca1b3ec290349f",
        },
        "frozen_hashes": frozen,
        "replay": {
            "structure_command": "python3 proof/check_cycle_11_certificates.py",
            "proof_command": "taskset -c 0-2 python3 proof/check_cycle_11_certificates.py --proofs",
            "check_command": "python3 proof/build_cycle_11_lrc_certified_sat.py --check",
            "test_command": "python3 -m unittest tests/test_cycle_11_lrc_certified_sat.py -v",
        },
        "sealer": {"path": "proof/build_cycle_11_lrc_certified_sat.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
