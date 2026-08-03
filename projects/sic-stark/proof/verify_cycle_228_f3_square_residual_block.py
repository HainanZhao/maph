#!/usr/bin/env python3
"""Exact ordinary-gamma residual-block audit for Cycle 228/B065."""
from __future__ import annotations

import json
from fractions import Fraction


F = Fraction


def factor(argument: F, alpha: tuple[F, F], beta: tuple[F, F]) -> dict[str, object]:
    return {"argument_mu": str(argument), "alpha": [str(x) for x in alpha], "beta": [str(x) for x in beta]}


def blocks() -> dict[str, list[dict[str, object]]]:
    # Equation (17), m=0, followed twice.  Pairs are coefficients in (omega1,omega2).
    return {
        "A": [
            factor(F(1, 24), (F(1, 24), F(5, 24)), (F(0), F(1))),
            factor(F(1, 24), (F(1), F(0)), (F(-115, 24), F(1, 24))),
            factor(F(1), (F(24), F(0)), (F(-115), F(1))),
            factor(F(1), (F(1), F(5)), (F(0), F(24))),
        ],
        "C": [
            factor(F(1, 24), (F(1, 24), F(-5, 24)), (F(0), F(1))),
            factor(F(1, 24), (F(1), F(0)), (F(115, 24), F(1, 24))),
            factor(F(1), (F(24), F(0)), (F(115), F(1))),
            factor(F(1), (F(1), F(-5)), (F(0), F(24))),
        ],
    }


def audit() -> dict[str, object]:
    rows = []
    for start, block in blocks().items():
        for index, item in enumerate(block):
            alpha = tuple(F(x) for x in item["alpha"])
            beta = tuple(F(x) for x in item["beta"])
            partner_constant = (alpha[0] + beta[0], alpha[1] + beta[1])
            # All frozen arguments are c*mu with no period constant.  Equation
            # (32)'s partner alpha+beta-c*mu has this nonzero constant.
            assert partner_constant != (F(0), F(0))
            rows.append({"start": start, "position": index + 1, "reflection_partner_period_constant": [str(x) for x in partner_constant], "reflection_match_available": False})
    assert len(rows) == 8
    return {"epistemic_status": "PROVED", "blocks": blocks(), "reflection_audit": rows, "multiplication_audit": {"equation_15_operand_available": False, "reason": "Equation (15) decomposes one rarefied gamma into a complete k=24 Delta-index product. Neither four-factor block is such an operand, and no factor is omitted to manufacture one."}, "conclusion": "Neither frozen four-factor block has a reflection pair under equation (32), and equation (15) supplies no applicable four-factor multiplication/decomposition. Both ordered blocks remain unreduced."}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
