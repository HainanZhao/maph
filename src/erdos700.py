"""Exact computations for Erdős Problem 700.

The optimized implementation never constructs a binomial coefficient.  A
small direct implementation is retained as an independent reference oracle.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import comb, gcd, isqrt


@dataclass(frozen=True)
class Minimum:
    """The value of f(n) and every k attaining it."""

    n: int
    value: int
    minimizers: tuple[int, ...]


@dataclass(frozen=True)
class SinglePrimeWitness:
    """A k for which the gcd for a squarefree triple is one prime."""

    target: int
    k: int
    multiplier: int


@dataclass(frozen=True)
class TripleAnalysis:
    """The reduced analysis of f(p*q*r) for distinct primes."""

    primes: tuple[int, int, int]
    value: int
    upper_bound: int
    witnesses: tuple[SinglePrimeWitness, ...]


@dataclass(frozen=True)
class NearMultipleAnalysis:
    """Analysis of f(M*(M-1)) when M-1 is prime."""

    multiple: int
    value: int
    witness_multipliers: tuple[int, ...]


@dataclass(frozen=True)
class LucasResidueBox:
    """Finite residue box encoding one full shifted Lucas condition."""

    prime: int
    modulus: int
    shifted_upper: int
    allowed_residue_count: int


@dataclass(frozen=True)
class DefectPort:
    """First shifted Lucas digit expressed through reciprocal defect."""

    prime: int
    exponent_twist: int
    upper_digit: int
    allowed_multiplier_residues: tuple[int, ...]


@dataclass(frozen=True)
class BlindSecondDigitPort:
    """Second shifted digit when the first upper digit is maximal."""

    prime: int
    quotient_residue: int
    upper_second_digit: int
    allowed_multiplier_residue_count: int


@dataclass(frozen=True)
class BoxWitnessSearch:
    """Result of enumerating the smallest finite Lucas residue box."""

    multiple: int
    required_primes: tuple[int, ...]
    pivot_prime: int
    box_size: int
    compatible_box_values: int
    candidate_multipliers_tested: int
    sieve_profile: tuple[tuple[int, int], ...]
    witness_multipliers: tuple[int, ...]
    complete: bool


def factorize(n: int) -> dict[int, int]:
    """Return the prime factorization of a positive integer."""
    if n < 1:
        raise ValueError("n must be positive")

    factors: dict[int, int] = {}
    while n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n //= 2

    divisor = 3
    while divisor <= isqrt(n):
        while n % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            n //= divisor
        divisor += 2

    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def reciprocal_defect(n: int) -> int:
    """Return rad(n) - sum(rad(n) // p for p dividing n).

    The reciprocal-prime sum is above 1 exactly when this integer is
    negative. It can never be zero for n > 1.
    """
    if n < 2:
        raise ValueError("n must be at least 2")
    primes = tuple(factorize(n))
    radical = 1
    for p in primes:
        radical *= p
    return radical - sum(radical // p for p in primes)


def factorial_valuation(n: int, p: int) -> int:
    """Return v_p(n!) for prime p using Legendre's formula."""
    if n < 0:
        raise ValueError("n must be nonnegative")
    if p < 2:
        raise ValueError("p must be at least 2")

    total = 0
    while n:
        n //= p
        total += n
    return total


def binomial_valuation(n: int, k: int, p: int) -> int:
    """Return v_p(binomial(n, k))."""
    if not 0 <= k <= n:
        raise ValueError("require 0 <= k <= n")
    return (
        factorial_valuation(n, p)
        - factorial_valuation(k, p)
        - factorial_valuation(n - k, p)
    )


def lucas_nonzero(n: int, k: int, p: int) -> bool:
    """Return whether binomial(n, k) is nonzero modulo prime p.

    Lucas's theorem says this holds exactly when every base-p digit of k is
    at most the corresponding digit of n.
    """
    if not 0 <= k <= n:
        raise ValueError("require 0 <= k <= n")
    if p < 2:
        raise ValueError("p must be at least 2")

    while n or k:
        if k % p > n % p:
            return False
        n //= p
        k //= p
    return True


def lucas_first_failure(n: int, k: int, p: int) -> int | None:
    """Return the least base-p digit where Lucas's criterion fails.

    Digit positions are zero-indexed. Return None when the binomial
    coefficient is nonzero modulo p.
    """
    if not 0 <= k <= n:
        raise ValueError("require 0 <= k <= n")
    if p < 2:
        raise ValueError("p must be at least 2")

    position = 0
    while n or k:
        if k % p > n % p:
            return position
        n //= p
        k //= p
        position += 1
    return None


def near_multiple_shifted_failure_depth(m: int, t: int, p: int) -> int | None:
    """Return the one-based shifted Lucas failure depth for M*(M-1), M*t.

    If p^a exactly divides M, the original Lucas comparison has a forced
    block of a trailing zeroes. The returned depth counts digits after that
    block. Return None when the full Lucas test is nonzero modulo p.
    """
    if m < 2:
        raise ValueError("m must be at least 2")
    if not 0 <= t <= m - 1:
        raise ValueError("require 0 <= t <= m - 1")
    factors = factorize(m)
    if p not in factors:
        raise ValueError("p must divide m")
    exponent = factors[p]
    position = lucas_first_failure(m * (m - 1), m * t, p)
    if position is None:
        return None
    return position - exponent + 1


def near_multiple_lucas_residue_box(m: int, p: int) -> LucasResidueBox:
    """Return the finite digit box for the base-p near-multiple condition."""
    if m < 2:
        raise ValueError("m must be at least 2")
    factors = factorize(m)
    if p not in factors:
        raise ValueError("p must divide m")

    prime_power = p ** factors[p]
    u = m // prime_power
    shifted_upper = u * (m - 1)
    modulus = 1
    while modulus <= shifted_upper:
        modulus *= p

    value = shifted_upper
    allowed_residue_count = 1
    while modulus > 1:
        allowed_residue_count *= value % p + 1
        value //= p
        modulus //= p

    # Reconstruct the least power of p larger than the shifted upper value.
    modulus = 1
    while modulus <= shifted_upper:
        modulus *= p
    return LucasResidueBox(
        prime=p,
        modulus=modulus,
        shifted_upper=shifted_upper,
        allowed_residue_count=allowed_residue_count,
    )


def near_multiple_defect_port(m: int, p: int) -> DefectPort:
    """Return the exact first shifted base-p condition from rad(m)'s defect.

    If p^a exactly divides m, R = rad(m), D = D(R), and
    c = m / (p^(a-1) R), then the shifted upper digit is c*D modulo p.
    The corresponding lower digit is -c*D*t modulo p.
    """
    if m < 2:
        raise ValueError("m must be at least 2")
    factors = factorize(m)
    if p not in factors:
        raise ValueError("p must divide m")

    radical = 1
    for q in factors:
        radical *= q
    exponent_twist = m // (p ** (factors[p] - 1) * radical)
    upper_digit = (exponent_twist * reciprocal_defect(radical)) % p
    if upper_digit == 0:
        raise AssertionError("the defect port must be nonzero")
    allowed = tuple(
        t
        for t in range(p)
        if (-upper_digit * t) % p <= upper_digit
    )
    return DefectPort(
        prime=p,
        exponent_twist=exponent_twist,
        upper_digit=upper_digit,
        allowed_multiplier_residues=allowed,
    )


def near_multiple_blind_second_digit_port(
    m: int, p: int
) -> BlindSecondDigitPort:
    """Return the second-digit filter when M/p^a is 1 modulo p."""
    if m < 2:
        raise ValueError("m must be at least 2")
    factors = factorize(m)
    if p not in factors:
        raise ValueError("p must divide m")

    exponent = factors[p]
    complement = m // (p**exponent)
    if complement % p != 1:
        raise ValueError("the first shifted digit is not blind")
    quotient_residue = ((complement - 1) // p) % p
    upper_second_digit = (
        -quotient_residue - 1 + int(exponent == 1)
    ) % p
    return BlindSecondDigitPort(
        prime=p,
        quotient_residue=quotient_residue,
        upper_second_digit=upper_second_digit,
        allowed_multiplier_residue_count=p * (upper_second_digit + 1),
    )


def search_near_multiple_via_smallest_box(
    m: int,
    max_box_size: int = 1_000_000,
    required_primes: tuple[int, ...] | None = None,
) -> BoxWitnessSearch:
    """Search common witnesses for selected prime bases via the smallest box.

    By default every prime divisor of m is required.  Otherwise,
    required_primes must be a nonempty collection of distinct prime divisors
    of m.  The result is complete exactly when the smallest selected box has
    at most max_box_size digit values.
    """
    if m < 4:
        raise ValueError("m must be at least 4")
    if max_box_size < 1:
        raise ValueError("max_box_size must be positive")

    factors = factorize(m)
    if required_primes is None:
        active_primes = tuple(factors)
    else:
        active_primes = tuple(sorted(required_primes))
        if not active_primes:
            raise ValueError("required_primes must be nonempty")
        if len(set(active_primes)) != len(active_primes):
            raise ValueError("required_primes must be distinct")
        if any(p not in factors for p in active_primes):
            raise ValueError("required_primes must divide m")

    boxes = {
        p: near_multiple_lucas_residue_box(m, p)
        for p in active_primes
    }
    pivot = min(boxes, key=lambda p: boxes[p].allowed_residue_count)
    box = boxes[pivot]
    if box.allowed_residue_count > max_box_size:
        return BoxWitnessSearch(
            multiple=m,
            required_primes=active_primes,
            pivot_prime=pivot,
            box_size=box.allowed_residue_count,
            compatible_box_values=0,
            candidate_multipliers_tested=0,
            sieve_profile=(),
            witness_multipliers=(),
            complete=False,
        )

    # Construct every number whose base-p digits lie below the corresponding
    # digits of the shifted upper argument. Zero digits do not expand the
    # working list, which keeps sparse boxes efficient even at large depth.
    digit_values = [0]
    remaining = box.shifted_upper
    place = 1
    while remaining:
        upper_digit = remaining % pivot
        if upper_digit:
            digit_values = [
                value + digit * place
                for value in digit_values
                for digit in range(upper_digit + 1)
            ]
        remaining //= pivot
        place *= pivot

    pivot_power = pivot ** factors[pivot]
    pivot_complement = m // pivot_power
    half = (m - 1) // 2
    tested = 0
    compatible = 0
    candidate_multipliers = []
    for lower_value in digit_values:
        if lower_value % pivot_complement:
            continue
        multiplier = lower_value // pivot_complement
        compatible += 1
        if not 1 <= multiplier <= half:
            continue
        tested += 1
        candidate_multipliers.append(multiplier)

    survivors = sorted(candidate_multipliers)
    sieve_profile = [(pivot, len(survivors))]
    for p in active_primes:
        if p == pivot:
            continue
        exponent = factors[p]
        complement = m // (p**exponent)
        shifted_upper = complement * (m - 1)
        survivors = [
            multiplier
            for multiplier in survivors
            if lucas_nonzero(
                shifted_upper,
                complement * multiplier,
                p,
            )
        ]
        sieve_profile.append((p, len(survivors)))

    return BoxWitnessSearch(
        multiple=m,
        required_primes=active_primes,
        pivot_prime=pivot,
        box_size=box.allowed_residue_count,
        compatible_box_values=compatible,
        candidate_multipliers_tested=tested,
        sieve_profile=tuple(sieve_profile),
        witness_multipliers=tuple(survivors),
        complete=True,
    )


def find_near_multiple_witness(
    m: int,
    required_primes: tuple[int, ...] | None = None,
    max_multiplier: int | None = None,
) -> int | None:
    """Return the first multiplier passing selected shifted Lucas tests.

    The search is exhaustive when max_multiplier is None or at least
    (m-1)//2.  A None result from a shorter search is therefore only
    inconclusive, while any returned multiplier is an exact certificate.
    """
    if m < 4:
        raise ValueError("m must be at least 4")
    factors = factorize(m)
    if required_primes is None:
        active_primes = tuple(factors)
    else:
        active_primes = tuple(sorted(required_primes))
        if not active_primes:
            raise ValueError("required_primes must be nonempty")
        if len(set(active_primes)) != len(active_primes):
            raise ValueError("required_primes must be distinct")
        if any(p not in factors for p in active_primes):
            raise ValueError("required_primes must divide m")
    if max_multiplier is not None and max_multiplier < 1:
        raise ValueError("max_multiplier must be positive")

    tests = []
    for p in active_primes:
        complement = m // (p ** factors[p])
        tests.append((complement * (m - 1), complement, p))

    half = (m - 1) // 2
    limit = half if max_multiplier is None else min(half, max_multiplier)
    for multiplier in range(1, limit + 1):
        if all(
            lucas_nonzero(upper, complement * multiplier, p)
            for upper, complement, p in tests
        ):
            return multiplier
    return None


def primary_pseudoperfect_candidates(m: int) -> tuple[int, ...]:
    """Return the only possible near-multiple witnesses for a primary
    pseudoperfect number m.

    Such an m satisfies 1 + sum(m // p for p | m) = m. Proposition 15
    shows that every multiplier passing Lucas's test for all p | m must be
    a subset sum of the distinct values m // p.
    """
    if m < 2:
        raise ValueError("m must be at least 2")
    factors = factorize(m)
    if any(exponent != 1 for exponent in factors.values()):
        raise ValueError("m is not primary pseudoperfect")
    summands = tuple(m // p for p in factors)
    if 1 + sum(summands) != m:
        raise ValueError("m is not primary pseudoperfect")

    candidates = {0}
    for summand in summands:
        candidates |= {value + summand for value in tuple(candidates)}
    return tuple(
        sorted(value for value in candidates if 1 <= value <= (m - 1) // 2)
    )


def binomial_gcd_from_factors(
    n: int, k: int, factors: dict[int, int] | None = None
) -> int:
    """Return gcd(n, binomial(n, k)) using only valuations."""
    if not 0 <= k <= n:
        raise ValueError("require 0 <= k <= n")
    if factors is None:
        factors = factorize(n)

    result = 1
    for p, exponent in factors.items():
        valuation = min(exponent, binomial_valuation(n, k, p))
        result *= p**valuation
    return result


def f_details(n: int) -> Minimum:
    """Compute f(n) and all minimizing k for n >= 4."""
    if n < 4:
        raise ValueError("n must be at least 4 so the admissible set is nonempty")

    factors = factorize(n)
    theoretical_floor = min(factors)
    best = n + 1
    minimizers: list[int] = []

    for k in range(2, n // 2 + 1):
        candidate = binomial_gcd_from_factors(n, k, factors)
        if candidate < best:
            best = candidate
            minimizers = [k]
        elif candidate == best:
            minimizers.append(k)

    # We deliberately do not stop when the theoretical floor is first reached:
    # callers use the complete set of minimizing k's for pattern discovery.
    assert best >= theoretical_floor
    return Minimum(n=n, value=best, minimizers=tuple(minimizers))


def f(n: int) -> int:
    """Compute f(n)."""
    return f_details(n).value


def f_direct(n: int) -> Minimum:
    """Slow reference implementation that constructs binomial coefficients."""
    if n < 4:
        raise ValueError("n must be at least 4 so the admissible set is nonempty")

    values = [(gcd(n, comb(n, k)), k) for k in range(2, n // 2 + 1)]
    best = min(value for value, _ in values)
    return Minimum(
        n=n,
        value=best,
        minimizers=tuple(k for value, k in values if value == best),
    )


def is_prime_power(n: int) -> bool:
    """Return whether n is a power of one prime."""
    return len(factorize(n)) == 1


def is_composite(n: int) -> bool:
    """Return whether n is composite."""
    if n < 4:
        return False
    factors = factorize(n)
    return sum(factors.values()) >= 2


def analyze_squarefree_triple(p: int, q: int, r: int) -> TripleAnalysis:
    """Analyze f(p*q*r) via the Lucas reduction for distinct primes.

    The witnesses returned are exactly the structured candidates at which
    the gcd is one prime. The search is O(p + q + r), rather than O(p*q*r).
    """
    primes = tuple(sorted((p, q, r)))
    if len(set(primes)) != 3 or any(factorize(s) != {s: 1} for s in primes):
        raise ValueError("p, q, r must be distinct primes")

    n = p * q * r
    upper_bound = primes[0] * primes[1]  # Witness k = largest prime.
    best = upper_bound
    witnesses: list[SinglePrimeWitness] = []

    for target in primes:
        other_primes = tuple(s for s in primes if s != target)
        complement = other_primes[0] * other_primes[1]
        for multiplier in range(1, target // 2 + 1):
            k = multiplier * complement
            if (
                not lucas_nonzero(n, k, target)
                and all(lucas_nonzero(n, k, s) for s in other_primes)
            ):
                best = min(best, target)
                witnesses.append(
                    SinglePrimeWitness(
                        target=target, k=k, multiplier=multiplier
                    )
                )
    return TripleAnalysis(
        primes=primes,
        value=best,
        upper_bound=upper_bound,
        witnesses=tuple(witnesses),
    )


def f_squarefree_triple(p: int, q: int, r: int) -> int:
    """Compute f(p*q*r) with the reduced squarefree-triple analyzer."""
    return analyze_squarefree_triple(p, q, r).value


def eligible_2qr_witnesses(q: int, r: int) -> tuple[SinglePrimeWitness, ...]:
    """Return every single-prime witness for 2*q*r when q < r < 2*q.

    This is the specialized criterion proved in the mathematical notes.
    A target-q witness is purely a binary submask condition. A target-r
    witness adds a Lucas condition modulo q.
    """
    if (
        factorize(q) != {q: 1}
        or factorize(r) != {r: 1}
        or not 2 < q < r < 2 * q
    ):
        raise ValueError("require odd primes q < r < 2*q")

    witnesses: list[SinglePrimeWitness] = []
    half_n = q * r

    # A gcd-q witness has k = 2*r*t. Lucas modulo r restricts the range.
    for multiplier in range(1, (2 * q - r) // 2 + 1):
        if lucas_nonzero(half_n, r * multiplier, 2):
            witnesses.append(
                SinglePrimeWitness(
                    target=q,
                    k=2 * r * multiplier,
                    multiplier=multiplier,
                )
            )

    # A gcd-r witness has k = 2*q*t. Divisibility modulo r is automatic;
    # nondivisibility modulo 2 and q gives the two tests below.
    for multiplier in range(1, r // 2 + 1):
        if lucas_nonzero(half_n, q * multiplier, 2) and lucas_nonzero(
            2 * r, 2 * multiplier, q
        ):
            witnesses.append(
                SinglePrimeWitness(
                    target=r,
                    k=2 * q * multiplier,
                    multiplier=multiplier,
                )
            )

    return tuple(witnesses)


def analyze_near_multiple(multiple: int) -> NearMultipleAnalysis:
    """Compute f(M*(M-1)) via Lucas checks when M-1 is prime.

    The value is necessarily either M or M-1. A witness multiplier t means
    k=M*t and gcd(M*(M-1), binomial(M*(M-1), k))=M-1.
    """
    if multiple < 4 or factorize(multiple - 1) != {multiple - 1: 1}:
        raise ValueError("require M >= 4 with M-1 prime")

    r = multiple - 1
    n = multiple * r
    prime_divisors = tuple(factorize(multiple))
    witnesses = []
    for multiplier in range(1, r // 2 + 1):
        k = multiple * multiplier
        if all(lucas_nonzero(n, k, p) for p in prime_divisors):
            witnesses.append(multiplier)

    return NearMultipleAnalysis(
        multiple=multiple,
        value=r if witnesses else multiple,
        witness_multipliers=tuple(witnesses),
    )
