# Cycle 102: exact cross-valuation inverse atlas

## Theorem 1 (exact core)

`PROVED`.  Fix a Cycle-100 fiber split.  Put

```text
g0=(s,t), s1=s/g0, t1=t/g0,
x=(s1,R), y=(t1,N),
s1=x*s2, R=x*R2, t1=y*t2, N=y*N2.
```

Then

```text
(sN,tR)=g0*x*y,
B=lambda*t2*R2,
C=lambda*s2*N2,
lambda<=Q/max(t2*R2,s2*N2),
W=g0*(x*s2+y*t2).
```

Moreover

```text
(s2,R2)=(t2,N2)=(x,y)=(y*N2,x*R2)=1.
```

Thus each exceptional row is a coprime coefficient core plus two oriented
cross-valuation decorations.  A prime power dividing `x` divides `s/g0` and
`R`, but divides neither `t/g0` nor `N`; a prime power dividing `y` has the
side-reversed signature.

### Proof

Cycle 100 proves `(sN,tR)=g0*x*y`.  Substitute the four displayed
factorizations into `tR/(sN,tR)` and `sN/(sN,tR)` to obtain `t2*R2` and
`s2*N2`.  The equation for `W=s+t` is immediate.  The first two coprimalities
follow because `x` and `y` are the complete corresponding gcds.  The last two
follow from `(s1,t1)=1` and `(N,R)=1`.  Those same two primitive relations
give the prime exclusions.

## Theorem 2 (weighted colour concentration)

`PROVED`.  Let exceptional atoms of total nonnegative mass `E` have total
mass at most `A` over every fixed nonzero `w`, and suppose `|w|<=2M`.  Assign
each atom one of its side-labelled full prime powers.  With `P(H)` denoting
the number of prime powers at most `H`, some colour occurs on at least

```text
E/(2*P(2M)*A)
```

distinct `w`.  If both dyadic indices of `x,y` are also frozen, the lower
bound is

```text
E/(2*P(2M)*L_M^2*A),  L_M=1+floor(log2(2M)).
```

The assigned atoms retain their complete opaque stationary/anchor payloads;
the theorem does not assert that those payloads coincide.

### Proof

There are at most `2*P(2M)` side/prime-power colours and at most `L_M^2`
dyadic pairs.  One cell therefore carries at least total mass divided by the
corresponding alphabet size.  Its mass at each `w` is at most `A`, so its
support has at least the displayed size.

## Boundary and implication

The informal claim that “excess forces many labels” is valid only after the
excess and per-`w` cap beat the colour entropy in Theorem 2.  The result is an
exact inverse interface for E16, not an analytic estimate for the exceptional
mass.  Actual cancellation still requires the stationary phases/amplitudes;
weak near-double and simple-root rows remain open.
