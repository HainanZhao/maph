# Cycle 109: the complete smooth triple-B scale kernel is summable

## A self-contained one-dimensional bound

`PROVED`. Let `phi` be real `C^2` on a compact interval, suppose `phi''` has
fixed sign and `|phi''|>=lambda>0`, and let `w` be compactly supported `C^1`.
Put `mu=sqrt(lambda)`. Since `phi'` is monotone, the set
`{|phi'|<=mu}` has length at most `2/sqrt(lambda)` and contributes at most
`2||w||_infinity/sqrt(lambda)`.

On each of the at most two complementary intervals, integrate by parts using

```text
e(phi)'=2pi i phi' e(phi).
```

The boundary terms, the `w'` term, and
`int |w phi''/(phi')^2|` are bounded using `|phi'|>=mu` and
`int |phi''|/|phi'|^2<=1/mu` on each side. A safe combined bound is

```text
|int w(x)e(phi(x))dx|
 <=(4||w||_infinity+||w'||_1)lambda^(-1/2).        (1)
```

## Three-variable iteration

`PROVED`. For a separable phase `phi_1(x_1)+phi_2(x_2)+phi_3(x_3)` and a
joint fixed smooth amplitude `W`, apply (1) successively. Differentiation in
the remaining variables passes under the preceding integral because the
phase is separable. Thus a fixed finite mixed-symbol norm
`N_111(W)` controls every step and

```text
|I|<=C_box N_111(W)(lambda_1 lambda_2 lambda_3)^(-1/2). (2)
```

## Actual logarithmic kernel

`PROVED`. After the Cycle-107 scale substitution, the three phase second
derivatives are

```text
-ell c Delta/k^2,
+ell c H/r^2,
-ell c(H-Delta)/(r')^2.                            (3)
```

They have fixed signs and magnitude comparable to `ell` on the frozen
positive compact charts. Their stationary points are independent of `ell`.
Cycles 81, 87, and 90 freeze fixed smooth compact weights, so the mixed symbol
norm in (2) is uniform. Therefore the *complete* joint kernel—not just its
leading term—satisfies

```text
|I_ell|<=C_W ell^(-3/2).                           (4)
```

Using Cycle 108's summability,

```text
sum_(ell<=L)|I_ell|<3C_W                           (5)
```

uniformly in the scale length and base-phase resonance.

## Consequence and boundary

The full perfect-power coefficient-scale multiplicity is closed in the
registered smooth stationary-alias model: it costs no power. Cycle 100's
sign-provenance correction is respected; no Möbius sign is used.

Different core aggregation, nonsmooth coefficient variants, large-degree
irrational cores, weak/simple-root rows, the complete moment, density gain,
and interval gain remain open.
