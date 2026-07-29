#!/usr/bin/env python3
"""Independent verifier for the complete production prime schedule.

This module intentionally imports no project arithmetic helper.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from math import gcd, isqrt, prod
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
SCHEDULE = ROOT / "data" / "primes-schedule-v1.json"
OUTPUT = ROOT / "certificates" / "cycle-014-prime-schedule-manifest.json"
GENERATOR = ROOT / "scripts" / "generate_prime_schedule_v1.py"


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def canonical_digest(value: object) -> str:
    return sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
    ).hexdigest()


def is_small_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    limit = isqrt(value)
    while divisor <= limit:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def parse_factorization(raw: dict[str, int]) -> dict[int, int]:
    factors: dict[int, int] = {}
    for raw_prime, raw_exponent in raw.items():
        prime = int(raw_prime)
        exponent = int(raw_exponent)
        if str(prime) != raw_prime or exponent < 1:
            raise ValueError("noncanonical factorization field")
        if not is_small_prime(prime):
            raise ValueError(f"composite factor in certificate: {prime}")
        factors[prime] = exponent
    return factors


def verify_record(record: dict, expected_index: int) -> dict[str, object]:
    if record["index"] != expected_index:
        raise ValueError("schedule index mismatch")
    expected_role = "WORK" if expected_index < 3738 else "OVERFLOW"
    if record["role"] != expected_role:
        raise ValueError("schedule role mismatch")
    p = int(record["p"])
    c = int(record["c"])
    if p != c * 2**32 + 1:
        raise ValueError("prime family identity failed")
    if not 0 < c < 2**30 or record["coefficient_bit_length"] > 30:
        raise ValueError("coefficient exceeds 30-bit family")

    c_factors = parse_factorization(
        record["coefficient_factorization"]
    )
    if prod(q**e for q, e in c_factors.items()) != c:
        raise ValueError("coefficient factorization is incomplete")
    n_factors = parse_factorization(
        record["p_minus_one_factorization"]
    )
    if prod(q**e for q, e in n_factors.items()) != p - 1:
        raise ValueError("p-1 factorization is incomplete")
    expected_n_factors = c_factors.copy()
    expected_n_factors[2] = expected_n_factors.get(2, 0) + 32
    if n_factors != expected_n_factors:
        raise ValueError("p-1 factorization does not derive from c")

    certificate = record["n_minus_one_certificate"]
    witness = int(certificate["witness_a"])
    if not 1 < witness < p:
        raise ValueError("witness outside range")
    fermat = pow(witness, p - 1, p)
    if fermat != 1 or int(certificate["fermat_residue"]) != fermat:
        raise ValueError("Fermat equality failed")

    checks = certificate["prime_divisor_checks"]
    if [int(check["q"]) for check in checks] != sorted(n_factors):
        raise ValueError("prime-divisor check coverage mismatch")
    for check in checks:
        q = int(check["q"])
        if int(check["exponent_in_p_minus_one"]) != n_factors[q]:
            raise ValueError("factor exponent mismatch")
        residue = pow(witness, (p - 1) // q, p)
        result_gcd = gcd(residue - 1, p)
        if int(check["power_residue"]) != residue:
            raise ValueError("power residue transcript mismatch")
        if (
            int(check["gcd_power_residue_minus_one_with_p"])
            != result_gcd
        ):
            raise ValueError("gcd transcript mismatch")
        if result_gcd != 1:
            raise ValueError("Lucas/Pocklington gcd condition failed")

    valuation = 0
    remainder = p - 1
    while remainder % 2 == 0:
        valuation += 1
        remainder //= 2
    if record["two_adic_valuation_of_p_minus_one"] != valuation:
        raise ValueError("2-adic valuation mismatch")
    if int(record["maximum_power_of_two_transform_length"]) != 2**valuation:
        raise ValueError("transform capacity mismatch")
    if record["primitive_root"] != witness:
        raise ValueError("primitive-root witness mismatch")
    # Full factorization, Fermat equality, and the gcd condition for every
    # prime divisor of p-1 are the Lucas N-1 criterion and also prove the
    # witness has exact order p-1.
    return {
        "index": expected_index,
        "p": str(p),
        "c": c,
        "witness": witness,
        "distinct_prime_divisors": len(n_factors),
        "two_adic_valuation": valuation,
        "status": "VERIFIED",
    }


def regenerate_twice(schedule: Path) -> dict[str, object]:
    expected = schedule.read_bytes()
    with tempfile.TemporaryDirectory(
        prefix="certified-qmc-cycle014-regeneration-"
    ) as temporary:
        paths = [
            Path(temporary) / "regenerated-1.json",
            Path(temporary) / "regenerated-2.json",
        ]
        for path in paths:
            subprocess.run(
                [
                    sys.executable,
                    str(GENERATOR),
                    "--output",
                    str(path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )
        rendered = [path.read_bytes() for path in paths]
    return {
        "runs": 2,
        "schedule_sha256": sha256(expected).hexdigest(),
        "regenerated_sha256": [
            sha256(value).hexdigest() for value in rendered
        ],
        "generator_runs_byte_identical_to_each_other": (
            rendered[0] == rendered[1]
        ),
        "generator_runs_byte_identical_to_banked_schedule": (
            all(value == expected for value in rendered)
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--schedule", type=Path, default=SCHEDULE)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument(
        "--skip-regeneration",
        action="store_true",
        help="verify certificates only; manifest gate remains false",
    )
    args = parser.parse_args()

    raw = args.schedule.read_bytes()
    schedule = json.loads(raw)
    if schedule["schema"] != "certified-qmc-primes-schedule-v1":
        raise ValueError("schedule schema mismatch")
    if schedule["count"] != 3740 or len(schedule["primes"]) != 3740:
        raise ValueError("schedule count mismatch")
    coefficients = [record["c"] for record in schedule["primes"]]
    if any(
        left <= right for left, right in zip(coefficients, coefficients[1:])
    ):
        raise ValueError("coefficients are not strictly descending")

    verified = [
        verify_record(record, index)
        for index, record in enumerate(schedule["primes"])
    ]
    regeneration = (
        {
            "runs": 0,
            "generator_runs_byte_identical_to_each_other": False,
            "generator_runs_byte_identical_to_banked_schedule": False,
            "skipped": True,
        }
        if args.skip_regeneration
        else regenerate_twice(args.schedule)
    )
    gate_passed = (
        len(verified) == 3740
        and regeneration[
            "generator_runs_byte_identical_to_each_other"
        ]
        and regeneration[
            "generator_runs_byte_identical_to_banked_schedule"
        ]
    )
    payload = {
        "schema": "certified-qmc-cycle-014-prime-schedule-manifest-v1",
        "claim_tag": (
            "VERIFIED_FULL_N_MINUS_ONE_PRIME_SCHEDULE"
            if gate_passed
            else "INCOMPLETE_VERIFICATION"
        ),
        "schedule": {
            "path": str(args.schedule.relative_to(ROOT)),
            "sha256": sha256(raw).hexdigest(),
            "bytes": len(raw),
            "count": len(verified),
            "work_prime_count": 3738,
            "universal_overflow_prime_count": 2,
            "first": verified[0],
            "last_work": verified[3737],
            "overflow": verified[3738:],
        },
        "independent_verifier": {
            "path": str(Path(__file__).resolve().relative_to(ROOT)),
            "sha256": digest(Path(__file__).resolve()),
            "imports_project_arithmetic_helpers": False,
            "coefficient_factor_primality": (
                "independent deterministic trial division"
            ),
            "candidate_primality": (
                "full-factorization Lucas/Pocklington N-1 criterion"
            ),
            "records_verified": len(verified),
            "all_records_verified": len(verified) == 3740,
        },
        "generator": {
            "path": str(GENERATOR.relative_to(ROOT)),
            "sha256": digest(GENERATOR),
            "regeneration": regeneration,
        },
        "gate": {
            "complete_schedule_verified": len(verified) == 3740,
            "two_overflow_primes_verified": (
                all(row["status"] == "VERIFIED" for row in verified[3738:])
            ),
            "byte_identical_regeneration_demonstrated": (
                regeneration[
                    "generator_runs_byte_identical_to_banked_schedule"
                ]
            ),
            "cycle_014_exit_gate_passed": gate_passed,
        },
        "boundary": (
            "VERIFIED means every p has an independently replayed complete "
            "factorization of p-1, Fermat equality, and gcd condition for "
            "each distinct prime divisor, which proves primality and the "
            "claimed primitive root. It does not benchmark modular kernels."
        ),
    }
    payload["certificate_sha256"] = canonical_digest(payload)
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n"
    )
    print(args.output)


if __name__ == "__main__":
    main()
