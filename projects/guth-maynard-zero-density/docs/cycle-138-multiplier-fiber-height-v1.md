# Cycle 138: edge multiplicity lowers the multiplier height

Let `r=A/B` be reduced and compact, with `A,B~H`.  If `x=p/q` is primitive,
then

```text
gcd(Ap,Bq)=gcd(A,q) gcd(B,p).                      (1)
```

Indeed every common prime lies in exactly one of the two cross-gcds.  Put
`u=gcd(A,q)` and `v=gcd(B,p)`.  If both `x` and `rx` have compact height
`N`, reduction of

```text
rx=Ap/(Bq)
```

forces `uv~H`.  For fixed `u|A`, `v|B`, the available numerator-denominator
pairs are at most

```text
O(N/u) O(N/v) << N^2/H.                           (2)
```

Summing divisor classes costs only `X^epsilon`.  Thus a multiplier of height
`H` has at most

```text
N^2 H^(-1) X^epsilon                              (3)
```

height-`N` realizations.  An edge class `|E_d|~J` therefore forces

```text
height(r_d) << N^2/J X^epsilon.                   (4)
```

Replacing the Cycle-137 height `N^2` by (4), the exceptional-difference count
becomes

```text
B_exc << X^epsilon
  (N^4/J^2 + D N^6/(J^2 S^2)).                   (5)
```

After multiplication by the coherent edge cost `J^2`, the multiplicity
cancels exactly.  Comparison with `(Q/M)^2` gives the two strict conditions

```text
rho < 1/6-mu/2,
tau-3rho > mu-1/30.                               (6)
```

Hence every edge-multiplicity class meets the exceptional-average diagonal
budget in (6).  The denominator ceiling in the first inequality exceeds the
Cycle-131 ceiling by

```text
(1/6-mu/2)-(7/45-2mu/3)
  =1/90+mu/6 >=1/90.                              (7)
```

On this subrange the second inequality is automatically generous at the
Cycle-132 minimum `tau=xi+1/3-rho`; it is nevertheless retained explicitly
as part of the theorem.

This closes the exceptional-multiplier weighted average for all `J` only in
the region (6).  It does not by itself prove the full paired norm, endpoint,
moment, density, or prime-interval theorem.
