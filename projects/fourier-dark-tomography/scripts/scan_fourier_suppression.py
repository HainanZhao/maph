#!/usr/bin/env python3
"""Enumerate exact dark events in a prime-power Fourier multiport."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.fourier_suppression import (  # noqa: E402
    canonical_dark_pair,
    has_at_most_two_fourier_support_types,
    is_dark_prime_power,
    occupation_vectors,
    phase_histogram,
    prime_power_base,
    simple_cyclic_rule_predicts_dark,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--modes", type=int, required=True)
    parser.add_argument("--particles", type=int, required=True)
    parser.add_argument("--show-families", type=int, default=20)
    args = parser.parse_args()

    if prime_power_base(args.modes) is None:
        parser.error("--modes must be a prime power")

    occupations = list(occupation_vectors(args.particles, args.modes))
    dark_count = 0
    symmetry_count = 0
    residual: set[tuple[tuple[int, ...], tuple[int, ...]]] = set()
    two_type_residual: set[
        tuple[tuple[int, ...], tuple[int, ...]]
    ] = set()
    multitype_residual: set[
        tuple[tuple[int, ...], tuple[int, ...]]
    ] = set()

    for input_occupation in occupations:
        for output_occupation in occupations:
            dark = is_dark_prime_power(input_occupation, output_occupation)
            predicted = simple_cyclic_rule_predicts_dark(
                input_occupation, output_occupation
            )
            if predicted and not dark:
                raise AssertionError("cyclic rule predicted a non-dark event")
            if dark:
                dark_count += 1
                if predicted:
                    symmetry_count += 1
                else:
                    representative = canonical_dark_pair(
                        input_occupation, output_occupation
                    )
                    residual.add(representative)
                    if has_at_most_two_fourier_support_types(
                        input_occupation, output_occupation
                    ):
                        two_type_residual.add(representative)
                    else:
                        multitype_residual.add(representative)

    pair_count = len(occupations) ** 2
    print(f"modes={args.modes} particles={args.particles}")
    print(f"occupation vectors: {len(occupations)}")
    print(f"input/output pairs: {pair_count}")
    print(f"exact dark pairs: {dark_count}")
    print(f"caught by elementary cyclic rule: {symmetry_count}")
    print(f"residual equivalence families: {len(residual)}")
    print(f"  at most two support types: {len(two_type_residual)}")
    print(f"  three or more support types: {len(multitype_residual)}")
    for pair in sorted(residual)[:args.show_families]:
        print(f"  {pair[0]} -> {pair[1]}  histogram={phase_histogram(*pair)}")


if __name__ == "__main__":
    main()
