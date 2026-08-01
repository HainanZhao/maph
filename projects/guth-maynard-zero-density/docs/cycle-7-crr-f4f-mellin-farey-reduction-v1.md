# Cycle 7 CRR F4F Mellin--Farey reduction v1

## Claim boundary

`PROVED`: the local fourth moment on the true logarithmic Farey union has an
exact Fourier expansion against one explicit reduced-Farey Mellin sum.  An
energy-bin/Cauchy argument reduces `F4F_eta` to a fixed-power Wiener bound
for that sum.

`PROVED`: the low-frequency continuum/Möbius calculation gives the expected
`Q^2/(1+|tau|)` Mellin decay only up to the point at which its lattice error
is comparable.  More decisively, the absolute Wiener norm required by the
energy-bin/Cauchy route is bounded below by an absolute constant on a
high-frequency band.  Thus that route cannot prove any fixed-power F4F
saving, even though its low-frequency part would save a full factor `Q`.

`CONJECTURED`: no cancellation-preserving high-frequency estimate, no
fixed-saving `F4F_eta`, no Base-compatible counterexample, and no CRR-U
theorem is proved here.  The no-go is only for the explicitly displayed
absolute Fourier-bin/energy argument.  It does not rule out an argument
using signed correlations of the pair-sum measure, the common coefficient
vector, or a new actual log-Farey inverse theorem.

## Logarithmic form of the actual Farey union

Use the frozen scales

```text
H=v^12=Q^3,  Q=v^4,  R=v^8=Q^2,
delta(v)=1/sqrt(log v).
```

Let `F_Q` be the actual reduced shell

```text
F_Q={(r,s): Q<=r,s<2Q, (r,s)=1, 3/4<=r/s<=5/4}.
```

For `a=r/s`, the genuine jitter interval is

```text
I_a={a exp(theta/H): |theta|<=3},
U_v=union_(a in F_Q) I_a.
```

The Cycle 5 geometry makes these intervals disjoint.  Work first with the
logarithmic measure

```text
dmu_v(u)=1_(U_v)(u) du/u.
```

Since `U_v subset [1/2,3/2]`, the original fourth moment is bounded by

```text
integral_(U_v)|R_W(u)|^4 du
 <= (3/2) integral |R_W(u)|^4 dmu_v(u).                 (1)
```

For real `tau`, define the exact jitter factor and reduced Mellin--Farey sum

```text
J_H(tau)=(1/H) integral_(-3)^3 exp(i tau theta/H) dtheta
        =2 sin(3 tau/H)/tau,       J_H(0)=6/H,

S_Q(tau)=sum_((r,s) in F_Q) (r/s)^(i tau).
```

`PROVED`: changing variables `u=(r/s)exp(theta/H)` gives the exact Fourier
coefficient

```text
mu_hat_v(tau):=integral u^(i tau)dmu_v(u)=J_H(tau)S_Q(tau).  (2)
```

Every label in (2) is an original coprime ordered pair `(r,s)`; no generic
logarithmic packet is substituted.  The true jitter gives

```text
|J_H(tau)|<=7/H   (all real tau).                        (3)
```

## `PROVED`: exact fourth-moment and energy-bin reduction

For a finite real `W`, write

```text
R_W(u)=sum_(t in W)u^(it),
I4_log(W)=integral |R_W(u)|^4dmu_v(u).
```

Expanding `R_W^2` and using (2) gives the exact identity

```text
I4_log(W)=
 sum_(t1,t2,t3,t4 in W)
 mu_hat_v(t1+t2-t3-t4).                                  (4)
```

This is the requested time-difference/Farey-log expansion.  It has no
positivity term by term; its total is nonnegative because it is the integral
of a square.

Partition `[0,2H]` into unit half-open bins and put

```text
p_j=#{(t1,t2) in W^2:t1+t2 in [j,j+1)}.
```

The frozen tolerance-one energy satisfies

```text
sum_j p_j^2 <= E(W).                                    (5)
```

For `m in Z`, define the true log-Farey Wiener coefficients

```text
B_m=sup_(|tau-m|<=1)|J_H(tau)S_Q(tau)|,
W_Q=sum_(|m|<=2H+2) B_m.                                (6)
```

If one pair sum lies in bin `j` and the other in bin `k`, their difference
lies within one of `j-k`.  Cauchy gives

`sum_j p_j p_(j-m)<=sum_jp_j^2`.  Hence (4)--(6) imply

```text
I4_log(W)<=E(W) W_Q,
integral_(U_v)|R_W(u)|^4du <=(3/2)E(W)W_Q.               (7)
```

This is a rigorous sufficient route, not an equality after binning.  In
particular, if for fixed `kappa>0` one had

```text
W_Q<=v^(-kappa),                                        (8)
```

then Base's `E(W)<=v^(20+delta(v))` would give
`F4F_(kappa/2)` for all sufficiently large `v`.  By the prior actual-Farey
reduction, that would imply AFARI and then CRR-U.

## `PROVED`: what the continuum/Möbius calculation really controls

For the sharp reduced shell, two-dimensional Euler summation after Möbius
inversion

```text
1_(r,s)=sum_(d|r,s)mu(d)
```

gives

```text
S_Q(tau)=Q^2 I(tau)/zeta(2)
          +O(Q+Q(1+|tau|)log(2Q)),                      (9)
```

where `I(tau)` is the continuum integral over

```text
{(x,y) in [1,2]^2:3/4<=x/y<=5/4}
```

of `(x/y)^(i tau)`.  Integrating first in `x` proves

```text
I(tau)<<1/(1+|tau|).                                    (10)
```

The error in (9) is the exact issue: it is the sum over divisors of the
lattice boundary/variation error `O((Q/d)(1+|tau|))`.  Consequently the
continuum bound

```text
S_Q(tau)<<Q^2/(1+|tau|)                                 (11)
```

follows from (9) only while

```text
(1+|tau|)^2 log(2Q)<<Q.                                 (12)
```

On that low range, (3) and (11) yield

```text
sum_(|m| satisfying (12)) B_m << Q^(-1)log(2Q).         (13)
```

Thus the continuum part alone would leave a power saving.  Equation (12)
is not asserted to be the true onset of large values; it is the exact
breakdown scale of this elementary continuum/Möbius estimate.  Any extension
must control discrete Mellin sums rather than merely their continuum
integrals.

The discrete content can be isolated without changing reduced labels.  If the
real-valued function `phi` is supported in `[1,9/8]`, then its pair support lies inside the actual
ratio shell, and Möbius inversion gives the exact core identity

```text
S_(phi,Q)(tau)=
 sum_(r,s>=1,(r,s)=1) phi(r/Q)phi(s/Q)(r/s)^(i tau)
 =sum_(d>=1)mu(d) |sum_n phi(d n/Q)n^(i tau)|^2.         (14)
```

This does not bound the full sharp-shell sum by itself.  It identifies the
remaining high-frequency task as a signed combination of genuine Dirichlet
polynomial large-value problems at lengths `Q/d`, not as an additive Farey
correlation theorem.

## `PROVED`: high-frequency no-go for the absolute Wiener route

The obstruction in (7) is not merely a missing estimate.  It cannot have a
fixed power saving.  Let

```text
N_Q=#F_Q.
```

The elementary count already sealed in Cycle 5 gives `N_Q>=Q^2/200`, while
`N_Q<=Q^2`.  Distinct reduced ratios in the shell obey

```text
|log(r/s)-log(r'/s')|>=1/(5Q^2).                         (15)
```

Indeed their rational difference is at least `1/(4Q^2)` and the derivative
of log is at least `4/5` on `[3/4,5/4]`.

Apply the continuous Montgomery--Vaughan Hilbert mean-value inequality to
the `N_Q` frequencies in (15), on

```text
T_0=[H/10,9H/10],   |T_0|=4H/5.
```

It gives

```text
integral_(T_0)|S_Q(tau)|^2dtau
 >= |T_0|N_Q-2*pi*(5Q^2)N_Q
 >= Q^5/500                                                (16)
```

for every sufficiently large `Q` (for example `Q>=20000`).  The final bound
uses the displayed count lower and `N_Q<=Q^2`; only the eventual regime is
needed by F4F.

On `T_0`, `3tau/H` lies in `[3/10,27/10]`, where
`sin(3tau/H)>=1/4`.  Therefore

```text
|J_H(tau)|>=1/(2H).                                      (17)
```

Since `|S_Q(tau)|<=N_Q<=Q^2`, (16)--(17) imply

```text
integral_(T_0)|J_H(tau)S_Q(tau)|dtau >=1/1000.           (18)
```

The sum of unit-bin suprema in (6) dominates this integral.  Hence

```text
W_Q>=1/1000                                               (19)
```

for all sufficiently large `Q`.  `PROVED`: condition (8) is false for every
fixed positive `kappa`.  Thus the absolute Fourier-bin/Cauchy use of the
tolerance-one energy cannot prove F4F, even with the exact reduced Farey
labels and bounded jitter retained.

This is not a counterexample to F4F.  It says precisely that replacing the
signed four-linear sum (4) by binwise absolute values throws away the
cancellation needed for any saving.  The high-frequency Mellin--Farey sum
in (2), equivalently the Dirichlet-square family in (14), is the remaining
decisive object.

## Consequences and falsifiers

`PROVED`: this reduction does not change CRR-U's truth status.  It narrows
the F4F route: a successful proof must exploit cancellation among different
pair-sum offsets, a Base/coefficient constraint, or a new high-frequency
Mellin--Farey estimate stronger than the absolute Wiener route.  A valid
fixed-saving F4F theorem would still imply AFARI and CRR-U.

The reduction would fail if log-window disjointness, (2), the energy-bin
inequality, the coprime Euler summation, the Farey log spacing, or the
Hilbert mean-value calculation failed.  A proof that the signed sum (4)
has a fixed saving despite (19) would be a genuine advance rather than a
contradiction.

## Replay

```sh
python3 proof/build_cycle_7_crr_f4f_mellin_farey_reduction_v1.py --write
python3 proof/build_cycle_7_crr_f4f_mellin_farey_reduction_v1.py --check
python3 -m unittest tests/test_cycle_7_crr_f4f_mellin_farey_reduction_v1.py
```
