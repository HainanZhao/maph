# Cycle 87 discovery candidate: signed second-moment alias atlas

## Status

`CONJECTURED`: discovery-only reduction candidate.

## Candidate

Expanding the signed second moment in the primal variables gives the exact
pair kernel

```text
M2(K)=sum_(d1,q1,d2,q2) a_1 conjugate(a_2)
       sum_k U(k/K)e(k(z_1-z_2)),
z_(d,q)=c0 q exp(2pi d/D).                         (1)
```

Poisson in `k` turns the inner sum into

```text
K sum_m hat U(K(m-(z_1-z_2))).                     (2)
```

The atom diagonal has exponent `xi+14/15`, exactly the Cycle-86 target.
The off-diagonal kernel has zero continuous mean because `U(0)=0`; bounding
it by absolute near-collision counts would reintroduce an inadmissible
volume term.

In the Cycle-81 dual variables, a column has phase

```text
(hD/(2pi))log(kc0/r).
```

Crossing two columns produces a `k`-phase

```text
t log k-mk,  t=D(h-h')/(2pi).                      (3)
```

For `h!=h'`, stationary Poisson aliases satisfy

```text
k=t/m=D(h-h')/(2pi m),
m~D|h-h'|/K,  1<=m<<Q.                             (4)
```

The stationary amplitude is `sqrt(|t|)/m~sqrt(K/m)`.  Thus the moment should
split into:

1. `h=h'` logarithmic correlations;
2. `0<|h-h'|<K/D`, where no nonzero stationary alias exists;
3. `m>=1` stationary aliases, with `m` on the original denominator scale.

## Falsifiers

1. The primal pair-kernel sign or Poisson normalization differs from (2).
2. The atom diagonal is not exactly exponent `xi+14/15`.
3. A nonzero alias occurs for `|h-h'|<K/D`.
4. The stationary inverse or amplitude in (4) has a missing `D`, `2pi`, or
   power of `m`.
5. The stationary alias range exceeds `Q` at the Cycle-81 support ceiling.

