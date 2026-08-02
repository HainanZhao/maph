"""Cycle 124 bilinear sparse-exponential self-duality ledger."""

from __future__ import annotations

from fractions import Fraction


def exponent_ledger(xi: Fraction) -> dict[str, Fraction]:
    if not Fraction(16, 25) <= xi < Fraction(58, 75):
        raise ValueError("xi outside lower band")
    atom_count = Fraction(14, 15)  # DQ
    return {
        "one_polynomial_length": atom_count,
        "trivial_bilinear": xi + 2 * atom_count,
        "diagonal_second_moment": xi + atom_count,
        "alias_target": xi + atom_count,
        "required_trivial_saving": atom_count,
    }


def theorem_record() -> dict[str, object]:
    return {
        "mode_change": (
            "a=u,b=u+v, alpha=q0/p0; the phase is "
            "e(-ell n'g^a)e(-ell alpha m g^b)"
        ),
        "tensor_separation": (
            "every fixed smooth compact coupled symbol in "
            "(ell/K,n'g^a/Q,alpha m g^b/Q) has, for each epsilon,A>0, "
            "a tensor expansion of rank O(X^epsilon), l1 coefficient norm "
            "O(X^epsilon), and uniform error O(X^(-A))"
        ),
        "polynomial": (
            "T_alpha(ell)=sum_(a,n) w_alpha(a,n;ell)e(-ell alpha n g^a), "
            "with a-length D and n-length Q"
        ),
        "bilinear_reduction": (
            "the Cycle-123 operator is, up to X^epsilon separated terms and "
            "power-negligible error, sum_(ell~K) T_1(ell)T_alpha(ell)"
        ),
        "cauchy_target": (
            "if sum|T_1|^2 and sum|T_alpha|^2 are both O(KDQ X^epsilon), "
            "Cauchy gives O(KDQ X^epsilon), exactly the Cycle-87 target"
        ),
        "self_duality": (
            "T_alpha is the Cycle-87 primal sparse-exponential polynomial "
            "with a bounded rational anchor, up to sign, smooth weights, and "
            "tensor-frequency shifts; the transform is norm-neutral at the "
            "diagonal second-moment level"
        ),
        "inverse": (
            "if one separated bilinear term exceeds L*K*D*Q, then at least "
            "one of its two normalized second moments exceeds diagonal size "
            "by a factor at least L, yielding a labelled pair-collision energy witness"
        ),
        "boundary": (
            "self-duality is scoped to tensor separation plus Cauchy and diagonal "
            "second moments; it does not exclude correlated bilinear cancellation "
            "or prove simple-root closure, a complete moment, density, or intervals"
        ),
    }
