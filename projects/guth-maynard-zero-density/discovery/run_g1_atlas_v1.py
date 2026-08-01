#!/usr/bin/env python3
"""Run the frozen Cycle-3 G1 discovery atlas (discovery only).

Claim boundary: this program evaluates the finite, preregistered G1 protocol.
It does not prove a large-values estimate, zero-density estimate, short-
interval result, extremizer, or saturation theorem.  Complex observations are
``RECOGNIZED``; exact formula substitutions are merely a pinned structural
map.  This module imports no code from ``proof/``.

The default action is a no-experiment integrity check.  ``--run-full`` is an
explicit, potentially long-running action and is intentionally never implicit.
"""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import platform
import resource
import sys
import time
from typing import Any, Iterable

import mpmath

# Permit both documented invocations from the repository root and direct
# invocation while retaining a single project-local conventions source.
PROJECT_IMPORT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_IMPORT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_IMPORT_ROOT))

from conventions.g1_atlas_v1 import (
    BASE_SEED,
    COEFFICIENT_FAMILIES,
    COEFFICIENT_XOR,
    MASK64,
    PRECISIONS_BITS,
    REGISTERED_PAIRS,
    SCREEN_SCALE,
    SET_FAMILIES,
    SET_XOR,
    SPLITMIX64_GAMMA,
    SPLITMIX64_MUL1,
    SPLITMIX64_MUL2,
    VALIDATION_SCALES,
    energy_regime,
    local_n_grid,
    local_s_grid,
    local_v_grid,
    local_w_grid,
    primary_spine,
    q,
)


ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "artifacts/cycle-3-g1-atlas-preregistration-v1.json"
PREREG_DOCUMENT = ROOT / "docs/cycle-3-g1-atlas-preregistration-v1.md"
DEFAULT_OBSERVATIONS = ROOT / "artifacts/cycle-3-g1-atlas-observations-v1.json"
DEFAULT_PERFORMANCE = ROOT / "artifacts/cycle-3-g1-atlas-performance-v1.json"

# These are direct pins, not merely values read from a potentially replaced
# preregistration record.  They match the sealed v1 artifact and the primary
# source identities recorded there.
PREREG_ARTIFACT_SHA256 = "227ec1c66b2e109653354b6c3245b4e809fe52692c01514ac10064c23db2b6f8"
PREREG_DOCUMENT_SHA256 = "0510bb5ced5b3a5fd4377dea57216b226b58b49158ad6ddb6185775c967bfd72"
GM_TEX_PATH = ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex"
GM_TEX_SHA256 = "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"
GM_TAR_PATH = ROOT / "artifacts/sources/arxiv-2405.20552v2.tar"
GM_TAR_SHA256 = "9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc"

ROW_SECONDS_CAP = 180
ROW_RSS_CAP = 2 * 1024 * 1024 * 1024
MAX_FINITE_ROWS = 660
AGGREGATE_CPU_CAP_SECONDS = 128 * 60 * 60
RHO_MIN = Fraction(-1, 400)
PRECISION_DISAGREEMENT_MAX = Fraction(1, 1600)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def require(condition: bool, message: str) -> None:
    """Optimization-safe invariant guard for sealed discovery inputs."""
    if not condition:
        raise RuntimeError(message)


def fraction_from_text(value: str) -> Fraction:
    numerator, denominator = value.split("/", 1)
    return Fraction(int(numerator), int(denominator))


def integer_nth_root_floor(value: int, degree: int) -> int:
    """Exact floor(value**(1/degree)), without a float conversion."""
    if value < 0 or degree < 1:
        raise ValueError("invalid integer-root arguments")
    if value < 2 or degree == 1:
        return value
    lo, hi = 1, 1
    while hi**degree <= value:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid**degree <= value:
            lo = mid
        else:
            hi = mid
    return lo


def floor_rational_power(base: int, exponent: Fraction) -> int:
    """Exact floor(base**exponent) for a nonnegative rational exponent."""
    if base < 1 or exponent < 0:
        raise ValueError("base must be positive and exponent nonnegative")
    return integer_nth_root_floor(base**exponent.numerator, exponent.denominator)


class SplitMix64:
    """Reference unsigned-64 SplitMix64 stream with explicit wraparound."""

    def __init__(self, seed: int) -> None:
        self.state = seed & MASK64

    def next_u64(self) -> int:
        self.state = (self.state + SPLITMIX64_GAMMA) & MASK64
        z = self.state
        z = ((z ^ (z >> 30)) * SPLITMIX64_MUL1) & MASK64
        z = ((z ^ (z >> 27)) * SPLITMIX64_MUL2) & MASK64
        return (z ^ (z >> 31)) & MASK64


def stream_seed(tag: int, row_number: int) -> int:
    """Pinned independent stream convention: seed XOR tag XOR screen index."""
    if row_number < 0:
        raise ValueError("screen row number must be nonnegative")
    return (BASE_SEED ^ tag ^ row_number) & MASK64


def text_fraction_map(values: dict[str, Fraction]) -> dict[str, str]:
    return {key: q(value) for key, value in values.items()}


def complete_tie_set(values: dict[str, Fraction], target: Fraction) -> list[str]:
    return [key for key, value in values.items() if value == target]


def local_activity(s: Fraction, n: Fraction, v: Fraction, w: Fraction) -> dict[str, Any]:
    """Exact source-formula substitution only; no numerical experiment."""
    one = Fraction(1)
    a_terms = {
        "A1": 2 * n * (one - v),
        "A2": n * (Fraction(18, 5) - 4 * v),
        "A3": one + n * (Fraction(12, 5) - 4 * v),
    }
    g = max(a_terms.values())
    c_terms = {
        "C1": 2 * n * (one - v),
        "C2": one + n * (one - 2 * v),
        "C3": one + n * (4 - 6 * v),
    }
    c_inner = min(c_terms["C2"], c_terms["C3"])
    c_outer = max(c_terms["C1"], c_inner)
    residuals = {
        "A1-A2": a_terms["A1"] - a_terms["A2"],
        "A1-A3": a_terms["A1"] - a_terms["A3"],
        "A2-A3": a_terms["A2"] - a_terms["A3"],
        "C1-C2": c_terms["C1"] - c_terms["C2"],
        "C1-C3": c_terms["C1"] - c_terms["C3"],
        "C2-C3": c_terms["C2"] - c_terms["C3"],
        "C-G": c_outer - g,
    }
    result: dict[str, Any] = {
        "epistemic_status": "PROVED",
        "claim_boundary": "Exact substitution of frozen displayed source formulas; not a new large-values inequality.",
        "coordinates": {"s": q(s), "n": q(n), "v": q(v), "w": q(w)},
        "large_values": {
            "terms": text_fraction_map(a_terms), "G": q(g),
            "active_terms": complete_tie_set(a_terms, g),
        },
        "classical": {
            "terms": text_fraction_map(c_terms), "inner_min": q(c_inner),
            "inner_active_terms": complete_tie_set({"C2": c_terms["C2"], "C3": c_terms["C3"]}, c_inner),
            "C": q(c_outer),
            "outer_active_terms": [
                *(["C1"] if c_terms["C1"] == c_outer else []),
                *(["min(C2,C3)"] if c_inner == c_outer else []),
            ],
            "Delta_LV": q(c_outer - g),
        },
        "signed_residuals": text_fraction_map(residuals),
        "energy_eligible": v == s,
        "energy": None,
    }
    if v == s:
        e_terms = {
            "E1": w + n * (4 - 4 * s),
            "E2": Fraction(21, 8) * w + Fraction(1, 4) + n * (1 - 2 * s),
            "E3": 3 * w + n * (1 - 2 * s),
        }
        e_max = max(e_terms.values())
        result["energy"] = {
            "terms": text_fraction_map(e_terms), "maximum": q(e_max),
            "active_terms": complete_tie_set(e_terms, e_max),
            "signed_residuals": text_fraction_map({
                "E1-E2": e_terms["E1"] - e_terms["E2"],
                "E1-E3": e_terms["E1"] - e_terms["E3"],
                "E2-E3": e_terms["E2"] - e_terms["E3"],
            }),
        }
    return result


def transfer_activity(s: Fraction, n0: Fraction) -> dict[str, Any]:
    """Exact finite transfer-chart record, separate from the local chart."""
    one = Fraction(1)
    ell = Fraction(10, 1) / (6 + 10 * s)
    upper = Fraction(15, 1) / (6 + 10 * s)
    d = Fraction(18, 5) - 4 * s
    b = 15 * (one - s) / (3 + 5 * s)
    alpha = b / d
    quotient = ell / n0
    k = -(-quotient.numerator // quotient.denominator) if n0 <= ell / 2 else 2
    value_q = k * n0
    provenance = "ASYMPTOTIC_ENDPOINT_ONLY" if n0 == Fraction(1, 2) else "EXACT_POWER_SCALE"
    gm_terms = {
        "T1": 2 * value_q * (one - s),
        "T2": d * value_q,
        "T3": one + (Fraction(12, 5) - 4 * s) * value_q,
    }
    mvt_terms = {
        "M1": 2 * value_q * (one - s),
        "M2": one + (one - 2 * s) * value_q,
    }
    branch = "q<=alpha" if value_q <= alpha else "q>alpha"
    return {
        "epistemic_status": "PROVED",
        "claim_boundary": "Exact source-transfer formula substitution; not a new zero-density result.",
        "s": q(s), "n0": q(n0), "k": k, "q": q(value_q),
        "ell": q(ell), "u": q(upper), "alpha": q(alpha), "B": q(b),
        "provenance": provenance, "branch": branch,
        "containment": {
            "k_in_range": 1 <= k <= 77,
            "q_ge_ell": value_q >= ell,
            "q_le_u_exact": value_q <= upper if provenance == "EXACT_POWER_SCALE" else None,
            "q_le_u_asymptotic_only": provenance == "ASYMPTOTIC_ENDPOINT_ONLY",
        },
        "source_term_exponents": {
            "gm": text_fraction_map(gm_terms), "mvt": text_fraction_map(mvt_terms),
            "selected": "gm" if branch == "q<=alpha" else "mvt",
        },
        "residual_against_B": {
            "gm": text_fraction_map({key: b - value for key, value in gm_terms.items()}),
            "mvt": text_fraction_map({key: b - value for key, value in mvt_terms.items()}),
        },
    }


def transfer_grid() -> list[dict[str, Any]]:
    rows = []
    for s in local_s_grid():
        ell = Fraction(10, 1) / (6 + 10 * s)
        n0s = {Fraction(j, 100) for j in range(2, 51)} | {Fraction(5, 13), ell / 2}
        for n0 in sorted(n0s):
            rows.append(transfer_activity(s, n0))
    require(any(row["s"] == "7/10" and row["n0"] == "5/13" and row["k"] == 2 and row["q"] == "10/13" for row in rows), "frozen transfer anchor is absent")
    return rows


def structural_local_rows() -> list[dict[str, Any]]:
    rows = [
        local_activity(s, n, v, w)
        for s in local_s_grid()
        for n in local_n_grid()
        for v in local_v_grid()
        for w in local_w_grid()
    ]
    require(len(rows) == 7744, "frozen local atlas count is not 7744")
    anchor = next(row for row in rows if row["coordinates"] == {"s": "7/10", "n": "5/6", "v": "7/10", "w": "2/3"})
    require(bool(anchor["energy"]) and anchor["energy"]["terms"] == {"E1": "5/3", "E2": "5/3", "E3": "5/3"}, "frozen local energy anchor mismatch")
    return rows


def canonical_screen_specs() -> list[dict[str, Any]]:
    """Enumerate the 588 finite experiments in frozen spine/pair order."""
    specs = []
    for spine_index, (s, n, v, w) in enumerate(primary_spine()):
        for pair_index, (coefficient, set_family) in enumerate(REGISTERED_PAIRS):
            index = len(specs)
            specs.append({
                "screen_index": index,
                "spine_index": spine_index,
                "pair_index": pair_index,
                "row_id": f"G1-S{index:03d}",
                "local": {"s": s, "n": n, "v": v, "w": w},
                "coefficient": coefficient,
                "set": set_family,
            })
    require(len(specs) == 588, "frozen screen count is not 588")
    require(len({spec["row_id"] for spec in specs}) == 588, "frozen screen row IDs are not unique")
    return specs


def check_set_invariants(points: list[int], U: int, M: int) -> str | None:
    if len(points) != M:
        return "CARDINALITY_MISMATCH"
    if points != sorted(points) or len(set(points)) != len(points):
        return "SET_NOT_INCREASING_DISTINCT"
    if any(point < 0 or point > U for point in points):
        return "SET_OUT_OF_RANGE"
    if any(right - left < 1 for left, right in zip(points, points[1:])):
        return "SPACING_VIOLATION"
    return None


def sidon_points(U: int, M: int) -> list[int] | None:
    """The declared greedy >1-separated unordered-pair-sum construction."""
    points: list[int] = []
    pair_sums: list[int] = []
    for candidate in range(U + 1):
        new_sums = [candidate + point for point in points] + [2 * candidate]
        # This is deliberately the literal preregistered one-step test:
        # every *new* unordered sum is compared to every previously retained
        # sum.  It does not silently strengthen the finite construction by a
        # post-hoc new-versus-new condition.
        if any(abs(new_sum - old_sum) <= 1 for new_sum in new_sums for old_sum in pair_sums):
            continue
        points.append(candidate)
        pair_sums.extend(new_sums)
        if len(points) == M:
            return points
    return None


def mpmath_rational_step(U: int) -> tuple[int, bool]:
    """Evaluate W5's half-up logarithmic step at two frozen precisions."""
    Q = 1
    while Q**3 < U:
        Q += 1
    values = []
    for bits in PRECISIONS_BITS:
        with mpmath.workprec(bits):
            r = mpmath.mpf(Q + 8) / Q
            step = int(mpmath.floor(2 * mpmath.pi / abs(mpmath.log(r)) + mpmath.mpf("0.5")))
            values.append(step)
    return values[-1], values[0] == values[1]


def build_set(set_family: str, U: int, w: Fraction, row_number: int) -> tuple[list[int] | None, dict[str, Any], str | None]:
    """Build a frozen W and always return a retention-safe failure code."""
    M = floor_rational_power(U, w)
    metadata: dict[str, Any] = {"M": M, "construction": set_family}
    if set_family == "W0-sidon":
        if w != Fraction(1, 2):
            return None, metadata, "INFEASIBLE_CARDINALITY"
        points = sidon_points(U, M)
        if points is None:
            return None, metadata, "INFEASIBLE_CARDINALITY"
    elif set_family == "W1-uniform":
        generator = SplitMix64(stream_seed(SET_XOR, row_number))
        seen: set[int] = set()
        limit = 100 * (U + 1)
        draws = 0
        while len(seen) < M and draws < limit:
            seen.add(generator.next_u64() % (U + 1))
            draws += 1
        metadata.update({"draws": draws, "draw_cap": limit})
        if len(seen) != M:
            return None, metadata, "SET_DRAW_LIMIT"
        points = sorted(seen)
    elif set_family == "W2-jitter":
        generator = SplitMix64(stream_seed(SET_XOR, row_number))
        occupied: set[int] = set()
        points_unsorted: list[int] = []
        for j in range(M):
            candidate = (j * (U + 1)) // M + int(generator.next_u64() % 3) - 1
            candidate = min(U, max(0, candidate))
            chosen = None
            for point in list(range(candidate, U + 1)) + list(range(0, candidate)):
                if point not in occupied:
                    chosen = point
                    break
            if chosen is None:
                return None, metadata, "INFEASIBLE_CARDINALITY"
            occupied.add(chosen)
            points_unsorted.append(chosen)
        points = sorted(points_unsorted)
    elif set_family == "W3-AP":
        a = U // 7
        h = max(1, (U - 2 * a) // max(1, M - 1))
        points = [a + j * h for j in range(M)]
        metadata.update({"a": a, "h": h})
        if points and points[-1] > U:
            return None, metadata, "INFEASIBLE_CARDINALITY"
    elif set_family == "W4-four-block":
        r = (M + 3) // 4
        h = max(1, U // (32 * r))
        points_unsorted = []
        for block in range(4):
            origin = ((2 * block + 1) * U) // 8
            for j in range(r):
                candidate = origin + j * h
                if 0 <= candidate <= U and candidate not in points_unsorted:
                    points_unsorted.append(candidate)
                if len(points_unsorted) == M:
                    break
            if len(points_unsorted) == M:
                break
        metadata.update({"r": r, "h": h})
        if len(points_unsorted) != M:
            return None, metadata, "INFEASIBLE_CARDINALITY"
        points = sorted(points_unsorted)
    elif set_family == "W5-rational":
        h, precision_agrees = mpmath_rational_step(U)
        metadata.update({"h": h, "construction_precision_agrees": precision_agrees})
        if not precision_agrees:
            return None, metadata, "SET_CONSTRUCTION_PRECISION_DISAGREEMENT"
        a = (U - (M - 1) * h) // 2
        metadata["a"] = a
        if a < 0:
            return None, metadata, "INFEASIBLE_CARDINALITY"
        points = [a + j * h for j in range(M)]
    else:
        raise ValueError(f"unknown set family: {set_family}")
    invariant_failure = check_set_invariants(points, U, M)
    return (None, metadata, invariant_failure) if invariant_failure else (points, metadata, None)


@dataclass(frozen=True)
class CoefficientData:
    family: str
    L: int
    symbols: tuple[tuple[int, Any], ...]
    definition: dict[str, Any]

    @property
    def hash(self) -> str:
        return sha256_bytes(canonical_json({"family": self.family, "L": self.L, "symbols": self.symbols, "definition": self.definition}).encode())


def rational_symbol(value: Fraction) -> tuple[int, int]:
    return value.numerator, value.denominator


def build_coefficients(family: str, L: int, v: Fraction, row_number: int, t0: int | None) -> tuple[CoefficientData | None, str | None]:
    """Return symbolic coefficient specifications, never platform complex bytes."""
    H = max(1, floor_rational_power(L, v))
    indices = range(L + 1, 2 * L + 1)
    definition: dict[str, Any] = {"family": family, "L": L, "H": H}
    symbols: list[tuple[int, Any]] = []
    if family == "C0-flat":
        symbols = [(m, (1, 1)) for m in indices]
    elif family == "C1-tent":
        centre = L + L // 2
        definition["centre"] = centre
        for m in indices:
            value = max(Fraction(0), Fraction(1) - Fraction(abs(m - centre), H))
            symbols.append((m, rational_symbol(value)))
    elif family == "C2-two-tent":
        c1, c2 = L + L // 3, L + (2 * L) // 3
        h = max(1, H // 8)
        definition.update({"c1": c1, "c2": c2, "h": h, "phases": [1, -1]})
        for m in indices:
            one = max(Fraction(0), Fraction(1) - Fraction(abs(m - c1), h))
            two = max(Fraction(0), Fraction(1) - Fraction(abs(m - c2), h))
            symbols.append((m, rational_symbol(one - two)))
    elif family == "C3-root-chirp":
        definition.update({"modulus": 509, "phase": "(m mod 509)^2 mod 509"})
        symbols = [(m, ((m % 509) ** 2) % 509) for m in indices]
    elif family == "C4-rademacher":
        generator = SplitMix64(stream_seed(COEFFICIENT_XOR, row_number))
        symbols = [(m, 1 if generator.next_u64() & 1 else -1) for m in indices]
    elif family == "C5-point-aligned":
        if t0 is None:
            return None, "COEFFICIENT_REQUIRES_POINT"
        definition["t0"] = t0
        symbols = [(m, -t0) for m in indices]
    else:
        raise ValueError(f"unknown coefficient family: {family}")
    data = CoefficientData(family=family, L=L, symbols=tuple(symbols), definition=definition)
    for _, symbol in data.symbols:
        if family in {"C0-flat", "C1-tent", "C2-two-tent"}:
            if abs(Fraction(symbol[0], symbol[1])) > 1:
                return None, "COEFFICIENT_LINF_VIOLATION"
        elif family == "C4-rademacher" and abs(symbol) != 1:
            return None, "COEFFICIENT_LINF_VIOLATION"
    return data, None


def coefficient_value(data: CoefficientData, symbol: Any, t: int) -> Any:
    # Caller establishes mpmath working precision.  The returned object is a
    # recognized numerical evaluation, never a serialization of a complex byte.
    if data.family in {"C0-flat", "C1-tent", "C2-two-tent"}:
        return mpmath.mpf(symbol[0]) / symbol[1]
    if data.family == "C3-root-chirp":
        return mpmath.expj(2 * mpmath.pi * symbol / 509)
    if data.family == "C4-rademacher":
        return mpmath.mpf(symbol)
    if data.family == "C5-point-aligned":
        # The symbol stores the exact integer phase multiplier -t0.
        # m is supplied by the evaluator; this branch is patched there.
        return symbol
    raise ValueError(data.family)


def evaluate_values(data: CoefficientData, points: list[int], bits: int, budget: "RowBudget") -> dict[str, Any]:
    """Independent fixed-precision complex pass over the frozen finite data."""
    with mpmath.workprec(bits):
        values = []
        for t_index, t in enumerate(points):
            total = mpmath.mpc(0)
            for m_index, (m, symbol) in enumerate(data.symbols):
                phase = mpmath.expj(t * mpmath.log(m))
                if data.family == "C5-point-aligned":
                    coefficient = mpmath.expj(symbol * mpmath.log(m))
                else:
                    coefficient = coefficient_value(data, symbol, t)
                total += coefficient * phase
                if (m_index & 255) == 0:
                    budget.check()
            magnitude = abs(total)
            if not mpmath.isfinite(magnitude):
                raise NonfiniteObservation("NONFINITE_COMPLEX_VALUE")
            values.append(magnitude)
            if (t_index & 15) == 0:
                budget.check()
        minimum, maximum = min(values), max(values)
        threshold = mpmath.power(data.L, budget.v)
        ratio = minimum / threshold
        if ratio <= 0 or not mpmath.isfinite(ratio):
            raise NonfiniteObservation("NONPOSITIVE_VALUE_RATIO")
        rho_value = mpmath.log(ratio) / mpmath.log(budget.U)
        if not mpmath.isfinite(rho_value):
            raise NonfiniteObservation("NONFINITE_RHO_VALUE")
        return {
            "precision_bits": bits,
            "minimum_abs_D": mp_text(minimum), "maximum_abs_D": mp_text(maximum),
            "threshold_L_to_v": mp_text(threshold), "minimum_ratio": mp_text(ratio),
            "rho_value": mp_text(rho_value), "_rho_value": rho_value,
        }


def mp_text(value: Any) -> str:
    """Fixed decimal rendering avoids host float conversion and locale effects."""
    # 384 bits provide about 115 decimal digits.  Retaining 112 digits makes
    # the quota ordering reproducible at the computation's meaningful
    # precision instead of reparsing a shortened display at mpmath defaults.
    return mpmath.nstr(value, n=112, strip_zeros=False)


class RowFailure(Exception):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(code)


class NonfiniteObservation(RowFailure):
    pass


@dataclass
class RowBudget:
    U: int
    v: Fraction
    started: float
    cpu_started: float
    seconds_cap: int = ROW_SECONDS_CAP
    rss_cap: int = ROW_RSS_CAP

    def rss_bytes(self) -> int:
        # Linux ru_maxrss is KiB; this repository's frozen host is Linux.  The
        # diagnostic is intentionally separate from timing-independent output.
        return int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * 1024

    def check(self) -> None:
        if time.monotonic() - self.started > self.seconds_cap:
            raise RowFailure("RESOURCE_TIMEOUT")
        if self.rss_bytes() > self.rss_cap:
            raise RowFailure("RESOURCE_RSS_EXCEEDED")

    def performance(self) -> dict[str, Any]:
        return {
            "wall_seconds": time.monotonic() - self.started,
            "cpu_seconds": time.process_time() - self.cpu_started,
            "peak_rss_bytes": self.rss_bytes(),
        }


def exact_energy(points: list[int], budget: RowBudget) -> int:
    """Exact integer enumeration of |a+b-c-d|<=1 using pair-sum multiplicities."""
    multiplicities = Counter()
    for left_index, left in enumerate(points):
        for right in points:
            multiplicities[left + right] += 1
        if (left_index & 63) == 0:
            budget.check()
    energy = sum(count * (multiplicities[total - 1] + count + multiplicities[total + 1]) for total, count in multiplicities.items())
    return int(energy)


def energy_target(M: int, U: int, regime: str) -> Fraction:
    if regime == "low":
        return Fraction(M * M)
    if regime == "intermediate":
        return max(Fraction(M * M), Fraction(M**4, U))
    if regime == "high":
        return Fraction(M**3)
    raise ValueError(regime)


def exact_energy_record(energy: int, target: Fraction) -> dict[str, Any]:
    difference = Fraction(energy) - target
    return {
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Exact integer output of one discovery implementation; not independently certified per row and not a theorem.",
        "value": str(energy), "enumeration": "pair-sum multiplicities for |a+b-c-d|<=1",
        "radius": "0", "target": q(target), "target_difference": q(difference),
    }


def rho_energy(energy: int, target: Fraction, U: int, bits: int) -> Any:
    with mpmath.workprec(bits):
        quotient = mpmath.mpf(energy) / (mpmath.mpf(target.numerator) / target.denominator)
        value = -abs(mpmath.log(quotient) / mpmath.log(U))
        if not mpmath.isfinite(value):
            raise NonfiniteObservation("NONFINITE_RHO_ENERGY")
        return value


def local_from_spec(spec: dict[str, Any]) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    local = spec["local"]
    return local["s"], local["n"], local["v"], local["w"]


def serial_local(s: Fraction, n: Fraction, v: Fraction, w: Fraction) -> dict[str, str]:
    return {"s": q(s), "n": q(n), "v": q(v), "w": q(w)}


def failed_screen_row(spec: dict[str, Any], U: int, code: str, detail: dict[str, Any], *, scale_label: str) -> dict[str, Any]:
    s, n, v, w = local_from_spec(spec)
    return {
        "row_id": spec["row_id"], "screen_index": spec["screen_index"],
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Failed or infeasible discovery row retained under the frozen no-retry rule; no mathematical conclusion.",
        "chart": {"local": serial_local(s, n, v, w)},
        "family": {"coefficient": spec["coefficient"], "set": spec["set"], "declared_energy_regime": energy_regime(spec["set"])},
        "scale": scale_label, "status": "FAILED", "retention": {"eligible": False, "reason": code},
        "failure": {"code": code, "detail": detail},
    }


def run_screen_row(spec: dict[str, Any], U: int = SCREEN_SCALE, *, scale_label: str | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    """Evaluate exactly one frozen finite row, preserving every failure state."""
    s, n, v, w = local_from_spec(spec)
    scale_label = scale_label or f"2^{U.bit_length() - 1}" if U and U & (U - 1) == 0 else str(U)
    started = time.monotonic()
    budget = RowBudget(U=U, v=v, started=started, cpu_started=time.process_time())
    try:
        L = floor_rational_power(U, n)
        points, set_parameters, set_failure = build_set(spec["set"], U, w, spec["screen_index"])
        budget.check()
        if set_failure:
            return failed_screen_row(spec, U, set_failure, {"set_parameters": set_parameters}, scale_label=scale_label), budget.performance()
        require(points is not None, "successful set build returned no point set")
        coefficient, coefficient_failure = build_coefficients(spec["coefficient"], L, v, spec["screen_index"], points[0] if points else None)
        if coefficient_failure:
            return failed_screen_row(spec, U, coefficient_failure, {"L": L, "set_parameters": set_parameters}, scale_label=scale_label), budget.performance()
        require(coefficient is not None, "successful coefficient build returned no data")
        energy = exact_energy(points, budget)
        target = energy_target(len(points), U, energy_regime(spec["set"]))
        evaluations = []
        rho_energies = []
        for bits in PRECISIONS_BITS:
            evaluation = evaluate_values(coefficient, points, bits, budget)
            rho_e = rho_energy(energy, target, U, bits)
            evaluation["rho_energy"] = mp_text(rho_e)
            evaluations.append(evaluation)
            rho_energies.append(rho_e)
        rho_values = [item.pop("_rho_value") for item in evaluations]
        value_disagreement = abs(rho_values[0] - rho_values[1])
        energy_disagreement = abs(rho_energies[0] - rho_energies[1])
        with mpmath.workprec(384):
            threshold = mpmath.mpf(PRECISION_DISAGREEMENT_MAX.numerator) / PRECISION_DISAGREEMENT_MAX.denominator
            rho_floor = mpmath.mpf(RHO_MIN.numerator) / RHO_MIN.denominator
            both_value = all(value >= rho_floor for value in rho_values)
            both_energy = all(value >= rho_floor for value in rho_energies)
            precision_agrees = value_disagreement <= threshold and energy_disagreement <= threshold
            eligible = bool(both_value and both_energy and precision_agrees)
            score = min(*rho_values, *rho_energies)
        min_spacing = min((right - left for left, right in zip(points, points[1:])), default=None)
        row = {
            "row_id": spec["row_id"], "screen_index": spec["screen_index"],
            "epistemic_status": "RECOGNIZED",
            "claim_boundary": "Finite fixed-precision complex experiment only; no theorem, extremizer, sharpness, or density improvement.",
            "chart": {"local": serial_local(s, n, v, w)},
            "family": {
                "coefficient": spec["coefficient"], "set": spec["set"],
                "declared_energy_regime": energy_regime(spec["set"]),
                "parameters": {**coefficient.definition, **set_parameters},
            },
            "scale": scale_label,
            "seed_streams": {
                "coefficient": f"0x{stream_seed(COEFFICIENT_XOR, spec['screen_index']):016x}",
                "set": f"0x{stream_seed(SET_XOR, spec['screen_index']):016x}",
            },
            "input_hashes": {
                "coefficient_spec_sha256": coefficient.hash,
                "set_points_sha256": sha256_bytes(canonical_json(points).encode()),
                "preregistration_sha256": sha256_path(PREREG),
            },
            "validity": {"coefficient_linf": True, "one_separated": True, "point_count": len(points), "minimum_spacing": min_spacing},
            "exact_observables": {"L": L, "M": len(points), "W": points, "energy": exact_energy_record(energy, target)},
            "recognized_observables": {"evaluations": evaluations},
            "activity_labels": local_activity(s, n, v, w),
            "status": "COMPLETED",
            "retention": {
                "eligible": eligible,
                "rho_value_min": "-1/400", "rho_energy_min": "-1/400",
                "precision_disagreement_max": "1/1600",
                "rho_value_disagreement": mp_text(value_disagreement),
                "rho_energy_disagreement": mp_text(energy_disagreement),
                "score": mp_text(score),
                "reason": "PENDING_GLOBAL_QUOTA" if eligible else "THRESHOLD_OR_PRECISION_FAILURE",
            },
            "failure": None,
        }
        return row, budget.performance()
    except RowFailure as exc:
        return failed_screen_row(spec, U, exc.code, {}, scale_label=scale_label), budget.performance()


def retention_selection(rows: Iterable[dict[str, Any]]) -> list[str]:
    """Apply the frozen 2-per-(regime, coefficient), then total-36 quota."""
    eligible = [row for row in rows if row["status"] == "COMPLETED" and row["retention"]["eligible"]]
    # Decimal parses the fixed 112-digit recorded score exactly.  The ranking
    # therefore does not depend on mpmath's process-global default precision.
    with localcontext() as context:
        context.prec = 128
        eligible.sort(key=lambda row: (-Decimal(row["retention"]["score"]), row["row_id"]))
    selected: list[str] = []
    quotas: Counter[tuple[str, str]] = Counter()
    for row in eligible:
        key = (row["family"]["declared_energy_regime"], row["family"]["coefficient"])
        if quotas[key] >= 2:
            row["retention"]["reason"] = "QUOTA_PER_REGIME_COEFFICIENT"
            continue
        if len(selected) >= 36:
            row["retention"]["reason"] = "QUOTA_TOTAL"
            continue
        quotas[key] += 1
        selected.append(row["row_id"])
        row["retention"]["reason"] = "RETAINED"
    return selected


def frozen_config() -> dict[str, Any]:
    require(sha256_path(PREREG) == PREREG_ARTIFACT_SHA256, "sealed G1 preregistration artifact hash mismatch")
    require(sha256_path(PREREG_DOCUMENT) == PREREG_DOCUMENT_SHA256, "sealed G1 preregistration document hash mismatch")
    require(sha256_path(GM_TEX_PATH) == GM_TEX_SHA256, "pinned Guth--Maynard TeX source hash mismatch")
    require(sha256_path(GM_TAR_PATH) == GM_TAR_SHA256, "pinned Guth--Maynard source tar hash mismatch")
    data = json.loads(PREREG.read_text(encoding="utf-8"))
    document_hash = sha256_path(PREREG_DOCUMENT)
    if data["document"]["sha256"] != document_hash or document_hash != PREREG_DOCUMENT_SHA256:
        raise ValueError("frozen G1 preregistration document hash mismatch")
    sources = data.get("sources", {})
    if sources.get("gm_tex", {}).get("sha256") != GM_TEX_SHA256 or sources.get("gm_tar", {}).get("sha256") != GM_TAR_SHA256:
        raise ValueError("frozen G1 preregistration source identities mismatch")
    if data["screen"]["expected_rows"] != 588 or data["local_grid"]["expected_rows"] != 7744:
        raise ValueError("frozen G1 row counts mismatch")
    if tuple(tuple(pair) for pair in data["screen"]["pairs"]) != REGISTERED_PAIRS:
        raise ValueError("registered pair ordering mismatch")
    return data


def integrity_report() -> dict[str, Any]:
    data = frozen_config()
    local_rows = structural_local_rows()
    transfers = transfer_grid()
    specs = canonical_screen_specs()
    require(len(local_rows) == data["local_grid"]["expected_rows"], "local atlas count disagrees with frozen artifact")
    require(len(specs) == data["screen"]["expected_rows"], "screen count disagrees with frozen artifact")
    return {
        "epistemic_status": "PROVED",
        "claim_boundary": "Exact integrity check of frozen finite protocol; it performs no complex G1 screen evaluation.",
        "frozen_preregistration_sha256": sha256_path(PREREG),
        "document_sha256": sha256_path(PREREG_DOCUMENT),
        "structural_local_rows": len(local_rows), "transfer_rows": len(transfers),
        "screen_rows": len(specs), "screen_first": specs[0]["row_id"], "screen_last": specs[-1]["row_id"],
        "mandatory_energy_anchor": next(row["energy"]["terms"] for row in local_rows if row["coordinates"] == {"s": "7/10", "n": "5/6", "v": "7/10", "w": "2/3"}),
    }


def build_observations(screen_rows: list[dict[str, Any]], validation_rows: list[dict[str, Any]], *, run_mode: str) -> dict[str, Any]:
    config = frozen_config()
    local_rows = structural_local_rows()
    transfer_rows = transfer_grid()
    selected = retention_selection(screen_rows)
    return {
        "artifact_id": "cycle-3-g1-atlas-observations-v1",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Timing-independent discovery record. Structural substitutions are exact; finite complex rows are RECOGNIZED. No entry is a theorem or a G1 route decision.",
        "frozen_before_discovery": config["frozen_before_discovery"],
        "preregistration": {
            "path": str(PREREG.relative_to(ROOT)), "sha256": sha256_path(PREREG),
            "document_sha256": sha256_path(PREREG_DOCUMENT),
        },
        "runtime": {"implementation": platform.python_implementation(), "python": platform.python_version(), "mpmath": mpmath.__version__, "precisions_bits": list(PRECISIONS_BITS)},
        "run_mode": run_mode,
        "structural": {"local_rows": local_rows, "transfer_rows": transfer_rows},
        "screen_rows": sorted(screen_rows, key=lambda row: row["screen_index"]),
        "retained_screen_row_ids": selected,
        "validation": {
            "status": "COMPLETED" if validation_rows else "NO_RETAINED_SCREEN_ROWS",
            "authorized_only_for_retained_rows": True,
            "scales": [f"2^{scale.bit_length() - 1}" for scale in VALIDATION_SCALES],
            "rows": validation_rows,
        },
    }


def write_json_new(path: Path, data: dict[str, Any]) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite existing discovery artifact: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def aggregate_cap_failure(spec: dict[str, Any], U: int, *, scale_label: str, cpu_seconds: float, finite_rows: int) -> tuple[dict[str, Any], dict[str, Any]]:
    return (
        failed_screen_row(spec, U, "RESOURCE_AGGREGATE_CPU_CAP", {"aggregate_cpu_seconds": cpu_seconds, "aggregate_cpu_cap_seconds": AGGREGATE_CPU_CAP_SECONDS, "finite_rows_started": finite_rows}, scale_label=scale_label),
        {"wall_seconds": 0.0, "cpu_seconds": 0.0, "peak_rss_bytes": int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * 1024},
    )


def compute_full() -> tuple[dict[str, Any], dict[str, Any]]:
    """Run phase 1 and the frozen retained-row replays, with hard accounting."""
    rows: list[dict[str, Any]] = []
    performance_rows: list[dict[str, Any]] = []
    specs = canonical_screen_specs()
    cpu_started = time.process_time()
    finite_rows_started = 0
    for spec in specs:
        cpu_used = time.process_time() - cpu_started
        if cpu_used >= AGGREGATE_CPU_CAP_SECONDS or finite_rows_started >= MAX_FINITE_ROWS:
            row, performance = aggregate_cap_failure(spec, SCREEN_SCALE, scale_label="2^12", cpu_seconds=cpu_used, finite_rows=finite_rows_started)
        else:
            finite_rows_started += 1
            row, performance = run_screen_row(spec)
        rows.append(row)
        performance_rows.append({"phase": "screen", "row_id": spec["row_id"], **performance})

    selected = retention_selection(rows)
    spec_by_id = {spec["row_id"]: spec for spec in specs}
    validation_rows: list[dict[str, Any]] = []
    for row_id in selected:
        for scale in VALIDATION_SCALES:
            spec = spec_by_id[row_id]
            cpu_used = time.process_time() - cpu_started
            label = f"2^{scale.bit_length() - 1}"
            if cpu_used >= AGGREGATE_CPU_CAP_SECONDS or finite_rows_started >= MAX_FINITE_ROWS:
                row, performance = aggregate_cap_failure(spec, scale, scale_label=label, cpu_seconds=cpu_used, finite_rows=finite_rows_started)
            else:
                finite_rows_started += 1
                row, performance = run_screen_row(spec, U=scale, scale_label=label)
            row["validation_of"] = row_id
            row["validation_scale"] = label
            validation_rows.append(row)
            performance_rows.append({"phase": "validation", "row_id": row_id, "scale": label, **performance})

    require(finite_rows_started <= MAX_FINITE_ROWS, "frozen G1 finite-row cap exceeded")
    observations = build_observations(rows, validation_rows, run_mode="FROZEN_588_SCREEN_AND_RETAINED_REPLAY")
    performance = {
        "artifact_id": "cycle-3-g1-atlas-performance-v1", "epistemic_status": "OBSERVED",
        "claim_boundary": "Host performance only; excluded from timing-independent discovery observations.",
        "row_count": len(performance_rows), "finite_rows_started": finite_rows_started,
        "aggregate_cpu_seconds": time.process_time() - cpu_started,
        "rows": performance_rows,
        "resource_caps": {
            "seconds_per_finite_row": ROW_SECONDS_CAP, "max_rss_bytes": ROW_RSS_CAP,
            "maximum_finite_rows": MAX_FINITE_ROWS, "aggregate_cpu_hours": 128,
            "aggregate_cpu_cap_seconds": AGGREGATE_CPU_CAP_SECONDS,
        },
    }
    return observations, performance


def run_full(write_path: Path, performance_path: Path | None) -> None:
    observations, performance = compute_full()
    write_json_new(write_path, observations)
    if performance_path:
        write_json_new(performance_path, performance)


def check_observations(path: Path) -> None:
    """Full deterministic replay: recompute screen plus retained replays."""
    observations, _ = compute_full()
    rendered = json.dumps(observations, sort_keys=True, indent=2) + "\n"
    if not path.is_file() or path.read_text(encoding="utf-8") != rendered:
        raise SystemExit(f"G1 observations mismatch: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check-integrity", action="store_true", help="exact protocol checks; no finite complex screen rows")
    action.add_argument("--run-row", type=int, metavar="INDEX", help="evaluate one frozen screen row and print it")
    action.add_argument("--run-full", action="store_true", help="explicitly evaluate all 588 frozen screen rows")
    action.add_argument("--check-observations", type=Path, metavar="PATH", help="full deterministic replay against an existing observations artifact")
    parser.add_argument("--write-observations", type=Path, help="new path for --run-full output")
    parser.add_argument("--write-performance", type=Path, help="new path for separate --run-full performance output")
    args = parser.parse_args()
    if args.check_integrity:
        if args.write_observations or args.write_performance:
            parser.error("write arguments require --run-full")
        print(json.dumps(integrity_report(), sort_keys=True))
        return 0
    if args.run_row is not None:
        if args.write_observations or args.write_performance:
            parser.error("write arguments require --run-full")
        specs = canonical_screen_specs()
        if not 0 <= args.run_row < len(specs):
            parser.error(f"row index must be in [0,{len(specs) - 1}]")
        row, performance = run_screen_row(specs[args.run_row])
        print(json.dumps({"row": row, "performance": performance}, sort_keys=True, indent=2))
        return 0
    if args.check_observations is not None:
        if args.write_observations or args.write_performance:
            parser.error("write arguments cannot accompany --check-observations")
        check_observations(args.check_observations)
        print(json.dumps({"artifact": str(args.check_observations), "replayed": True}, sort_keys=True))
        return 0
    if not args.write_observations:
        parser.error("--run-full requires --write-observations PATH")
    run_full(args.write_observations, args.write_performance)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
