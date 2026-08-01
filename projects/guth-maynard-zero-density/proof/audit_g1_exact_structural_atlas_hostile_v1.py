#!/usr/bin/env python3
"""Independent hostile audit of the frozen G1 exact structural atlas v1.

The exact rational formulas are recomputed here without importing the target
atlas or its convention module.  The audit also tests the execution modes and
single-source-convention discipline required by the repository instructions.
It records defects rather than modifying the sealed v1 inputs in place.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import resource
import subprocess
import sys
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "artifacts/g1-exact-structural-atlas-hostile-audit-v1.json"
PERFORMANCE = ROOT / "artifacts/g1-exact-structural-atlas-hostile-audit-v1-performance.json"
PREREG = ROOT / "artifacts/cycle-3-g1-atlas-preregistration-v1.json"
ATLAS = ROOT / "artifacts/cycle-3-g1-exact-structural-atlas-v1.json"
ATLAS_SCRIPT = ROOT / "discovery/run_g1_exact_structural_atlas_v1.py"
PREREG_SCRIPT = ROOT / "discovery/build_g1_atlas_preregistration_v1.py"
CONVENTIONS = ROOT / "conventions/g1_atlas_v1.py"
DOC = ROOT / "docs/cycle-3-g1-atlas-preregistration-v1.md"

FROZEN = {
    "preregistration": (PREREG, "227ec1c66b2e109653354b6c3245b4e809fe52692c01514ac10064c23db2b6f8"),
    "exact_atlas": (ATLAS, "16b46d32fbe0b2d24eceda1dceebf51d2591019e36acd92085fe749685fc4023"),
    "exact_atlas_script": (ATLAS_SCRIPT, "24deb3435082349905d002c030fb8e9a022018c6bf34cdb63d9a516470d0aaea"),
    "preregistration_script": (PREREG_SCRIPT, "7383a7c5659d385d6255028b53e9f3b4541624303a0663fc22470f791bd4ccad"),
    "conventions": (CONVENTIONS, "3d3cef60c32dff2a2e4cbd3c10b229464d74aadbbaef53ba1fccc7158b78d726"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def f(value: str) -> Fraction:
    numerator, denominator = value.split("/", maxsplit=1)
    return Fraction(int(numerator), int(denominator))


def ceil_q(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def pairwise(values: dict[str, Fraction]) -> dict[str, str]:
    names = list(values)
    return {
        f"{left}-{right}": q(values[left] - values[right])
        for index, left in enumerate(names)
        for right in names[index + 1:]
    }


def groups(values: dict[str, Fraction]) -> list[list[str]]:
    found: list[list[str]] = []
    seen: set[Fraction] = set()
    for value in values.values():
        if value in seen:
            continue
        seen.add(value)
        labels = [label for label, candidate in values.items() if candidate == value]
        if len(labels) > 1:
            found.append(labels)
    return found


def local_grid() -> tuple[list[Fraction], list[Fraction], list[Fraction], list[Fraction]]:
    s = [Fraction(7, 10) + Fraction(index, 100) for index in range(11)]
    n = [Fraction(3, 4) + Fraction(index, 60) for index in range(16)]
    return s, n, list(s), [Fraction(1, 2), Fraction(7, 12), Fraction(2, 3), Fraction(3, 4)]


def audit_local_rows(rows: list[dict[str, Any]]) -> None:
    s_grid, n_grid, v_grid, w_grid = local_grid()
    require(len(rows) == 7744, "wrong number of local rows")
    expected_ids = [f"L:s={q(s)};n={q(n)};v={q(v)};w={q(w)}" for s in s_grid for n in n_grid for v in v_grid for w in w_grid]
    require([row["id"] for row in rows] == expected_ids, "local grid/order/ID differs from frozen rational grid")
    energy_rows = 0
    for row in rows:
        s, n, v, w = (f(row[key]) for key in ("s", "n", "v", "w"))
        a = {"A1": 2 * n * (1 - v), "A2": n * (Fraction(18, 5) - 4 * v), "A3": 1 + n * (Fraction(12, 5) - 4 * v)}
        c = {"C1": 2 * n * (1 - v), "C2": 1 + n * (1 - 2 * v), "C3": 1 + n * (4 - 6 * v)}
        require({label: f(value) for label, value in row["large_values"]["terms"].items()} == a, "local A-term mismatch: " + row["id"])
        require({label: f(value) for label, value in row["classical"]["terms"].items()} == c, "local C-term mismatch: " + row["id"])
        require(f(row["large_values"]["G"]) == max(a.values()), "local G mismatch: " + row["id"])
        inner = min(c["C2"], c["C3"])
        require(f(row["classical"]["inner_min"]) == inner and f(row["classical"]["C"]) == max(c["C1"], inner), "local nested classical mismatch: " + row["id"])
        require(f(row["Delta_LV"]) == max(c["C1"], inner) - max(a.values()), "local Delta mismatch: " + row["id"])
        require(row["large_values"]["pairwise_signed_residuals"] == pairwise(a), "local A residual mismatch: " + row["id"])
        require(row["large_values"]["tie_groups"] == groups(a), "local A tie mismatch: " + row["id"])
        require(row["large_values"]["max_tie_set"] == [label for label, value in a.items() if value == max(a.values())], "local A max-tie mismatch: " + row["id"])
        require(row["classical"]["pairwise_signed_residuals"] == pairwise(c), "local C residual mismatch: " + row["id"])
        require(row["classical"]["tie_groups"] == groups(c), "local C tie mismatch: " + row["id"])
        require(row["classical"]["inner_min_tie_set"] == [label for label in ("C2", "C3") if c[label] == inner], "local inner tie mismatch: " + row["id"])
        outer = {"C1": c["C1"], "min(C2,C3)": inner}
        require(row["classical"]["outer_max_tie_set"] == [label for label, value in outer.items() if value == max(outer.values())], "local outer tie mismatch: " + row["id"])
        all_terms = {**a, **c}
        require(row["all_formula_pairwise_signed_residuals"] == pairwise(all_terms), "full formula residual mismatch: " + row["id"])
        require(row["all_formula_tie_groups"] == groups(all_terms), "full formula tie mismatch: " + row["id"])
        require(row["energy_eligible"] == (v == s), "energy eligibility mismatch: " + row["id"])
        if v != s:
            require("energy" not in row, "off-diagonal energy leakage: " + row["id"])
            continue
        energy_rows += 1
        e = {"E1": w + n * (4 - 4 * s), "E2": Fraction(21, 8) * w + Fraction(1, 4) + n * (1 - 2 * s), "E3": 3 * w + n * (1 - 2 * s)}
        require({label: f(value) for label, value in row["energy"]["terms"].items()} == e, "energy term mismatch: " + row["id"])
        require(f(row["energy"]["max"]) == max(e.values()), "energy max mismatch: " + row["id"])
        require(row["energy"]["pairwise_signed_residuals"] == pairwise(e), "energy residual mismatch: " + row["id"])
        require(row["energy"]["tie_groups"] == groups(e), "energy tie mismatch: " + row["id"])
    require(energy_rows == 704, "wrong diagonal energy count")


def expected_transfer_rows() -> list[dict[str, Any]]:
    answer: list[dict[str, Any]] = []
    for s in local_grid()[0]:
        ell = Fraction(10, 1) / (6 + 10 * s)
        upper = Fraction(15, 1) / (6 + 10 * s)
        alpha = Fraction(15, 1) * (1 - s) / ((3 + 5 * s) * (Fraction(18, 5) - 4 * s))
        for n0 in sorted({Fraction(index, 100) for index in range(2, 51)} | {Fraction(5, 13), ell / 2}):
            k = ceil_q(ell / n0) if n0 <= ell / 2 else 2
            value = k * n0
            b = Fraction(15, 1) * (1 - s) / (3 + 5 * s)
            branch = "q<=alpha" if value <= alpha else "q>alpha"
            terms = ({"LV1": 2 * value * (1 - s), "LV2": value * (Fraction(18, 5) - 4 * s), "LV3": 1 + value * (Fraction(12, 5) - 4 * s)} if branch == "q<=alpha" else {"MVT1": 2 * value * (1 - s), "MVT2": 1 + value * (1 - 2 * s)})
            answer.append({
                "id": f"T:s={q(s)};n0={q(n0)};k={k};q={q(value)}", "s": q(s), "n0": q(n0), "k": k, "q": q(value),
                "ell": q(ell), "u": q(upper), "alpha": q(alpha), "B": q(b),
                "provenance": "ASYMPTOTIC_ENDPOINT_ONLY" if n0 == Fraction(1, 2) else "EXACT_POWER_SCALE",
                "upper_bound_status": "QUARANTINED_SOURCE_ASYMPTOTIC_ENDPOINT" if n0 == Fraction(1, 2) else "EXACT_POWER_SCALE",
                "branch": branch,
                "feasibility": {"n0_strictly_above_1_100": True, "k_in_1_to_77": True, "q_at_least_ell": True, "q_at_most_u_exact": True},
                "source_term_exponents": {label: q(term) for label, term in terms.items()},
                "B_minus_source_term": {label: q(b - term) for label, term in terms.items()},
                "source_term_tie_groups": groups(terms), "source_term_pairwise_signed_residuals": pairwise(terms),
            })
    return answer


def audit_transfer_rows(rows: list[dict[str, Any]], prereg: dict[str, Any]) -> None:
    expected = expected_transfer_rows()
    require(len(expected) == len(rows) == 560, "wrong transfer count")
    require(rows == expected, "transfer formula/grid/residual/tie data differs from independent recomputation")
    frozen_keys = ("s", "n0", "k", "q", "ell", "u", "alpha", "provenance", "branch")
    require([{key: row[key] for key in frozen_keys} for row in rows] == [{key: row[key] for key in frozen_keys} for row in prereg["transfer_rows"]], "atlas/prereg transfer coordinate mismatch")
    anchor = next(row for row in rows if row["id"] == "T:s=7/10;n0=5/13;k=2;q=10/13")
    require(anchor["source_term_exponents"] == {"LV1": "6/13", "LV2": "8/13", "LV3": "9/13"}, "mandatory transfer exponent anchor fails")
    require(anchor["B_minus_source_term"] == {"LV1": "3/13", "LV2": "1/13", "LV3": "0/1"}, "mandatory transfer residual anchor fails")


def imports_convention(text: str) -> bool:
    tree = ast.parse(text)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module in {"conventions.g1_atlas_v1", "g1_atlas_v1"}:
            return True
        if isinstance(node, ast.Import) and any(alias.name in {"conventions.g1_atlas_v1", "g1_atlas_v1"} for alias in node.names):
            return True
    return False


def checked(command: list[str], expected: int, label: str) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    require(completed.returncode == expected, label + ": " + json.dumps({"returncode": completed.returncode, "stdout": completed.stdout, "stderr": completed.stderr}, sort_keys=True))
    return completed


def certificate() -> dict[str, Any]:
    require(sys.flags.optimize == 0, "hostile audit forbids -O/-OO")
    hashes = {}
    for label, (path, expected) in FROZEN.items():
        observed = digest(path)
        require(observed == expected, "frozen hash mismatch: " + str(path))
        hashes[label] = observed
    prereg = json.loads(PREREG.read_text())
    atlas = json.loads(ATLAS.read_text())
    require(digest(DOC) == prereg["document"]["sha256"], "preregistration document hash mismatch")
    for source in prereg["sources"].values():
        require(digest(ROOT / source["path"]) == source["sha256"], "cited source hash mismatch: " + source["path"])
    require(atlas["epistemic_status"] == "PROVED", "unexpected atlas status")
    require(atlas["scope"] == {"finite_complex_probes_evaluated": 0, "screen_rows_evaluated": 0, "local_rows": 7744, "transfer_rows": 560}, "exact atlas scope changed")
    require(atlas["frozen_inputs"]["preregistration"]["sha256"] == hashes["preregistration"], "atlas does not pin preregistration")
    require(atlas["frozen_inputs"]["runtime"] == {"implementation": "CPython", "python": "3.12.3", "fractions": "stdlib Fraction"}, "atlas runtime differs from frozen execution runtime")
    audit_local_rows(atlas["local_rows"])
    audit_transfer_rows(atlas["transfer_rows"], prereg)
    local_anchor = atlas["mandatory_anchors"]["local"]
    require(local_anchor["energy"]["terms"] == {"E1": "5/3", "E2": "5/3", "E3": "5/3"}, "mandatory energy tie fails")
    require(local_anchor["large_values"]["max_tie_set"] == ["A2", "A3"], "mandatory large-values tie fails")
    checked([sys.executable, str(ATLAS_SCRIPT), "--check"], 0, "normal exact-atlas replay failed")
    checked([sys.executable, "-O", str(ATLAS_SCRIPT), "--check"], 1, "exact atlas did not fail closed under -O")
    checked([sys.executable, str(PREREG_SCRIPT), "--check"], 0, "normal preregistration replay failed")
    optimized_prereg = checked([sys.executable, "-O", str(PREREG_SCRIPT), "--check"], 0, "expected preregistration optimization bypass disappeared")
    prereg_ast = ast.parse(PREREG_SCRIPT.read_text())
    require(any(isinstance(node, ast.Assert) for node in ast.walk(prereg_ast)), "known preregistration bare assert surface disappeared")
    atlas_text = ATLAS_SCRIPT.read_text()
    require(not imports_convention(atlas_text), "known convention-derivation defect disappeared; issue a successor audit instead")
    require(all(f"def {name}()" in atlas_text for name in ("s_grid", "n_grid", "v_grid", "w_grid")), "known duplicated-grid surface disappeared")
    return {
        "artifact_id": "g1-exact-structural-atlas-hostile-audit-v1",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "OBSERVED hostile audit of G1 exact structural atlas v1. It independently recomputes the frozen rational grid, formulas, residuals, ties, transfer branches, and anchors; it records a runtime and convention-provenance defect. It proves no new large-values, density, short-interval, extremizer, or saturation theorem and is not a G1 route decision.",
        "frozen_hashes": hashes,
        "exact_rational_recomputation": {"status": "PASS", "epistemic_status": "PROVED", "conditional_scope": "Exact substitution into the preregistered formulas and direct source-hash verification only.", "local_rows": 7744, "transfer_rows": 560, "energy_diagonal_rows": 704, "transfer_branches": dict(sorted(Counter(row["branch"] for row in atlas["transfer_rows"]).items()))},
        "execution_mode_checks": {"normal_exact_atlas": {"status": "PASS", "epistemic_status": "OBSERVED"}, "optimized_exact_atlas": {"status": "PASS_FAIL_CLOSED", "epistemic_status": "OBSERVED", "exit_status": 1}, "normal_preregistration": {"status": "PASS", "epistemic_status": "OBSERVED"}, "optimized_preregistration": {"status": "CONTAINED_OPTIMIZATION_BYPASS_OBSERVED", "epistemic_status": "OBSERVED", "exit_status": optimized_prereg.returncode, "cause": "CPython -O strips the preregistration builder's bare assert checks."}},
        "convention_provenance": {"status": "CONTAINED_DUPLICATED_CONVENTION_OBSERVED", "epistemic_status": "OBSERVED", "target_imports_conventions_g1_atlas_v1": False, "surface": "The atlas redefines s_grid, n_grid, v_grid, and w_grid rather than deriving them from conventions/g1_atlas_v1.py.", "implication": "Current row arithmetic agrees independently, but v1 does not meet the repository single-source convention requirement and future drift could evade a mere row-count check."},
        "decision": {"status": "REMEDIATION_REQUIRED", "epistemic_status": "OBSERVED", "mathematical_v1_rows": "RETAINED_AS_EXACTLY_RECOMPUTED", "promotion_boundary": "Do not treat v1 as a fully AGENTS.md-compliant final authority. A versioned v2 successor must reject optimized mode in the preregistration builder, directly verify its source/document/runtime pins before the atlas, and derive frozen grids from the convention module. Preserve v1 unchanged."},
        "falsifier": "Any changed frozen hash, direct source/document hash failure, formula/residual/tie/transfer mismatch, nonzero complex-probe scope, normal replay failure, failure of the exact atlas to reject -O, or disappearance of the recorded preregistration -O bypass invalidates this bounded audit and requires a new versioned record.",
        "replay": {"script_sha256": digest(Path(__file__)), "write_command": "python3 projects/guth-maynard-zero-density/proof/audit_g1_exact_structural_atlas_hostile_v1.py --write", "check_command": "python3 projects/guth-maynard-zero-density/proof/audit_g1_exact_structural_atlas_hostile_v1.py --check", "performance_command": "python3 projects/guth-maynard-zero-density/proof/audit_g1_exact_structural_atlas_hostile_v1.py --write-performance"},
    }


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def write_performance(start: float, finish: float, payload: dict[str, Any]) -> None:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    observed = {"artifact_id": "g1-exact-structural-atlas-hostile-audit-v1-performance", "epistemic_status": "OBSERVED", "claim_boundary": "OBSERVED one-host replay measurement only; it certifies neither the exact algebra nor a finite-probe resource cap.", "audit_artifact": {"path": str(OUTPUT.relative_to(ROOT)), "sha256": digest(OUTPUT)}, "environment": {"implementation": platform.python_implementation(), "python": platform.python_version(), "platform": platform.platform()}, "measurement": {"wall_seconds": finish - start, "ru_maxrss": usage.ru_maxrss, "ru_maxrss_unit": "KiB on Linux"}, "command": payload["replay"]["performance_command"]}
    PERFORMANCE.write_text(render(observed))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write-performance", action="store_true")
    args = parser.parse_args()
    started = time.perf_counter()
    value = certificate()
    finished = time.perf_counter()
    payload = render(value)
    if args.write:
        OUTPUT.write_text(payload)
    elif args.check:
        require(OUTPUT.is_file() and OUTPUT.read_text() == payload, "hostile G1 exact-atlas audit mismatch")
        print(json.dumps({"artifact": OUTPUT.name, "status": "REMEDIATION_REQUIRED", "verified": True}, sort_keys=True))
    else:
        require(OUTPUT.is_file() and OUTPUT.read_text() == payload, "write/check hostile audit before recording performance")
        write_performance(started, finished, value)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
