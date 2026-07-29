"""Exact Phase-0 audit helpers for proposed 64-bit NTT primes."""

from __future__ import annotations

from math import prod


# Deterministic Miller--Rabin bases for unsigned 64-bit integers.
MILLER_RABIN_BASES_64 = (
    2,
    325,
    9375,
    28178,
    450775,
    9780504,
    1795265022,
)


def is_prime_u64(value: int) -> bool:
    """Deterministic primality test for 0 <= value < 2^64."""

    if not 0 <= value < 2**64:
        raise ValueError("value must fit in an unsigned 64-bit integer")
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    if value in small_primes:
        return True
    if value < 2 or any(value % prime == 0 for prime in small_primes):
        return False

    odd_part = value - 1
    exponent = 0
    while odd_part % 2 == 0:
        odd_part //= 2
        exponent += 1

    for base in MILLER_RABIN_BASES_64:
        if base % value == 0:
            continue
        witness = pow(base, odd_part, value)
        if witness in (1, value - 1):
            continue
        for _ in range(exponent - 1):
            witness = witness * witness % value
            if witness == value - 1:
                break
        else:
            return False
    return True


def audit_ntt_prime(
    prime: int,
    primitive_root: int,
    p_minus_one_factorization: dict[int, int],
) -> dict[str, object]:
    """Verify primality, factorization, root order, and 2-adic capacity."""

    if any(base < 2 or exponent < 1 for base, exponent in
           p_minus_one_factorization.items()):
        raise ValueError("factorization must use prime bases and exponents")
    if any(not is_prime_u64(base) for base in p_minus_one_factorization):
        raise ValueError("factorization contains a composite base")
    reconstructed = prod(
        base**exponent
        for base, exponent in p_minus_one_factorization.items()
    )
    if reconstructed != prime - 1:
        raise ValueError("factorization does not multiply to p-1")
    if not is_prime_u64(prime):
        raise ValueError("candidate modulus is not prime")
    if not 1 < primitive_root < prime:
        raise ValueError("primitive root is outside the valid range")

    root_checks = {
        str(divisor): pow(primitive_root, (prime - 1) // divisor, prime)
        for divisor in sorted(p_minus_one_factorization)
    }
    if any(value == 1 for value in root_checks.values()):
        raise ValueError("claimed primitive root has deficient order")
    two_adic_valuation = p_minus_one_factorization.get(2, 0)
    return {
        "tag": "VERIFIED",
        "prime": str(prime),
        "unsigned_64_bit": prime < 2**64,
        "signed_63_bit": prime < 2**63,
        "primality": "deterministic-Miller-Rabin-u64",
        "p_minus_one_factorization": {
            str(base): exponent
            for base, exponent in sorted(
                p_minus_one_factorization.items()
            )
        },
        "primitive_root": primitive_root,
        "primitive_root_order": str(prime - 1),
        "root_checks": root_checks,
        "two_adic_valuation": two_adic_valuation,
        "maximum_power_of_two_transform_length": str(
            2**two_adic_valuation
        ),
    }


def factor_integer(value: int) -> dict[int, int]:
    """Return an exact trial-division factorization for small cofactors."""

    if value < 1:
        raise ValueError("value must be positive")
    factors: dict[int, int] = {}
    divisor = 2
    remainder = value
    while divisor * divisor <= remainder:
        while remainder % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            remainder //= divisor
        divisor = 3 if divisor == 2 else divisor + 2
    if remainder > 1:
        factors[remainder] = factors.get(remainder, 0) + 1
    return factors


def primitive_root_prime(prime: int, factorization: dict[int, int]) -> int:
    """Find the least primitive root using the complete factorization."""

    if prod(q**e for q, e in factorization.items()) != prime - 1:
        raise ValueError("factorization does not multiply to p-1")
    for candidate in range(2, prime):
        if all(
            pow(candidate, (prime - 1) // q, prime) != 1
            for q in factorization
        ):
            return candidate
    raise ArithmeticError("primitive root search failed")


def generate_ntt_prime_schedule(
    count: int,
    *,
    coefficient_start: int = 2**30 - 1,
    power_of_two: int = 32,
) -> list[dict[str, object]]:
    """Generate a deterministic descending family p=c*2^k+1."""

    if count < 1:
        raise ValueError("count must be positive")
    if coefficient_start < 1 or power_of_two < 1:
        raise ValueError("invalid family parameters")
    schedule: list[dict[str, object]] = []
    coefficient = coefficient_start
    while coefficient >= 1 and len(schedule) < count:
        prime = coefficient * 2**power_of_two + 1
        if prime < 2**63 and is_prime_u64(prime):
            factorization = factor_integer(coefficient)
            factorization[2] = factorization.get(2, 0) + power_of_two
            root = primitive_root_prime(prime, factorization)
            audit = audit_ntt_prime(prime, root, factorization)
            audit["coefficient"] = coefficient
            audit["family"] = f"p=c*2^{power_of_two}+1"
            schedule.append(audit)
        coefficient -= 1
    if len(schedule) != count:
        raise ArithmeticError("prime schedule search exhausted")
    return schedule
