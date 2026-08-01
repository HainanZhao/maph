#!/usr/bin/env python3
"""Read-only final hostile audit of Cycle 4 P1R preregistration v4."""
from __future__ import annotations

import argparse
from fractions import Fraction
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
SCRIPT = ROOT / "proof/build_cycle_4_p1r_preregistration_v4.py"
ARTIFACT = ROOT / "artifacts/cycle-4-p1r-preregistration-v4.json"
DOCUMENT = ROOT / "docs/cycle-4-p1r-preregistration-v4-source-attribution-correction.md"
TESTS = ROOT / "tests/test_cycle_4_p1r_preregistration_v4.py"
SNAPSHOT = ROOT / "artifacts/cycle-4-p1r-authorization-snapshot-v1.json"
V3 = ROOT / "artifacts/cycle-4-p1r-preregistration-v3.json"
V3_FAIL = ROOT / "artifacts/cycle-4-p1r-preregistration-v3-hostile-audit-v1.json"
GM_TEX = ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex"
PLAN = ROOT / "PLAN.md"
PACKAGE = {
    "builder": "4dd7c196085ce60f5174072020b1c6b726338f53316a0746968c273f956c6e6c",
    "artifact": "e2aeec9ec90e1fea0a9eade53d5ff1e57020df48bd92ae852121a941fbadd7f9",
    "document": "511569062b0a2efa0e565b94374d3ed40246800dcef4cc6b6a02189ab1fe6a28",
    "tests": "265744a93d87691c57d862ae31b3a7453a51c509eb69de2a1e7d49662a117990",
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


def no_plan_replay(module: Any) -> bytes:
    """Make either text or byte reads of live PLAN.md fatal during sealing."""
    original_text, original_bytes = Path.read_text, Path.read_bytes

    def deny_text(path: Path, *args: Any, **kwargs: Any) -> str:
        if path.resolve() == PLAN.resolve():
            raise RuntimeError("v4 historical replay attempted a live PLAN read")
        return original_text(path, *args, **kwargs)

    def deny_bytes(path: Path, *args: Any, **kwargs: Any) -> bytes:
        if path.resolve() == PLAN.resolve():
            raise RuntimeError("v4 historical replay attempted a live PLAN read")
        return original_bytes(path, *args, **kwargs)

    Path.read_text, Path.read_bytes = deny_text, deny_bytes
    try:
        return module.render(module.seal())
    finally:
        Path.read_text, Path.read_bytes = original_text, original_bytes


def audit() -> dict[str, Any]:
    require(platform.python_implementation() == "CPython", "audit requires CPython")
    require(platform.python_version() == "3.12.3", "audit requires CPython 3.12.3")
    require(sys.flags.optimize == 0, "audit requires non-optimized mode")
    paths = {"builder": SCRIPT, "artifact": ARTIFACT, "document": DOCUMENT, "tests": TESTS}
    hashes = {label: sha256(path) for label, path in paths.items()}
    for label, expected in PACKAGE.items():
        require(hashes[label] == expected, f"v4 package hash mismatch: {label}")

    builder_text = SCRIPT.read_text(encoding="utf-8")
    require("PLAN.md" not in builder_text, "static live-PLAN path reference in v4 builder")
    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    v3 = json.loads(V3.read_text(encoding="utf-8"))
    v3_fail = json.loads(V3_FAIL.read_text(encoding="utf-8"))
    require(payload["sealer"] == {"path": "proof/build_cycle_4_p1r_preregistration_v4.py", "sha256": PACKAGE["builder"]}, "v4 self identity mismatch")
    require(payload["historical_replay"] == {"authorization_source": "immutable authorization snapshot", "current_plan_read": False, "current_plan_eligibility": "EXCLUDED_FROM_HISTORICAL_ARTIFACT"}, "v4 replay declaration mismatch")
    require(snapshot["artifact_id"] == "cycle-4-p1r-authorization-snapshot-v1", "authorization snapshot identity mismatch")
    require(v3["correction"]["pinned_hostile_failures"] == {"v1": "FAIL_REPLAY_LIFECYCLE_SOURCE_AND_STATUS", "v2": "FAIL_PLAN_LIFECYCLE_SEMANTIC_COUPLING"}, "v1/v2 failures not preserved through v3")
    require(v3_fail["status"] == "FAIL_SOURCE_ATTRIBUTION_COMPLETENESS", "v3 source-attribution failure mismatch")
    require(payload["correction"]["pinned_v3_hostile_failure"] == v3_fail["status"] and payload["correction"]["preserves_v1_v3"] is True, "prior failure chain not pinned")
    require(payload["p1r_fs"]["gate_status"] == "PREREGISTERED_UNEXECUTED" and payload["p1r_fs"]["completed_theorem"] is False, "P1R-FS overclaim")
    require(payload["p1r_crr"]["epistemic_status"] == "CONJECTURED" and payload["p1r_crr"]["formalization_gate"]["search_authorized"] is False, "CRR search is not prohibited")

    module = load_module(SCRIPT, "p1r_v4_hostile_target")
    require(all("preflight" not in str(path) for path, _ in module.INPUTS.values()), "operational preflight is frozen in v4")
    historical = no_plan_replay(module)
    require(historical == ARTIFACT.read_bytes(), "no-PLAN replay does not reproduce v4 bytes")

    ledger = {entry["id"]: entry for entry in payload["source_hypothesis_ledger"]}
    theorem = ledger["GM-T1.1"]
    require(theorem == {
        "id": "GM-T1.1", "epistemic_status": "PROVED", "locator": "GM TeX lines 68--79, thrm:LargeValues",
        "hypotheses": ["|b_n| <= 1", "t_r are 1-separated points in [0,T]", "|sum_{n=N}^{2N} b_n n^(i t_r)| >= V for all r <= R"],
        "statement": "R <= T^(o(1))(N^2 V^(-2) + N^(18/5) V^(-4) + T N^(12/5) V^(-4))",
        "permitted_use": "exact formal exponent substitution (N,T,V)=(L,H,v^7), yielding [6,8,8]; upper-bound bookkeeping only",
    }, "GM-T1.1 source record mismatch")
    tex = GM_TEX.read_text(encoding="utf-8")
    require("\\begin{thrm}[Large values estimate]\\label{thrm:LargeValues}" in tex, "GM theorem label absent")
    require("N^2V^{-2}+N^{18/5}V^{-4}+TN^{12/5}V^{-4}" in tex, "GM three-term formula absent")
    require("\\begin{prpstn}[$S_3$ Bound]\\label{prpstn:S3}" in tex and "Let $N\\ge T^{3/4}$" in tex, "four-term S3 source/range absent")
    scales = payload["p1r_crr"]["scale_bookkeeping"]
    independent = [2 * 10 - 2 * 7, Fraction(18 * 10, 5) - 4 * 7, 12 + Fraction(12 * 10, 5) - 4 * 7]
    require(independent == [6, 8, 8], "independent GM-T1.1 exponent calculation failed")
    require(scales["source_variable_relabeling"] == {"theorem_N": "L=v^10", "theorem_T": "H=v^12", "theorem_V": "v^7"}, "variable relabeling mismatch")
    require(scales["large_values_source"] == "GM Theorem thm:LargeValues" and scales["large_values_term_exponents_in_v"] == ["6", "8", "8"], "large-values source/scale mismatch")
    require(scales["four_term_range_check"] == "L=H^(5/6)>=H^(3/4)", "four-term range bookkeeping mismatch")

    documented = run([sys.executable, str(SCRIPT), "--check"])
    optimized = run([sys.executable, "-O", str(SCRIPT), "--check"])
    optimized_twice = run([sys.executable, "-OO", str(SCRIPT), "--check"])
    overwrite = run([sys.executable, str(SCRIPT), "--write"])
    tests = run([sys.executable, "-m", "unittest", "tests/test_cycle_4_p1r_preregistration_v4.py"])
    require(documented == 0 and optimized != 0 and optimized_twice != 0 and overwrite != 0 and tests == 0, "CLI or final regression test failure")

    with tempfile.TemporaryDirectory() as temporary:
        directory = Path(temporary)
        original = module.INPUTS["gm_tex"]
        tampered_source = directory / "tampered.tex"
        tampered_source.write_bytes(original[0].read_bytes() + b"\n")
        module.INPUTS["gm_tex"] = (tampered_source, original[1])
        try:
            try:
                module.seal()
            except RuntimeError as error:
                require("frozen input hash mismatch: gm_tex" in str(error), "wrong source tamper error")
            else:
                raise RuntimeError("source tamper did not fail closed")
        finally:
            module.INPUTS["gm_tex"] = original

    with tempfile.NamedTemporaryFile(dir=ROOT / "proof", suffix=".py") as handle:
        handle.write(SCRIPT.read_bytes() + b"\n# hostile self tamper\n")
        handle.flush()
        original_self = module.SELF
        module.SELF = Path(handle.name)
        try:
            changed = module.seal()["sealer"]
            require(changed["sha256"] != PACKAGE["builder"] and changed["path"].startswith("proof/"), "self tamper not bound")
        finally:
            module.SELF = original_self

    return {
        "artifact_id": "cycle-4-p1r-preregistration-v4-hostile-audit-v1",
        "epistemic_status": "OBSERVED",
        "status": "PASS",
        "claim_boundary": "Read-only audit of v4 source attribution and replay integrity. It proves no P1R mathematical theorem and authorizes no CRR discovery.",
        "auditor": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "audited_v4_hashes": hashes,
        "checks": {
            "static_zero_PLAN_reference": "PASS", "runtime_zero_PLAN_read": "PASS", "immutable_snapshot_and_prior_failure_chain": "PASS",
            "v3_sole_failure_pinned": "PASS", "preflight_not_frozen": "PASS", "GM_T1_1_exact_formula_hypotheses_and_permitted_use": "PASS",
            "independent_6_8_8_substitution": "PASS", "S3_source_and_range": "PASS", "FS_unexecuted": "PASS", "CRR_search_prohibited": "PASS",
            "documented_CLI": "PASS", "optimized_O": "PASS", "optimized_OO": "PASS", "overwrite": "PASS", "self_tamper": "PASS", "source_tamper": "PASS",
            "v4_regression_test": "PASS", "v4_regression_test_identity_audit_pinned": "PASS",
        },
        "test_binding_assessment": "The sealed v4 artifact need not use its post-seal regression test as a mathematical/source input: --check is its self-contained historical replay. This hostile audit hash-pins and executes the v4 regression test, so the test byte used for this verification is independently replayable.",
        "conclusion": "The sole v3 defect is corrected: the direct GM theorem, hypotheses, three-term formula, variable relabeling, and exact [6,8,8] calculation are all present and independently checked. No new mathematical conclusion follows.",
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
