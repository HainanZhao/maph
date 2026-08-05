#!/usr/bin/env python3
"""Exact H11 mask-cover diagnostic for the weighted-dual family."""

from __future__ import annotations

import itertools
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
K, P, C, Q = 3, 11, 4, 44


def bad_mask(speed: int, modulus: int) -> int:
    return sum(
        1 << time
        for time in range(modulus)
        if (K + 1) * min((time * speed) % modulus, modulus - ((time * speed) % modulus)) < modulus
    )


def main() -> None:
    base_masks = [bad_mask(speed, P) for speed in range(P)]
    lift_masks = [bad_mask(speed, Q) for speed in range(Q)]
    full = (1 << Q) - 1
    witnesses: list[str] = []
    bases = covers = 0
    for base in itertools.product(range(1, P), repeat=K):
        if base_masks[base[0]] | base_masks[base[1]] | base_masks[base[2]] != (1 << P) - 1:
            continue
        bases += 1
        for digits in itertools.product(range(C), repeat=K):
            selected = [lift_masks[value + P * digit] for value, digit in zip(base, digits, strict=True)]
            if selected[0] | selected[1] | selected[2] == full:
                covers += 1
                witnesses.append("{} {} {} | {} {} {}".format(*base, *digits))
                break
        else:
            raise AssertionError(f"no mask-cover falsifier for base {base}")
    if bases != 240 or covers != 240:
        raise AssertionError(f"unexpected H11 diagnostic counts: {(bases, covers)}")
    (ROOT / "discovery/out/cycle9-h11-dual-falsifiers.txt").write_text("\n".join(witnesses) + "\n")
    print(f"h11_l1_improper_bases={bases} mask_cover_falsifiers={covers}")


if __name__ == "__main__":
    main()
