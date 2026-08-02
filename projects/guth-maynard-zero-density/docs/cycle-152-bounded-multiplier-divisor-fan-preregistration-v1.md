# Cycle 152 preregistration: bounded-multiplier negative-tail divisor fan

Date frozen: 2026-08-02 UTC.

## Frozen input and normalization

Fix a Cycle-149 witness denominator `h`.  The eligible modes are only the
smooth positive-chart halo modes already licensed by Cycle 151:

```text
h_b <= Q X^(-delta_*),       L_b=lcm(h,h_b)=h m_b <= cK,
d_b=gcd(h,h_b),              m_b=h_b/d_b,
tau_b=KQ(c0 g^b-r_b/h_b),    gcd(r_b,h_b)=1.
```

Here `delta_*>0` and `c>0` are fixed independently of `X`; retain the
literal `Q X^(-delta_*)` condition.  Do not replace it by a `Q`-power
condition as a sufficient hypothesis.  The coefficient-chart weights satisfy

```text
w_b >= 0,       sum_b w_b <= 1.
```

Fix `C,kappa>0`, independent of `X`.  For each eligible mode let `n_b` be
its actual normalized negative relative mass after the Cycle-151
tail-transform error and all admitted aggregate negligible errors have been
accounted for.  Freeze the admissibility condition

```text
0 <= n_b <= C w_b/m_b.                              (1)
```

Thus `C` is a uniform bound for the complete fixed-chart contribution on the
chosen tau window, not merely a bound for the continuum transform.  The
working antecedent is `sum_b n_b >= kappa`; without it, this cycle makes no
population claim.

## Registered theorem/inverse dichotomy

Set

```text
M_0=ceil(2C/kappa).
```

Prove that (1) and `sum_b n_b>=kappa` force one multiplier
`1<=m_0<=M_0` with

```text
sum_(b:m_b=m_0) n_b >= kappa/(2M_0).               (2)
```

For every retained mode prove, with all labels retained,

```text
h_b=m_0 d_b,       d_b|h,       gcd(m_0,h/d_b)=1.  (3)
```

The output is the labelled divisor fan

```text
(b,d_b,m_0,r_b,tau_b,w_b,n_b),
```

not an anonymous denominator count.  It must retain the literal strict
range, the lcm bound, the negative-lobe/sign information incorporated in
`n_b`, and the coefficient weight.

## Success, failure, and boundary

Success is exactly the conditional bounded-multiplier divisor-fan inverse
(2)--(3).  This is a structural inverse allowed by E14D-L; it is not a
gcd-weighted incidence upper bound.  The next stage may apply spacing or
order-three curvature to this fan, but neither is used or claimed here.

Failure means preserving every failed algebraic or normalization check and
making no gate promotion.  The theorem must not absorb boundary denominators,
phase-changing charts, nonsmooth payload, unbounded tau regimes, or an
uncontrolled aggregate Poisson/Riemann error into `C`.

## Session-companion decision record

The live session companion `/root/guth_maynard_session_mentor` was checked
and reactivated for this critical decision.  Its `PROVED` assessment was
that the tail bound plus the exact identity (3) gives a legitimate explicit
divisor-fan inverse provided `C` and `kappa` are fixed independently of `X`,
the positive weights are normalized, and all actual errors are included in
`C`.  The primary worker adopts that recommendation.  The companion also
recorded that this is a conditional concentration inverse, not the stronger
incidence theorem originally contemplated.
