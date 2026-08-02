# Cycle 102 discovery candidate: remove the cross gcds first

`CONJECTURED` before proof sealing.

For a Cycle-100 split, set

```text
s=g0*s1,  t=g0*t1,  (s1,t1)=1,
x=(s1,R), y=(t1,N),
s1=x*s2, R=x*R2, t1=y*t2, N=y*N2.
```

The exceptional-looking gcd then disappears from the primitive coefficient
bases:

```text
gcd(sN,tR)=g0*x*y,
B0=tR/gcd(sN,tR)=t2*R2,
C0=sN/gcd(sN,tR)=s2*N2.
```

Thus a cross-valuation row is an ordinary coprime core decorated by `x,y`
and the additive constraint

```text
W=g0*(x*s2+y*t2).
```

Every prime power in `x` divides the `R`-side mode and label coordinate and
is absent from the opposite mode and label coordinate; the analogous claim
holds for `y` on the `N` side.  This is the proposed E16 inverse datum.

A purely combinatorial common-colour conclusion needs a threshold.  Assign
each positive-mass exceptional atom one canonical side/full-prime-power
colour.  If total mass is `E`, mass on each `w` is at most `A`, and the colour
alphabet has size at most `C`, one colour has mass at least `E/C` and hence
support on at least `E/(C*A)` distinct `w`.  Here
`C<=2*P(2M)` without dyadic data and
`C<=2*P(2M)*(1+floor(log2(2M)))^2` when both cross-gcd scales are retained.

Kill test: exhaustive equality of the original and core bases for all reduced
small labels and splits.  A mismatch kills the parametrization.  Failure to
exceed the colour-entropy threshold does not kill the valuation engine; it
means actual phases or a sharper per-`w` cap are still required.
