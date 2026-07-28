# SIC--Stark research cycle 102: exact \(S\)-set normalization

Date: 2026-07-28

## Question

Does the functional equation in cycle 98 apply to the precise
\(S\)-imprimitive derivative occurring in the TCC bridge, or is an Euler
factor still missing?

## Exact conductor check

The primitive order-six character has conductor

\[
 \mathfrak f_\chi=(6)\infty_2.
\]

The finite \(S\)-set in the ray-class partial zeta construction consists
of the primes dividing \((6)\).  Those primes already divide
\(\mathfrak f_\chi\), so their primitive local factors are absent.  Removing
the \(S\)-Euler factors therefore changes nothing:

\[
\boxed{L_S(s,\chi_1)=L(s,\chi_1).}
\]

This is special to the faithful order-six pair.  The conductor-three
quadratic character in the same ray group does acquire the familiar
factor \(2\), as certified separately in
`dimension_six_primitive_fourier_audit.gp`.

The functional-equation certificate now prints the finite and infinite
conductors and records the equality explicitly:

```text
scripts/dimension_six_weight_one_functional_equation.gp
```

## Consequence

The exact formula from cycle 98 needs no algebraic Euler multiplier:

\[
 2L'_S(0,\chi_1)
 =
 \frac{i\sqrt{756}}{\pi}L(1,\overline{\chi_1}).
\]

Thus the level-\(756\) modular-period target is exactly the TCC target,
not merely proportional to it.

