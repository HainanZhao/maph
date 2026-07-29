"""Build and invoke the compiled direct modular baseline."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import subprocess
from typing import Sequence

from .exact_error import RuleSpec


PROJECT = Path(__file__).resolve().parents[1]
NATIVE_BINARY = PROJECT / "build" / "native" / "direct_modular"


def build_native_baseline() -> Path:
    subprocess.run(
        ["make", "-C", str(PROJECT / "native"), "all"],
        check=True,
        capture_output=True,
        text=True,
    )
    return NATIVE_BINARY


def native_error_numerator_residue(
    modulus: int,
    generator: Sequence[int],
    weights: Sequence[Fraction | int | str],
    prime: int,
    *,
    binary: Path | None = None,
) -> int:
    spec = RuleSpec.create(modulus, generator, weights)
    executable = binary or build_native_baseline()
    command = [
        str(executable),
        str(spec.modulus),
        str(prime),
        ",".join(str(value) for value in spec.generator),
        ",".join(str(weight.numerator) for weight in spec.weights),
        ",".join(str(weight.denominator) for weight in spec.weights),
    ]
    completed = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
    )
    return int(completed.stdout.strip())
