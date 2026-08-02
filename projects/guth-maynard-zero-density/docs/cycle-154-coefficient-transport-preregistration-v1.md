# Cycle 154 preregistration: coefficient transport or labelled escape

Date frozen: 2026-08-02 UTC.

## Objective

Starting from the Cycle-153 strict branch, construct an exact additive,
coefficient-faithful refinement

```text
H=T+F,
```

where `T=sum_b T_b` is the actually transported smooth positive fixed-chart,
strict-denominator class and `F` is its exhaustive labelled complement.  This
cycle must not assume that a local fixed-phase chart carries a fixed portion
of the original operator.

## Frozen labels and desired strict interface

Each `T_b` must retain

```text
(b,w_b,r_b,h_b,d_b,m_b,L_b,tau_b,gamma_b),
d_b=gcd(h,h_b), m_b=h_b/d_b, L_b=hm_b,
gamma_b=<T_b,w_h>/(KQ^2/h).
```

The target transport theorem is either an `O(1)` normalization

```text
w_b>=0,       sum_b w_b<=C_W,
n_b=(-Re gamma_b)_+<=Cw_b/m_b,                    (1)
```

with fixed `C_W,C`, or the same statement after one explicit fixed
renormalization by `C_W`.  All constants must include Riemann, Poisson,
stationary-phase, chart, tensor, and truncation errors.  An `X^(o(1))`
weight loss is not silently accepted as a bounded-multiplier input.

Every term that cannot satisfy (1) is placed in `F` with one explicit source
label: coefficient-transport failure, boundary denominator, phase-changing
chart, nonsmooth payload, unbounded tail, failed rational label, inadmissible
lcm, or registered truncation.  The partition must be additive, exhaustive,
and disjoint.

## Registered outcomes

If (1) is proved and the Cycle-153 strict negative mass is at least
`mu_*/2`, compose it with Cycle 152 after the displayed fixed normalization:
obtain an actual bounded-multiplier labelled divisor fan.  Otherwise prove a
quantitative labelled negative-correlation obligation for `F`; no unnamed
remainder is allowed.

Success is this transport-or-escape dichotomy.  It does not require an
incidence bound on the fan or escape class, and proves no full moment, density,
or prime-interval result.

## Session-companion decision record

The checked, reactivated session companion
`/root/guth_maynard_session_mentor` found that Cycle 123 and Cycle 147 prove
only local fixed-sign coherence, while Cycle 144 proves that no
coefficient-preserving transport is sealed.  It recommends this
transport-or-escape formulation; the primary worker adopts it.
