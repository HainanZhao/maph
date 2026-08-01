#!/usr/bin/env python3
"""Read-only hostile audit of the sealed G1 route-decision v2 package."""
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
from typing import Any
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
SCRIPT = ROOT / "proof/adjudicate_g1_route_selection_v2.py"
ARTIFACT = ROOT / "artifacts/cycle-3-g1-route-decision-v2.json"
DOCUMENT = ROOT / "docs/cycle-3-g1-route-decision-v2-correction.md"
TESTS = ROOT / "tests/test_g1_route_selection_v2.py"
PACKAGE = {
    "adjudicator": "7129eab33fd08ede2cf590ef60d5b3afd5e962fa5a7771ef9ad6b414d4a7442a",
    "artifact": "87e697850dea074664227f6be5b187cc12ab4491bad6d2bda0065ee9df1b3872",
    "document": "92cd2ce9ef1ed06d0201d97becd74ff436ae7bfd888a014ad0ae098079b4f683",
    "tests": "e33bacb8172b28a7aba1822862a252da3bab266d1dc31b978a95930b31769014",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module():
    spec = importlib.util.spec_from_file_location("g1_route_v2_hostile_target", SCRIPT)
    require(spec is not None and spec.loader is not None, "cannot import v2 adjudicator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(command: list[str]) -> dict[str, Any]:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    return {"returncode": result.returncode, "stderr": result.stderr}


def audit() -> dict[str, Any]:
    require(platform.python_implementation() == "CPython", "audit requires CPython")
    require(platform.python_version() == "3.12.3", "audit requires CPython 3.12.3")
    require(sys.flags.optimize == 0, "audit requires non-optimized mode")
    paths = {"adjudicator": SCRIPT, "artifact": ARTIFACT, "document": DOCUMENT, "tests": TESTS}
    hashes: dict[str, str] = {}
    for label, path in paths.items():
        require(path.is_file(), f"package member absent: {label}")
        actual = sha256(path)
        require(actual == PACKAGE[label], f"package member hash mismatch: {label}")
        hashes[label] = actual

    data = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    require(data["epistemic_status"] == "OBSERVED", "wrong epistemic status")
    require(data["decision"] == "NO_SELECTION", "wrong decision")
    require(data["gate_status"] == "G1_CLOSED_NO_SELECTION", "wrong G1 status")
    require(data["adjudicator"] == {"path": "proof/adjudicate_g1_route_selection_v2.py", "sha256": PACKAGE["adjudicator"]}, "self identity is not bound")
    summary = data["evidence_summary"]
    require((summary["screen_rows"], summary["completed_rows"], summary["failed_rows"], summary["retained_rows"], summary["validation_rows"]) == (588, 429, 159, 0, 0), "zero-retained evidence summary mismatch")
    require(data["preservation"]["rejected_means_not_selected_not_refuted"] is True, "routes improperly refuted")
    require("authorizes none" in data["next_action_boundary"], "unauthorized next action")
    doc = DOCUMENT.read_text(encoding="utf-8")
    require("no-selection-only" in doc and "or refutation" in doc and "fails closed" in doc, "document claim boundary mismatch")

    normal = run([sys.executable, str(SCRIPT), "--check", str(ARTIFACT)])
    optimized = run([sys.executable, "-O", str(SCRIPT), "--check", str(ARTIFACT)])
    optimized_twice = run([sys.executable, "-OO", str(SCRIPT), "--check", str(ARTIFACT)])
    require(normal["returncode"] == 0, "normal sealed replay failed")
    require(optimized["returncode"] != 0 and optimized_twice["returncode"] != 0, "optimized modes do not fail closed")

    module = load_module()
    original_load = module.load_json
    empirical_path = module.INPUTS["empirical_reconciliation_v1"][0]
    empirical = original_load(empirical_path)
    retained_cf = copy.deepcopy(empirical)
    retained_cf["agreement"]["retained_rows"] = 1
    validation_cf = copy.deepcopy(empirical)
    validation_cf["agreement"]["validation_rows"] = 1

    def check_counterfactual(counterfactual: dict[str, Any]) -> None:
        def patched(path: Path):
            if path == empirical_path:
                return counterfactual
            return original_load(path)
        with mock.patch.object(module, "load_json", side_effect=patched):
            try:
                module.adjudicate()
            except RuntimeError as error:
                require("positive feature adjudication required" in str(error), "wrong counterfactual failure")
            else:
                raise RuntimeError("counterfactual retained/validation evidence did not fail closed")

    check_counterfactual(retained_cf)
    check_counterfactual(validation_cf)
    with tempfile.TemporaryDirectory() as temporary:
        mutated_input = Path(temporary) / "exact-atlas-tampered.json"
        mutated_input.write_bytes(module.INPUTS["exact_atlas_v2"][0].read_bytes() + b"\n")
        original_input = module.INPUTS["exact_atlas_v2"]
        module.INPUTS["exact_atlas_v2"] = (mutated_input, original_input[1])
        try:
            try:
                module.adjudicate()
            except RuntimeError as error:
                require("frozen input hash mismatch: exact_atlas_v2" in str(error), "wrong tamper failure")
            else:
                raise RuntimeError("actual frozen-input tamper did not fail closed")
        finally:
            module.INPUTS["exact_atlas_v2"] = original_input

        with tempfile.NamedTemporaryFile(dir=ROOT / "proof", suffix=".py") as stream:
            stream.write(SCRIPT.read_bytes() + b"\n# hostile identity mutation\n")
            stream.flush()
            original_self = module.SELF
            module.SELF = Path(stream.name)
            try:
                require(module.adjudicate()["adjudicator"] != data["adjudicator"], "self-identity mutation was not exposed")
            finally:
                module.SELF = original_self

    return {
        "artifact_id": "g1-route-decision-v2-hostile-audit-v1",
        "epistemic_status": "OBSERVED",
        "status": "PASS",
        "claim_boundary": "Read-only hostile audit of the sealed G1 route-decision v2 program decision. It certifies neither a mathematical theorem nor a route refutation.",
        "auditor": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "audited_package_hashes": hashes,
        "checks": {
            "sealed_normal_replay": "PASS",
            "self_identity_binding": "PASS",
            "actual_zero_retained_branch": "PASS",
            "retained_counterfactual_fail_closed": "PASS",
            "validation_counterfactual_fail_closed": "PASS",
            "actual_frozen_input_tamper_fail_closed": "PASS",
            "optimized_O_fail_closed": "PASS",
            "optimized_OO_fail_closed": "PASS",
            "document_artifact_boundary": "PASS",
            "unauthorized_next_action": "PASS",
        },
        "replay_returncodes": {"normal": normal["returncode"], "optimized": optimized["returncode"], "optimized_twice": optimized_twice["returncode"]},
        "conclusion": "G1 is legitimately closed only as OBSERVED NO_SELECTION for the sealed zero-retained branch. P2A/P2B/P2C and combinations are not selected and not refuted; the package authorizes no P2 theorem search.",
    }


def render(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    require(args.check.is_file(), "hostile-audit artifact absent")
    recorded = json.loads(args.check.read_text(encoding="utf-8"))
    require(recorded.get("auditor") == result["auditor"], "hostile-auditor identity mismatch")
    require(args.check.read_bytes() == render(result), "hostile-audit artifact mismatch")
    print(json.dumps({"status": result["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
