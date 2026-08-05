"""Seal Cycle 21's coupled-incidence theorem and 15 leaf certificates."""

from __future__ import annotations

import csv
from pathlib import Path

from check_cycle_21_coupled_incidence import audit
from cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle21-coupled-incidence"
OUTPUT = ROOT / "artifacts/cycle-21-b021-lrc-coupled-incidence-v1.json"
INPUTS = {
    "preregistration": (ROOT / "docs/cycle-21-b021-lrc-coupled-incidence-preregistration-v1.md", "2505f79788aecc3c255aa5ccb5f70dba0b460e2b55a3d4d02a509c0fddd156ef"),
    "prior_artifact": (ROOT / "artifacts/cycle-20-b020-lrc-crt-diagonal-v1.json", "cd2ced396549a819cd891472a1a71a1072dfbd8b322eb096fb2b2ce1841f62c6"),
    "soundness": (ROOT / "proof/cycle_21_coupled_incidence_soundness.md", "2666b8f025842975133da1f89eb36ab8cf9616fb7a36633b7f37149b2052bb15"),
    "search": (ROOT / "discovery/lrc_coupled_incidence.py", "b40d9ff5077b40caaeda0e1622d456ce9e9673c9451bc6cd19d2b58286853469"),
    "transfer": (ROOT / "discovery/transfer_cycle_21_certificates.py", "48de0c7e93ca03cd9ed15607863cd0da493f542d2a1f531068733ffc705159b0"),
    "audit": (ROOT / "proof/check_cycle_21_coupled_incidence.py", "3188f0a97576d4843f198dc1a55bc233afd2ebfd98dbfb64d773c5207e38ef2c"),
    "test": (ROOT / "tests/test_cycle_21_coupled_incidence.py", "af5ebd571f8f9a714b5b9b5c38956ead8eff419290c665140a79994520ddc19b"),
    "interface": (OUT / "interface.tsv", "f49afad834acdd1783d1e7f07b06993eb02680db401a124bd15e482780a8a67b"),
    "results": (OUT / "results.tsv", "122c1977f4c3314f311ada8d36e7f3816ae6d1e80b9320d1b322a7cac4809832"),
    "summary": (OUT / "result.txt", "d446f4981471147786603db65df0948e112abca60b6e73739f8ca93b1a3e6ff8"),
    "timing": (OUT / "run.time", "2fe7c0863b255644017d9320f2ac5bfcebe44f7849c5406e24cd16d23e36ee98"),
    "transfer_results": (OUT / "transfer.tsv", "112e48c8f304d5c77858d0298e003b4dce0c949b202fce1e018d473b7527eca7"),
    "transfer_summary": (OUT / "transfer-result.txt", "de3e58719a2a8820ce87cac16340eda1f0a4d3a0ca09cc28a512c76f2f7f9823"),
    "transfer_timing": (OUT / "transfer.time", "2be61b2cbe5cb9c2e6c4e1e89b895647cc76f2146115b6651196b3fb35a68289"),
    "audit_output": (OUT / "audit-final.json", "aabeabda9d3ecde4c7c676b746c69eea49e78f77b19a582d6b92e90cb425025f"),
    "scaffold": (ROOT / "proof/cycle_seal_v1.py", "9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
}


def certified_rows() -> list[dict[str, object]]:
    with (OUT / "results.tsv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    return [
        {
            "base_index": int(row["base_index"]),
            "leaf_ordinal": int(row["leaf_ordinal"]),
            "partition": row["partition"],
            "support": int(row["support"]),
            "W": int(row["W"]),
            "U": int(row["U"]),
            "margin": int(row["W"]) - int(row["U"]),
        }
        for row in rows if row["status"] == "CERTIFIED_DEFICIT"
    ]


def payload() -> dict:
    return {
        "artifact_id": "cycle-21-b021-lrc-coupled-incidence-v1",
        "budget_ordinal": "B021",
        "cycle": 21,
        "record_type": "PROVED_LOCAL_INTERFACE_AND_LEAF_CERTIFICATES",
        "recorded_at_utc": "2026-08-04T00:30:16Z",
        "status": "SEALED",
        "epistemic_status": "PROVED",
        "outcome": "The coupled CRT row-fiber formula is exact, and independently replayed width-three integer deficits exclude 15 previously unresolved canonical p199 leaves: nine for base 4 and six for base 3.",
        "claim_boundary": "Exactly 15 named leaves are newly excluded. Sixty-one Cycle-18 survivors remain unresolved; neither frozen base is complete, and no F_1, J, or LRC(13) claim follows. Zero successes in the bounded cyclic transfer pass are an OBSERVED method result only.",
        "audit": audit(),
        "certificates": certified_rows(),
        "interface": {"epistemic_status": "PROVED", "instances": 295, "predicate_comparisons": 1873178, "result": "CRT-generated and direct Cycle-11 formula tuples and frozen hashes agree."},
        "transfer": {"epistemic_status": "OBSERVED", "trials": 11895, "certificates": 0, "remaining_leaves": 61, "boundary": "No claim against other partitions, weights, coordinate maps, width-four blocks, or spectral methods."},
        "companion_decision": {
            "identity": "/root/decision_companion_2",
            "scope_review": "The interface and 15 named leaf exclusions are proved; 61 leaves and both bases remain open.",
            "recommendation": "Continue Cycle 21 for bounded exact transfer; if it produces little closure, seal and open targeted width-four blocks.",
            "strongest_flaw": "Repeated witnesses can reflect encoding proximity rather than a semantic orbit, so only target-specific direct replay is valid.",
            "falsifier": "Any target replay with U>=W or direct-CNF disagreement invalidates the affected elimination.",
            "independent_ideas": ["canonical labeled-incidence transfer", "targeted width-four blocks", "later Fourier character obstruction"],
            "final_action": "The exact direct transfer produced zero closures, so seal Cycle 21 and open distinct Cycle 22 width-four blocks.",
        },
        "resources": {"search_wall_seconds": 2230.309162, "search_peak_rss_kib": 948008, "transfer_wall_seconds": 126.981752, "transfer_peak_rss_kib": 73876, "aggregate_wall_seconds": 2357.290914, "worker_cpus": [0, 1, 2], "reserved_cpu": 3, "temporary_disk_cap_bytes": 21474836480, "output_corpus_bytes": 60897},
        "runtime": check_runtime("Cycle 21 coupled incidence"),
        "frozen_hashes": freeze_inputs(ROOT, INPUTS),
        "replay": {"search_command": "taskset -c 0-2 .venv/bin/python discovery/lrc_coupled_incidence.py", "transfer_command": "taskset -c 0-2 .venv/bin/python discovery/transfer_cycle_21_certificates.py", "audit_command": ".venv/bin/python proof/check_cycle_21_coupled_incidence.py", "check_command": "python3 proof/build_cycle_21_lrc_coupled_incidence.py --check", "test_command": ".venv/bin/python -m unittest tests.test_cycle_21_coupled_incidence -v"},
        "sealer": {"path": "proof/build_cycle_21_lrc_coupled_incidence.py", "sha256": sha256(Path(__file__))},
    }


if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__, output=OUTPUT, payload_factory=payload))
