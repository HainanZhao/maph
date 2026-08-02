"""Cycle 133 determinant-labelled cluster energy ledger."""

from __future__ import annotations

from fractions import Fraction

Matrix2 = tuple[tuple[int, int], tuple[int, int]]


def matmul(a: Matrix2, b: Matrix2) -> Matrix2:
    return (
        (a[0][0] * b[0][0] + a[0][1] * b[1][0], a[0][0] * b[0][1] + a[0][1] * b[1][1]),
        (a[1][0] * b[0][0] + a[1][1] * b[1][0], a[1][0] * b[0][1] + a[1][1] * b[1][1]),
    )


def determinant(a: Matrix2) -> int:
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def inverse_unimodular(a: Matrix2) -> Matrix2:
    det = determinant(a)
    if det not in (-1, 1):
        raise ValueError("matrix is not unimodular")
    return (
        (det * a[1][1], -det * a[0][1]),
        (-det * a[1][0], det * a[0][0]),
    )


def transition(a: Matrix2, b: Matrix2) -> Matrix2:
    """Return T_{a,b}=U_b U_a^{-1}."""
    return matmul(b, inverse_unimodular(a))


def energy_ledger(xi: Fraction, mu: Fraction) -> dict[str, Fraction]:
    if not Fraction(16, 25) <= xi < Fraction(58, 75):
        raise ValueError("xi outside lower band")
    if not 0 <= mu <= (1 - xi) / 4:
        raise ValueError("mu outside low-multiplicity range")
    exact_ceiling = (xi + Fraction(1, 3)) / 4
    hs_ceiling = Fraction(7, 45) - 2 * mu / 3
    full_ceiling = Fraction(1, 3) - mu
    return {
        "exact_ceiling": exact_ceiling,
        "hs_ceiling": hs_ceiling,
        "extension_beyond_hs": exact_ceiling - hs_ceiling,
        "full_ceiling": full_ceiling,
        "nonexact_width": full_ceiling - exact_ceiling,
        "threshold_energy_exponent": Fraction(11, 15) - 4 * mu,
    }


def theorem_record() -> dict[str, object]:
    return {
        "integer_forcing": (
            "an additive mode quadruple has rational-label product error "
            "O(1/(NS)); a nonzero difference of products has size >>N^{-4}, "
            "so S>>N^3 forces x1*x2=x3*x4 exactly"
        ),
        "forced_region": (
            "because S>>KQ/N, exactness is automatic for "
            "rho<(xi+1/3)/4; this exceeds the Cycle-131 ceiling by at least 79/900"
        ),
        "remaining_width": (
            "between the exactness ceiling and rho=1/3-mu, the exponent width "
            "is exactly (1-xi)/4-mu and vanishes at maximal low multiplicity"
        ),
        "energy": (
            "a hit set of size L has additive energy at least L^4/(2D-1); "
            "at L=Q/M its exponent is 11/15-4mu"
        ),
        "valuation_web": (
            "inside the exact region every prime valuation of x_a is a Freiman "
            "2-homomorphism on the additive quadruples of the hit set"
        ),
        "matrix_cocycle": (
            "U_a=[[P_a,p_a],[R_a,q_a]] lies in GL_2(Z), and "
            "T_{a,b}=U_b U_a^{-1} obeys T_{b,c}T_{a,b}=T_{a,c} with "
            "det(T_{a,b})=s_a*s_b"
        ),
        "missing_invariant": (
            "energy and the cocycle law do not force a repeated-difference "
            "transition T_{a,a+d} to recur; chain depth needs concentration of "
            "these transition matrices, or an equivalent phase-anchored edge invariant"
        ),
        "boundary": (
            "no transition concentration, recurrence seed, endpoint, lower moment, "
            "density, or prime-interval theorem is proved"
        ),
    }
