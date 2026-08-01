#!/usr/bin/env python3
"""Corrected exact G1 energy audit with strict Sidon and self-contained pi bounds.

V1 is preserved: it omitted an explicit new-versus-new prospective Sidon
check and cited pi bounds without their derivation.  This successor retains
the same frozen screen but closes both finite-certification boundaries.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from discovery import run_g1_atlas_v1 as frozen_engine
from proof import audit_g1_energy_no_retention_v1 as route


OUTPUT = ROOT / "artifacts/g1-energy-no-retention-audit-v2.json"
ENGINE = ROOT / "discovery/run_g1_atlas_v1.py"
EXPECTED_ENGINE = "78f5088cbe615237d565854428511cda03e22fc04838d192c64d3215748c28ee"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def partial_arctan(inverse: int, final_index: int) -> Fraction:
    x = Fraction(1, inverse)
    return sum(((-1) ** index) * x ** (2 * index + 1) / (2 * index + 1) for index in range(final_index + 1))


def machin_pi_bounds() -> tuple[Fraction, Fraction]:
    """Certified rational bounds from pi/4=4 atan(1/5)-atan(1/239)."""
    # For positive x<1, even alternating partial sums are upper bounds and
    # odd partial sums lower bounds for arctan(x).
    atan5_upper, atan5_lower = partial_arctan(5, 12), partial_arctan(5, 13)
    atan239_upper, atan239_lower = partial_arctan(239, 2), partial_arctan(239, 3)
    lower = 16 * atan5_lower - 4 * atan239_upper
    upper = 16 * atan5_upper - 4 * atan239_lower
    require(lower < upper, "Machin pi enclosure ordering failed")
    return lower, upper


def w5_step_certified() -> tuple[int, dict[str, str]]:
    log_lower, log_upper = route.rational_log_3_over_2_bounds()
    pi_lower, pi_upper = machin_pi_bounds()
    # These strict bounds prove 14.5 < 2*pi/log(3/2) < 15.5.
    require(log_lower > 4 * pi_upper / 31, "W5 upper step bound failed")
    require(log_upper < 4 * pi_lower / 29, "W5 lower step bound failed")
    return 15, {
        "pi_lower": route.q(pi_lower), "pi_upper": route.q(pi_upper),
        "pi_radius": route.q((pi_upper - pi_lower) / 2),
        "log_3_over_2_lower": route.q(log_lower), "log_3_over_2_upper": route.q(log_upper),
        "lower_margin_for_14_5": route.q(4 * pi_lower / 29 - log_upper),
        "upper_margin_for_15_5": route.q(log_lower - 4 * pi_upper / 31),
    }


def strict_sidon(U: int, M: int) -> list[int] | None:
    """Greedy declared scan with both old-new and new-new sum separation."""
    points: list[int] = []
    pair_sums: set[int] = set()
    for candidate in range(U + 1):
        new_sums = [candidate + point for point in points] + [2 * candidate]
        # By induction pair_sums is already >1-separated.  The following two
        # exact checks are therefore equivalent to checking every unordered
        # pair in the prospective union, but avoid a quadratic scan of all
        # old-old pairs at every candidate.
        if any(value + delta in pair_sums for value in new_sums for delta in (-1, 0, 1)):
            continue
        if any(right - left <= 1 for left, right in zip(new_sums, new_sums[1:])):
            continue
        points.append(candidate)
        pair_sums.update(new_sums)
        if len(points) == M:
            return points
    return None


def parsed_fraction(text: str) -> Fraction:
    numerator, denominator = text.split("/", 1)
    return Fraction(int(numerator), int(denominator))


def certificate() -> dict[str, Any]:
    require(digest(ENGINE) == EXPECTED_ENGINE, "preserved v1 engine hash mismatch")
    hashes = {"v1_energy_audit": digest(ROOT / "proof/audit_g1_energy_no_retention_v1.py"), "v1_engine": digest(ENGINE), "preregistration": digest(route.PREREG), "conventions": digest(route.CONVENTIONS)}
    for label, expected in route.EXPECTED.items():
        require(hashes[label] == expected, "frozen hash mismatch: " + label)
    step, step_certificate = w5_step_certified()
    original_sidon, original_w5_step = route.sidon, route.w5_step_certified
    route.sidon = strict_sidon
    route.w5_step_certified = lambda: step
    try:
        rows = []
        for spec in route.screen_specs():
            points, parameters, failure = route.build_set(spec["set"], spec["w"], spec["screen_index"])
            engine_points, _engine_parameters, engine_failure = frozen_engine.build_set(spec["set"], route.SCREEN_SCALE, spec["w"], spec["screen_index"])
            require(engine_failure == failure, "independent/engine construction failure mismatch: " + spec["row_id"])
            base = {key: value for key, value in spec.items() if key != "w"}
            base["declared_energy_regime"] = route.regime(spec["set"])
            base["set_parameters"] = parameters
            if failure:
                require(points is None and engine_points is None, "failed construction unexpectedly has points")
                rows.append({**base, "status": "FAILED", "failure_code": failure, "energy": None, "set_points_sha256": None})
                continue
            require(points is not None and engine_points is not None, "successful construction has no points")
            require(points == engine_points, "independent/engine point mismatch: " + spec["row_id"])
            point_hash = hashlib.sha256(json.dumps(points, separators=(",", ":")).encode()).hexdigest()
            exact_energy = route.energy(points)
            exact_target = route.target(len(points), route.SCREEN_SCALE, route.regime(spec["set"]))
            quotient = Fraction(exact_energy, 1) / exact_target
            larger = max(quotient, 1 / quotient)
            power = larger ** 100
            require(power > 8, "energy reaches frozen retention band: " + spec["row_id"])
            rows.append({
                **base, "status": "COMPLETED", "failure_code": None,
                "energy": str(exact_energy), "target": route.q(exact_target),
                "energy_target_ratio": route.q(quotient),
                "symmetric_ratio_power_100": route.q(power),
                "strict_margin_over_8": route.q(power - 8),
                "set_points_sha256": point_hash,
                "rho_energy_retention": "REJECTED_EXACTLY",
            })
    finally:
        route.sidon, route.w5_step_certified = original_sidon, original_w5_step
    feasible = [row for row in rows if row["status"] == "COMPLETED"]
    failed = [row for row in rows if row["status"] == "FAILED"]
    require(len(feasible) == 434 and len(failed) == 154, "corrected feasibility count mismatch")
    closest = min(feasible, key=lambda row: parsed_fraction(row["symmetric_ratio_power_100"]))
    by_set = {}
    for name in sorted({row["set"] for row in rows}):
        group = [row for row in rows if row["set"] == name]
        by_set[name] = {"scheduled": len(group), "completed": sum(row["status"] == "COMPLETED" for row in group), "failed": sum(row["status"] == "FAILED" for row in group)}
    return {
        "artifact_id": "g1-energy-no-retention-audit-v2",
        "epistemic_status": "CERTIFIED_NUMERICAL",
        "claim_boundary": "Corrected finite U=2^12 energy certificate only. It does not evaluate complex values or prove an asymptotic obstruction, saturation theorem, density estimate, or G1 route decision.",
        "supersedes": {"artifact": "g1-energy-no-retention-audit-v1.json", "reason": "V1 did not explicitly check prospective new-new Sidon sums and did not derive its pi enclosure."},
        "frozen_hashes": hashes,
        "exact_method": {
            "energy": "integer pair-sum multiplicities for |a+b-c-d|<=1", "energy_radius": "0",
            "threshold_equivalence": "rho_energy >= -1/400 iff max(E/Target,Target/E)^100 <= 8, since U=2^12",
            "comparison_margin": "strict_margin_over_8 in every completed row",
            "sidon": "prospective all-pair sum separation, including old-new and new-new comparisons",
            "engine_point_reconciliation": "Every completed independent point list equals the preserved v1 constructor and is hash-recorded.",
            "W5_step": {"value": step, "status": "CERTIFIED_NUMERICAL", "machin_identity": "pi/4=4*atan(1/5)-atan(1/239)", **step_certificate},
        },
        "summary": {
            "scheduled_rows": len(rows), "feasible_rows": len(feasible), "failed_rows": len(failed), "energy_retention_eligible_rows": 0,
            "conclusion": "Every feasible frozen screen row fails rho_energy >= -1/400 by an exact positive margin; no row can pass the conjunctive G1 retention rule before complex-value evaluation.",
            "closest_to_energy_band": closest["row_id"], "closest_symmetric_ratio_power_100": closest["symmetric_ratio_power_100"], "closest_margin_over_8": closest["strict_margin_over_8"], "by_set": by_set,
        },
        "rows": rows,
        "falsifier": "Any hash mismatch, strict prospective-Sidon violation, engine point-list mismatch, finite-energy mismatch, invalid exact threshold equivalence, or completed row with symmetric_ratio_power_100 <= 8 refutes this finite certificate.",
        "replay": {"script_sha256": digest(Path(__file__)), "write_command": "python3 projects/guth-maynard-zero-density/proof/audit_g1_energy_no_retention_v2.py --write", "check_command": "python3 projects/guth-maynard-zero-density/proof/audit_g1_energy_no_retention_v2.py --check"},
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
        require(not OUTPUT.exists(), "refusing to overwrite corrected energy artifact")
        OUTPUT.write_text(payload, encoding="utf-8")
    else:
        require(OUTPUT.is_file() and OUTPUT.read_text(encoding="utf-8") == payload, "corrected G1 energy audit mismatch")
        print(json.dumps({"artifact": OUTPUT.name, "status": "ZERO_ENERGY_RETENTION_ROWS", "verified": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
