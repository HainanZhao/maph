# SIC--Stark research cycle 54: finite minor reduction

## Result

For one \(7\times7\) matrix there are

\[
\binom72^2=441
\]

rank-two minors.  The two formal shifts therefore give \(882\) displayed
minors, but they depend on only eight reciprocal Zauner-orbit variables.

Direct evaluation gives

\[
\max|\text{minor}|<2.16\cdot10^{-10}
\]

for each shift.

The exact finite proof should not expand \(882\) unrelated expressions.
The efficient certificate is:

1. adjoin one selected positive root for each of the eight reciprocal
   orbit pairs;
2. reduce matrix entries in
   \(K(\zeta_7)\) and the four ray-field strata;
3. use the reciprocal class polynomials to reduce powers;
4. quotient by Zauner and parity actions; and
5. verify orbit representatives of the minor ideal.

`scripts/dimension_seven_symbolic_reduction.py` records the exact 16
orbits, their eight reciprocal pairs, and the minor counts.

## Gate

No evidence of a new analytic identity appeared.  The obstruction is now
purely certificate engineering: exact root selection and reduction in a
degree-\(24\) ray field.

