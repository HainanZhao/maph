#!/usr/bin/env python3
"""Checkpoint the direct CU:P2 producer forward-error enclosure."""

from __future__ import annotations

from fractions import Fraction
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.producer_error import direct_product_p2_bound


PLAN_CERTIFICATE = ROOT / "certificates" / "workstream-b-fftw-plan-audit.json"
OUTPUT = ROOT / "certificates" / "workstream-b-direct-producer-bound.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    plan_certificate = json.loads(PLAN_CERTIFICATE.read_text())
    scaling_hex = plan_certificate["environment"]["p2_scaling_hex"]
    cases = [
        {
            "name": "small-balanced",
            "modulus": 8,
            "generator": [1, 3],
            "weights": ["1", "1/4"],
        },
        {
            "name": "mixed-scale",
            "modulus": 16,
            "generator": [1, 7, 5],
            "weights": ["1", "1/1000", "7/9"],
        },
        {
            "name": "factorial-denominators",
            "modulus": 64,
            "generator": [1, 31, 15, 7, 25, 11],
            "weights": [str(Fraction(1, j * j)) for j in range(1, 7)],
        },
    ]
    results = []
    for case in cases:
        result = direct_product_p2_bound(
            case["modulus"],
            case["generator"],
            case["weights"],
            scaling_hex=scaling_hex,
            precision=256,
        )
        results.append({**case, "result": result})

    certificate = {
        "schema": "certified-qmc/workstream-b-direct-producer-bound/v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "ENCLOSED_DIRECT_PRODUCER_ERROR",
        "producer_model": {
            "latnet_builder_commit": "39dd60fceb0c86a6124b701072d91f8e3aed73df",
            "task": "evaluation",
            "lattice": "ordinary unilevel symmetric",
            "figure": "CU:P2",
            "weights": "product",
            "operation_order": (
                "CoordUniformCBC + CoordUniformInnerProd + compressedSum"
            ),
            "binary64_rounding": "FE_TONEAREST",
            "p2_scaling_hex": scaling_hex,
        },
        "method": {
            "midpoint": "binary64 operation replay",
            "local_rounding_error": (
                "exact dyadic difference at every add/subtract/multiply/divide"
            ),
            "propagation": "Arb outward absolute-error balls at 256 bits",
            "independent_oracle": (
                "-1 + N^-1 sum_k product_j(1+gamma_j*2*pi^2*B2)"
            ),
        },
        "source_artifacts": {
            "implementation": "src/producer_error.py",
            "implementation_sha256": sha256(ROOT / "src" / "producer_error.py"),
            "test": "tests/test_producer_error.py",
            "test_sha256": sha256(ROOT / "tests" / "test_producer_error.py"),
            "plan_certificate": str(PLAN_CERTIFICATE.relative_to(ROOT)),
            "plan_certificate_sha256": sha256(PLAN_CERTIFICATE),
        },
        "adversarial_cases": results,
        "gate": {
            "all_independent_arb_targets_contained": all(
                item["result"]["contains_independent_arb_target"]
                for item in results
            )
        },
        "boundary": (
            "This certificate closes the direct evaluation arithmetic only. "
            "It does not bound FFTW transforms, fast-CBC candidate scores, "
            "minimum-selection decisions, or historical decimal output."
        ),
    }
    OUTPUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(OUTPUT)


if __name__ == "__main__":
    main()
