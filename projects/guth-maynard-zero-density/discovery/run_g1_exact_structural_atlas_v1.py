#!/usr/bin/env python3
"""Build/check the exact, non-complex structural part of the frozen G1 atlas.

This is deliberately discovery code, rather than a proof of a new
large-values result.  It uses exact rational arithmetic only and does not
evaluate any registered finite Dirichlet polynomial.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import platform
import resource
import sys
import time
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PREREGISTRATION = ROOT / "artifacts/cycle-3-g1-atlas-preregistration-v1.json"
OUTPUT = ROOT / "artifacts/cycle-3-g1-exact-structural-atlas-v1.json"
PERFORMANCE = ROOT / "artifacts/cycle-3-g1-exact-structural-atlas-v1-performance.json"

# This identity is frozen before this structural atlas was evaluated.
PREREGISTRATION_SHA256 = "227ec1c66b2e109653354b6c3245b4e809fe52692c01514ac10064c23db2b6f8"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def q(value: Fraction) -> str:
    """Canonical reduced rational serialization used in identifiers and JSON."""
    return f"{value.numerator}/{value.denominator}"


def fq(value: str) -> Fraction:
    numerator, denominator = value.split("/", maxsplit=1)
    return Fraction(int(numerator), int(denominator))


def ceil_q(value: Fraction) -> int:
    return -(-value.numerator // value.denominator)


def tie_set(values: dict[str, Fraction], target: Fraction) -> list[str]:
    return [name for name, value in values.items() if value == target]


def tie_groups(values: dict[str, Fraction]) -> list[list[str]]:
    """All non-singleton equality classes, in insertion order."""
    groups: list[list[str]] = []
    seen: set[Fraction] = set()
    for value in values.values():
        if value in seen:
            continue
        seen.add(value)
        names = [name for name, candidate in values.items() if candidate == value]
        if len(names) > 1:
            groups.append(names)
    return groups


def pairwise_residuals(values: dict[str, Fraction]) -> dict[str, str]:
    names = list(values)
    return {
        f"{left}-{right}": q(values[left] - values[right])
        for index, left in enumerate(names)
        for right in names[index + 1:]
    }


def s_grid() -> list[Fraction]:
    return [Fraction(7, 10) + Fraction(index, 100) for index in range(11)]


def n_grid() -> list[Fraction]:
    return [Fraction(3, 4) + Fraction(index, 60) for index in range(16)]


def v_grid() -> list[Fraction]:
    return s_grid()


def w_grid() -> list[Fraction]:
    return [Fraction(1, 2), Fraction(7, 12), Fraction(2, 3), Fraction(3, 4)]


def local_row(s: Fraction, n: Fraction, v: Fraction, w: Fraction) -> dict[str, Any]:
    a_terms = {
        "A1": 2 * n * (1 - v),
        "A2": n * (Fraction(18, 5) - 4 * v),
        "A3": 1 + n * (Fraction(12, 5) - 4 * v),
    }
    g = max(a_terms.values())
    c_terms = {
        "C1": 2 * n * (1 - v),
        "C2": 1 + n * (1 - 2 * v),
        "C3": 1 + n * (4 - 6 * v),
    }
    inner = min(c_terms["C2"], c_terms["C3"])
    c = max(c_terms["C1"], inner)
    all_terms = {**a_terms, **c_terms}
    result: dict[str, Any] = {
        "id": f"L:s={q(s)};n={q(n)};v={q(v)};w={q(w)}",
        "s": q(s),
        "n": q(n),
        "v": q(v),
        "w": q(w),
        "large_values": {
            "terms": {name: q(value) for name, value in a_terms.items()},
            "G": q(g),
            "max_tie_set": tie_set(a_terms, g),
            "pairwise_signed_residuals": pairwise_residuals(a_terms),
            "tie_groups": tie_groups(a_terms),
        },
        "classical": {
            "terms": {name: q(value) for name, value in c_terms.items()},
            "inner_min": q(inner),
            "inner_min_tie_set": tie_set({"C2": c_terms["C2"], "C3": c_terms["C3"]}, inner),
            "C": q(c),
            "outer_max_tie_set": [
                name for name, value in {"C1": c_terms["C1"], "min(C2,C3)": inner}.items() if value == c
            ],
            "term_max_tie_set": tie_set(c_terms, max(c_terms.values())),
            "pairwise_signed_residuals": pairwise_residuals(c_terms),
            "tie_groups": tie_groups(c_terms),
        },
        "Delta_LV": q(c - g),
        "all_formula_pairwise_signed_residuals": pairwise_residuals(all_terms),
        "all_formula_tie_groups": tie_groups(all_terms),
        "energy_eligible": v == s,
    }
    if v == s:
        e_terms = {
            "E1": w + n * (4 - 4 * s),
            "E2": Fraction(21, 8) * w + Fraction(1, 4) + n * (1 - 2 * s),
            "E3": 3 * w + n * (1 - 2 * s),
        }
        result["energy"] = {
            "terms": {name: q(value) for name, value in e_terms.items()},
            "max": q(max(e_terms.values())),
            "max_tie_set": tie_set(e_terms, max(e_terms.values())),
            "pairwise_signed_residuals": pairwise_residuals(e_terms),
            "tie_groups": tie_groups(e_terms),
        }
    return result


def local_rows() -> list[dict[str, Any]]:
    rows = [local_row(s, n, v, w) for s in s_grid() for n in n_grid() for v in v_grid() for w in w_grid()]
    require(len(rows) == 7744, "frozen local grid does not have 7744 rows")
    require(len({row["id"] for row in rows}) == len(rows), "local row identifier collision")
    return rows


def transfer_row(s: Fraction, n0: Fraction) -> dict[str, Any]:
    ell = Fraction(10, 1) / (6 + 10 * s)
    upper = Fraction(15, 1) / (6 + 10 * s)
    alpha = Fraction(15, 1) * (1 - s) / ((3 + 5 * s) * (Fraction(18, 5) - 4 * s))
    k = ceil_q(ell / n0) if n0 <= ell / 2 else 2
    value = k * n0
    b = Fraction(15, 1) * (1 - s) / (3 + 5 * s)
    provenance = "ASYMPTOTIC_ENDPOINT_ONLY" if n0 == Fraction(1, 2) else "EXACT_POWER_SCALE"
    require(n0 > Fraction(1, 100), "forbidden source-inactive n0 row")
    require(1 <= k <= 77, "transfer k violates frozen bound")
    require(value >= ell, "transfer q falls below lower bound")
    require(value <= upper, "transfer q exceeds upper bound")
    branch = "q<=alpha" if value <= alpha else "q>alpha"
    if branch == "q<=alpha":
        terms = {
            "LV1": 2 * value * (1 - s),
            "LV2": value * (Fraction(18, 5) - 4 * s),
            "LV3": 1 + value * (Fraction(12, 5) - 4 * s),
        }
    else:
        terms = {
            "MVT1": 2 * value * (1 - s),
            "MVT2": 1 + value * (1 - 2 * s),
        }
    require(all(term <= b for term in terms.values()), "source transfer term exceeds B(s)")
    return {
        "id": f"T:s={q(s)};n0={q(n0)};k={k};q={q(value)}",
        "s": q(s),
        "n0": q(n0),
        "k": k,
        "q": q(value),
        "ell": q(ell),
        "u": q(upper),
        "alpha": q(alpha),
        "B": q(b),
        "provenance": provenance,
        "upper_bound_status": "QUARANTINED_SOURCE_ASYMPTOTIC_ENDPOINT" if provenance == "ASYMPTOTIC_ENDPOINT_ONLY" else "EXACT_POWER_SCALE",
        "branch": branch,
        "feasibility": {
            "n0_strictly_above_1_100": True,
            "k_in_1_to_77": True,
            "q_at_least_ell": True,
            "q_at_most_u_exact": True,
        },
        "source_term_exponents": {name: q(term) for name, term in terms.items()},
        "B_minus_source_term": {name: q(b - term) for name, term in terms.items()},
        "source_term_tie_groups": tie_groups(terms),
        "source_term_pairwise_signed_residuals": pairwise_residuals(terms),
    }


def transfer_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for s in s_grid():
        ell = Fraction(10, 1) / (6 + 10 * s)
        n0s = {Fraction(index, 100) for index in range(2, 51)} | {Fraction(5, 13), ell / 2}
        rows.extend(transfer_row(s, n0) for n0 in sorted(n0s))
    require(len(rows) == 560, "frozen transfer chart does not have 560 rows")
    require(len({row["id"] for row in rows}) == len(rows), "transfer row identifier collision")
    anchor = {
        "s": "7/10", "n0": "5/13", "k": 2, "q": "10/13",
        "ell": "10/13", "u": "15/13", "alpha": "45/52", "B": "9/13",
        "provenance": "EXACT_POWER_SCALE", "branch": "q<=alpha",
    }
    require(any(all(row[field] == expected for field, expected in anchor.items()) for row in rows), "mandatory transfer anchor absent")
    return rows


def verify_preregistration(preregistration: dict[str, Any], transfers: list[dict[str, Any]]) -> None:
    """Audit every frozen transfer row, not merely its cardinality or anchor."""
    require(preregistration["artifact_id"] == "cycle-3-g1-atlas-preregistration-v1", "wrong preregistration artifact")
    require(preregistration["frozen_before_discovery"] is True, "preregistration is not frozen")
    require(preregistration["local_grid"]["expected_rows"] == 7744, "preregistered local count changed")
    require(preregistration["screen"]["expected_rows"] == 588, "preregistered finite count changed")
    frozen_keys = ("s", "n0", "k", "q", "ell", "u", "alpha", "provenance", "branch")
    frozen = [{key: row[key] for key in frozen_keys} for row in preregistration["transfer_rows"]]
    generated = [{key: row[key] for key in frozen_keys} for row in transfers]
    require(frozen == generated, "generated transfer chart differs from a preregistered row")


def certificate() -> dict[str, Any]:
    require(sys.flags.optimize == 0, "exact atlas forbids -O/-OO")
    require(PREREGISTRATION.is_file(), "missing frozen preregistration artifact")
    require(sha256(PREREGISTRATION) == PREREGISTRATION_SHA256, "frozen preregistration artifact hash changed")
    preregistration = json.loads(PREREGISTRATION.read_text())
    rows = local_rows()
    transfers = transfer_rows()
    verify_preregistration(preregistration, transfers)
    local_anchor = next(row for row in rows if row["id"] == "L:s=7/10;n=5/6;v=7/10;w=2/3")
    require(local_anchor["energy_eligible"], "mandatory local anchor must be energy-eligible")
    require(local_anchor["energy"]["terms"] == {"E1": "5/3", "E2": "5/3", "E3": "5/3"}, "mandatory local energy tie fails")
    require(local_anchor["energy"]["max_tie_set"] == ["E1", "E2", "E3"], "mandatory local energy tie labels fail")
    return {
        "artifact_id": "cycle-3-g1-exact-structural-atlas-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "PROVED exact rational evaluation of the finite formulas frozen by the G1 preregistration, conditional on the cited published formulas. It evaluates no finite complex Dirichlet polynomial and proves no new large-values, density, short-interval, extremizer, or saturation theorem.",
        "scope": {
            "finite_complex_probes_evaluated": 0,
            "screen_rows_evaluated": 0,
            "local_rows": len(rows),
            "transfer_rows": len(transfers),
        },
        "frozen_inputs": {
            "preregistration": {
                "path": str(PREREGISTRATION.relative_to(ROOT)),
                "sha256": PREREGISTRATION_SHA256,
                "transfer_coordinate_digest": hashlib.sha256(json.dumps([
                    {key: row[key] for key in ("s", "n0", "k", "q", "ell", "u", "alpha", "provenance", "branch")}
                    for row in preregistration["transfer_rows"]
                ], sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
            },
            "runtime": {"implementation": platform.python_implementation(), "python": platform.python_version(), "fractions": "stdlib Fraction"},
        },
        "formula_conventions": {
            "fraction_serialization": "reduced numerator/denominator strings",
            "signed_residual": "left-minus-right",
            "transfer_residual": "B-minus-source-term",
            "energy_terms_present_only_when": "v=s",
        },
        "counts": {
            "local_total": len(rows),
            "local_energy_eligible": sum(row["energy_eligible"] for row in rows),
            "local_energy_ineligible": sum(not row["energy_eligible"] for row in rows),
            "transfer_total": len(transfers),
            "transfer_exact_power_scale": sum(row["provenance"] == "EXACT_POWER_SCALE" for row in transfers),
            "transfer_asymptotic_endpoint_only": sum(row["provenance"] == "ASYMPTOTIC_ENDPOINT_ONLY" for row in transfers),
            "transfer_by_branch": dict(sorted(Counter(row["branch"] for row in transfers).items())),
        },
        "mandatory_anchors": {"local": local_anchor, "transfer": next(row for row in transfers if row["id"] == "T:s=7/10;n0=5/13;k=2;q=10/13")},
        "local_rows": rows,
        "transfer_rows": transfers,
        "replay": {
            "script_sha256": sha256(Path(__file__)),
            "write_command": "python3 projects/guth-maynard-zero-density/discovery/run_g1_exact_structural_atlas_v1.py --write",
            "check_command": "python3 projects/guth-maynard-zero-density/discovery/run_g1_exact_structural_atlas_v1.py --check",
            "performance_command": "python3 projects/guth-maynard-zero-density/discovery/run_g1_exact_structural_atlas_v1.py --write-performance",
        },
    }


def render(value: dict[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def write_performance(started: float, finished: float, payload: dict[str, Any]) -> None:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    # Linux ru_maxrss is KiB; record the unit rather than silently converting it.
    observed = {
        "artifact_id": "cycle-3-g1-exact-structural-atlas-v1-performance",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "OBSERVED single-host execution measurement only; it is not a mathematical or resource-cap certificate.",
        "atlas_artifact": {"path": str(OUTPUT.relative_to(ROOT)), "sha256": sha256(OUTPUT)},
        "workload": payload["scope"],
        "environment": {"implementation": platform.python_implementation(), "python": platform.python_version(), "platform": platform.platform()},
        "measurement": {"wall_seconds": finished - started, "ru_maxrss": usage.ru_maxrss, "ru_maxrss_unit": "KiB on Linux"},
        "command": "python3 projects/guth-maynard-zero-density/discovery/run_g1_exact_structural_atlas_v1.py --write-performance",
    }
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
        require(OUTPUT.is_file() and OUTPUT.read_text() == payload, "exact structural atlas artifact mismatch")
        print(json.dumps({"artifact": OUTPUT.name, "finite_complex_probes_evaluated": 0, "local_rows": 7744, "transfer_rows": 560, "verified": True}, sort_keys=True))
    else:
        require(OUTPUT.is_file() and OUTPUT.read_text() == payload, "write/check atlas before recording performance")
        write_performance(started, finished, value)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
