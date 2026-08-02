# Cycle 132: the endpoint volume closes after a unimodular lift

Write `alpha=g^a`.  Let `p/q` be a Cycle-129 convergent and let `P/R` be
its next convergent.  With the orientation `s=Pq-pR`, elementary continued
fraction theory gives

```text
s in {+1,-1},       pR=-s (mod q),
1/[q(q+R)] < |alpha-p/q| < 1/(qR).                (1)
```

Fix `p/q` and `s`.  The possible `R` occupy one residue class modulo `q`.
The right endpoint of the error shell in (1) for `R+q` is the left endpoint
for `R`.  Thus all shells with `R~S` telescope into one interval on the
appropriate side of `p/q`, of alpha-length `O(1/(qS))`.  In the exact mode
coordinate

```text
y=(D/(2pi)) log(alpha),
```

compact support turns this into an interval of length

```text
w << D/(qS).                                      (2)
```

Let `q~N=X^rho` and `R~S=X^tau`.  There are `O(N^2)` primitive compact
labels `p/q`, and (2) has natural Fourier bandwidth

```text
H=NS/D.                                           (3)
```

The continued-fraction jump from Cycle 129 gives `S>>KQ/N`, hence

```text
tau >= xi+1/3-rho.                                (4)
```

After restoring the multiplicity `M=X^mu`, the zeroth Fourier mode is

```text
M N^2/H = M D N/S,
```

with exponent

```text
mu+rho-tau+3/5 <= mu+2rho+4/15-xi.                (5)
```

At the largest remaining denominator `rho=1/3-mu`, (5) is
`14/15-xi-mu`.  It is below the target `1/3` by

```text
xi+mu-3/5 >= 1/25.                                (6)
```

Therefore volume closes the whole Cycle-131 endpoint, not merely another
subrange.  This is not yet endpoint closure: the nonzero Fourier modes can
detect alignment of the logarithmic centers with the integer mode grid.
A sufficient smooth dyadic estimate is

```text
(1/H) sum_{1<=|h|<=H}
  | sum_{p/q in V(N,S)} e(hD log(p/q)/(2pi)) |
    << (Q/M) X^epsilon.                            (7)
```

The exact inverse retains more information than the old rational ray.  If a
block has more than `(Q/M)X^epsilon` hits, its hit vertices have pairwise
relations

```text
|p q'/(p' q)-g^(a-a')| << 1/(NS) <= 1/(KQ).       (8)
```

Each vertex also carries

```text
U=[[P,p],[R,q]],        det(U)=s in {+1,-1}.       (9)
```

Thus failure of (7) outputs a determinant-labelled rational-ray graph that
can enter the Cycle-125/126 additive-energy and recurrence compilers.  In a
clustered-large-sieve formulation, the allowable local multiplicity has
exponent `2(1/3-mu-rho)`; it shrinks to subpower size at the full endpoint.

The volume term in (7) is closed.  The Fourier norm itself is open, so no
endpoint, low-multiplicity, simple-root, complete-moment, density, or
prime-interval theorem is claimed.
