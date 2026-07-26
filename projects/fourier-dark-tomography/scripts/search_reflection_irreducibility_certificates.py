#!/usr/bin/env python3
"""Search for additional finite-field certificates for Conjecture T3e.

This is intentionally separate from ``audit_reflection_irreducibility.py``:
the latter is the stable, recorded certificate checker, while this script is
an exploratory increasing-prime search.  A reported pair ``a: p`` means that
the conjecturally irreducible part of Q_a is irreducible in F_p[b], as checked
by the exact standard-library Rabin implementation in the audit script.

The search is rigorous when it reports a certificate, but failure to find a
prime below ``--prime-limit`` says nothing about irreducibility over Q.
"""

from __future__ import annotations

import argparse
from time import perf_counter

from audit_reflection_irreducibility import (
    conjecturally_irreducible_part,
    is_irreducible_mod_prime,
    reflection_integer_coefficients,
)


def primes_through(limit: int) -> list[int]:
    """Return all primes at most limit by an elementary sieve."""
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for candidate in range(2, int(limit**0.5) + 1):
        if sieve[candidate]:
            start = candidate * candidate
            count = (limit - start) // candidate + 1
            sieve[start : limit + 1 : candidate] = b"\x00" * count
    return [value for value in range(2, limit + 1) if sieve[value]]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-a", type=int, default=39)
    parser.add_argument("--max-a", type=int, default=50)
    parser.add_argument("--prime-limit", type=int, default=10_000)
    parser.add_argument(
        "--search-backend",
        choices=("stdlib", "sympy"),
        default="stdlib",
        help=(
            "use SymPy to search more quickly, then independently verify each "
            "reported certificate with the standard-library Rabin test"
        ),
    )
    args = parser.parse_args()

    if args.min_a < 2 or args.max_a < args.min_a:
        parser.error("require 2 <= --min-a <= --max-a")

    primes = primes_through(args.prime_limit)
    sympy_irreducible = None
    sympy_domain = None
    if args.search_backend == "sympy":
        try:
            from sympy.polys.domains import ZZ as sympy_domain
            from sympy.polys.galoistools import (
                gf_irreducible_p as sympy_irreducible,
            )
        except ImportError:
            parser.error("--search-backend sympy requires SymPy")
    total_start = perf_counter()
    certificates: dict[int, int] = {}

    for a in range(args.min_a, args.max_a + 1):
        row_start = perf_counter()
        residual = conjecturally_irreducible_part(
            a,
            reflection_integer_coefficients(a),
        )
        tested = 0
        certificate = None
        for prime in primes:
            tested += 1
            if sympy_irreducible is None:
                irreducible = is_irreducible_mod_prime(residual, prime)
            else:
                irreducible = sympy_irreducible(
                    list(reversed(residual)),
                    prime,
                    sympy_domain,
                )
            if irreducible:
                # The search backend is not part of the certificate: always
                # repeat the decisive positive test with the small independent
                # implementation used by the stable audit.
                if sympy_irreducible is not None and not is_irreducible_mod_prime(
                    residual,
                    prime,
                ):
                    raise AssertionError(
                        f"backends disagree for a={a}, p={prime}"
                    )
                certificate = prime
                certificates[a] = prime
                break
        elapsed = perf_counter() - row_start
        if certificate is None:
            print(
                f"a={a}: no certificate through p={args.prime_limit}; "
                f"tested={tested}; seconds={elapsed:.3f}",
                flush=True,
            )
        else:
            print(
                f"a={a}: p={certificate}; tested={tested}; "
                f"seconds={elapsed:.3f}",
                flush=True,
            )

    print(f"certificates={certificates}")
    print(f"total_seconds={perf_counter() - total_start:.3f}")


if __name__ == "__main__":
    main()
