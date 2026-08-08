#!/usr/bin/env python3
"""Exact firewall for the global phase-potential construction.

This exercises the algebra of the global phase telescoping lemma on a finite
path model.  It does not stand in for the still-required grid-core replay.
"""

from __future__ import annotations

import json


PRIMES = (1_000_000_007, 1_000_000_009)
BLOCKS = 5
STATES = tuple(range(4))


def transitions(block: int, left: int):
    """Two labelled local subsets from every state."""
    for subset in (0, 1):
        right = (left + 1 + subset + block) & 3
        yield subset, right


def q_local(block: int, subset: int, left: int, right: int) -> int:
    return (subset + (left & 1) * ((right >> 1) & 1) + block * (right & 1)) & 1


def h_local(block: int, subset: int, left: int, right: int) -> int:
    return (subset + ((left ^ right) >> (block & 1))) & 1


def all_paths():
    rows = [(0, (), 0)]
    prefixes = [[(0, (), 0)]]
    for block in range(BLOCKS):
        updated = []
        for left, path, phase_value in rows:
            for subset, right in transitions(block, left):
                updated.append(
                    (
                        right,
                        path + ((subset, left, right),),
                        phase_value ^ q_local(block, subset, left, right),
                    )
                )
        rows = updated
        prefixes.append(rows)
    complete = [row for row in rows if row[0] == 0]
    if not complete:
        raise AssertionError("test automaton has no closed paths")
    return prefixes, complete


def suffixes():
    result = [dict() for _ in range(BLOCKS + 1)]
    result[BLOCKS][0] = ()
    for block in range(BLOCKS - 1, -1, -1):
        for left in STATES:
            candidates = []
            for subset, right in transitions(block, left):
                if right in result[block + 1]:
                    candidates.append(((subset, left, right),) + result[block + 1][right])
            if candidates:
                result[block][left] = min(candidates)
    return result


def phase(path) -> int:
    return sum(
        q_local(block, subset, left, right)
        for block, (subset, left, right) in enumerate(path)
    ) & 1


def verify():
    prefixes, complete = all_paths()
    right_references = suffixes()
    left_references = []
    for block, rows in enumerate(prefixes):
        selected = {}
        for state, path, _ in rows:
            if state in right_references[block]:
                selected.setdefault(state, path)
        left_references.append(selected)

    potentials = []
    for block, rows in enumerate(prefixes):
        table = {}
        for state, path, _ in rows:
            if state not in right_references[block]:
                continue
            suffix = right_references[block][state]
            reference = left_references[block][state]
            table[path] = phase(path + suffix) ^ phase(reference + suffix)
        potentials.append(table)

    recovered = {}
    for block in range(BLOCKS):
        for left, path, _ in prefixes[block]:
            if path not in potentials[block]:
                continue
            for subset, right in transitions(block, left):
                extended = path + ((subset, left, right),)
                if extended not in potentials[block + 1]:
                    continue
                value = potentials[block][path] ^ potentials[block + 1][extended]
                key = block, subset, left, right
                if key in recovered and recovered[key] != value:
                    raise AssertionError(f"history-dependent residual phase at {key}")
                recovered[key] = value

    endpoint_constant = potentials[BLOCKS][left_references[BLOCKS][0]]
    for _, path, theta in complete:
        total = endpoint_constant
        for block, transition in enumerate(path):
            total ^= recovered[(block,) + transition]
        if total != theta:
            raise AssertionError("recovered local phase did not telescope")

    prime_rows = []
    for prime in PRIMES:
        for evaluation in (0, 1):
            weights = {
                (block, subset, left, right):
                (
                    2
                    + 104729 * (1 + block * 17 + subset * 7 + left * 5 + right)
                    + evaluation * 13007
                )
                % prime
                for block in range(BLOCKS)
                for left in STATES
                for subset, right in transitions(block, left)
            }
            for epsilon in range(1 << BLOCKS):
                vector = [1, 0, 0, 0]
                for block in range(BLOCKS):
                    updated = [0] * 4
                    for left in STATES:
                        for subset, right in transitions(block, left):
                            # A transition with no zero-to-zero completion never
                            # contributes to the selected boundary contraction;
                            # its phase may be fixed arbitrarily.
                            exponent = recovered.get((block, subset, left, right), 0)
                            exponent ^= ((epsilon >> block) & 1) * h_local(
                                block, subset, left, right
                            )
                            sign = prime - 1 if exponent else 1
                            updated[right] = (
                                updated[right]
                                + vector[left]
                                * sign
                                * weights[(block, subset, left, right)]
                            ) % prime
                    vector = updated
                contracted = vector[0]

                direct = 0
                for _, path, theta in complete:
                    exponent = theta
                    product = 1
                    for block, (subset, left, right) in enumerate(path):
                        exponent ^= ((epsilon >> block) & 1) * h_local(
                            block, subset, left, right
                        )
                        product = product * weights[(block, subset, left, right)] % prime
                    direct = (direct + (-product if exponent else product)) % prime
                if contracted != direct:
                    raise AssertionError("core contraction disagrees with direct path sum")
            prime_rows.append(
                {
                    "prime": prime,
                    "evaluation": evaluation,
                    "all_spin_structures_agree": True,
                }
            )

    return {
        "claim_status": "PROVED algebraic lemma with exact finite firewall",
        "blocks": BLOCKS,
        "states": len(STATES),
        "closed_paths": len(complete),
        "recovered_transition_phases": len(recovered),
        "history_independence_checked": True,
        "prime_rows": prime_rows,
        "claim_boundary": (
            "This validates phase-potential recovery and denominator-free core "
            "contraction on an exhaustive finite path model. It is not the required "
            "direct checkerboard-grid core replay."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
