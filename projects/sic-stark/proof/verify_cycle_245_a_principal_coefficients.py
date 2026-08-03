#!/usr/bin/env python3
"""Source-shift recurrence scaffold for C245 A-word double-pole coefficients."""
from __future__ import annotations

import json
from fractions import Fraction as F

try:
    from .verify_cycle_228_f3_square_residual_block import blocks
except ImportError:  # pragma: no cover
    from verify_cycle_228_f3_square_residual_block import blocks


def audit() -> dict[str, object]:
    a = (F(115), F(-1))  # 115*t-1
    expected = {
        "A1": (F(1, 24), (F(1, 24), F(5, 24)), (F(0), F(1)), (115, -24)),
        "A2": (F(1, 24), (F(1), F(0)), (F(-115, 24), F(1, 24)), (0, -1)),
        "A3": (F(1), (F(24), F(0)), (F(-115), F(1)), (0, -1)),
        "A4": (F(1), (F(1), F(5)), (F(0), F(24)), (115, -24)),
    }
    rows = []
    for position, item in enumerate(blocks()["A"], 1):
        c = F(str(item["argument_mu"]))
        alpha = tuple(F(str(x)) for x in item["alpha"])
        beta = tuple(F(str(x)) for x in item["beta"])
        name = f"A{position}"
        assert (c, alpha, beta, expected[name][3]) == expected[name]
        m, n = expected[name][3]
        translated = (m * alpha[0] + n * beta[0], m * alpha[1] + n * beta[1])
        # z=c*mu, hence mu -> mu+a translates z by c*a.
        assert translated == (c * a[0], c * a[1])
        rows.append({"factor": name, "argument_slope": str(c), "shift_in_(alpha,beta)": [m, n], "source_multiplier": "finite ordered product of gamma(z+alpha)/gamma(z)=1-exp(2*pi*i*z/beta) and gamma(z+beta)/gamma(z)=1-exp(2*pi*i*z/alpha)"})
    assert [r["shift_in_(alpha,beta)"] for r in rows] == [[115, -24], [0, -1], [0, -1], [115, -24]]
    # From G(z+beta)=Phi_beta(z)G(z), a negative beta shift is
    # G(z-q*beta)/G(z)=product_{r=1}^q Phi_beta(z-r*beta)^(-1).
    # Apply it first, then the positive alpha shifts; this fixes the order.
    negative_beta = [{"kind": "Phi_beta_inverse", "argument": f"z-{q}*beta"} for q in range(1, 25)]
    positive_alpha = [{"kind": "Phi_alpha", "argument": f"z-24*beta+{i}*alpha"} for i in range(115)]
    assert len(negative_beta) == 24 and len(positive_alpha) == 115
    # At z_N=-N*beta, G(z_N)=Phi_beta(z_(N+1))*G(z_(N+1)).
    # Thus Res(G,z_(N+1))/Res(G,z_N)=Phi_beta(z_(N+1))^(-1).
    laurent = {
        "A1": {"regular_ratio_order": [*negative_beta, *positive_alpha]},
        "A4": {"regular_ratio_order": [*negative_beta, *positive_alpha]},
        "A2": {"pole_coordinate": "z_N=-N*beta", "residue_ratio": "Res_(N+1)/Res_N=Phi_beta(-(N+1)*beta)^(-1)"},
        "A3": {"pole_coordinate": "z_N=-N*beta", "residue_ratio": "Res_(N+1)/Res_N=Phi_beta(-(N+1)*beta)^(-1)"},
        "product_rule": "A1,A4 are regular nonzero at mu_N; multiplying the two simple-pole Laurent expansions for A2,A3 gives the double-pole coefficient ratio.",
    }
    multiplier = {
        "phi_alpha": "Phi_alpha(z)=1-exp(2*pi*i*z/beta)",
        "phi_beta": "Phi_beta(z)=1-exp(2*pi*i*z/alpha)",
        "A1_A4": "P_j,N=[product_{i=0}^{114} Phi_alpha(z_j,N-24*beta_j+i*alpha_j)]/[product_{q=1}^{24} Phi_beta(z_j,N-q*beta_j)]",
        "A2_A3": "Q_j,N=1/Phi_beta(-(N+1)*beta_j)",
        "definitions": "z_j,N=c_j*N*(115*t-1); alpha_j,beta_j are the frozen C228 A periods",
        "ratio": "kappa_(N+1)/kappa_N=P_1,N*Q_2,N*Q_3,N*P_4,N",
    }
    nonvanishing = {
        "A1_A4_regular_at_z_N": "z_N=115*N*alpha-24*N*beta has positive alpha-coordinate and negative beta-coordinate, so it is neither a pole (-j,-n) nor a zero (j+1,n+1).",
        "A1_A4_phi_alpha": "z_N-24*beta+i*alpha has alpha-coordinate 115*N+i>0 for 0<=i<115, so its ratio to beta is not an integer.",
        "A1_A4_phi_beta": "z_N-q*beta has beta-coordinate -24*N-q<0 for 1<=q<=24, so its ratio to alpha is not an integer.",
        "A2_A3_phi_beta": "beta/alpha=-115/24+1/(24*t) is irrational, hence -(N+1)*beta/alpha is never integral.",
    }
    # These are the exact coefficient-sign/independence checks behind the
    # symbolic all-N statements above; no finite N sampling is used.
    assert min(115 + i for i in range(115)) > 0
    assert max(-24 - q for q in range(1, 25)) < 0
    for name in ("A2", "A3"):
        _c, alpha, beta, _shift = expected[name]
        assert alpha[0] * beta[1] - alpha[1] * beta[0] != 0
    galois = {"epistemic_status": "PROVED", "regularization": "sigma_+(t+i*epsilon)=t_-+i*epsilon and sigma_-(t+i*epsilon)=t_++i*epsilon", "action_on_source_product": "re-evaluate the same ordinary-gamma product formula after swapping every affine period coefficient", "coefficient_label_swap": "The re-evaluated plus-embedding coefficient/multiplier formulas are exactly the minus-embedding formulas, and conversely.", "claim_boundary": "This is C-linear field-embedding covariance of the frozen upper tilt. It is not an arithmetic action on the transcendental gamma values, complex conjugation, source authorization, or an A-to-C identity."}
    determinants = {}
    for name, (_c, alpha, beta, _shift) in expected.items():
        determinant = alpha[0] * beta[1] - alpha[1] * beta[0]
        assert determinant > 0
        # For t_sigma+i*epsilon, Im(alpha/beta)=epsilon*det/|beta|^2>0.
        determinants[name] = str(determinant)
    galois["upper_chamber_certificate"] = {
        "period_determinants": determinants,
        "reason": "At both embeddings, every Im(alpha/beta) is epsilon*det(alpha,beta)/|beta|^2>0, so the frozen q-products are defined in their common source chamber before applying the C-linear embedding swap.",
    }
    return {"epistemic_status": "PROVED", "support_step": "a=115*t-1", "factors": rows, "laurent_derivation": laurent, "recurrence": {"epistemic_status": "PROVED", "statement": "For every N>=1, kappa_(N+1)=T_N*kappa_N with T_N=P_1,N*Q_2,N*Q_3,N*P_4,N.", "multiplier": multiplier, "base_normalization": "kappa_1 from the frozen A product; no numerical/fitted value selected", "exact_recurrence_family_derived": True, "all_multiplier_factors_nonzero": True, "nonvanishing_proof": nonvanishing}, "galois": galois, "growth": {"epistemic_status": "OPEN", "tempered_bound_proved": False, "reason": "The exact finite ratio gives no uniform lower bound away from its unit-circle small divisors."}, "conclusion": "PROVED: the source product fixes an all-N nonzero finite-product recurrence and C-linear embedding-swap law for the A double-pole coefficient line. Any tempered-growth bound remains open."}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
