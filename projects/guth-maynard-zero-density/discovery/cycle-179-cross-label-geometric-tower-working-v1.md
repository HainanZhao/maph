# Cycle 179 working ledger: cross-label geometric rational-base tower

## Frozen test

See the Cycle-179 preregistration.  The C177 ray used one rational root.  Its
minimal simultaneous extension is `1+alpha_m=((r+1)/r)^m`, not an arbitrary
union of rational approximants.  This provides a real actual-curve obstruction
candidate against which a cross-label theorem must be calibrated.

## Candidate calculation — `CONJECTURED` pending exact replay

For `A_m=(r+1)^m-r^m`, `gcd(A_m,r)=1`, hence the reduced denominator is
`r^m`.  Put `J=floor(log_r(2H))`.  Only `m<=min(M,J)` can have an exact row,
and their total count should satisfy

```text
sum_m N_m <= sum_(m<=J) (H/r^m+1)
             <= H/(r-1)+J.
```

Since `r>=2`, this is `O(H+log H)` uniformly even if `r` varies.  Thus the
ordered cross mass should be `O(H^2)` and fall a fixed `2/5` exponent below
the Cycle-178 critical cross-label scale.

## Exact-rational compression — `CONJECTURED` pending exact replay

This prototype may cover every exact-rational family. If
`z=exp(2 pi/Delta)` and each `z^ell_i` is rational, let
`g=gcd(ell_i)` and `ell_i=g m_i`. Bézout coefficients with
`sum c_i m_i=1` should give

```text
z^g=product_i (z^ell_i)^(c_i) in Q.
```

Writing this base as `u/v>1` in lowest terms makes every retained rational
label a subset of `(u^m-v^m)/v^m`. At beta zero with exact residual, for
`v>=2` geometric denominators give `O(H)` total rows; for `v=1`, chart
admissibility bounds the number of multiples by a constant because `u>=2`.
Thus exact rational **exact-row** roots should be unable to generate critical
ordered cross mass. This says nothing about arbitrary fixed-beta approximate
strip hits at large denominator; that approximate geometry is the genuine
hard case for the area engine.

## Next-state design requirement

The next invariant cannot only know the rational root at each label: the
tower has many exact cross-label labels yet remains subcritical.  It should
retain an ordered pair of rows, both label indices, primitive denominators,
the beta residuals, and a cross-difference/area determinant.  A proposed
formula must be tested on this tower before promotion.

## Frozen area engine — `CONJECTURED` pending exact replay

For two rows at `ell` and one at `m!=ell`, define

```text
A=(h2-h3)j1+(h3-h1)j2+(h1-h2)j3.
```

The coefficients sum to zero, so substituting
`j_i=h_i alpha_i-beta+e_i` should cancel beta. If the first two labels agree,
the phase term should collapse exactly to

```text
Phi=h3(h2-h1)(alpha_ell-alpha_m),
|A-Phi|<=2CH/X,
```

because the cyclic absolute height differences sum to at most `2H`. There
are exactly

```text
Q_tri=sum_ell N_ell(N_ell-1)(T-N_ell)
```

ordered such triangles. In the Cycle-178 light branch,
`sum N_ell(N_ell-1)>=T-Delta`; at direct failure and `X>=2^25`, this should
give `Q_tri>=T^2/4>=X^(32/25)/4`. An upper bound for this new area-resonance
census is deliberately not assumed.
