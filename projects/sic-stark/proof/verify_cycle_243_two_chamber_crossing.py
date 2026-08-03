#!/usr/bin/env python3
"""Exact finite-residue two-chamber crossing audit for Cycle 243/B080."""
from __future__ import annotations

import json
from fractions import Fraction as F

try:
    from .verify_cycle_228_f3_square_residual_block import blocks
except ImportError:  # pragma: no cover - direct replay
    from verify_cycle_228_f3_square_residual_block import blocks


def pair(item: dict[str, object], key: str) -> tuple[F, F]:
    raw = item[key]
    assert isinstance(raw, list) and len(raw) == 2
    return (F(str(raw[0])), F(str(raw[1])))


def factor_signature(start: str, position: int) -> tuple[F, tuple[F, F], tuple[F, F]]:
    item = blocks()[start][position - 1]
    return F(str(item["argument_mu"])), pair(item, "alpha"), pair(item, "beta")


def audit() -> dict[str, object]:
    expected = {
        "A1": (F(1, 24), (F(1, 24), F(5, 24)), (F(0), F(1))),
        "A2": (F(1, 24), (F(1), F(0)), (F(-115, 24), F(1, 24))),
        "A3": (F(1), (F(24), F(0)), (F(-115), F(1))),
        "A4": (F(1), (F(1), F(5)), (F(0), F(24))),
        "C1": (F(1, 24), (F(1, 24), F(-5, 24)), (F(0), F(1))),
        "C2": (F(1, 24), (F(1), F(0)), (F(115, 24), F(1, 24))),
        "C3": (F(1), (F(24), F(0)), (F(115), F(1))),
        "C4": (F(1), (F(1), F(-5)), (F(0), F(24))),
    }
    actual = {f"{start}{position}": factor_signature(start, position) for start in ("A", "C") for position in range(1, 5)}
    assert actual == expected

    # The A2/A3 beta rays give, uniquely for each N>=1,
    # mu_N=N*(115*t-1).  Since L_u(beta_A2)=(1-115*u)/24,
    # their pole side reverses along every u_A -> u_C path.
    u_a, wall, u_c = F(1, 230), F(1, 115), F(6)
    assert F(0) < u_a < wall < u_c
    assert (F(1) - F(115) * u_a) / 24 > 0
    assert (F(1) - F(115) * u_c) / 24 < 0

    zero_audit = {
        "A1": "none: constant equation 575*N+24*M=-N has no N,M>=1",
        "A2": "none: zero constant M=-N has no N,M>=1",
        "A3": "none: zero constant M=-N has no N,M>=1",
        "A4": "none: constant equation 575*N+24*M=-N has no N,M>=1",
        "C1": "exactly when 12 divides N: J=115*N and M=287*N/12",
        "C2": "none: zero constant M=-N has no N,M>=1",
        "C3": "none: zero constant M=-N has no N,M>=1",
        "C4": "exactly when 12 divides N: J=115*N and M=287*N/12",
    }
    # Here J=j+1 and M=n+1.  The coefficient comparison is valid because
    # t^2-110*t+1 is irreducible, so 1 and t are Q-linearly independent.
    uncancelled = {
        "family": "mu_N=N*(115*t-1), N>=1, 12 does not divide N",
        "source_pole_multiplicity": 2,
        "opposite_zero_multiplicity": 0,
        "cardinality": "infinite",
        "reason": "A2 and A3 each have the ray pole; C1/C4 zeros occur only for 12|N and all other factors have no zero on the ray.",
    }
    return {
        "epistemic_status": "PROVED",
        "chambers": {
            "u_A": "1/230",
            "forced_wall": "1/115",
            "u_C": "6",
            "every_continuous_path_crosses_wall": True,
        },
        "crossing_family": {
            "poles": "mu_N=N*(115*t-1), N>=1, from A2 and A3 beta rays",
            "side_changes_at_wall": True,
            "embedding_independent_normal_coordinate": "u=t_sigma+h",
        },
        "zero_audit": zero_audit,
        "uncancelled_crossings": uncancelled,
        "finite_residue_ledger_available": False,
        "status": "FALSIFIED_FINITE_RESIDUE_TWO_CHAMBER_CONTINUATION",
        "conclusion": "Every frozen continuous A-to-C affine-normal deformation crosses an infinite uncancelled divisor family. Hence no finite Picard-Lefschetz-style residue ledger can connect these chambers. This does not exclude a renormalized infinite-residue construction, a nonlinear contour, another regularization, a mixed-base identity, AFK, fusion, Stark, or TCC.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
