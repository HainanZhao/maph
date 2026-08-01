# Cycle 4 CRR logarithmic-alias model barrier v1

## Claim boundary

`PROVED`: the elementary construction below shows that **generic** conditions
of the following type do not force a fixed-power saving in a smoothed
logarithmic-alias packet:

```text
W subset [0,H], H^(1/100)-separated,
|W| asymp q^2,
E_R,1(W) asymp q^5,
and an H^(-1)-scale positive smoothing of |R_W|^2.
```

Here `E_R,1` is the real, tolerance-one energy used by Guth--Maynard.  The
packet consists of neighborhoods of `exp(2*pi*j/(C K))`, not ordinary
rationals.  Thus this is an implication barrier for a proposed *generic
spacing/energy/smoothing argument*, not a counterexample to their affine
proposition or its rational example.

It does **not** construct the actual rational net in CRR v2; construct
coefficients `b_n`; make a Dirichlet polynomial large on `W`; satisfy the CRR
Base predicate; prove a positive cubic contribution; prove a CRR witness; or
prove a zero-density, short-interval, saturation, or L-function statement.
It gives no conclusion at all about the actual Farey neighborhoods
`r/s+O(H^(-1))` with `Q<=r,s<2Q`.

Guth--Maynard's source explains the relevance, but not this theorem: its
Section 9 remark gives the *actual* rational example at
`LargevaluesDirichlet17.tex`, lines 1433--1441, and its final critical remark
is at lines 2398--2399.  The CRR-v2 rational predicate is deliberately
stronger and pins a different net.  This result is therefore a contained
analytic model, not a claimed obstruction to that predicate.

## The theorem

Fix any integer `q>=256`, and put

```text
m=floor(q/64),       K=q^2,       L=64q,
C=1024,              H=16 C K L=2^20 q^3.
```

There are a set `A subset [0,K/4)` of `m` integers and

```text
W=C(A+K{0,...,L-1})
```

such that, with

```text
E_R,1(W) = #{(w1,w2,w3,w4) in W^4:
                 |w1+w2-w3-w4|<=1},
R_W(u)=sum_(w in W) u^(i w),  u>0,
```

the following hold.

1. `W subset [0,H]`, its minimum spacing is at least `12q`, hence it is
   `H^(1/100)`-separated, and
   `q^2/2 <= |W| <= q^2`.
2. `E_R,1(W) asymp q^5`, with absolute constants.
3. Let the fixed positive CRR-v2 smoothing be written

   ```text
   F_H(u)=integral H psi1(H(u-u')) psi2(u') |R_W(u')|^2 du'.
   ```

   There is a union `U_q subset [3/4,5/4]` of disjoint intervals of length
   `asymp H^(-1)` centered at logarithmic alias nodes
   `u_j=exp(2*pi*j/(C K))`, such that

   ```text
   |U_q| asymp q^(-1),
   integral_(U_q) F_H(u) du       >> q^2,
   integral_(U_q) F_H(u)^2 du     >> q^5.
   ```

The constants in `asymp` and `>>` do not depend on `q`.  Thus, for every
fixed `delta>0`, the listed generic hypotheses cannot imply either
`integral_(U_q) F_H << q^(2-delta)` or
`integral_(U_q) F_H^2 << q^(5-delta)` for every logarithmic-alias packet.
That is the exact and only no-go conclusion.

## A jittered, hard-core, low-energy digit set

For `0<=i<m`, independently choose

```text
r_i in {0,...,2q-1},       a_i=8q i+r_i.
```

Every realization has strictly increasing `a_i`, with gaps at least
`8q-(2q-1)=6q+1`, and

```text
max A < 8q m+2q <= K/4.
```

In particular it has the hard-core separation required later without an
unbounded dilation.  This corrects the tempting but invalid idea of obtaining
`H^(1/100)` spacing solely by taking an absolute fixed dilation of a unit-gap
Sidon set.

Only index quadruples `i+j=k+l` can contribute to an additive equation in
the `a_i`: the residual term has absolute value below `4q`, whereas a nonzero
multiple of `8q` cannot be cancelled.  The exact interval-index energy is

```text
E({0,...,m-1})=(2m^3+m)/3.
```

Apart from the `2m^2-m` trivial ordered solutions, every residual equation
has probability at most `1/(2q)`: condition on all but a variable occurring
with coefficient `+/-1`, or in the doubled-variable case on either of the
two remaining independent variables.  Hence

```text
E E(A) <= 2m^2-m + (2m^3+m)/(6q) <= 3m^2.
```

There is therefore one deterministic realization with `E(A)<=3m^2`.  Every
finite set has the trivial lower bound `E(A)>=2m^2-m`.  Since `A+A subset
[0,K/2)`, modular and integer additive equations for `A` are identical:
`E_(Z/KZ)(A)=E(A)`.

## Real energy and the block boundary calculation

All members of `W` are multiples of the fixed integer `C=1024`.  Therefore
the real tolerance-one condition is exact equality:

```text
|w1+w2-w3-w4|<=1  iff  w1+w2=w3+w4.
```

There is no hidden modular energy here.  In an exact block equation, the
`A`-difference has magnitude less than `K/2`, so

```text
a1+a2+K(l1+l2)=a3+a4+K(l3+l4)
```

forces both `l1+l2=l3+l4` and `a1+a2=a3+a4`.  This also handles the boundary
and carry issue: the block sums range from `0` to `2L-2`, and their exact
energy is

```text
E({0,...,L-1})=(2L^3+L)/3.
```

Consequently

```text
E_R,1(W)=E(A)(2L^3+L)/3 asymp m^2 L^3 asymp q^5.
```

## Aliases: exact Parseval and Paley--Zygmund count

For the unnormalised Fourier transform on `Z/KZ`, let

```text
Ahat(j)=sum_(a in A) exp(2*pi*i*j*a/K).
```

Exact Parseval and the exact fourth-moment identity are

```text
sum_j |Ahat(j)|^2 = K m,
sum_j |Ahat(j)|^4 = K E_(Z/KZ)(A) <= 3K m^2.
```

Let `G={j mod K: |Ahat(j)|^2>=m/2}`.  Removing its complement loses at most
`Km/2` from the first sum.  Cauchy--Schwarz then gives

```text
|G| >= (Km/2)^2/(3Km^2)=K/12.
```

Use all integers `0<=j<8K`.  Since `C/128=8`, this is eight complete residue
cycles.  At

```text
y_j=2*pi*j/(C K),       u_j=exp(y_j),
```

the block factor is exactly aligned:

```text
R_W(exp(y_j+h))
 = (sum_(a in A) exp(2*pi*i*j*a/K) exp(i C a h))
   (sum_(0<=l<L) exp(i C K l h)).
```

For `|h|<=1/(100H)`, the second factor has magnitude at least `.99L`; the
first differs from `Ahat(j)` by at most `m/(6400L)`.  Thus, for every good
residue and all such `h`,

```text
|R_W(exp(y_j+h))| >= (9/10)L sqrt(m/2) >> q^(3/2).
```

There are at least `8(K/12)=2K/3` good node indices.  Moreover
`y_j<pi/64<1/20` (using `pi<22/7`), so `u_j<exp(1/20)<5/4`; the small
neighborhoods lie safely in `[3/4,5/4]`.  Their separation in the log
variable is `2*pi/(C K)`, much bigger than `H^(-1)`.

## Width and height of the smoothing

The v2 functions obey `psi1>=0`, are positive near zero, and `psi2` is
positive on a fixed neighborhood of `[1,exp(1/20)]`.  On a core interval
`|u-u_j|<=1/(1000H)`, restrict the smoothing integral to
`|u-u'|<=1/(1000H)`.  The preceding raw lower bound applies to `u'`, while
`H psi1(H(u-u'))` has height `asymp H` and is integrated over a width
`asymp H^(-1)`.  The positive fixed factors therefore give

```text
F_H(u) >> L^2 m
```

on every core.  The cores are disjoint and have total measure
`asymp K/H=asymp q^(-1)`.  Integrating `F_H` and its square gives exactly the
two displayed moment scales `q^2` and `q^5`.

## What would refute this barrier

Any claimed deduction using only the enumerated generic conditions and
concluding one of the two forbidden `q^(-delta)` bounds on every
logarithmic-alias packet would be refuted by this construction.  The barrier
itself would be refuted by a failure in one of the digit carry factorization,
the real tolerance-one reduction, the Fourier fourth-moment identity, or the
positive-smoothing lower bound.  It survives those lightweight checks here.

Paper-stage hostile audit remains deferred by project policy.
