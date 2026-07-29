#!/usr/bin/env python3
"""Deterministically generate the complete production NTT-prime schedule."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import gcd
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.ntt_prime import factor_integer, generate_ntt_prime_schedule


WORK_PRIMES = 3738
OVERFLOW_PRIMES = 2
TOTAL_PRIMES = WORK_PRIMES + OVERFLOW_PRIMES
OUTPUT = ROOT / "data" / "primes-schedule-v1.json"


def factor_map(value: int) -> dict[str, int]:
    return {
        str(prime): exponent
        for prime, exponent in sorted(factor_integer(value).items())
    }


def certificate(index: int, generated: dict[str, object]) -> dict:
    prime = int(generated["prime"])
    coefficient = int(generated["coefficient"])
    witness = int(generated["primitive_root"])
    coefficient_factors = factor_integer(coefficient)
    p_minus_one_factors = coefficient_factors.copy()
    p_minus_one_factors[2] = p_minus_one_factors.get(2, 0) + 32
    divisors = []
    for divisor in sorted(p_minus_one_factors):
        residue = pow(witness, (prime - 1) // divisor, prime)
        divisors.append(
            {
                "q": str(divisor),
                "exponent_in_p_minus_one": p_minus_one_factors[divisor],
                "power_residue": str(residue),
                "gcd_power_residue_minus_one_with_p": str(
                    gcd(residue - 1, prime)
                ),
            }
        )
    return {
        "index": index,
        "role": "WORK" if index < WORK_PRIMES else "OVERFLOW",
        "p": str(prime),
        "c": coefficient,
        "family": "p=c*2^32+1",
        "coefficient_bit_length": coefficient.bit_length(),
        "coefficient_factorization": factor_map(coefficient),
        "p_minus_one_factorization": {
            str(prime_factor): exponent
            for prime_factor, exponent in sorted(
                p_minus_one_factors.items()
            )
        },
        "n_minus_one_certificate": {
            "method": "full-factorization Lucas/Pocklington N-1",
            "witness_a": witness,
            "fermat_residue": str(pow(witness, prime - 1, prime)),
            "prime_divisor_checks": divisors,
        },
        "two_adic_valuation_of_p_minus_one": p_minus_one_factors[2],
        "primitive_root": witness,
        "maximum_power_of_two_transform_length": str(
            2 ** p_minus_one_factors[2]
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()

    generated = generate_ntt_prime_schedule(TOTAL_PRIMES)
    records = [
        certificate(index, item)
        for index, item in enumerate(generated)
    ]
    payload = {
        "schema": "certified-qmc-primes-schedule-v1",
        "verification_status": "PENDING_INDEPENDENT_VERIFIER_MANIFEST",
        "generation": {
            "algorithm": (
                "scan c downward from 2^30-1; admit p=c*2^32+1 "
                "when deterministic u64 Miller-Rabin passes; choose the "
                "least complete-factor primitive root"
            ),
            "coefficient_start": 2**30 - 1,
            "order": "strictly descending coefficient",
            "family": "p=c*2^32+1",
            "coefficient_maximum_bits": 30,
            "work_prime_count": WORK_PRIMES,
            "universal_overflow_prime_count": OVERFLOW_PRIMES,
        },
        "count": len(records),
        "primes": records,
        "verification_manifest": (
            "certificates/cycle-014-prime-schedule-manifest.json"
        ),
        "boundary": (
            "The generator emits certificate claims but does not promote "
            "them. VERIFIED status is supplied only by the independent "
            "manifest after every record and deterministic regeneration "
            "pass."
        ),
    }
    rendered = json.dumps(
        payload, indent=2, sort_keys=True
    ).encode("utf-8") + b"\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(rendered)
    print(
        json.dumps(
            {
                "output": str(args.output),
                "sha256": sha256(rendered).hexdigest(),
                "bytes": len(rendered),
                "count": len(records),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
