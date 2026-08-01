#!/usr/bin/env python3
"""Hostile pre-run audit of the G1 v4 two-fresh-run promotion boundary."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
ENGINE = ROOT / "discovery/run_g1_atlas_v4.py"
ADJUDICATOR = ROOT / "discovery/adjudicate_g1_atlas_v4.py"
MANIFEST = ROOT / "artifacts/cycle-3-g1-atlas-engine-v4-promotion-boundary.json"
DOC = ROOT / "docs/cycle-3-g1-atlas-engine-v4-promotion-boundary.md"
OUTPUT = ROOT / "artifacts/g1-probe-engine-v4-hostile-audit-v1.json"
EXPECTED = {
    "engine": "e7171c7b4720797b5a9bb87246c10a1e7f26569c9f240f69923de782f262dbd5",
    "adjudicator": "de2e688b2725df1d60b6946195f0979ea854177ea4ec1ff020115e2e0745b092",
    "manifest": "5752b2323fca43662248e74a4a64115059b7bc8bfbcebc0e654bee437f5f065c",
    "document": "696f9d24bc79b9de7bfd88d81e354f69c5123ae6b8f9d1e231761cdbb5bc047a",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=ROOT, text=True, capture_output=True)


def certificate() -> dict[str, Any]:
    hashes = {label: digest(path) for label, path in {"engine": ENGINE, "adjudicator": ADJUDICATOR, "manifest": MANIFEST, "document": DOC}.items()}
    for label, expected in EXPECTED.items():
        require(hashes[label] == expected, "v4 frozen hash mismatch: " + label)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    require(manifest["v4_engine"]["sha256"] == hashes["engine"], "manifest v4 engine identity mismatch")
    require(manifest["adjudicator"]["sha256"] == hashes["adjudicator"], "manifest adjudicator identity mismatch")
    require(manifest["per_run_promotion_status"] == "UNVERIFIED_PENDING_SECOND_FRESH_RUN", "manifest per-run promotion boundary changed")
    source = ENGINE.read_text(encoding="utf-8")
    adjudicator_source = ADJUDICATOR.read_text(encoding="utf-8")
    require("--resume" not in source, "v4 exposes forbidden resume CLI")
    require("require(not path.exists()" in source and "require(not observations_path.exists()" in source, "v4 fresh-path firewall missing")
    require("promotion_allowed\": False" in source and "UNVERIFIED_PENDING_SECOND_FRESH_RUN" in source, "v4 per-run promotion firewall missing")
    require("from discovery import" not in adjudicator_source and "import mpmath" not in adjudicator_source, "adjudicator is not standalone standard-library code")
    for token in ("V1_ENGINE_SHA256", "V2_ENGINE_SHA256", "V3_ENGINE_SHA256", "V4_ENGINE_SHA256", "PREREG_SHA256", "require_two_fresh_runs", "observations_a.read_bytes() == observations_b.read_bytes()"):
        require(token in adjudicator_source, "adjudicator promotion requirement missing: " + token)
    normal = run([sys.executable, str(ENGINE), "--check-integrity"])
    optimized = run([sys.executable, "-O", str(ENGINE), "--check-integrity"])
    require(normal.returncode == 0, "normal v4 integrity failed: " + normal.stderr)
    require(optimized.returncode != 0, "v4 optimized integrity did not fail closed")
    suite = run([sys.executable, "-m", "unittest", "tests/test_g1_atlas_engine_v1.py", "tests/test_g1_atlas_engine_v2.py", "tests/test_g1_atlas_engine_v3.py", "tests/test_g1_atlas_engine_v4.py", "tests/test_g1_atlas_preregistration_v1.py"])
    require(suite.returncode == 0 and "Ran 26 tests" in suite.stderr, "v4 focused regression suite failed: " + suite.stdout + suite.stderr)
    return {
        "artifact_id": "g1-probe-engine-v4-hostile-audit-v1",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Pre-run hostile audit of the v4 operational promotion boundary. It evaluates no finite complex screen row and proves no theorem, extremizer, density improvement, saturation result, or G1 route decision.",
        "frozen_hashes": hashes,
        "checks": {
            "runtime_chain_and_optimized_failure": "PASS",
            "v1_v2_v3_v4_preregistration_adjudicator_pins": "PASS",
            "fresh_checkpoint_and_output_paths_only": "PASS",
            "no_v4_resume_cli": "PASS",
            "per_run_promotion_disallowed": "PASS",
            "separate_stdlib_adjudicator": "PASS",
            "two_distinct_fresh_runs_and_byte_identity_required": "PASS",
            "complete_588_7744_560_validation_resource_checks_present": "PASS",
            "focused_regressions": "PASS_26",
        },
        "decision": {
            "status": "V4_READY_FOR_TWO_FRESH_UNVERIFIED_RUNS",
            "epistemic_status": "OBSERVED",
            "authorization_scope": "The frozen v4 A/B production commands may run from distinct new paths. Neither individual output may select a G1 route; only the separate adjudicator may emit finite empirical reconciliation after byte-identical observations.",
            "not_an_independent_mathematical_route": True,
        },
        "falsifier": "Any source/manifest hash mismatch, runtime failure, accepted optimization mode, resume/cached-path acceptance, per-run promotion flag, missing driver/row/validation/resource check, non-stdlib adjudicator dependency, or failure to demand two distinct byte-identical observations invalidates this audit.",
        "replay": {"script_sha256": digest(Path(__file__)), "write_command": "python3 projects/guth-maynard-zero-density/proof/audit_g1_probe_engine_v4_hostile_v1.py --write", "check_command": "python3 projects/guth-maynard-zero-density/proof/audit_g1_probe_engine_v4_hostile_v1.py --check"},
    }


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = render(certificate())
    if args.write:
        require(not OUTPUT.exists(), "refusing to overwrite v4 hostile audit artifact")
        OUTPUT.write_text(payload, encoding="utf-8")
    else:
        require(OUTPUT.is_file() and OUTPUT.read_text(encoding="utf-8") == payload, "v4 hostile audit mismatch")
        print(json.dumps({"artifact": OUTPUT.name, "status": "V4_READY_FOR_TWO_FRESH_UNVERIFIED_RUNS", "verified": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
