# Cycle 153 preregistration: actual negative-mass routing compiler

Date frozen: 2026-08-02 UTC.

## Frozen normalized input

Fix the Cycle-149 witness denominator `h` and its one-witness scale

```text
W_h=KQ^2/h.
```

Use the post-error Cycle-150 residual, not the pre-error Cycle-149 symbol:

```text
H=S+E,
-Re <H,w_h>/W_h >= mu_* >= kappa_*>0.             (1)
```

All constants in (1) are fixed independently of `X`.  The partition is
exhaustive and disjoint.  `S` consists exactly of smooth positive-chart halo
modes with retained labels

```text
(b,w_b,r_b,h_b,d_b,m_b,L_b,tau_b,gamma_b),
d_b=gcd(h,h_b), m_b=h_b/d_b, L_b=hm_b,
h_b<=QX^(-delta_*), L_b<=cK,
gamma_b=<S_b,w_h>/W_h.
```

Every other residual mode belongs to `E` and carries an explicit exclusion
reason: boundary denominator, phase-changing chart, nonsmooth payload,
unbounded tau, failed rational label, inadmissible lcm, or registered
truncation.  No mode may be discarded as negligible unless its aggregate
error is included before `mu_*` is frozen.

## Registered routing theorem

Set

```text
N_S=sum_b (-Re gamma_b)_+.
```

Prove the exact dichotomy

```text
N_S >= mu_*/2,
```

or

```text
-Re <E,w_h>/W_h >= mu_*/2.                        (2)
```

The first alternative exports the complete labelled strict-halo negative
mass.  It activates Cycle 152 only after separately proving or importing

```text
sum_b w_b<=1,
0<=(-Re gamma_b)_+<=Cw_b/m_b
```

with fixed uniform `C`.  The second alternative exports the complete labelled
escape correlation and its reason classes.  It is not enough merely to say
that “some residual remains.”

## Success and boundary

Success is the exact compiler (2) with an exhaustive label audit.  This is a
routing theorem, not an estimate: it does not bound the strict mass, prove
the Cycle-152 uniform weight bound, bound any escape class, prove a moment,
density improvement, or prime-interval theorem.  A failed exhaustiveness,
scale, or post-error check prevents promotion and is preserved as a failed
row.

## Session-companion decision record

The session companion `/root/guth_maynard_session_mentor` was checked and
reactivated for this preregistration.  It verified the sign inequality with
the post-error `mu_*`, required the exact disjoint partition and all retained
labels, and recommended this first Cycle 153 theorem.  The primary worker
adopts that recommendation.
