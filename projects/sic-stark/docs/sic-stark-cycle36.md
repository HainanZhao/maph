# SIC--Stark research cycle 36: the root number does not orient the unit

Date: 2026-07-27

## Outcome

The primitive global root numbers are

\[
 W(\chi_1)=i,\qquad W(\chi_5)=-i.
\]

This is convention-compatible with the arithmetic Frobenius orientation
already certified in cycle 27.  It does not determine the missing Stark
phase.

The functional equation has the schematic form

\[
 L'_S(0,\chi_1)
 =
 i\,C\,L_S(1,\bar\chi_1),
 \qquad C>0.
\]

The value \(L_S(1,\bar\chi_1)\) is itself complex and noncritical.  The
root number fixes the quarter-turn between the two sides but imposes no
positivity or reality condition on that value.

Numerically,

\[
 \arg L'_S(0,\chi_1)=1.177\ldots,
\qquad
 \arg\!\left(L'_S(0,\chi_1)/i\right)=-0.393\ldots,
\]

so the missing phase is not merely the root number or a root of unity
visible from the functional equation.

## Conclusion

Local epsilon factors verify conventions but cannot upgrade the
absolute-value theorem of cycle 34 to the oriented equality.

## Reproducibility

- `scripts/dimension_six_phase_audit.gp`
