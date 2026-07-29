#!/usr/bin/env python3
"""Audit and record the prepared-but-not-activated Phase-0 state."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[1]
SIC = WORKSPACE / "projects" / "sic-stark"
OUTPUT = ROOT / "artifacts" / "phase0-preparation-audit-v1.json"


def read_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_sha256(commit: str, path: str) -> str:
    payload = subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=WORKSPACE,
        check=True,
        capture_output=True,
    ).stdout
    return hashlib.sha256(payload).hexdigest()


def is_squarefree(value: int) -> bool:
    factor = 2
    while factor * factor <= value:
        if value % (factor * factor) == 0:
            return False
        factor += 1
    return True


def main() -> None:
    files = {
        "range": "data/range-v1.json",
        "anchors": "data/anchor-battery-v1.json",
        "schema": "data/corpus-record-schema-v1.json",
        "predicates": "data/engine-predicates-v1.json",
        "literature": "data/literature-perimeter-v1.json",
        "sequencing": "data/sequencing-gate-v1.json",
    }
    objects = {name: read_json(path) for name, path in files.items()}
    checks: dict[str, bool] = {}

    radicands = [
        value for value in range(2, 201) if is_squarefree(value)
    ]
    checks["field_count_121"] = (
        len(radicands) == objects["range"]["field_count"] == 121
    )
    checks["anchor_count_7"] = (
        len(objects["anchors"]["anchors"])
        == objects["anchors"]["expected_anchor_count"]
        == 7
    )
    checks["engine_partition_2_4_1"] = [
        anchor["engine"] for anchor in objects["anchors"]["anchors"]
    ].count("A") == 2 and [
        anchor["engine"] for anchor in objects["anchors"]["anchors"]
    ].count("B") == 4 and [
        anchor["engine"] for anchor in objects["anchors"]["anchors"]
    ].count("C") == 1
    checks["final_verdicts_binary"] = (
        objects["schema"]["properties"]["verdict"]["enum"]
        == ["PROVED", "FRONTIER"]
    )
    checks["final_tag_verified_only"] = (
        objects["schema"]["properties"]["claim_tag"]["enum"]
        == ["VERIFIED"]
    )
    checks["literature_perimeter_11"] = (
        len(objects["literature"]["sources"]) == 11
    )
    checks["sequencing_not_activated"] = not objects["sequencing"][
        "activated"
    ]
    checks["gp_available"] = shutil.which("gp") is not None
    checks["python_flint_environment"] = (
        SIC / ".venv" / "bin" / "python"
    ).is_file()

    frozen_commit = objects["anchors"]["source"]["sic_stark_commit"]
    tree = subprocess.run(
        [
            "git",
            "rev-parse",
            f"{frozen_commit}:projects/sic-stark",
        ],
        cwd=WORKSPACE,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    checks["source_tree_frozen"] = (
        tree == objects["anchors"]["source"]["sic_stark_tree"]
    )
    paper_i = (
        "projects/sic-stark/paper/sic-stark-dimensions-four-five.tex"
    )
    paper_ii = (
        "projects/sic-stark/paper/sic-stark-dimensions-seven-eight.tex"
    )
    checks["paper_I_hash_frozen"] = (
        frozen_sha256(frozen_commit, paper_i)
        == objects["anchors"]["source"]["paper_I_sha256"]
    )
    checks["paper_II_hash_frozen"] = (
        frozen_sha256(frozen_commit, paper_ii)
        == objects["anchors"]["source"]["paper_II_sha256"]
    )

    failed = sorted(name for name, passed in checks.items() if not passed)
    artifact = {
        "activation_authorized": False,
        "checks": checks,
        "claim_tag": "VERIFIED" if not failed else "FAILED_GATE",
        "failed_checks": failed,
        "file_hashes": {
            path: sha256(ROOT / path) for path in files.values()
        },
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "schema": "effective-stark-phase0-preparation-audit-v1",
        "sequencing_verdict": objects["sequencing"]["verdict"],
        "sic_stark_tree": tree,
        "verdict": (
            "PREPARATION_AUDIT_PASSED_NOT_ACTIVATED"
            if not failed
            else "PREPARATION_AUDIT_FAILED"
        ),
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(artifact, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"CHECK_COUNT={len(checks)}")
    print(f"FAILED_CHECK_COUNT={len(failed)}")
    print(f"ACTIVATION_AUTHORIZED={int(artifact['activation_authorized'])}")
    print(f"VERDICT={artifact['verdict']}")
    print(f"ARTIFACT={OUTPUT}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
