#!/usr/bin/env python3
"""Read-only hostile audit of Cycle 4 P1R preregistration v3."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
SCRIPT = ROOT / "proof/build_cycle_4_p1r_preregistration_v3.py"
ARTIFACT = ROOT / "artifacts/cycle-4-p1r-preregistration-v3.json"
SNAPSHOT = ROOT / "artifacts/cycle-4-p1r-authorization-snapshot-v1.json"
PREFLIGHT = ROOT / "proof/preflight_cycle_4_p1r_current_plan_v1.py"
V1 = ROOT / "artifacts/cycle-4-p1r-preregistration-v1.json"
V1_FAIL = ROOT / "artifacts/cycle-4-p1r-preregistration-v1-hostile-audit-v1.json"
V2_FAIL = ROOT / "artifacts/cycle-4-p1r-preregistration-v2-hostile-audit-v1.json"
GM_TEX = ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex"
PLAN = ROOT / "PLAN.md"
PACKAGE = {
    "builder": "0b75dfac9f69b52d51a84d7db1e05705cd00698e6a129bbfa443b77362fb1807",
    "artifact": "60597c5e6aefd65fa4ce11a1a0c6e9494b048bed0fb4df6e87e26d4f07cab0ee",
    "snapshot": "cd42352b145f67af0289aa21b142f40fbc2aac891944bb49d054631384c176d0",
    "preflight": "bf242ed25dc6acd55aaa762332db71ea47abda3229718df2acdc40acca3c4891",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot import: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(command: list[str]) -> int:
    return subprocess.run(command, cwd=ROOT, capture_output=True, text=True).returncode


def guarded_historical_replay(module: Any) -> bytes:
    """Exercise seal with every attempted read of the live PLAN made fatal."""
    original_text, original_bytes = Path.read_text, Path.read_bytes

    def deny_plan_text(path: Path, *args: Any, **kwargs: Any) -> str:
        if path.resolve() == PLAN.resolve():
            raise RuntimeError("historical replay attempted to read mutable PLAN.md")
        return original_text(path, *args, **kwargs)

    def deny_plan_bytes(path: Path, *args: Any, **kwargs: Any) -> bytes:
        if path.resolve() == PLAN.resolve():
            raise RuntimeError("historical replay attempted to read mutable PLAN.md")
        return original_bytes(path, *args, **kwargs)

    Path.read_text, Path.read_bytes = deny_plan_text, deny_plan_bytes
    try:
        return module.render(module.seal())
    finally:
        Path.read_text, Path.read_bytes = original_text, original_bytes


def audit() -> dict[str, Any]:
    require(platform.python_implementation() == "CPython", "audit requires CPython")
    require(platform.python_version() == "3.12.3", "audit requires CPython 3.12.3")
    require(sys.flags.optimize == 0, "audit requires non-optimized mode")
    paths = {"builder": SCRIPT, "artifact": ARTIFACT, "snapshot": SNAPSHOT, "preflight": PREFLIGHT}
    hashes = {label: sha256(path) for label, path in paths.items()}
    for label, expected in PACKAGE.items():
        require(hashes[label] == expected, f"v3 package hash mismatch: {label}")

    builder_text = SCRIPT.read_text(encoding="utf-8")
    require("PLAN.md" not in builder_text, "static live-PLAN path reference in historical builder")
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    v1 = json.loads(V1.read_text(encoding="utf-8"))
    v1_fail = json.loads(V1_FAIL.read_text(encoding="utf-8"))
    v2_fail = json.loads(V2_FAIL.read_text(encoding="utf-8"))
    require(payload["sealer"] == {"path": "proof/build_cycle_4_p1r_preregistration_v3.py", "sha256": PACKAGE["builder"]}, "self identity is unbound")
    require(payload["historical_replay"] == {"authorization_source": "immutable authorization snapshot", "current_plan_read": False, "current_plan_eligibility": "EXCLUDED_FROM_HISTORICAL_ARTIFACT"}, "historical replay declaration mismatch")
    require(snapshot["observed_plan"]["historical_sha256"] == v1["frozen_hashes"]["plan"]["sha256"], "snapshot does not bind historical Plan identity")
    require(set(snapshot["p1r_authorization"]) == {"crr_before_search", "crr_status", "fs_architecture", "fs_next_gate", "p1r_status"}, "authorization snapshot schema mismatch")
    require(v1_fail["status"] == "FAIL_REPLAY_LIFECYCLE_SOURCE_AND_STATUS", "v1 failure not preserved")
    require(v2_fail["status"] == "FAIL_PLAN_LIFECYCLE_SEMANTIC_COUPLING", "v2 failure not preserved")
    require(payload["correction"]["pinned_hostile_failures"] == {"v1": v1_fail["status"], "v2": v2_fail["status"]}, "prior failure containment mismatch")
    require(payload["p1r_fs"]["gate_status"] == "PREREGISTERED_UNEXECUTED" and payload["p1r_fs"]["completed_theorem"] is False, "FS status overclaimed")
    require(payload["p1r_crr"]["formalization_gate"]["search_authorized"] is False, "CRR search not prohibited")

    module = load_module(SCRIPT, "p1r_v3_hostile_target")
    historical_bytes = guarded_historical_replay(module)
    preflight = load_module(PREFLIGHT, "p1r_v3_hostile_preflight")
    require(all(path.resolve() != PREFLIGHT.resolve() for path, _ in module.INPUTS.values()), "mutable preflight frozen as an input")
    active = "| P1R | ACTIVE |\nP1R-FS: fixed-splice obstruction\nP1R-CRR: critical rational/random compatibility\nBefore any search, a versioned preregistration must freeze:\nNo P2A/P2B/P2C route is presently selected.\n"
    lifecycle: dict[str, str] = {}
    with tempfile.TemporaryDirectory() as temporary:
        directory = Path(temporary)
        cases = {
            "active": (active, "ELIGIBLE_CURRENT_PLAN"),
            "completed": (active.replace("| P1R | ACTIVE |", "| P1R | COMPLETE |"), "INELIGIBLE_CURRENT_PLAN"),
            "later_p2": (active.replace("No P2A/P2B/P2C route is presently selected.", "P2B selected after a later affirmative route decision."), "INELIGIBLE_CURRENT_PLAN"),
        }
        for label, (text, expected) in cases.items():
            path = directory / f"{label}.md"
            path.write_text(text, encoding="utf-8")
            result = preflight.evaluate(path)
            require(result["epistemic_status"] == "OBSERVED" and result["historical_replay_dependency"] == "EXCLUDED", "preflight overclaims or enters historic replay")
            require(result["status"] == expected, f"preflight lifecycle status mismatch: {label}")
            require(guarded_historical_replay(module) == historical_bytes, f"historical bytes change under lifecycle: {label}")
            lifecycle[label] = result["status"]

        source = module.INPUTS["gm_tex"]
        tampered = directory / "tampered.tex"
        tampered.write_bytes(source[0].read_bytes() + b"\n")
        module.INPUTS["gm_tex"] = (tampered, source[1])
        try:
            try:
                module.seal()
            except RuntimeError as error:
                require("frozen input hash mismatch: gm_tex" in str(error), "wrong source-tamper failure")
            else:
                raise RuntimeError("source tamper did not fail closed")
        finally:
            module.INPUTS["gm_tex"] = source

    with tempfile.NamedTemporaryFile(dir=ROOT / "proof", suffix=".py") as handle:
        handle.write(SCRIPT.read_bytes() + b"\n# hostile self-tamper\n")
        handle.flush()
        original_self = module.SELF
        module.SELF = Path(handle.name)
        try:
            require(module.seal()["sealer"]["sha256"] != PACKAGE["builder"], "self tamper was not reflected")
        finally:
            module.SELF = original_self

    documented = run([sys.executable, str(SCRIPT), "--check"])
    optimized = run([sys.executable, "-O", str(SCRIPT), "--check"])
    optimized_twice = run([sys.executable, "-OO", str(SCRIPT), "--check"])
    overwrite = run([sys.executable, str(SCRIPT), "--write"])
    require(documented == 0 and optimized != 0 and optimized_twice != 0 and overwrite != 0, "CLI failure-closed check failed")

    tex = GM_TEX.read_text(encoding="utf-8")
    require("\\begin{thrm}[Large values estimate]\\label{thrm:LargeValues}" in tex, "GM large-values theorem unavailable")
    require("N^2V^{-2}+N^{18/5}V^{-4}+TN^{12/5}V^{-4}" in tex, "GM large-values formula unavailable")
    ledger_ids = {row["id"] for row in payload["source_hypothesis_ledger"]}
    direct_large_values_attribution = "GM-T1.1" in ledger_ids and any("LargeValues" in item for item in module.SOURCE_FRAGMENTS)
    require(not direct_large_values_attribution, "audit target unexpectedly repaired; revise audit status")
    return {
        "artifact_id": "cycle-4-p1r-preregistration-v3-hostile-audit-v1",
        "epistemic_status": "OBSERVED",
        "status": "FAIL_SOURCE_ATTRIBUTION_COMPLETENESS",
        "claim_boundary": "Read-only audit of v3 lifecycle isolation and source attribution. It decides no P1R mathematical theorem.",
        "auditor": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "audited_v3_hashes": hashes,
        "checks": {
            "static_zero_PLAN_reference": "PASS",
            "runtime_zero_PLAN_read": "PASS",
            "immutable_snapshot_chain_and_schema": "PASS",
            "v1_v2_failure_containment": "PASS",
            "preflight_observed_only_not_frozen": "PASS",
            "lifecycle_historical_replay": "PASS",
            "FS_unexecuted": "PASS",
            "CRR_search_prohibited": "PASS",
            "documented_CLI": "PASS",
            "optimized_O": "PASS",
            "optimized_OO": "PASS",
            "overwrite": "PASS",
            "self_tamper": "PASS",
            "source_tamper": "PASS",
            "four_term_S3_source_and_range": "PASS",
            "large_values_formula_exists_in_GM_source": "PASS",
            "large_values_direct_source_attribution": "FAIL",
        },
        "lifecycle_preflight_statuses": lifecycle,
        "defect": "scale_bookkeeping asserts the large-values exponent vector [6,8,8], which comes from GM Theorem thm:LargeValues and its three-term bound, but v3 SOURCE_FRAGMENTS and source_hypothesis_ledger contain no GM-T1.1 entry or LargeValues fragment. Hash-pinning the full TeX file does not identify the theorem, hypotheses, or permitted use for that material formula.",
        "required_correction": [
            "Add a GM-T1.1 source-ledger row with the exact theorem locator, coefficient/separation hypotheses, and the permitted scale-bookkeeping use.",
            "Add the thm:LargeValues theorem label and its three-term formula to the source-fragment checks (or an equivalently precise pinned source extractor).",
            "Retain the v3 lifecycle-decoupling architecture and all preserved v1/v2 hostile failures; this audit does not reopen those corrected defects.",
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
    require(args.check.read_bytes() == render(result), "hostile audit artifact mismatch")
    print(json.dumps({"status": result["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
