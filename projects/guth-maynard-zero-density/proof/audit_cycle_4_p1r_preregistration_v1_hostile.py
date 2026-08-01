#!/usr/bin/env python3
"""Read-only hostile audit of Cycle 4 P1R preregistration v1."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
BUILDER = ROOT / "proof/build_cycle_4_p1r_preregistration_v1.py"
ARTIFACT = ROOT / "artifacts/cycle-4-p1r-preregistration-v1.json"
DOCUMENT = ROOT / "docs/cycle-4-p1r-preregistration-v1.md"
TESTS = ROOT / "tests/test_cycle_4_p1r_preregistration_v1.py"
PLAN = ROOT / "PLAN.md"
TEX = ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex"
PACKAGE = {
    "builder": "9010102782404cf63eb669714dadfb1a0f4b67005f895c3175ec669c60c94059",
    "artifact": "c6491407fb3cc5096610ddda8a8db952ffe0e002441d105024368f6486e39a5b",
    "document": "675708d31772f9483f3d6d53c5975908d40fe6ab76d9a5c189170c7a332899f8",
    "tests": "779f504a333dcbfda1ed7f06d380a20b369919a3a494004e974621e6fc97e8b4",
    "plan": "ce8cfb2c4c196b53a0e823667da2ce4e840d7ce18c754a9be1423064d9fce479",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str]) -> int:
    return subprocess.run(command, cwd=ROOT, capture_output=True, text=True).returncode


def audit() -> dict[str, Any]:
    require(platform.python_implementation() == "CPython", "audit requires CPython")
    require(platform.python_version() == "3.12.3", "audit requires CPython 3.12.3")
    require(sys.flags.optimize == 0, "audit requires non-optimized mode")
    paths = {"builder": BUILDER, "artifact": ARTIFACT, "document": DOCUMENT, "tests": TESTS, "plan": PLAN}
    hashes: dict[str, str] = {}
    for label, path in paths.items():
        require(path.is_file(), f"sealed v1 member absent: {label}")
        actual = sha256(path)
        require(actual == PACKAGE[label], f"sealed v1 member hash mismatch: {label}")
        hashes[label] = actual

    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    builder_text = BUILDER.read_text(encoding="utf-8")
    tex = TEX.read_text(encoding="utf-8")
    documented = run([sys.executable, str(BUILDER), "--check", "artifacts/cycle-4-p1r-preregistration-v1.json"])
    actual_check = run([sys.executable, str(BUILDER), "--check"])
    optimized = run([sys.executable, "-O", str(BUILDER), "--check"])
    optimized_twice = run([sys.executable, "-OO", str(BUILDER), "--check"])
    overwrite = run([sys.executable, str(BUILDER), "--write"])
    require(documented != 0, "expected documented-command defect absent")
    require(actual_check == 0, "actual v1 check unexpectedly fails")
    require(optimized != 0 and optimized_twice != 0, "optimized mode does not fail closed")
    require(overwrite != 0, "overwrite did not fail closed")

    live_plan_defect = '"plan": (ROOT / "PLAN.md"' in builder_text
    source_s3_defect = (
        '"GM-S3"' in builder_text
        and '"locator": "GM TeX lines 1684--1692, Proposition prpstnS3"' in builder_text
        and '"statement": "refined four-term S3 upper bound"' in builder_text
        and '\\begin{prpstn}[Refined $S_3$ bound] \\label{prpstnS3}' in tex
        and 'S_{3} \\lessapprox_\\epsilon T^2 |W|^{3/2}+TN|W|^{1/2}E(W)^{1/2}' in tex
        and '\\begin{prpstn}[$S_3$ Bound]\\label{prpstn:S3}' in tex
        and 'Let $N\\ge T^{3/4}$' in tex
    )
    fs_status_defect = artifact["p1r_fs"]["epistemic_status"] == "PROVED" and "UNEXECUTED_REQUIRES_TWO_INDEPENDENT" in artifact["p1r_fs"]["gate"]
    fs_authorized = artifact["status"] == "SEALED_PREREGISTRATION_NO_SEARCH_AUTHORIZED" and "execute the two independent exact P1R-FS routes" in PLAN.read_text(encoding="utf-8")
    crr_forbidden = artifact["p1r_crr"]["formalization_gate"]["search_authorized"] is False and "Before any search" in PLAN.read_text(encoding="utf-8")
    require(live_plan_defect and source_s3_defect and fs_status_defect, "expected v1 defects not found")
    require(fs_authorized and crr_forbidden, "authorization boundary unexpectedly differs")

    return {
        "artifact_id": "cycle-4-p1r-preregistration-v1-hostile-audit-v1",
        "epistemic_status": "OBSERVED",
        "status": "FAIL_REPLAY_LIFECYCLE_SOURCE_AND_STATUS",
        "claim_boundary": "Read-only audit of P1R preregistration v1. It records program/source-record defects and does not decide either P1R-FS or P1R-CRR mathematical target.",
        "auditor": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "audited_v1_hashes": hashes,
        "checks": {
            "actual_check_command": "PASS",
            "documented_check_command_verbatim": "FAIL",
            "optimized_O_fail_closed": "PASS",
            "optimized_OO_fail_closed": "PASS",
            "overwrite_fail_closed": "PASS",
            "self_identity_binding": "PASS",
            "mutable_live_PLAN_replay_lifecycle": "FAIL",
            "four_term_S3_source_locator_and_hypothesis": "FAIL",
            "FS_status_wording": "FAIL",
            "FS_authorized_after_preregistration": "PASS",
            "CRR_search_forbidden": "PASS",
        },
        "defects": {
            "documented_replay": "The document supplies --check followed by an artifact path, but v1 accepts only a boolean --check; the literal documented command exits nonzero.",
            "mutable_plan": "The sealer hashes the live mutable PLAN.md. Repository policy requires PLAN updates at gate changes, so a legitimate future P1R-FS gate update makes the v1 artifact unreplayable.",
            "source_s3": "The cited Refined S3 proposition prpstnS3 is two-term. The v1 four-term scale algebra instead uses the later S3 Bound prpstn:S3, whose N>=T^(3/4) condition is not pinned in the v1 source ledger.",
            "fs_status": "p1r_fs is tagged PROVED while its own gate says UNEXECUTED and requires two independent routes plus hostile audit. It must remain an unexecuted target/premise until that gate passes.",
        },
        "authorization": "FS execution is authorized by the current PLAN after this preregistration; CRR discovery/search remains forbidden until a separate formalization preregistration seals every listed field.",
        "required_correction": [
            "Create a v2 artifact with a frozen PLAN snapshot or an explicitly archived plan-byte input; do not make replay depend on live PLAN.md after later mandatory gate updates.",
            "Make the documented and parser replay commands identical, and add a verbatim-command regression.",
            "Replace the GM-S3 four-term source pin with Proposition prpstn:S3 and its N>=T^(3/4) gate, while separately retaining prpstnS3 only for its two-term statement if needed.",
            "Downgrade the P1R-FS branch from PROVED to an unexecuted route target until its required independent routes, reconciliation, and hostile audit close.",
        ],
    }


def render(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    require(args.check.is_file(), "hostile audit artifact absent")
    recorded = json.loads(args.check.read_text(encoding="utf-8"))
    require(recorded.get("auditor") == result["auditor"], "hostile auditor identity mismatch")
    require(args.check.read_bytes() == render(result), "hostile audit artifact mismatch")
    print(json.dumps({"status": result["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
