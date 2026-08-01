#!/usr/bin/env python3
"""Independent exact audit of the G1 screen's energy retention gate.

The audit evaluates no complex Dirichlet polynomial.  It independently builds
each preregistered finite set at U=2^12, enumerates its integer additive
energy, and decides the rho_energy threshold through an exact rational
100th-power comparison.  It is a finite certificate, not a theorem about the
asymptotic Guth--Maynard method.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from conventions.g1_atlas_v1 import (
    BASE_SEED, COEFFICIENT_XOR, MASK64, REGISTERED_PAIRS, SCREEN_SCALE,
    SET_XOR, SPLITMIX64_GAMMA, SPLITMIX64_MUL1, SPLITMIX64_MUL2,
    primary_spine, q,
)


OUTPUT = ROOT / "artifacts/g1-energy-no-retention-audit-v1.json"
PREREG = ROOT / "artifacts/cycle-3-g1-atlas-preregistration-v1.json"
CONVENTIONS = ROOT / "conventions/g1_atlas_v1.py"
EXPECTED = {
    "preregistration": "227ec1c66b2e109653354b6c3245b4e809fe52692c01514ac10064c23db2b6f8",
    "conventions": "642a61fc03e5de6c7f7df5338e88da552ef1c72a7b7d7897898fb23740106ca5",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class SplitMix64:
    """Independently transcribed unsigned-64 reference stream."""
    def __init__(self, seed: int) -> None:
        self.state = seed & MASK64

    def next_u64(self) -> int:
        self.state = (self.state + SPLITMIX64_GAMMA) & MASK64
        z = self.state
        z = ((z ^ (z >> 30)) * SPLITMIX64_MUL1) & MASK64
        z = ((z ^ (z >> 27)) * SPLITMIX64_MUL2) & MASK64
        return (z ^ (z >> 31)) & MASK64


def set_seed(row_number: int) -> int:
    return (BASE_SEED ^ SET_XOR ^ row_number) & MASK64


def floor_power_of_two(exponent: Fraction) -> int:
    # U=2^12, so U^(a/b)=2^(12a/b), and direct integer comparison is exact.
    numerator = 12 * exponent.numerator
    denominator = exponent.denominator
    lo, hi = 1, 1
    target = 2**numerator
    while hi**denominator <= target:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid**denominator <= target:
            lo = mid
        else:
            hi = mid
    return lo


def rational_log_3_over_2_bounds() -> tuple[Fraction, Fraction]:
    """Exact alternating-series bounds sufficient to certify W5's h=15."""
    x = Fraction(1, 2)
    lower = sum(((-1) ** (term + 1)) * x**term / term for term in range(1, 15))
    upper = sum(((-1) ** (term + 1)) * x**term / term for term in range(1, 14))
    # 333/106 < pi < 355/113.  The following force 14.5 < 2pi/log(3/2) < 15.5.
    require(lower > Fraction(4 * 355, 31 * 113), "insufficient lower log bound for W5 step")
    require(upper < Fraction(4 * 333, 29 * 106), "insufficient upper log bound for W5 step")
    return lower, upper


def w5_step_certified() -> int:
    rational_log_3_over_2_bounds()
    return 15


def invariant(points: list[int], M: int) -> str | None:
    if len(points) != M:
        return "CARDINALITY_MISMATCH"
    if points != sorted(points) or len(set(points)) != len(points):
        return "SET_NOT_INCREASING_DISTINCT"
    if any(point < 0 or point > SCREEN_SCALE for point in points):
        return "SET_OUT_OF_RANGE"
    if any(right - left < 1 for left, right in zip(points, points[1:])):
        return "SPACING_VIOLATION"
    return None


def sidon(U: int, M: int) -> list[int] | None:
    # Membership in {old-1,old,old+1} is exactly the declared >1 test.
    points: list[int] = []
    old_sums: set[int] = set()
    for candidate in range(U + 1):
        new_sums = [candidate + point for point in points] + [2 * candidate]
        if any(value + delta in old_sums for value in new_sums for delta in (-1, 0, 1)):
            continue
        points.append(candidate)
        old_sums.update(new_sums)
        if len(points) == M:
            return points
    return None


def build_set(name: str, w: Fraction, row_number: int) -> tuple[list[int] | None, dict[str, Any], str | None]:
    U = SCREEN_SCALE
    M = floor_power_of_two(w)
    metadata: dict[str, Any] = {"M": M, "construction": name}
    if name == "W0-sidon":
        if w != Fraction(1, 2):
            return None, metadata, "INFEASIBLE_CARDINALITY"
        points = sidon(U, M)
        if points is None:
            return None, metadata, "INFEASIBLE_CARDINALITY"
    elif name == "W1-uniform":
        stream = SplitMix64(set_seed(row_number))
        values: set[int] = set()
        cap = 100 * (U + 1)
        draws = 0
        while len(values) < M and draws < cap:
            values.add(stream.next_u64() % (U + 1))
            draws += 1
        metadata.update({"draws": draws, "draw_cap": cap})
        if len(values) != M:
            return None, metadata, "SET_DRAW_LIMIT"
        points = sorted(values)
    elif name == "W2-jitter":
        stream = SplitMix64(set_seed(row_number))
        occupied: set[int] = set()
        raw: list[int] = []
        for j in range(M):
            candidate = (j * (U + 1)) // M + int(stream.next_u64() % 3) - 1
            candidate = min(U, max(0, candidate))
            chosen = next((point for point in range(candidate, U + 1) if point not in occupied), None)
            if chosen is None:
                chosen = next((point for point in range(0, candidate) if point not in occupied), None)
            if chosen is None:
                return None, metadata, "INFEASIBLE_CARDINALITY"
            occupied.add(chosen)
            raw.append(chosen)
        points = sorted(raw)
    elif name == "W3-AP":
        a = U // 7
        h = max(1, (U - 2 * a) // max(1, M - 1))
        metadata.update({"a": a, "h": h})
        points = [a + j * h for j in range(M)]
        if points and points[-1] > U:
            return None, metadata, "INFEASIBLE_CARDINALITY"
    elif name == "W4-four-block":
        r = (M + 3) // 4
        h = max(1, U // (32 * r))
        metadata.update({"r": r, "h": h})
        raw: list[int] = []
        seen: set[int] = set()
        for block in range(4):
            origin = ((2 * block + 1) * U) // 8
            for j in range(r):
                point = origin + j * h
                if 0 <= point <= U and point not in seen:
                    raw.append(point)
                    seen.add(point)
                if len(raw) == M:
                    break
            if len(raw) == M:
                break
        if len(raw) != M:
            return None, metadata, "INFEASIBLE_CARDINALITY"
        points = sorted(raw)
    elif name == "W5-rational":
        h = w5_step_certified()
        a = (U - (M - 1) * h) // 2
        metadata.update({"a": a, "h": h, "certified_log_step": True})
        if a < 0:
            return None, metadata, "INFEASIBLE_CARDINALITY"
        points = [a + j * h for j in range(M)]
    else:
        raise ValueError(name)
    failure = invariant(points, M)
    return (None, metadata, failure) if failure else (points, metadata, None)


def target(M: int, U: int, regime: str) -> Fraction:
    if regime == "low":
        return Fraction(M * M)
    if regime == "intermediate":
        return max(Fraction(M * M), Fraction(M**4, U))
    if regime == "high":
        return Fraction(M**3)
    raise ValueError(regime)


def regime(name: str) -> str:
    if name == "W0-sidon":
        return "low"
    if name == "W3-AP":
        return "high"
    return "intermediate"


def energy(points: list[int]) -> int:
    multiplicities = Counter(left + right for left in points for right in points)
    return sum(count * (multiplicities[total - 1] + count + multiplicities[total + 1]) for total, count in multiplicities.items())


def screen_specs() -> list[dict[str, Any]]:
    rows = []
    for spine_index, (s, n, v, w) in enumerate(primary_spine()):
        for pair_index, (coefficient, set_name) in enumerate(REGISTERED_PAIRS):
            index = len(rows)
            rows.append({
                "row_id": f"G1-S{index:03d}", "screen_index": index,
                "spine_index": spine_index, "pair_index": pair_index,
                "coefficient": coefficient, "set": set_name,
                "local": {"s": q(s), "n": q(n), "v": q(v), "w": q(w)},
                "w": w,
            })
    require(len(rows) == 588, "screen row count changed")
    return rows


def certificate() -> dict[str, Any]:
    hashes = {"preregistration": digest(PREREG), "conventions": digest(CONVENTIONS)}
    for label, expected in EXPECTED.items():
        require(hashes[label] == expected, "frozen hash mismatch: " + label)
    lower_log, upper_log = rational_log_3_over_2_bounds()
    rows = []
    for spec in screen_specs():
        points, parameters, failure = build_set(spec["set"], spec["w"], spec["screen_index"])
        base = {key: value for key, value in spec.items() if key != "w"}
        base["declared_energy_regime"] = regime(spec["set"])
        base["set_parameters"] = parameters
        if failure:
            rows.append({**base, "status": "FAILED", "failure_code": failure, "energy": None})
            continue
        require(points is not None, "successful construction returned no points")
        exact_energy = energy(points)
        exact_target = target(len(points), SCREEN_SCALE, regime(spec["set"]))
        quotient = Fraction(exact_energy, 1) / exact_target
        larger = max(quotient, 1 / quotient)
        # U^(1/400)=2^(3/100); hence this is exactly the squared-free test
        # larger > U^(1/400) iff larger^100 > 8.
        power = larger**100
        require(power > 8, "an energy row reaches the frozen retention band")
        rows.append({
            **base, "status": "COMPLETED", "failure_code": None,
            "energy": str(exact_energy), "target": q(exact_target),
            "energy_target_ratio": q(quotient),
            "symmetric_ratio_power_100": q(power),
            "strict_margin_over_8": q(power - 8),
            "rho_energy_retention": "REJECTED_EXACTLY",
        })
    feasible = [row for row in rows if row["status"] == "COMPLETED"]
    failed = [row for row in rows if row["status"] == "FAILED"]
    require(len(feasible) == 434 and len(failed) == 154, "frozen feasibility count mismatch")
    def parsed_fraction(text: str) -> Fraction:
        numerator, denominator = text.split("/", 1)
        return Fraction(int(numerator), int(denominator))

    closest = min(feasible, key=lambda row: parsed_fraction(row["symmetric_ratio_power_100"]))
    by_set: dict[str, dict[str, int]] = {}
    for name in sorted({row["set"] for row in rows}):
        relevant = [row for row in rows if row["set"] == name]
        by_set[name] = {"scheduled": len(relevant), "completed": sum(row["status"] == "COMPLETED" for row in relevant), "failed": sum(row["status"] == "FAILED" for row in relevant)}
    return {
        "artifact_id": "g1-energy-no-retention-audit-v1",
        "epistemic_status": "CERTIFIED_NUMERICAL",
        "claim_boundary": "Finite U=2^12 energy-screen certificate only. It does not evaluate complex values or prove an asymptotic extremizer, saturation theorem, density estimate, or G1 route decision.",
        "frozen_hashes": hashes,
        "exact_method": {
            "energy": "integer pair-sum multiplicities for |a+b-c-d|<=1",
            "energy_radius": "0",
            "threshold_equivalence": "rho_energy >= -1/400 iff max(E/Target,Target/E)^100 <= 8, since U=2^12",
            "comparison_margin": "strict_margin_over_8 in every completed row",
            "W5_step": {"value": 15, "status": "CERTIFIED_NUMERICAL", "log_3_over_2_lower": q(lower_log), "log_3_over_2_upper": q(upper_log), "pi_bounds": ["333/106", "355/113"]},
        },
        "summary": {
            "scheduled_rows": len(rows), "feasible_rows": len(feasible), "failed_rows": len(failed),
            "energy_retention_eligible_rows": 0,
            "conclusion": "Every feasible frozen screen row fails rho_energy >= -1/400 by an exact positive margin; therefore no row can pass the conjunctive G1 retention rule before complex-value evaluation.",
            "closest_to_energy_band": closest["row_id"],
            "closest_symmetric_ratio_power_100": closest["symmetric_ratio_power_100"],
            "closest_margin_over_8": closest["strict_margin_over_8"],
            "by_set": by_set,
        },
        "rows": rows,
        "falsifier": "Any differing frozen hash, invalid finite-set invariant, energy mismatch, threshold-equivalence error, or a completed row with symmetric_ratio_power_100 <= 8 refutes this finite certificate.",
        "replay": {"script_sha256": digest(Path(__file__)), "write_command": "python3 projects/guth-maynard-zero-density/proof/audit_g1_energy_no_retention_v1.py --write", "check_command": "python3 projects/guth-maynard-zero-density/proof/audit_g1_energy_no_retention_v1.py --check"},
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
        require(not OUTPUT.exists(), "refusing to overwrite energy audit artifact")
        OUTPUT.write_text(payload, encoding="utf-8")
    else:
        require(OUTPUT.is_file() and OUTPUT.read_text(encoding="utf-8") == payload, "G1 exact energy audit mismatch")
        print(json.dumps({"artifact": OUTPUT.name, "status": "ZERO_ENERGY_RETENTION_ROWS", "verified": True}, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1)
