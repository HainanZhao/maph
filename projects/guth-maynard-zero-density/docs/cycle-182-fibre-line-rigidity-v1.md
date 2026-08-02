# Cycle 182: common-intercept fibre-line rigidity

## Claim boundary

`PROVED`: inside a fixed Cycle-181 common-intercept packet, every participating
actual fibre with at least two rows is a consecutive lattice segment on one
rational affine line. If its shared intercept is `rho=p/v` and its primitive
slope is `A/U`, then

```text
v | U,
N_ell <= 1 + H/U,
|A/U-alpha_ell| <= 2C/((N_ell-1)U X).                      (1)
```

The complete packet state—labels, four physical rows, individual residuals,
slope determinant, and product shell—remains attached to the fibre. This is
a fixed-packet rigidity/capacity reduction. It proves no upper bound for the
packet, recurrence, density improvement, or prime-interval result.

## One primitive slope in a fibre

For any actual pair in the fibre, its rational slope `a/d` obeys

```text
|a/d-alpha_ell| <= 2C/(dX) <= 2C/X.                        (2)
```

Two distinct reduced rational slopes with denominators at most `H` are
separated by at least `1/H^2`. Under the frozen cutoff
`4CH^2/X<1`, (2) makes distinct pair slopes impossible. Therefore all pairs
have a single reduced slope `A/U`, with `gcd(A,U)=1` and `U<=H`.

First take one packet-member pair at this label: C181 identifies its intercept
as `rho=p/v`. Fix one endpoint `(h0,j0)` of that pair. Every other actual row
forms a pair with it and has slope `A/U`, hence lies on the same line; only at
this point does the argument extend from the packet-member pair to the full
actual fibre. The reference row identifies that line as

```text
j = (A/U)h + p/v.                                          (3)
```

Thus no actual row can leave this line.

## Integral lattice and fibre completion

An integral row on (3) requires

```text
v*A*h + p*U == 0 mod U*v.                                  (4)
```

Since `gcd(A,U)=gcd(p,v)=1`, solvability of (4) first forces `v|U`.
After dividing by `v`, it becomes one congruence class modulo `U`, because
`A` is invertible modulo `U`. The integral heights on (3) therefore have
exact step `U`.

Take the extreme actual rows. The affine residual on (3) is a linear function
of height and is at most `C/X` at both extremes. Every integral lattice point
between them is consequently in the strip and hence actual. All actual rows
were already on the line, so the fibre is precisely a consecutive step-`U`
segment. Its height span is `(N_ell-1)U<=H`; applying (2) to that extreme
pair yields (1).

## Gate effect

C181's common-intercept packet is now a family of labelled primitive rational
lines indexed by `(p,v,A,U,residue)`, with `v|U`, a full fibre segment, and a
quantitative denominator capacity. The next analytic task is to bound the
stable cross-label rectangle census in this primitive-line packet, or to
construct a nonrational actual saturator. Merely restating the line
partition, counting scalar denominators, or dropping the base-row congruence
does not advance E13.
