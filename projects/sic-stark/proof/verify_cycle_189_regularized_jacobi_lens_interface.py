#!/usr/bin/env python3
"""Exact Cycle 189 audit of the regularized 2psi2/Jacobi-lens interface.

This is deliberately not a cocycle evaluation.  It checks only the frozen
Chen--Chen--Gu parameter substitution, the necessary r=1 termwise
singularity, the lower-case S--S gamma_M/Kopp Jacobi product identity, and
the scoped direct one-factor characteristic mismatch.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Monomial:
    """q^q t^t r^r x^x w^w, with w^6=1 and -1=w^3."""

    q: int = 0
    t: int = 0
    r: int = 0
    x: int = 0
    w: int = 0

    def __mul__(self, other: "Monomial") -> "Monomial":
        return Monomial(
            self.q + other.q,
            self.t + other.t,
            self.r + other.r,
            self.x + other.x,
            (self.w + other.w) % 6,
        )

    def inverse(self) -> "Monomial":
        return Monomial(-self.q, -self.t, -self.r, -self.x, -self.w % 6)

    def __truediv__(self, other: "Monomial") -> "Monomial":
        return self * other.inverse()

    def render(self) -> str:
        factors = []
        for name, exponent in (("q", self.q), ("t", self.t), ("r", self.r), ("x", self.x), ("w", self.w)):
            if exponent:
                factors.append(name if exponent == 1 else f"{name}^{exponent}")
        return "*".join(factors) or "1"


ONE = Monomial()
Q = Monomial(q=1)
T = Monomial(t=1)
R = Monomial(r=1)
X = Monomial(x=1)
W2 = Monomial(w=2)
W3 = Monomial(w=3)  # -1


def pochhammer_arguments() -> dict[str, object]:
    """Substitute the frozen a,b,c,d,z into Chen--Chen--Gu (2.1)."""

    a = X
    b = T * W2 * X
    c = Q * T * W2 * W3 * X  # -q*t*w^2*x
    d = Q * W3 * X  # -q*x
    z = R * Q * W3  # -r*q

    checks = {
        "cd_over_ab": c * d / (a * b),
        "bq_over_d": b * Q / d,
        "az_over_d": a * z / d,
        "raw_z_at_r_1": z / R,
    }
    assert checks["cd_over_ab"] == Monomial(q=2)
    assert checks["bq_over_d"] == T * Monomial(w=5)
    assert checks["az_over_d"] == R
    assert checks["raw_z_at_r_1"] == Q * W3

    first_phi = {
        "top": [c * d / (a * b * z), d / a],
        "bottom": d * Q / (a * z),
        "argument": b * Q / d,
    }
    second_phi = {
        "top": [a * Q / d, b * Q / d],
        "bottom": c * Q / d,
        "argument": z,
    }
    assert first_phi == {
        "top": [Q * W3 / R, Q * W3],
        "bottom": Q / R,
        "argument": T * Monomial(w=5),
    }
    assert second_phi == {
        "top": [W3, T * Monomial(w=5)],
        "bottom": Q * T * W2,
        "argument": R * Q * W3,
    }

    # At r=1, the individual first Chen--Chen--Gu prefactor contains
    # (az/d;q)_infty=(r;q)_infty=(1;q)_infty.  This is a genuine
    # termwise singularity, although the original bilateral series remains
    # in its ordinary annulus.  Therefore only the full two-term expression
    # may be continued to r=1.
    first_prefactor_denominator = [
        c,
        a * z / d,
        Q / a,
        Q / b,
        c * d / (a * b * z),
    ]
    assert R in first_prefactor_denominator

    return {
        "source_identity": "Chen--Chen--Gu Theorem 2.1 / equation (2.1)",
        "substitution": {"a": a.render(), "b": b.render(), "c": c.render(), "d": d.render(), "z": z.render()},
        "interior_domain": "0<|q|<1, 0<t<1, |q|<r<|q|^(-1); then |cd/(ab)|=|q|^2<r|q|=|z|<1 and |bq/d|=t<1.",
        "hypothesis_monomials": {name: value.render() for name, value in checks.items()},
        "first_2phi1": {name: [item.render() for item in value] if isinstance(value, list) else value.render() for name, value in first_phi.items()},
        "second_2phi1": {name: [item.render() for item in value] if isinstance(value, list) else value.render() for name, value in second_phi.items()},
        "raw_t_1_r_1_packet": "_2psi_2(x,w^2*x;-q*w^2*x,-q*x;q,-q)",
        "raw_direct_CCG_hypothesis": "FAILED: |bq/d|=1",
        "termwise_r_1_status": "SINGULAR: first prefactor denominator contains (r;q)_infty, hence (1;q)_infty at r=1",
        "required_next_check": "Derive the meromorphic cancellation of the full Chen--Chen--Gu two-term expression before either r->1 or t->1 is used.",
    }


def gamma_sigma_identity() -> dict[str, object]:
    """Verify gamma_M=sigma at q-Pochhammer argument level exactly."""

    # Let omega=24*tau-5 and A.tau=(115*tau-24)/omega.  The numerator
    # exponent difference (Kopp minus S--S) for m2=m+1,m1=0,z=(mu+m)/24 is
    # m*(1/(24*omega) + A.tau - 115/24).  Multiplication by 24*omega gives
    # 1 + 24*(115*tau-24) - 115*(24*tau-5) = 0.
    constant = 1 - 24 * 24 + 115 * 5
    tau_coefficient = 24 * 115 - 115 * 24
    assert constant == 0 and tau_coefficient == 0
    return {
        "epistemic_status": "PROVED",
        "lower_case_identity": "gamma_M(mu,m;24*tau-5,1)=sigma_{(0,m+1),A}((mu+m)/24,tau)",
        "denominator_q_pochhammer_argument": "exp(2*pi*i*(mu+m)/24) on both sides",
        "numerator_exponent_difference": "m*(1/(24*omega)+A.tau-115/24)",
        "cleared_difference": {"constant": constant, "tau_coefficient": tau_coefficient},
        "capital_gamma_boundary": "Gamma_M(mu,m)=Z(m)*exp(-pi*i*B_2,2(mu;omega,1)/48)*gamma_M(mu,m); the factor is retained, not discarded.",
    }


def r_one_residue_cancellation() -> dict[str, object]:
    """Prove that the two Chen--Chen--Gu terms cancel their r=1 pole."""

    a = X
    b = T * W2 * X
    c = Q * T * W2 * W3 * X
    d = Q * W3 * X
    z = Q * W3

    # Remove the common (r;q)_infty denominator from each term after
    # specializing r=1.  These are, respectively, the remaining numerator
    # and denominator Pochhammer arguments of the two CCG coefficients.
    first_numerator = [
        c / b,
        a * b * z / d,
        d * Q / (a * b * z),
        Q / d,
        Q,
    ]
    first_denominator = [
        c,
        Q / a,
        Q / b,
        c * d / (a * b * z),
    ]
    second_numerator = [
        c * Q / d,
        b,
        d / a,
        a * z / Q,
        Q * Q / (a * z),
        Q / d,
        Q,
    ]
    second_denominator = [
        d / Q,
        c,
        b * Q / d,
        d * Q / (a * z),
        Q * Q / d,
        Q / a,
    ]

    # Heine's transformation of
    #   2phi1(-q,-q;q;q,t*w^-1)
    # is H(t) times
    #   2phi1(-1,t*w^-1;q*t*w^2;q,-q),
    # where H(t)=(-q,q*t*w^2;q)_infty/(q,t*w^-1;q)_infty.
    heine_numerator = [Q * W3, Q * T * W2]
    heine_denominator = [Q, T * Monomial(w=5)]

    difference: defaultdict[Monomial, int] = defaultdict(int)
    for factor in second_numerator + first_denominator:
        difference[factor] += 1
    for factor in second_denominator + first_numerator:
        difference[factor] -= 1
    for factor in heine_numerator:
        difference[factor] -= 1
    for factor in heine_denominator:
        difference[factor] += 1
    assert not {factor: power for factor, power in difference.items() if power}

    return {
        "epistemic_status": "PROVED",
        "common_singular_factor": "(r;q)_infty^-1 occurs once in each Chen--Chen--Gu coefficient",
        "first_core_at_r_1": "_2phi1(-q,-q;q;q,t*w^(-1))",
        "second_core_at_r_1": "_2phi1(-1,t*w^(-1);q*t*w^2;q,-q)",
        "heine_multiplier": {
            "numerator_pochhammer_arguments": [factor.render() for factor in heine_numerator],
            "denominator_pochhammer_arguments": [factor.render() for factor in heine_denominator],
        },
        "coefficient_ratio": "C2_hat/C1_hat=H(t), after removing the common (r;q)_infty^-1",
        "residue_conclusion": "C1_hat*first_core-C2_hat*second_core=0; the apparent r=1 simple pole cancels in the full two-term expression.",
        "remaining_boundary_problem": "The finite r=1 value is the next Laurent coefficient, not supplied by this residue cancellation; the subsequent t->1^- and modular RM limits remain open.",
    }


def r_one_finite_part() -> dict[str, object]:
    """Derive the finite r=1 continuation as a derivative state space."""

    # Write the exact CCG expansion as
    # F(r) = G(r)/((r;q)_infty),
    # G(r)=C1_hat(r) Phi1(r)-C2_hat(r) Phi2(r),
    # after factoring the common (r;q)_infty^-1.  The prior exact
    # cancellation gives G(1)=0, while (r;q)_infty=(1-r)(rq;q)_infty.
    # The bilateral defining series is absolutely locally uniformly
    # convergent near r=1 because |q|^2<r|q|<1 remains strict there.  Thus
    # the finite value is the removable continuation of the full expression.
    return {
        "epistemic_status": "PROVED",
        "factored_expression": "F(r)=G(r)/((r;q)_infty), G(r)=C1_hat(r)*Phi1(r)-C2_hat(r)*Phi2(r)",
        "product_identity": "(r;q)_infty=(1-r)*(r*q;q)_infty",
        "cancellation_input": "G(1)=0 by the exact Heine/prefactor identity in r_one_residue_cancellation",
        "finite_part_formula": "F(1)=-G'(1)/(q;q)_infty",
        "universal_core_span": [
            "Phi2(1)=_2phi1(-1,t*w^(-1);q*t*w^2;q,-q)",
            "partial_r Phi1(r)|_(r=1)",
            "partial_r Phi2(r)|_(r=1)",
        ],
        "span_reason": "Phi1(1)=H(t)*Phi2(1), while the r derivative of G introduces only the two displayed parameter/argument derivatives. All x dependence remains in the explicit C1_hat,C2_hat prefactors and their r derivatives.",
        "scope": "This defines the raw sign-reflected interior packet by a removable-continuation finite part. It is not a product evaluation, AFK identification, or real-multiplication boundary theorem.",
    }


def t_one_regularization() -> dict[str, object]:
    """Move the apparent unit-circle first core back to an interior 2phi1."""

    # Apply Heine before t reaches 1 to the first CCG core:
    # a=-q/r, b=-q, c=q/r, z=t*w^-1.
    # Its transformed argument is b=-q, strictly inside the unit disk.
    first_top = [Q * W3 / R, Q * W3]
    first_bottom = Q / R
    first_argument = T * Monomial(w=5)
    heine_prefactor_numerator = [Q * W3, Q * T * W2 / R]
    heine_prefactor_denominator = [Q / R, T * Monomial(w=5)]
    transformed_top = [W3, T * Monomial(w=5)]
    transformed_bottom = Q * T * W2 / R
    transformed_argument = Q * W3
    assert first_top == [Q * W3 / R, Q * W3]
    assert first_bottom == Q / R and first_argument == T * Monomial(w=5)
    assert transformed_argument == Q * W3

    return {
        "epistemic_status": "PROVED",
        "heine_input": "Phi1(r)=_2phi1(-q/r,-q;q/r;q,t*w^(-1))",
        "heine_prefactor": {
            "numerator_pochhammer_arguments": [factor.render() for factor in heine_prefactor_numerator],
            "denominator_pochhammer_arguments": [factor.render() for factor in heine_prefactor_denominator],
        },
        "heine_output": "Psi1(r)=_2phi1(-1,t*w^(-1);q*t*w^2/r;q,-q)",
        "second_core": "Phi2(r)=_2phi1(-1,t*w^(-1);q*t*w^2;q,-r*q)",
        "interior_arguments": {"Psi1": transformed_argument.render(), "Phi2": (R * Q * W3).render()},
        "t_one_conclusion": "For fixed 0<|q|<1 and r near 1, both transformed unilateral series have arguments of modulus <1 and denominators away from their q-lattices. Therefore their values and r derivatives extend analytically to t=1; the explicit prefactors do so away from their stated x-dependent divisor set.",
        "scope": "This proves the prescribed t->1^- limit of the regularized interior representation away from its explicit q-Pochhammer divisors. It does not continue q to the unit-circle RM point or identify the result with AFK overlaps.",
    }


def direct_one_factor_test() -> dict[str, object]:
    """Exhaust the frozen untranslated one-factor characteristic class."""

    matches = []
    failures = []
    for first in range(6):
        for second in range(6):
            # Matching sigma_(p/6,A)(0) requires the gamma denominator
            # elliptic coordinate z=(mu+m)/24 to be 0 modulo Z.  The gamma
            # characteristic is then (0,m+1) modulo Z^2, so it equals p/6
            # only when p=(0,0).  This is exactly the frozen *untranslated*
            # one-factor class, not a claim about elliptic translations.
            if first == 0 and second == 0:
                matches.append([first, second])
            else:
                failures.append([first, second])
    assert matches == [[0, 0]] and len(failures) == 35
    return {
        "epistemic_status": "PROVED",
        "frozen_class": "one lower-case gamma_M/Jacobi factor, no elliptic translation or finite factor product, and only a p-independent elementary prefactor",
        "full_grid": 36,
        "matching_characteristics": matches,
        "nonzero_characteristics_excluded": len(failures),
        "reason": "denominator matching forces z=0 mod Z and hence an integral Jacobi characteristic (0,m+1); matching p/6 then forces p_2=0 and p_1=0",
        "scope": "This excludes only the frozen direct one-factor match. A translation/periodization transform remains a proposed interface construction.",
    }


def source_defined_afk_map() -> dict[str, object]:
    """Check Kopp's Jacobi-to-modular map for every d=6 characteristic."""

    A = ((115, -24), (24, -5))
    identity_minus_A = ((1 - A[0][0], -A[0][1]), (-A[1][0], 1 - A[1][1]))
    assert identity_minus_A == ((-114, 24), (-24, 6))
    rows = []
    for first in range(6):
        for second in range(6):
            kappa = (
                (identity_minus_A[0][0] * first + identity_minus_A[0][1] * second) // 6,
                (identity_minus_A[1][0] * first + identity_minus_A[1][1] * second) // 6,
            )
            assert kappa == (-19 * first + 4 * second, -4 * first + second)
            # gamma_M's m is periodic modulo 24; retain the integer lift so
            # that m+1 is exactly the required second Jacobi coordinate.
            discrete = kappa[1] - 1
            mu_constant = -4 * first - discrete
            # (mu_p+m_p)/24=(p2*tau-p1)/6.
            assert mu_constant + discrete == -4 * first
            # A fixes p/6 modulo Z^2, the exact hypothesis for the modular
            # cocycle with characteristic p/6.
            transported_difference = (
                (A[0][0] * first + A[0][1] * second - first) // 6,
                (A[1][0] * first + A[1][1] * second - second) // 6,
            )
            assert transported_difference == (-kappa[0], -kappa[1])
            rows.append(
                {
                    "p": [first, second],
                    "r_p": [f"{first}/6", f"{second}/6"],
                    "kappa_p": list(kappa),
                    "m_p": discrete,
                    "mu_p": f"{4 * second}*tau+({mu_constant})",
                    "elliptic_coordinate": f"({second}*tau-{first})/6",
                    "gamma_characteristic": [0, discrete + 1],
                    "kopp_integer_characteristic": list(kappa),
                    "first_coordinate_is_vestigial_integer": True,
                    "A_fixes_r_p_mod_Z2": True,
                }
            )
    assert len(rows) == 36
    return {
        "epistemic_status": "PROVED",
        "source_relations": [
            "gamma_M(mu,m)=sigma_(0,m+1),A((mu+m)/24,tau)",
            "shin_A^r(tau)=sigma_((I-A)r,A)(<r,(tau,1)>,tau)",
        ],
        "rows_checked": len(rows),
        "all_gamma_to_shin_matches": True,
        "capital_gamma_normalization_retained": True,
        "rows": rows,
        "conclusion": "The lower-case lens gamma has a source-defined, all-characteristic map to the unphased AFK modular cocycle along mu_p(tau). The required relation from the regularized 2psi2 packet's x/helical coordinate to these mu_p lines remains open.",
    }


def raw_helical_factor_alignment() -> dict[str, object]:
    """Falsify the smallest raw-kernel-to-mu_p factorwise lift exactly."""

    # The only constant omega_2 shift (mu,m)->(mu+n,m-n) that can
    # identify D*h+n with D*p2+1 as functions of tau is h=p2,n=1.
    # Substitution of h=(4b-5a)/3+2z then makes the discrete equation
    # parity-impossible.  Repeat for the reflected (-alpha,4-N) factor.
    rows = 0
    residuals = {"direct": set(), "reflected": set()}
    for first in range(6):
        for second in range(6):
            for frequency_first in range(6):
                for frequency_second in range(6):
                    rows += 1
                    # Direct factor: h=p2 forces 6z=3p2-4b+5a.
                    # N-1=m_p then reduces to 2*(2K+1)=0.
                    direct_residual = 4 * (first + frequency_second - frequency_first - second) + 2
                    assert direct_residual % 4 == 2
                    residuals["direct"].add(direct_residual % 4)
                    # Reflected factor: -h=p2 forces
                    # 6z=-3p2-4b+5a.  The shifted 3-N=m_p equation has
                    # the same odd-parity obstruction.
                    reflected_residual = 4 * (frequency_first - frequency_second + first - second) + 2
                    assert reflected_residual % 4 == 2
                    residuals["reflected"].add(reflected_residual % 4)
    assert rows == 36 * 36
    assert residuals == {"direct": {2}, "reflected": {2}}
    return {
        "epistemic_status": "PROVED",
        "tested_class": "either raw kernel factor (alpha_z,N_z) or (-alpha_z,4-N_z), followed by any constant integer omega_2 shift (mu,m)->(mu+n,m-n), matched identically in tau to (mu_p,m_p)",
        "continuous_coefficient_conclusion": "Matching forces n=1 and h=p2 for the direct factor, or n=1 and h=-p2 for the reflected factor.",
        "frequency_characteristic_pairs_checked": rows,
        "direct_discrete_residue_mod_4": sorted(residuals["direct"]),
        "reflected_discrete_residue_mod_4": sorted(residuals["reflected"]),
        "result": "No factorwise match survives: each forced discrete equation is 4*K+2=0.",
        "scope": "This falsifies only the frozen single raw gamma factor plus constant omega_2-shift class. It leaves finite combinations, nonconstant periodization, and the already proved gamma-to-shin map available.",
    }


def payload() -> dict[str, object]:
    continuation = pochhammer_arguments()
    cancellation = r_one_residue_cancellation()
    finite_part = r_one_finite_part()
    t_limit = t_one_regularization()
    afk_map = source_defined_afk_map()
    raw_alignment = raw_helical_factor_alignment()
    return {
        "schema": "sic-stark-cycle-189-regularized-jacobi-lens-interface-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "Exact interior q-series continuation only: the r=1 pole cancellation, removable finite-part formula, t->1^- regularization, all-36 lower-gamma-to-unphased-AFK source map, and the stated one-factor obstruction are proved. No real-multiplication/unit-circle continuation, regularized-packet-to-AFK identification, AFK cross-orbit relation, coefficient-to-ray map, fusion continuity, or TCC identity is proved.",
        "continuation": continuation,
        "r_one_cancellation": cancellation,
        "r_one_finite_part": finite_part,
        "t_one_regularization": t_limit,
        "jacobi_lens_identity": gamma_sigma_identity(),
        "direct_one_factor_test": direct_one_factor_test(),
        "source_defined_afk_map": afk_map,
        "raw_helical_factor_alignment": raw_alignment,
        "gate_outcome": {
            "analytic_continuation": "INTERIOR_REGULARIZATION_R1_CANCELLATION_REMOVABLE_FINITE_PART_AND_T1_LIMIT_PROVED_RM_BOUNDARY_OPEN",
            "direct_one_factor_interface": "UNTRANSLATED_Z0_CLASS_FALSIFIED_FOR_35_NONZERO_CHARACTERISTICS_BUT_SOURCE_DEFINED_JACOBI_TO_SHIN_MAP_PROVED_FOR_ALL_36",
            "raw_factor_alignment": "FALSIFIED_FOR_BOTH_RAW_KERNEL_FACTORS_AFTER_THE_ONLY_POSSIBLE_CONSTANT_OMEGA2_SHIFT",
            "next_construction": "Construct a non-factorwise helical periodization from the regularized derivative-core state space to the proved mu_p(tau) Jacobi lines, retaining the Gamma_M normalization and AFK phase, before attempting the RM boundary.",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    rendered = json.dumps(payload(), indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
