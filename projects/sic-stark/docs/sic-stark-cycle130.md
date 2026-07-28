# SIC--Stark research cycle 130: reflection closes on the grid

Date: 2026-07-28

The normalized gamma reflection used in the primitive quotient is

\[
 (\mu,h)\longmapsto
 (\omega_1+\omega_2-\mu,-h).
\]

Using the affine grid from cycle 129, this becomes

\[
\boxed{
 (a,b)\longmapsto(1-a,-b)\pmod6.
}
\]

The affine shift by \(1\) is forced by the primitive quotient
\(a\mapsto a-1\); plain characteristic negation would be the wrong
translation. All \(36\) cases close modulo the functional-equation
lattice.

This establishes that both factors of the two-gamma kernel live on the
same finite characteristic grid. The certificate is
`scripts/dimension_six_modular_gamma_grid.py`.
