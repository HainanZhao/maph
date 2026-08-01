"""Exact source-support and weighted fractional-tensor conventions, Cycle 13."""
from __future__ import annotations

from fractions import Fraction
from math import floor


Q = Fraction
TOTAL_UNITS = 25
GRID_DENOMINATOR = 5
GRID_FACTOR_COUNTS = tuple(range(3, 11))
GRID_CAP = 250_000


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def source_support_rows() -> dict[str, object]:
    return {
        "prime_divisors_below_cutoff": [1],
        "mobius_sum": 1,
        "prime_coefficient": "exp(-p/T^(1/2)) != 0",
        "normalized_prime_coefficient": "(N/p)^sigma exp(-p/T^(1/2)) != 0",
        "fivefold_support_minimum": 2**5,
        "fivefold_coefficient_at_prime": 0,
        "conclusion": "A sum of fivefold convolutions whose factors are supported on integers >=2 cannot equal the full detector on any interval containing a prime above the cutoff.",
    }


def moment_rows(y: tuple[Fraction, ...], tau: Fraction) -> dict[str, Fraction]:
    require(y and all(value > 0 for value in y), "factor exponents must be positive")
    require(sum(y, Q(0)) == 5, "factor exponents must sum to five")
    require(tau >= 0, "tau must be nonnegative")
    threshold = Q(7, 2)
    tensor_power = 2 + tau
    local_rows = 24 - 2 * threshold * tensor_power
    baseline = Q(8)
    gain = baseline - local_rows
    delta_loss = 2 * tensor_power
    upper_bound = Q(2, 5)
    require(local_rows == 10 - 7 * tau, "local exponent identity mismatch")
    require(gain == 7 * tau - 2, "gain identity mismatch")
    return {
        "tau": tau,
        "tensor_power": tensor_power,
        "local_rows": local_rows,
        "gain": gain,
        "delta_loss": delta_loss,
        "universal_tau_upper_bound": upper_bound,
    }


def singleton_design(y: tuple[Fraction, ...]) -> dict[str, object]:
    require(y and all(value > 0 for value in y), "factor exponents must be positive")
    require(sum(y, Q(0)) == 5, "factor exponents must sum to five")
    if max(y) > 2:
        return {
            "factor_exponents": list(y),
            "admissible": False,
            "reason": "A coordinate with y_i>2 has k_i=0 in every admissible pattern, so no positive uniform tau exists.",
            "tau": Q(0),
            "q": [],
            "probabilities": [],
            "moments": moment_rows(y, Q(0)),
        }
    q = tuple(floor(Q(2, 1) / value) for value in y)
    require(all(value >= 1 for value in q), "singleton multiplicities must be positive")
    reciprocal_sum = sum((Q(1, value) for value in q), Q(0))
    tau = 1 / reciprocal_sum
    probabilities = tuple(tau / value for value in q)
    require(sum(probabilities, Q(0)) == 1, "singleton probabilities do not sum to one")
    expectations = tuple(probabilities[index] * q[index] for index in range(len(y)))
    require(all(value == tau for value in expectations), "singleton expected increments mismatch")
    extra_lengths = tuple(y[index] * q[index] for index in range(len(y)))
    require(all(value <= 2 for value in extra_lengths), "singleton pattern exceeds local length")
    return {
        "factor_exponents": list(y),
        "admissible": True,
        "q": list(q),
        "probabilities": list(probabilities),
        "expected_increments": list(expectations),
        "extra_lengths": list(extra_lengths),
        "tau": tau,
        "moments": moment_rows(y, tau),
    }


def _partitions(total: int, count: int, minimum: int = 1):
    if count == 1:
        if total >= minimum:
            yield (total,)
        return
    maximum = total // count
    for first in range(minimum, maximum + 1):
        for tail in _partitions(total - first, count - 1, first):
            yield (first,) + tail


def enumerate_grid() -> dict[str, object]:
    checked = 0
    admissible = 0
    strict_gain = 0
    equality = 0
    negative_gain = 0
    failed = 0
    best: tuple[Fraction, tuple[Fraction, ...]] | None = None
    weakest_positive: tuple[Fraction, tuple[Fraction, ...]] | None = None
    counts: dict[str, int] = {}
    for count in GRID_FACTOR_COUNTS:
        count_rows = 0
        for units in _partitions(TOTAL_UNITS, count):
            checked += 1
            count_rows += 1
            y = tuple(Q(value, GRID_DENOMINATOR) for value in units)
            row = singleton_design(y)
            if not row["admissible"]:
                failed += 1
                continue
            admissible += 1
            gain = row["moments"]["gain"]
            if gain > 0:
                strict_gain += 1
                if best is None or gain > best[0]:
                    best = (gain, y)
                if weakest_positive is None or gain < weakest_positive[0]:
                    weakest_positive = (gain, y)
            elif gain == 0:
                equality += 1
            else:
                negative_gain += 1
        counts[str(count)] = count_rows
    require(checked < GRID_CAP, "registered grid cap exceeded")
    require(checked == admissible + failed, "grid accounting mismatch")
    require(best is not None and weakest_positive is not None, "grid lacks positive-gain cells")
    return {
        "checked": checked,
        "counts_by_factor_number": counts,
        "singleton_admissible": admissible,
        "strict_gain": strict_gain,
        "zero_gain": equality,
        "negative_gain": negative_gain,
        "singleton_failed": failed,
        "best_gain": best[0],
        "best_cell": list(best[1]),
        "weakest_positive_gain": weakest_positive[0],
        "weakest_positive_cell": list(weakest_positive[1]),
    }


def verify_all() -> dict[str, object]:
    balanced = singleton_design((Q(1),) * 5)
    require(balanced["q"] == [2] * 5, "balanced singleton multiplicities mismatch")
    require(balanced["tau"] == Q(2, 5), "balanced tau mismatch")
    require(balanced["moments"]["local_rows"] == Q(36, 5), "balanced local exponent mismatch")
    unbalanced = singleton_design((Q(1, 2), Q(1, 2), Q(1), Q(3, 2), Q(3, 2)))
    require(unbalanced["q"] == [4, 4, 2, 1, 1], "unbalanced singleton multiplicities mismatch")
    require(unbalanced["tau"] == Q(1, 3), "unbalanced tau mismatch")
    require(unbalanced["moments"]["local_rows"] == Q(23, 3), "unbalanced local exponent mismatch")
    rough = singleton_design((Q(1, 2), Q(1, 2), Q(1, 2), Q(1, 2), Q(3)))
    require(not rough["admissible"] and rough["tau"] == 0, "rough-cell failure mismatch")
    return {
        "source_support": source_support_rows(),
        "balanced": balanced,
        "registered_unbalanced": unbalanced,
        "registered_rough_failure": rough,
        "grid": enumerate_grid(),
    }
