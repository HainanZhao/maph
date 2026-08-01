# Cycle 7 CRR phase-lattice Base saturation and alias quotient v1

## Claim boundary

`PROVED`: for the actual reduced-Farey phase lattice attached to the sealed
label `(r_Q,s_Q)=(Q+1,5Q/4+1)`, the common capped Dirichlet coefficient
problem has an exact quotient by its rational phase aliases.  Every exact
alias class has at most four columns.  Thus exact rational phase aliasing can
change the relevant capped sampling norm only by an absolute constant, never
by a fixed power of `v`.

`PROVED`: a phase-lattice row set has a sharp, dimensionless capped all-row
efficiency `Xi_(P,A)`.  The full Base pointwise condition on that row set is
equivalent to one exact inequality involving `Xi_(P,A)` and the top sampling
eigenvalue `lambda_(P,A)`.  Consequently a Base-compatible phase lattice must
saturate both the global sampled mean-value exponent and the capped all-row
efficiency up to subpower loss.

`CONJECTURED`: no fixed-power bound for either of those two distinct-phase
statistics is proved, and no capped coefficient vector meeting Base on an
actual phase lattice is constructed.  This note therefore proves neither a
full phase-lattice exclusion nor a Base-compatible witness, F4F, AFARI,
CFARI, CRR-U, RationalMass, PositiveCubic, a density gain, a short-interval
theorem, a full-method saturation theorem, or an L-function result.

The exact missing object is now explicit: a high-frequency, *distinct-phase*
capped sampling estimate for the same common coefficient vector and the same
actual row set.  The energy-only phase-lattice extremizer does not settle it.

## Frozen phase lattice and coefficient rephasing

Take the actual label from the signed extremizer note:

```text
r_Q=Q+1,             s_Q=5Q/4+1,
alpha_Q=r_Q/s_Q,     beta_Q=s_Q/r_Q,
P_Q=2 pi/log(beta_Q).
```

For even `v`, `Q=v^4` is divisible by four.  The sealed integer calculation
gives

```text
gcd(r_Q,s_Q)=1,
4/5 < alpha_Q <=5/6,
6/5 <= beta_Q <5/4.                                    (1)
```

Let `A` be a finite set of integers and allow an arbitrary phase-lattice
offset:

```text
W_(tau_0,A)={tau_0+P_Q a:a in A}.
```

Write `I_L={n in Z:L<n<2L}` and `w_n=w(n/L)`, with the frozen smooth weight
`0<=w_n<=1`.  Replacing `b_n` by `b_n n^(i tau_0)` preserves `|b_n|<=1`.
Thus the common capped Base value problem on `W_(tau_0,A)` is exactly the
same as the zero-offset problem

```text
D_b(P_Q a)=sum_(n in I_L) w_n b_n z_n^a,
z_n=n^(iP_Q).                                          (2)
```

This removes only the lattice offset; it does not change the common
coefficient vector, the row labels, or the coefficient cap.

## `PROVED`: exact rational-alias quotient

For `n,m in I_L`, equation (2) has equal column phases precisely when

```text
z_n=z_m
 <=> P_Q log(n/m) is in 2 pi Z
 <=> n/m=beta_Q^k for some k in Z.                      (3)
```

Partition `I_L` into the equivalence classes `C` from (3).  Every class has
at most four elements.  Indeed, if it had five, the ratio of its largest to
smallest member would be at least

```text
beta_Q^4 >= (6/5)^4 >2,
```

which is impossible inside `(L,2L)`.

For each class choose its common phase `z_C` and define

```text
omega_C=sum_(n in C) w_n,
q_C=sum_(n in C) w_n b_n.
```

The exact set of possible `q_C` under `|b_n|<=1` is the closed disc
`|q_C|<=omega_C`: it is the Minkowski sum of the individual discs
`|w_n b_n|<=w_n`.  Hence the capped all-row program has the exact quotient
form

```text
Gamma_(P_Q,A)
 = max_(|q_C|<=omega_C) min_(a in A)
     |sum_C q_C z_C^a|.                                 (4)
```

No coefficient is optimized separately for different rows in (4).  It is an
equivalent parametrization of the one common capped coefficient vector in
(2).

There is also an exact operator factorization.  Put

```text
M_(A,P)(a,n)=w_n z_n^a,
Mbar_(A,P)(a,C)=z_C^a,
B(C,n)=1_(n in C)w_n.
```

Then

```text
M_(A,P)=Mbar_(A,P) B,
||B||_op^2=max_C sum_(n in C)w_n^2 <=4,
lambda_(P,A):=||M_(A,P)||_op^2 <=4||Mbar_(A,P)||_op^2. (5)
```

Similarly `omega_C<=4`, so if `Gamma_bar_1` denotes (4) with every cap
replaced by `|q_C|<=1`, then homogeneity gives

```text
Gamma_(P_Q,A)<=4 Gamma_bar_1.                           (6)
```

`PROVED`: exact aliases can therefore provide at most constant factors in
the spectral norm and capped all-row value.  They cannot close any
fixed-power deficit in the CRR Base threshold.  The unresolved behavior is
entirely in the quotient's distinct phases `z_C`, which can still be very
close without being exactly equal.

## `PROVED`: the sharp capped Base-saturation statistic

Let

```text
N_L=|I_L|=L-1,
m=|A|,
V_-(v)=v^(7-delta(v)),
lambda_(P,A)=||M_(A,P)||_op^2.
```

The compact capped program is

```text
Gamma_(P,A)=max_(|b_n|<=1) min_(a in A)|D_b(Pa)|.
```

Define its normalized all-row efficiency by

```text
Xi_(P,A)=m Gamma_(P,A)^2/(N_L lambda_(P,A)).            (7)
```

For every capped `b`, minimum is at most root-mean-square, and
`||b||_2^2<=N_L`.  Therefore

```text
0<=Xi_(P,A)<=1.                                        (8)
```

By definition, not an asymptotic approximation,

```text
Gamma_(P,A)^2=N_L lambda_(P,A) Xi_(P,A)/m.              (9)
```

Thus the common capped Base pointwise condition on this fixed phase lattice
is exactly equivalent to

```text
Gamma_(P,A)>=V_-(v)
 <=> lambda_(P,A) Xi_(P,A) >= m V_-(v)^2/N_L.           (10)
```

This is the requested equality statistic: `lambda` measures available
sampled energy, while `Xi` measures the exact loss from one capped vector
having to be large on *every* selected row.  Neither scalar energy of `A` nor
the Farey fourth-moment profile determines either quantity at present.

If the row set also meets the frozen Base cardinality lower bound
`m>=v^(8-delta(v))`, then (10) forces

```text
lambda_(P,A) Xi_(P,A) >= v^(12-3 delta(v)).             (11)
```

For a phase lattice lying in `[0,H]` (in particular, for a Base candidate),
the inherited sampled mean-value bound for the actual CRR matrix gives

```text
lambda_(P,A) <= C (H+L)(1+log(2L))
                 <= 2C v^12(1+log(2L)).                (12)
```

Consequently every Base-compatible phase lattice has the two necessary
near-saturation properties

```text
lambda_(P,A) >= v^(12-3delta(v)),
Xi_(P,A) >= v^(-3delta(v))/(2C(1+log(2L)))=v^(-o(1)).  (13)
```

In particular, for any fixed `kappa>0`, either fixed-power statement

```text
lambda_(P,A)<=v^(12-kappa)
```

or

```text
Xi_(P,A)<=v^(-kappa)
```

eventually excludes the Base pointwise condition on that phase lattice.
Equations (5)--(6) show that exact rational aliases can contribute only
absolute factors to the product test (10); they cannot repair a fixed-power
deficit there.

## Relation to the existing leading-vector/flatness gates

Let `u` be a top left singular vector of `M_(A,P)`, let `x` be its normalized
right partner, and phase-round `x` to the capped vector `b^ph`.  With the
already sealed quantities

```text
rho=||x||_1^2/N_L,
phi=sqrt(m) min_a |(M_(A,P)b^ph)_a|/||M_(A,P)b^ph||_2,
```

the leading-eigenvector certificate gives

```text
Gamma_(P,A)^2 >= lambda_(P,A) N_L rho phi^2/m,
Xi_(P,A)>=rho phi^2.                                   (14)
```

The all-row phase-flatness lemma further gives, when its coordinatewise
leakage hypothesis `chi_ph<=kappa_0<1` holds,

```text
Xi_(P,A) >= rho * ((1-kappa_0)^2/(1+kappa_0^2)) * mu_top. (15)
```

Thus the earlier `rho`, `mu_top`, and `chi_ph` conditions are a constructive
sufficient route to the exact efficiency `Xi`; (7)--(10) also cover any
other capped construction.  This specializes the general phase-lift program
to the actual rational phase lattice without replacing it by an abstract
matrix model.

## Consequence and remaining decisive question

`PROVED`: the energy-only signed extremizer is not automatically
Base-compatible.  For its same actual label and same row set, Base would
require the distinct-phase quotient to satisfy both conditions in (13).  A
large local fourth moment, additive-energy saturation, and constant-size
column aliases do not establish them.

`CONJECTURED`: either of the following would settle the phase-lattice/Base
coupling in its respective direction:

- a fixed-power upper bound for the distinct-phase quotient norm in (5), or
  a fixed-power upper bound for `Xi_(P,A)`, uniformly over the energy-relevant
  phase lattices; this would exclude Base there;
- a common capped vector attaining the exact product condition (10), together
  with the energy and row-set conditions for one `A`; this would construct a
  Base-compatible phase lattice.  The individual near-saturations in (13)
  are necessary diagnostics, not by themselves a sufficient replacement for
  that product condition.

No such theorem is claimed.  The remaining quantity is a high-frequency
Mellin/Vandermonde sampling problem with the actual coefficient cap and one
common row set, not a consequence of exact aliasing or of a generic PSD
bound.

## Replay

```sh
python3 proof/build_cycle_7_crr_phase_lattice_base_saturation_v1.py --write
python3 proof/build_cycle_7_crr_phase_lattice_base_saturation_v1.py --check
python3 -m unittest tests/test_cycle_7_crr_phase_lattice_base_saturation_v1.py
```
