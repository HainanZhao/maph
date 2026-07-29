#!/usr/bin/env python3
"""Checkpoint the reference radix-two model and sensitivity factors."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.radix2_model import (
    DEFAULT_TWIDDLE_ERROR,
    certify_reference_fft,
    local_butterfly_factor,
    transform_error_factor,
)


OUTPUT = ROOT / "certificates" / "workstream-b-radix2-model.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    validations = []
    for length in (2, 4, 8, 16, 32, 64):
        values = [
            complex((index - length / 3) / 17, (3 * index - 2) / 19)
            for index in range(length)
        ]
        validations.append(certify_reference_fft(values))
        validations.append(
            certify_reference_fft(
                values, inverse=True, normalize_inverse=True
            )
        )

    sensitivities = []
    for length in (2**10, 2**20):
        depth = length.bit_length() - 1
        sensitivities.append(
            {
                "length": length,
                "baseline": str(transform_error_factor(length)),
                "twiddle_x2": str(
                    transform_error_factor(
                        length, twiddle_error=2 * DEFAULT_TWIDDLE_ERROR
                    )
                ),
                "depth_x2": str(
                    transform_error_factor(
                        length, radix2_equivalent_depth=2 * depth
                    )
                ),
            }
        )
    certificate = {
        "schema": "certified-qmc/workstream-b-radix2-model/v1",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "claim_tag": "VERIFIED_MODEL_TRANSFORM_BOUND",
        "model_class": {
            "arithmetic": "binary64 round-to-nearest",
            "structure": (
                "radix-2/4 transform admitting no more than the declared "
                "radix-2-equivalent depth"
            ),
            "complex_multiply": "four real multiplies and two real adds",
            "twiddle_absolute_error": str(DEFAULT_TWIDDLE_ERROR),
            "overflow": "excluded",
            "harmful_underflow": "excluded",
        },
        "local_butterfly_factor": str(local_butterfly_factor()),
        "theorem": (
            "max_k |FFT_hat(x)_k-FFT(x)_k| <= "
            "((1+eta)^L-1)*||x||_1"
        ),
        "validation": validations,
        "gate": {
            "all_twiddles_contained": all(
                item["twiddles_contained"] for item in validations
            ),
            "all_transforms_contained": all(
                item["transform_contained"] for item in validations
            ),
        },
        "sensitivity": sensitivities,
        "artifacts": {
            "implementation": "src/radix2_model.py",
            "implementation_sha256": sha256(ROOT / "src" / "radix2_model.py"),
            "proof": "docs/workstream-b-radix2-model-bound.md",
            "proof_sha256": sha256(
                ROOT / "docs" / "workstream-b-radix2-model-bound.md"
            ),
        },
        "boundary": (
            "This closes the transform theorem for model class M. A complete "
            "T_eval(M) must additionally compose kernel construction, state "
            "updates, convolution products, normalization, and accumulation."
        ),
    }
    OUTPUT.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(OUTPUT)


if __name__ == "__main__":
    main()
