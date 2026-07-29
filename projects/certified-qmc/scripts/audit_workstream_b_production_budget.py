#!/usr/bin/env python3
"""Budget the frozen Workstream B grid before production compute."""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
import json
from math import ceil
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.scaled_integer import balanced_crt_bits, error_numerator_bound


FREEZE = ROOT / "data" / "workstream-b-production-freeze.json"
OUTPUT = ROOT / "certificates" / "workstream-b-production-budget.json"


def file_sha256(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def budget_cell(modulus_exponent: int, dimension: int, power: int) -> dict:
    modulus = 2**modulus_exponent
    weights = [
        Fraction(1, index**power)
        for index in range(1, dimension + 1)
    ]
    required_bits = balanced_crt_bits(
        error_numerator_bound(modulus, weights)
    )
    # Every scheduled p=c*2^32+1 in the frozen family has p>2^61.
    # Ceil(bits/61) is therefore a conservative count budget; actual
    # ordered primes and their cumulative product are verified later.
    work_primes = ceil(required_bits / 61)
    overflow_primes = 2
    modular_updates = modulus * dimension * work_primes
    return {
        "N": modulus,
        "modulus_exponent": modulus_exponent,
        "dimension": dimension,
        "weight_profile": f"gamma_j=1/j^{power}",
        "proved_reconstruction_bits": required_bits,
        "conservative_61_bit_work_primes": work_primes,
        "overflow_check_primes": overflow_primes,
        "total_prime_budget": work_primes + overflow_primes,
        "prime_major_state_bytes": modulus * 8,
        "prefix_residue_bytes": dimension * work_primes * 8,
        "direct_incremental_modular_update_lower_bound": modular_updates,
        "schedule_status": "BUDGETED_NOT_YET_GENERATED",
    }


def main() -> None:
    freeze = json.loads(FREEZE.read_text())
    families = len(freeze["source_families"])

    fidelity = [
        budget_cell(exponent, 3600, 2)
        for exponent in freeze["fidelity_grid"]["modulus_exponents"]
    ]
    usability = [
        budget_cell(exponent, 256, power)
        for exponent in freeze["usability_grid"]["modulus_exponents"]
        for power in (1, 3)
    ]
    fidelity_updates = families * sum(
        cell["direct_incremental_modular_update_lower_bound"]
        for cell in fidelity
    )
    usability_updates = families * sum(
        cell["direct_incremental_modular_update_lower_bound"]
        for cell in usability
    )
    worst = max(
        [*fidelity, *usability],
        key=lambda cell: cell["proved_reconstruction_bits"],
    )
    payload = {
        "schema": "certified-qmc-workstream-b-production-budget-v1",
        "claim_tag": "VERIFIED_PRECOMPUTE_BOUND_BUDGET",
        "production_freeze": str(FREEZE.relative_to(ROOT)),
        "production_freeze_sha256": file_sha256(FREEZE),
        "prime_count_rule": (
            "ceil(proved_reconstruction_bits/61), because every admitted "
            "work prime is strictly greater than 2^61"
        ),
        "fidelity_max_dimension_cells": fidelity,
        "usability_incremental_run_cells": usability,
        "totals": {
            "source_families": families,
            "fidelity_direct_update_lower_bound": fidelity_updates,
            "usability_direct_update_lower_bound": usability_updates,
            "combined_direct_update_lower_bound": (
                fidelity_updates + usability_updates
            ),
        },
        "worst_cell": worst,
        "gate": {
            "budget_computed_before_production": True,
            "full_production_authorized": False,
            "reason": (
                "the proved full-grid work and prime counts require a "
                "compiled streaming pilot and a generated verified schedule"
            ),
            "required_next_pilot": {
                "source_scope": "frozen 29102 prefix",
                "N": 1024,
                "dimension": 256,
                "weight_profile": "gamma_j=1/j^2",
                "acceptance": [
                    "exact agreement with Fraction and existing certificates",
                    "measured work within factor two of the updated projection",
                    "prime-major checkpoint replay",
                    "single-entry verifier replay"
                ]
            }
        },
        "boundary": (
            "This is an exact reconstruction-bound and operation-count "
            "preflight, not a runtime claim and not authorization to run "
            "the full grid."
        ),
    }
    payload["certificate_sha256"] = sha256(
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=True,
        ).encode("ascii")
    ).hexdigest()
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(OUTPUT)


if __name__ == "__main__":
    main()
