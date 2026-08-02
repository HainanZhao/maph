"""Exact physical-row numerator-divisor incidence ledger for Cycle 176."""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction as Q
from math import gcd, isqrt


def divisor_count(value: int) -> int:
    if value == 0:
        raise ValueError("physical row cannot be zero")
    value = abs(value)
    total = 0
    for d in range(1, isqrt(value) + 1):
        if value % d == 0:
            total += 1 if d * d == value else 2
    return total


def row_ledger(incidences: tuple[tuple[int, int, int, int], ...]) -> dict[int, dict[str, object]]:
    """Rows are (h, state_id, numerator a, range_valid 0/1)."""
    rows: dict[int, list[tuple[int, int, bool]]] = defaultdict(list)
    for h, state, a, range_valid in incidences:
        if h == 0 or a <= 0 or range_valid not in (0, 1):
            raise ValueError("invalid complete incidence")
        rows[h].append((state, a, bool(range_valid)))
    result: dict[int, dict[str, object]] = {}
    for h, entries in rows.items():
        numerators = sorted({a for _, a, _ in entries})
        dividing = sorted(a for a in numerators if h % a == 0)
        eligible = [(state, a) for state, a, valid in entries if valid and h % a == 0]
        multiplicities = Counter(a for _, a, _ in entries)
        gcd_energy = sum(Q(gcd(a, b) ** 2, a * b) for a in numerators for b in numerators if a != b)
        result[h] = {
            "incidences": tuple(entries), "codegree": len(entries), "numerators": tuple(numerators),
            "distinct_numerators": len(numerators), "dividing_numerators": tuple(dividing),
            "eligible": tuple(eligible), "eligible_distinct": len({a for _, a in eligible}),
            "divisor_cap": divisor_count(h), "avoidance_distinct": len(numerators) - len(dividing),
            "multiplicities": dict(sorted(multiplicities.items())), "gcd_energy": gcd_energy,
        }
        if result[h]["eligible_distinct"] > result[h]["divisor_cap"]:
            raise RuntimeError("physical divisor cap")
    return result


def split_codegree(ledger: dict[int, dict[str, object]], threshold: int) -> dict[str, tuple[int, ...]]:
    if threshold < 2:
        raise ValueError("frozen reuse threshold must be at least two")
    low = tuple(sorted(h for h, data in ledger.items() if int(data["codegree"]) < threshold))
    high = tuple(sorted(h for h, data in ledger.items() if int(data["codegree"]) >= threshold))
    if set(low) & set(high) or len(low) + len(high) != len(ledger):
        raise RuntimeError("codegree partition")
    return {"low_reuse": low, "high_reuse": high}


def verify_all() -> dict[str, object]:
    ledger = row_ledger(((60, 1, 2, 1), (60, 2, 3, 1), (60, 3, 5, 1), (60, 4, 7, 1), (60, 5, 7, 1), (77, 6, 2, 1)))
    h60 = ledger[60]
    if h60["divisor_cap"] != 12 or h60["dividing_numerators"] != (2, 3, 5):
        raise RuntimeError("divisor incidence")
    if h60["eligible"] != ((1, 2), (2, 3), (3, 5)) or h60["avoidance_distinct"] != 1:
        raise RuntimeError("eligible/avoidance split")
    split = split_codegree(ledger, 2)
    if split != {"low_reuse": (77,), "high_reuse": (60,)}:
        raise RuntimeError("physical support split")
    # Disjoint physical supports show state totals alone cannot force reuse.
    disjoint = row_ledger(tuple((101 + 2*i, i, 2, 1) for i in range(1, 8)))
    if any(data["codegree"] != 1 for data in disjoint.values()):
        raise RuntimeError("disjoint-support countermodel")
    return {
        "physical_divisibility": "at fixed nonzero h, integrality is exactly a|h; eligible distinct numerators are at most tau(|h|)",
        "high_reuse": "each high-reuse row retains numerator multiplicities, divisor-eligible groups, distinct numerator avoidance, and gcd energy",
        "support_separation": "low-reuse rows are a labelled physical-support-separation bank",
        "countermodel": "arbitrarily many states can have disjoint physical h supports, so state mass alone cannot force an aggregate covering principle",
        "boundary": "This is a finite physical-row modular-web classifier. It proves no actual row-reuse lower bound, eligible mass, target packet, recurrence, density, or interval gain.",
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
