#!/usr/bin/env python3
"""Meet-in-the-middle certificates for two defect-sensitive conjectures.

Two displayed witnesses for every pair disprove pair isolation; one
displayed witness for every triple disproves the adaptive three-base cover
conjecture.  These positive conclusions do not need an exhaustive scan.

When a pivot Lucas box is fully enumerated, the same search also gives
exact negative certificates: at most one recorded witness for a pair
containing that pivot certifies pair isolation, and no recorded witness for
a triple containing it certifies a three-base cover.  Resource-limited or
early-stopped pivots are never treated as complete.

Candidates are generated with a meet-in-the-middle enumeration of a
single prime's Lucas digit box.  If its allowed-residue count is B, the
largest materialized side is normally about sqrt(B), making boxes far
larger than the direct sparse-box cutoff accessible.
"""

from __future__ import annotations

import argparse
import random
import sys
from dataclasses import dataclass
from itertools import combinations, product
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.erdos700 import (  # noqa: E402
    factorize,
    lucas_nonzero,
    near_multiple_lucas_residue_box,
    reciprocal_defect,
)


DEFAULT_KERNELS = (
    (2, 3, 5),
    (2, 3, 7, 11),
    (2, 3, 7, 41),
    (2, 3, 11, 13),
    (2, 3, 11, 17, 19),
    (2, 5, 7, 11, 13),
    (2, 7, 11, 13, 17, 19, 23, 29),
)


@dataclass(frozen=True)
class SearchRecord:
    multiple: int
    primes: tuple[int, ...]
    exponents: tuple[int, ...]
    pair_witnesses: tuple[tuple[tuple[int, int], tuple[int, ...]], ...]
    triple_witnesses: tuple[
        tuple[tuple[int, int, int], tuple[int, ...]], ...
    ]
    processed_bases: tuple[int, ...]
    completed_bases: tuple[int, ...]
    generated_candidates: int

    @property
    def pair_score(self) -> tuple[int, int]:
        counts = tuple(len(values) for _, values in self.pair_witnesses)
        return min(counts), sum(count >= 2 for count in counts)

    @property
    def triple_score(self) -> int:
        return sum(bool(values) for _, values in self.triple_witnesses)


def digit_choice_groups(upper: int, prime: int) -> list[tuple[int, ...]]:
    """Return nontrivial positional digit choices for a Lucas box."""
    groups = []
    place = 1
    while upper:
        digit = upper % prime
        if digit:
            groups.append(tuple(d * place for d in range(digit + 1)))
        upper //= prime
        place *= prime
    return groups


def balanced_partition(
    groups: list[tuple[int, ...]],
) -> tuple[list[tuple[int, ...]], list[tuple[int, ...]], int, int]:
    """Greedily balance the products of digit-choice counts."""
    left: list[tuple[int, ...]] = []
    right: list[tuple[int, ...]] = []
    left_size = 1
    right_size = 1
    for group in sorted(groups, key=len, reverse=True):
        if left_size <= right_size:
            left.append(group)
            left_size *= len(group)
        else:
            right.append(group)
            right_size *= len(group)
    return left, right, left_size, right_size


def subset_sums(groups: list[tuple[int, ...]]) -> list[int]:
    values = [0]
    for group in groups:
        values = [old + contribution for old in values for contribution in group]
    return values


def scan_multiple(
    multiple: int,
    primes: tuple[int, ...],
    exponents: tuple[int, ...],
    *,
    max_side_values: int,
    max_candidates_per_base: int,
) -> SearchRecord:
    """Search for explicit pair and triple witnesses using all feasible pivots."""
    factors = factorize(multiple)
    pairs = tuple(combinations(primes, 2))
    triples = tuple(combinations(primes, 3))
    pair_witnesses = {pair: [] for pair in pairs}
    triple_witnesses = {triple: [] for triple in triples}
    half = (multiple - 1) // 2
    tests = {}
    for p in primes:
        complement = multiple // (p ** factors[p])
        tests[p] = (complement * (multiple - 1), complement)

    pivot_data = []
    for p in primes:
        box = near_multiple_lucas_residue_box(multiple, p)
        groups = digit_choice_groups(box.shifted_upper, p)
        left, right, left_size, right_size = balanced_partition(groups)
        complement = tests[p][1]
        estimated_candidates = (
            box.allowed_residue_count + complement - 1
        ) // complement
        pivot_data.append(
            (
                estimated_candidates,
                max(left_size, right_size),
                p,
                left,
                right,
                left_size,
                right_size,
            )
        )

    processed = []
    completed = []
    generated = 0
    for _, largest_side, p, left, right, _, _ in sorted(pivot_data):
        if largest_side > max_side_values:
            continue
        processed.append(p)
        complement = tests[p][1]
        left_values = subset_sums(left)
        right_values = subset_sums(right)
        if len(left_values) > len(right_values):
            left_values, right_values = right_values, left_values

        by_residue: dict[int, list[int]] = {}
        for value in left_values:
            by_residue.setdefault(value % complement, []).append(value)

        base_candidates = 0
        seen = set()
        stop_base = False
        truncated = False
        for right_value in right_values:
            target = (-right_value) % complement
            for left_value in by_residue.get(target, ()):
                multiplier = (left_value + right_value) // complement
                if multiplier in seen or not 1 <= multiplier <= half:
                    continue
                seen.add(multiplier)
                generated += 1
                base_candidates += 1

                passed = {
                    q
                    for q in primes
                    if lucas_nonzero(
                        tests[q][0],
                        tests[q][1] * multiplier,
                        q,
                    )
                }
                for pair in pairs:
                    witnesses = pair_witnesses[pair]
                    if (
                        len(witnesses) < 2
                        and multiplier not in witnesses
                        and set(pair) <= passed
                    ):
                        witnesses.append(multiplier)
                for triple in triples:
                    witnesses = triple_witnesses[triple]
                    if not witnesses and set(triple) <= passed:
                        witnesses.append(multiplier)

                if all(len(values) >= 2 for values in pair_witnesses.values()):
                    stop_base = True
                    truncated = True
                    break
                if all(values for values in triple_witnesses.values()):
                    stop_base = True
                    truncated = True
                    break
                if base_candidates >= max_candidates_per_base:
                    stop_base = True
                    truncated = True
                    break
            if stop_base:
                break
        if not truncated:
            completed.append(p)
            if any(
                p in pair and len(pair_witnesses[pair]) <= 1
                for pair in pairs
            ):
                break
        if (
            all(len(values) >= 2 for values in pair_witnesses.values())
            or all(values for values in triple_witnesses.values())
        ):
            break

    return SearchRecord(
        multiple=multiple,
        primes=primes,
        exponents=exponents,
        pair_witnesses=tuple(
            (pair, tuple(values)) for pair, values in pair_witnesses.items()
        ),
        triple_witnesses=tuple(
            (triple, tuple(values))
            for triple, values in triple_witnesses.items()
        ),
        processed_bases=tuple(processed),
        completed_bases=tuple(completed),
        generated_candidates=generated,
    )


def format_record(record: SearchRecord) -> str:
    pair_total = len(record.pair_witnesses)
    triple_total = len(record.triple_witnesses)
    return (
        f"M={record.multiple} kernel={record.primes} exponents={record.exponents} "
        f"pairs(min,saturated)={record.pair_score[0]},{record.pair_score[1]}/"
        f"{pair_total} triples={record.triple_score}/{triple_total} "
        f"processed_bases={record.processed_bases} "
        f"completed_bases={record.completed_bases} "
        f"candidates={record.generated_candidates}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument(
        "--exhaustive",
        action="store_true",
        help="enumerate the full exponent box for every selected kernel",
    )
    parser.add_argument("--min-exponent", type=int, default=1)
    parser.add_argument("--max-exponent", type=int, default=24)
    parser.add_argument("--max-side-values", type=int, default=300_000)
    parser.add_argument("--max-candidates-per-base", type=int, default=100_000)
    parser.add_argument("--seed", type=int, default=700)
    parser.add_argument("--progress-every", type=int, default=0)
    parser.add_argument(
        "--show-all-unresolved",
        action="store_true",
        help="print every unresolved exponent vector instead of the first 20",
    )
    parser.add_argument(
        "--kernel",
        type=int,
        nargs="+",
        action="append",
        help="prime kernel; may be supplied repeatedly",
    )
    parser.add_argument(
        "--exponents",
        type=int,
        nargs="+",
        action="append",
        help="scan only this exponent vector; may be supplied repeatedly",
    )
    parser.add_argument(
        "--min-balanced-side",
        type=int,
        default=0,
        help="skip jobs whose smallest balanced pivot side is at most this",
    )
    args = parser.parse_args()
    if args.iterations < 1:
        parser.error("--iterations must be positive")
    if not 1 <= args.min_exponent <= args.max_exponent:
        parser.error("invalid exponent range")

    kernels = tuple(
        tuple(sorted(kernel)) for kernel in (args.kernel or DEFAULT_KERNELS)
    )
    for kernel in kernels:
        if len(kernel) < 3 or len(set(kernel)) != len(kernel):
            parser.error(f"invalid kernel {kernel}")
        radical = 1
        for p in kernel:
            radical *= p
        if set(factorize(radical)) != set(kernel):
            parser.error(f"kernel contains a nonprime: {kernel}")
        if reciprocal_defect(radical) >= 0:
            parser.error(f"kernel is not reciprocal-supercritical: {kernel}")

    rng = random.Random(args.seed)
    best_pair: SearchRecord | None = None
    best_triple: SearchRecord | None = None
    processed = 0
    zero_pivot_cases = 0
    pair_isolation_certified = 0
    triple_cover_certified = 0
    unresolved_pair_cases: list[SearchRecord] = []
    if args.exponents:
        if len(kernels) != 1:
            parser.error("--exponents requires exactly one --kernel")
        if any(len(row) != len(kernels[0]) for row in args.exponents):
            parser.error("each --exponents vector must match the kernel")
        if any(
            exponent < 1
            for row in args.exponents
            for exponent in row
        ):
            parser.error("exponents must be positive")
        jobs = (
            (kernels[0], tuple(exponents))
            for exponents in args.exponents
        )
    elif args.exhaustive:
        jobs = (
            (primes, exponents)
            for primes in kernels
            for exponents in product(
                range(args.min_exponent, args.max_exponent + 1),
                repeat=len(primes),
            )
        )
    else:
        jobs = (
            (
                kernels[iteration % len(kernels)],
                tuple(
                    rng.randint(args.min_exponent, args.max_exponent)
                    for _ in kernels[iteration % len(kernels)]
                ),
            )
            for iteration in range(args.iterations)
        )

    for primes, exponents in jobs:
        multiple = 1
        for p, exponent in zip(primes, exponents):
            multiple *= p**exponent
        if args.min_balanced_side:
            smallest_side = min(
                max(balanced_partition(digit_choice_groups(
                    near_multiple_lucas_residue_box(multiple, p).shifted_upper,
                    p,
                ))[2:])
                for p in primes
            )
            if smallest_side <= args.min_balanced_side:
                continue
        record = scan_multiple(
            multiple,
            primes,
            exponents,
            max_side_values=args.max_side_values,
            max_candidates_per_base=args.max_candidates_per_base,
        )
        processed += 1
        if not record.processed_bases:
            zero_pivot_cases += 1
        completed = set(record.completed_bases)
        pair_certified = any(
            len(values) <= 1 and bool(completed.intersection(pair))
            for pair, values in record.pair_witnesses
        )
        if pair_certified:
            pair_isolation_certified += 1
        else:
            unresolved_pair_cases.append(record)
        if any(
            not values and bool(completed.intersection(triple))
            for triple, values in record.triple_witnesses
        ):
            triple_cover_certified += 1
        if args.progress_every and processed % args.progress_every == 0:
            print(
                f"progress cases={processed} no-feasible-pivot={zero_pivot_cases}",
                flush=True,
            )

        pair_rank = (
            record.pair_score,
            record.triple_score,
            record.generated_candidates,
        )
        if best_pair is None or pair_rank > (
            best_pair.pair_score,
            best_pair.triple_score,
            best_pair.generated_candidates,
        ):
            best_pair = record
        triple_rank = (
            record.triple_score,
            record.pair_score,
            record.generated_candidates,
        )
        if best_triple is None or triple_rank > (
            best_triple.triple_score,
            best_triple.pair_score,
            best_triple.generated_candidates,
        ):
            best_triple = record

        if record.pair_score[0] >= 2:
            print("PAIR-ISOLATION COUNTEREXAMPLE")
            print(format_record(record))
            print(f"pair witnesses={record.pair_witnesses}")
            return
        if record.triple_score == len(record.triple_witnesses):
            print("THREE-BASE-COVER COUNTEREXAMPLE")
            print(format_record(record))
            print(f"triple witnesses={record.triple_witnesses}")
            return

    assert best_pair is not None and best_triple is not None
    run_kind = (
        "selected-vectors"
        if args.exponents
        else "exhaustive-grid"
        if args.exhaustive
        else "deterministic-random"
    )
    print(
        f"No counterexample in {processed} "
        f"{run_kind} "
        f"cases; seed={args.seed}; exponent range="
        f"{args.min_exponent}..{args.max_exponent}; "
        f"max side={args.max_side_values}; "
        f"cases with no feasible pivot={zero_pivot_cases}; "
        f"pair isolation exactly certified={pair_isolation_certified}; "
        f"three-base cover exactly certified={triple_cover_certified}"
    )
    print(f"best pair near-miss: {format_record(best_pair)}")
    print(f"pair witnesses={best_pair.pair_witnesses}")
    print(f"best triple near-miss: {format_record(best_triple)}")
    print(f"triple witnesses={best_triple.triple_witnesses}")
    unresolved_limit = None if args.show_all_unresolved else 20
    unresolved_descriptions = [
        format_record(record)
        for record in unresolved_pair_cases[:unresolved_limit]
    ]
    print(
        "unresolved pair-isolation cases="
        f"{unresolved_descriptions}"
    )


if __name__ == "__main__":
    main()
