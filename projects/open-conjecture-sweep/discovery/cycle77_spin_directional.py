#!/usr/bin/env python3
"""Quarantined one-sided Ky Fan orientation at Q=I/2 for the C77 packet."""

from __future__ import annotations

import json

import numpy as np

from cycle77_spin_packet import (
    CONTROL_NUMERATOR,
    alignment_operator,
    primitive_canonical_vectors,
    target_operator,
    two_body_marginals,
)


STEPS = (2.0 ** -12, 2.0 ** -14)
ACTIVE_TOL = 1e-10


def ky_fan(operator: np.ndarray) -> np.ndarray:
    return np.cumsum(np.linalg.eigvalsh(operator)[::-1])


def main() -> None:
    half = CONTROL_NUMERATOR / 16.0
    target_half = ky_fan(target_operator(half))
    target_steps = {h: ky_fan(target_operator(half + h)) for h in STEPS}
    active = 0
    maxima = {h: (-float("inf"), None) for h in STEPS}
    by_index = {h: {k: (-float("inf"), None) for k in range(1, 8)} for h in STEPS}
    states = 0
    for u in primitive_canonical_vectors():
        marginals = two_body_marginals(u)
        base_gap = ky_fan(alignment_operator(*marginals, half)) - target_half
        states += 1
        for k, gap in enumerate(base_gap[:-1], start=1):
            if abs(gap) > ACTIVE_TOL:
                continue
            active += 1
            for h in STEPS:
                perturbed_gap = (
                    ky_fan(alignment_operator(*marginals, half + h))[k - 1]
                    - target_steps[h][k - 1]
                )
                slope = float(perturbed_gap / h)
                if slope > maxima[h][0]:
                    maxima[h] = (slope, {"u": u, "k": k,
                                        "recognized_gap": float(perturbed_gap)})
                if slope > by_index[h][k][0]:
                    by_index[h][k] = (slope, {"u": u,
                                               "recognized_gap": float(perturbed_gap)})
    payload = {
        "claim_tag": "OBSERVED",
        "state_rows": states,
        "active_constraints": active,
        "one_sided_maxima": {
            str(h): {"slope": entry[0], "witness": entry[1]}
            for h, entry in maxima.items()
        },
        "one_sided_by_index": {
            str(h): {
                str(k): {"slope": entry[0], "witness": entry[1]}
                for k, entry in entries.items()
            }
            for h, entries in by_index.items()
        },
    }
    print(json.dumps(payload, sort_keys=True))


if __name__ == "__main__":
    main()
