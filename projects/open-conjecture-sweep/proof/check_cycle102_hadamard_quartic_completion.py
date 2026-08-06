#!/usr/bin/env python3
"""Independent exact E001 completion check; intentionally no engine import."""
from __future__ import annotations

import argparse
import json
from itertools import combinations_with_replacement
from pathlib import Path


P = 167


def legendre(number: int) -> int:
    number %= P
    return 0 if number == 0 else (1 if pow(number, 83, P) == 1 else -1)


def correlation(word: list[int]) -> tuple[int, ...]:
    return tuple(sum(word[i] * word[(i + shift) % P] for i in range(P)) for shift in range(1, 84))


def signature(word: list[int]) -> tuple[int, ...]:
    return (sum(word) ** 2,) + correlation(word)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path)
    args = parser.parse_args()
    recorded = json.loads(args.result.read_text(encoding="utf-8"))
    a = [1] + [legendre(i) for i in range(1, P)]
    if signature(a) != (1,) + (-1,) * 83:
        raise SystemExit("fixed A control failed")
    words = {}
    for b in range(P):
        word = [legendre(i**4 + b * i * i + 1) for i in range(P)]
        if all(value != 0 for value in word):
            if any(word[i] != word[-i % P] for i in range(P)):
                raise SystemExit("reversal symmetry failed")
            words[b] = word
    parameters = sorted(words)
    vectors = {parameter: signature(word) for parameter, word in words.items()}
    target = (667,) + (1,) * 83
    hits = []
    for b, c, d in combinations_with_replacement(parameters, 3):
        total = tuple(vectors[b][i] + vectors[c][i] + vectors[d][i] for i in range(84))
        if total == target:
            hits.append((b, c, d))
    expected = {"q": P, "admissible_parameters": parameters, "parameter_count": len(parameters),
                "pair_count": len(parameters) * (len(parameters) + 1) // 2,
                "a_vector": signature(a), "target": target, "hits": hits}
    if recorded != json.loads(json.dumps(expected)):
        raise SystemExit("independent completion disagreement")
    print(json.dumps({"checked_triples": len(parameters) * (len(parameters) + 1) * (len(parameters) + 2) // 6, "hits": hits}, sort_keys=True))


if __name__ == "__main__":
    main()
