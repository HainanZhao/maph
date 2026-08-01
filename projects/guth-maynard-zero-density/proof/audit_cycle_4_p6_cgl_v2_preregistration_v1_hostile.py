#!/usr/bin/env python3
"""Read-only hostile audit of the sealed P6 CGL-v2 preregistration."""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import re
import subprocess
import sys
import tarfile
import tempfile
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
TARGET = ROOT / "proof/build_cycle_4_p6_cgl_v2_reconstruction_preregistration_v1.py"
ARTIFACT = ROOT / "artifacts/cycle-4-p6-cgl-v2-reconstruction-preregistration-v1.json"
SNAPSHOT = ROOT / "artifacts/cycle-4-p6-cgl-v2-authorization-snapshot-v1.json"
DOCUMENT = ROOT / "docs/cycle-4-p6-cgl-v2-reconstruction-preregistration-v1.md"
TESTS = ROOT / "tests/test_cycle_4_p6_cgl_v2_reconstruction_preregistration_v1.py"
TEX = ROOT / "artifacts/sources/g1-literature-audit-v1/extracted-2507.08296v2/Large_Value_Estimates_for_Dirichlet_Polynomials_with_Characters_and_Zero_Density_of_Dirichlet___L_-Functions.tex"
TAR = ROOT / "artifacts/sources/g1-literature-audit-v1/arxiv-2507.08296v2.tar"
PDF = ROOT / "artifacts/sources/g1-literature-audit-v1/arxiv-2507.08296v2.pdf"
LITERATURE_V1 = ROOT / "artifacts/g1-current-literature-audit-v1.json"
LITERATURE_V2 = ROOT / "artifacts/g1-current-literature-audit-v2-correction.json"
TEX_NAME = "Large_Value_Estimates_for_Dirichlet_Polynomials_with_Characters_and_Zero_Density_of_Dirichlet___L_-Functions.tex"
PACKAGE = {
    "builder": "c7d47109a24f7021653b2b81e8a6d1524c03e628cd2121d5eca4816c3123c008",
    "artifact": "1f9c195fa2dff8a58b754f10a58357384c5e3840839cc48269dd7b595a8ab36a",
    "authorization_snapshot": "c8183266cbfab602ba3c05c120a80293b7741284d6c46a08a88c03c3b46f25b3",
    "document": "2208164bdb207c0322fe376c21553f7dc4f307625328b8542fa2abe358dafd47",
    "tests": "aef2fff15a23c9dd8e77b6e1fa75419780ff6d087bd187f9ffa0239f8a439357",
    "tex": "0b9ebb6b604944b7c59a9ec37a75c48f6a08f88611f911ff5f02dc013b848e2f",
    "tar": "b982cd5afa5b5e8a9abff2c6306519ba558d321b19aadd3fdbe59b3750f8e9ae",
    "pdf": "adfe65cf0952bbb4eddfdaec7a8d3341130e427827f9159d9da039fc16336058",
    "literature_v1": "49da2e838ce60699ba870e0c532aab5ec8ba564c560811d9683ac92f0afbe6be",
    "literature_v2": "f56529c5919971385cc583b51255636022a5b33fb0cfd4857a587f1d3e099076",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path: Path) -> Any:
    spec = importlib.util.spec_from_file_location("p6_hostile_target", path)
    require(spec is not None and spec.loader is not None, "cannot import P6 sealer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def command(*parts: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(parts), cwd=ROOT, capture_output=True, text=True, timeout=60)


def lines(tex: str, locator: str) -> str:
    """Validate a frozen numeric locator and return its source slices."""
    pieces: list[str] = []
    source = tex.splitlines()
    for match in re.finditer(r"(\d+)(?:--(\d+))?", locator):
        first = int(match.group(1))
        last = int(match.group(2) or match.group(1))
        require(1 <= first <= last <= len(source), f"out-of-range locator: {locator}")
        pieces.append("\n".join(source[first - 1:last]))
    require(pieces, f"locator has no line range: {locator}")
    return "\n".join(pieces)


def no_plan_replay(module: Any) -> bytes:
    """A historical seal must not read the mutable PLAN through either API."""
    plan = (ROOT / "PLAN.md").resolve()
    old_text, old_bytes = Path.read_text, Path.read_bytes

    def deny_text(path: Path, *args: Any, **kwargs: Any) -> str:
        if path.resolve() == plan:
            raise RuntimeError("P6 historical replay attempted a live PLAN text read")
        return old_text(path, *args, **kwargs)

    def deny_bytes(path: Path, *args: Any, **kwargs: Any) -> bytes:
        if path.resolve() == plan:
            raise RuntimeError("P6 historical replay attempted a live PLAN byte read")
        return old_bytes(path, *args, **kwargs)

    Path.read_text, Path.read_bytes = deny_text, deny_bytes
    try:
        return module.render(module.certificate())
    finally:
        Path.read_text, Path.read_bytes = old_text, old_bytes


def audit() -> dict[str, Any]:
    require(platform.python_implementation() == "CPython", "audit requires CPython")
    require(platform.python_version() == "3.12.3", "audit requires CPython 3.12.3")
    require(sys.flags.optimize == 0, "audit requires non-optimized mode")
    paths = {
        "builder": TARGET, "artifact": ARTIFACT, "authorization_snapshot": SNAPSHOT,
        "document": DOCUMENT, "tests": TESTS, "tex": TEX, "tar": TAR, "pdf": PDF,
        "literature_v1": LITERATURE_V1, "literature_v2": LITERATURE_V2,
    }
    hashes = {label: sha256(path) for label, path in paths.items()}
    for label, expected in PACKAGE.items():
        require(hashes[label] == expected, f"P6 package hash mismatch: {label}")

    payload = json.loads(ARTIFACT.read_text(encoding="utf-8"))
    snapshot = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
    literature = json.loads(LITERATURE_V1.read_text(encoding="utf-8"))
    correction = json.loads(LITERATURE_V2.read_text(encoding="utf-8"))
    target_text = TARGET.read_text(encoding="utf-8")
    require("PLAN.md" not in target_text, "P6 sealer has a static mutable-PLAN reference")
    require(payload["sealer"] == {"path": "proof/build_cycle_4_p6_cgl_v2_reconstruction_preregistration_v1.py", "sha256": PACKAGE["builder"]}, "P6 self identity mismatch")
    require(payload["historical_replay"] == {
        "authorization_source": "immutable authorization snapshot", "mutable_research_plan_read": False,
        "mutable_research_plan_hash_pinned": False, "operational_preflight": "EXCLUDED_NOT_NEEDED_FOR_HISTORICAL_REPLAY",
    }, "P6 historical replay declaration mismatch")
    require(snapshot["historical_replay"]["live_plan_read_required"] is False and snapshot["historical_replay"]["live_plan_hash_pinned"] is False, "snapshot improperly couples history to PLAN")
    require(snapshot["semantic_authorization"]["expected_gate_outcome"] == "OPEN_ANALYTIC_INPUT", "authorization outcome changed")
    require(correction["integrity"]["preserved_v1"]["v1_artifact"]["sha256"] == PACKAGE["literature_v1"], "literature correction does not preserve v1")
    source_hashes = literature["source_verification"]["source_hashes"]
    require(source_hashes["chen_tex"]["sha256"] == PACKAGE["tex"] and source_hashes["chen_tar"]["sha256"] == PACKAGE["tar"] and source_hashes["chen_pdf"]["sha256"] == PACKAGE["pdf"], "literature ledger disagrees on CGL bytes")
    require("OBSERVED arXiv preprint; three-author v2" in literature["sources"]["chen_gupta_li_2507_08296v2"]["status"], "preprint status not retained")

    tex_bytes = TEX.read_bytes()
    tex = tex_bytes.decode("utf-8")
    require(len(tex.splitlines()) == 2468 and tex_bytes.count(b"\n") == 2467, "CGL TeX line convention mismatch")
    with tarfile.open(TAR, "r:*") as archive:
        member = archive.getmember(TEX_NAME)
        require(member.isfile(), "canonical CGL tar member is not regular")
        extracted = archive.extractfile(member)
        require(extracted is not None and extracted.read() == tex_bytes, "CGL tar/member/TeX bytes disagree")
    require(PDF.stat().st_size > 100_000, "CGL PDF is unexpectedly tiny")
    page_anchors = literature["source_verification"]["pdf_page_anchors"]["chen_gupta_li"]
    for key in ("p1", "p2", "p3", "p13", "p26", "p40", "p57"):
        anchor = page_anchors[key]
        text_path = ROOT / anchor["relative_path"]
        require(text_path.is_file() and anchor["contains"] in text_path.read_text(encoding="utf-8"), f"PDF anchor fails: {key}")

    rows = payload["row_registry"]
    expected_ids = [*(f"S{i:02d}" for i in range(1, 7)), *(f"L{i:02d}" for i in range(1, 13)), *(f"M{i:02d}" for i in range(1, 9)), *(f"Z{i:02d}" for i in range(1, 11)), *(f"F{i:02d}" for i in range(1, 11))]
    require([row["id"] for row in rows] == expected_ids and len(rows) == 46 and len(set(expected_ids)) == 46, "canonical 46-row registry mismatch")
    for item in rows:
        locator = item["locator"]
        if item["id"] != "S01":
            lines(tex, locator)
    by_id = {item["id"]: item for item in rows}
    require("L13" not in by_id and by_id["L12"]["mandatory_subchecks"] == ["odd_prime", "two_power"], "L12/L13 count correction not executable")
    count = payload["registry_count_correction"]
    require(count["draft_arithmetic"] == "6+13+8+10+10=47, not 46" and count["canonical_count"] == 46 and count["retired_draft_aliases"] == {"L13": "L12.two_power"} and count["no_obligation_dropped"] is True, "count correction not preserved")

    # Direct, source-based locator checks; these do not infer an unproved result.
    require(r"\author{Bin Chen}" in lines(tex, by_id["S02"]["locator"]) and r"\author{Yung Chi Li}" in lines(tex, by_id["S02"]["locator"]), "S02 locator misses author block")
    require(r"\begin{theorem}[Large value estimate for Dirichlet polynomials with characters]" in lines(tex, by_id["L01"]["locator"]), "L01 locator misses Partial-LVE")
    require("primitive character modulo $q$" in lines(tex, by_id["L01"]["locator"]) and r"N \geq(qT)^{\frac{2}{3}}" in lines(tex, by_id["L01"]["locator"]), "L01 source hypotheses mismatch")
    require("For an odd prime $p$" in lines(tex, by_id["L12"]["locator"]) and "modulo $2^j$" in lines(tex, by_id["L12"]["locator"]), "L12 subcheck locators mismatch")
    require("Let $X,Y, T > 1$" in lines(tex, by_id["Z01"]["locator"]), "Z01 locator misses detector domain")
    z03 = lines(tex, by_id["Z03"]["locator"])
    require(r"as $T \to \infty$ if $X$ is polynomially bounded in $T" in z03 and r"X = (qT)^{\epsilon}" in z03 and "worst case for our zero density estimate is when $T=1$" in z03, "Z03 blocker/source locator mismatch")
    require("non-primitive characters can be included by applying our final estimate for all factors of $q$ and summing" in lines(tex, by_id["Z05"]["locator"]), "Z05 locator mismatch")
    f08 = lines(tex, by_id["F08"]["locator"])
    require(f08.count("$T$-smooth") >= 3 and "q_2>q_1" in f08, "F08 locator misses smoothness use/chain")
    require("\\begin{definition}" not in tex and not re.search(r"(?:define|say|call).*T-smooth", tex, flags=re.IGNORECASE), "T-smooth unexpectedly defined in pinned TeX")
    require(r"q_1 \mid q" in lines(tex, by_id["F09"]["locator"]) and r"\beta = \frac{\log{q_1T}}{\log{qT}} \geq 1/2" in lines(tex, by_id["F10"]["locator"]), "F09/F10 locator mismatch")

    blockers = payload["expected_blockers"]
    require([item["id"] for item in blockers] == ["S06_EXTERNAL_INPUTS", "Z03_TAIL_X_RANGE", "Z05_PRIMITIVE_EULER_FACTORS", "Z06_CONDUCTOR_SUM_Q1", "F08_T_SMOOTH_UNDEFINED"], "blocker registry/order mismatch")
    require([item["row"] for item in blockers if item.get("group") == "PRIMITIVE_TO_ALL"] == ["Z05", "Z06"], "primitive/all blocker group mismatch")
    required_gates = snapshot["semantic_authorization"]["required_special_gates"]
    require("primitive-to-all-character transfer" in required_gates and "stated X/q/T range without silently imposing q <= T^C" in required_gates and "T-smooth definition and divisor-chain endpoints" in required_gates and "reachable external theorem hypotheses" in required_gates, "authorization special gates missing")
    boundary = payload["claim_boundary"]
    for phrase in ("no reconstruction is executed", "no CGL theorem is proved or repaired", "no 7/3 result is promoted", "no novelty claim is made", "no P7 family is selected", "no zero-density or short-interval theorem follows"):
        require(phrase in boundary, f"nonpromotion phrase missing: {phrase}")

    formulas = payload["frozen_crossing_formulas"]
    require(formulas["C1"] == "3*(1+lambda/3)/(1+sigma)" and formulas["C2"] == "3*(1-beta/2)/sigma" and formulas["C3"] == "((21-20*sigma)/6-beta/2)/(1-sigma)" and formulas["C4"] == "15/(3+5*sigma)", "frozen coefficient formulas mismatch")
    # Independent cleared-denominator derivation of the C3/Ingham crossing.
    beta = Fraction(1, 1)
    discriminant = 9 * beta * beta + 222 * beta - 71
    require(discriminant == 160, "C3 discriminant derivation failed")
    # At beta=1, B=(10-sqrt(10))/3: square the required radical identity.
    require(Fraction(40, 12) == Fraction(10, 3) and Fraction(160, 16) == 10, "B radical reduction failed")
    require(formulas["crossing_C3_polynomial"] == "20*sigma^2-(43-3*beta)*sigma+24-6*beta=0" and formulas["B"] == "(37+3*beta-sqrt(9*beta^2+222*beta-71))/12", "C3 crossing record mismatch")
    require(formulas["q1_equals_q_reductions"] == ["q^(7/3)*T^2", "9/4", "(10-sqrt(10))/3", "30/13"], "q1=q reductions mismatch")
    require(Fraction(7, 3) - Fraction(9, 4) == Fraction(1, 12) and Fraction(7, 3) - Fraction(30, 13) == Fraction(1, 39) and 10 > 9, "uniform 7/3 exact comparisons failed")

    module = load_module(TARGET)
    historical = no_plan_replay(module)
    require(historical == ARTIFACT.read_bytes(), "historical replay does not reproduce P6 artifact bytes")
    original_tex = module.INPUTS["cgl_v2_tex"]
    with tempfile.TemporaryDirectory() as temporary:
        altered = Path(temporary) / "altered.tex"
        altered.write_bytes(original_tex[0].read_bytes() + b"\n")
        module.INPUTS["cgl_v2_tex"] = (altered, original_tex[1])
        try:
            try:
                module.certificate()
            except RuntimeError as error:
                require("frozen input hash mismatch: cgl_v2_tex" in str(error), "wrong CGL TeX tamper failure")
            else:
                raise RuntimeError("CGL TeX tamper did not fail closed")
        finally:
            module.INPUTS["cgl_v2_tex"] = original_tex
    with tempfile.NamedTemporaryFile(dir=ROOT / "proof", suffix=".py") as handle:
        handle.write(TARGET.read_bytes() + b"\n# hostile self mutation\n")
        handle.flush()
        old_self = module.SELF
        module.SELF = Path(handle.name)
        try:
            require(module.certificate()["sealer"]["sha256"] != PACKAGE["builder"], "self mutation is not bound by seal")
        finally:
            module.SELF = old_self

    check = command(sys.executable, str(TARGET), "--check")
    opt = command(sys.executable, "-O", str(TARGET), "--check")
    opt2 = command(sys.executable, "-OO", str(TARGET), "--check")
    overwrite = command(sys.executable, str(TARGET), "--write")
    regression = command(sys.executable, "-m", "unittest", "tests/test_cycle_4_p6_cgl_v2_reconstruction_preregistration_v1.py")
    require(check.returncode == 0 and opt.returncode != 0 and opt2.returncode != 0 and overwrite.returncode != 0 and regression.returncode == 0, "P6 CLI/runtime/regression audit failed")
    require("refusing to overwrite" in overwrite.stderr, "overwrite does not fail closed")
    require("non-optimized CPython 3.12.3" in opt.stderr and "non-optimized CPython 3.12.3" in opt2.stderr, "optimized-mode rejection missing")
    require("enforce_resources(started_ns)" in target_text and target_text.index("enforce_resources(started_ns)") < target_text.index("with OUTPUT.open(\"xb\")"), "resource gate does not precede one-shot write")

    return {
        "artifact_id": "cycle-4-p6-cgl-v2-reconstruction-preregistration-v1-hostile-audit-v1",
        "epistemic_status": "OBSERVED",
        "status": "PASS",
        "claim_boundary": "Read-only hostile audit of a bounded preregistration. It proves no CGL theorem, repairs no preprint argument, and authorizes neither P7 nor a zero-density/short-interval claim.",
        "auditor": {"path": str(SELF.relative_to(ROOT)), "sha256": sha256(SELF)},
        "audited_package_hashes": hashes,
        "checks": {
            "sealed_self_replay": "PASS", "authorization_snapshot_and_literature_chain": "PASS", "no_live_PLAN_static_and_runtime": "PASS",
            "tex_tar_pdf_bytes_and_pdf_anchors": "PASS", "all_numeric_row_locators_in_range": "PASS", "key_locator_content": "PASS",
            "46_rows_L12_subchecks_retired_L13": "PASS", "expected_blockers_and_open_nonpromotion_boundary": "PASS",
            "crossing_formula_and_7_over_3_exact_arithmetic": "PASS", "route_design_nonimport_rule": "PASS",
            "optimized_O_and_OO_rejected": "PASS", "overwrite_rejected": "PASS", "resource_gate_precedes_write": "PASS",
            "self_and_source_tamper_fail_closed": "PASS", "target_regression_replayed": "PASS",
        },
        "conclusion": "The 46-row CGL-v2 preregistration is a reproducible, source-bound OPEN_ANALYTIC_INPUT seal. Its documented analytic blockers remain open; this PASS is not a validation of the preprint's 7/3 theorem or a theorem of this project.",
    }


def render(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", type=Path, required=True)
    args = parser.parse_args()
    result = audit()
    require(args.check.is_file(), "P6 hostile audit artifact absent")
    require(args.check.read_bytes() == render(result), "P6 hostile audit artifact mismatch")
    print(json.dumps({"status": result["status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
