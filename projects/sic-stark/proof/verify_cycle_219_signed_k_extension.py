#!/usr/bin/env python3
"""Exact diagonal signed-k extension census for Cycle 219/B056."""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path


def coordinate_sign_census() -> dict[str, object]:
    """Compare raw and positive-product coordinates coefficient by coefficient.

    The negative state has parameters (-p,-k,-r,-s).  A diagonal candidate
    feeds (a*mu,b*m;c*omega1,d*omega2) into the positive product with
    parameters (p,k,r,s).  Equality is checked for tau, u and tilde-u before
    any Pochhammer, reflection, or normalization manipulation.
    """
    rows = []
    survivors = []
    for a, b, c, d in itertools.product((-1, 1), repeat=4):
        # Coefficients relative to the raw coordinates.  Equality to 1 in
        # every slot is necessary and sufficient as p,k are nonzero.
        tau_omega1 = -c * d
        tau_r = 1
        u_mu = -a * d
        u_m = -b
        tilde_mu = -a * c
        tilde_pm = b
        tau_ok = tau_omega1 == 1 and tau_r == 1
        u_ok = u_mu == 1 and u_m == 1
        tilde_ok = tilde_mu == 1 and tilde_pm == 1
        row = {"signs": {"mu": a, "m": b, "omega1": c, "omega2": d}, "tau": tau_ok, "u": u_ok, "tilde_u": tilde_ok}
        rows.append(row)
        if tau_ok and u_ok and tilde_ok:
            survivors.append(row)
    assert len(rows) == 16
    assert not survivors
    # Solving tau and u gives a=c=-d and b=-1, which forces both the mu and
    # pm coefficients of tilde-u to -1 and supplies a symbolic contradiction.
    constrained = [row for row in rows if row["tau"] and row["u"]]
    assert len(constrained) == 2
    assert all(not row["tilde_u"] for row in constrained)
    return {"epistemic_status": "PROVED", "candidates": rows, "candidate_count": len(rows), "survivor_count": 0, "tau_and_u_candidates": constrained, "symbolic_conflict": "tau=u=1 forces a=c=-d and b=-1, hence tilde-u has mu coefficient -a*c=-1 and pm coefficient b=-1.", "conclusion": "No diagonal sign lift preserves tau, u, and tilde-u simultaneously."}


def extension_axiom_audit() -> dict[str, object]:
    census = coordinate_sign_census()
    assert census["survivor_count"] == 0
    return {"epistemic_status": "PROVED", "agreement_with_positive_product": False, "involutivity_tested": False, "reflection_tested": False, "shift_tested": False, "factorization_tested": False, "reason": "No diagonal lift reaches the defining product-coordinate domain, so downstream axioms would test an undefined extension rather than a constructed function."}


def run() -> dict[str, object]:
    census = coordinate_sign_census()
    axioms = extension_axiom_audit()
    return {"schema": "sic-stark-cycle-219-signed-k-extension-prototype-v1", "epistemic_status": "PROVED", "claim_boundary": "All 16 diagonal sign lifts of the raw negative-k coordinates fail to preserve the three defining product coordinates tau, u, and tilde-u simultaneously. Consequently this diagonal family supplies no signed-k Gamma_M extension and cannot satisfy downstream axioms. This does not exclude a non-diagonal extension involving reflection, theta/Pochhammer factors, additive shifts, period swaps, a new source theorem, a packet cocycle, AFK covariance, fusion, Stark, or TCC.", "coordinate_sign_census": census, "extension_axiom_audit": axioms, "gate_outcome": {"diagonal_signed_k_extension": "FALSIFIED", "remaining_design_problem": "Construct a non-diagonal signed-k extension with an explicit correction factor and prove its product/reflection/shift/factorization compatibility before any affine E comparison."}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
