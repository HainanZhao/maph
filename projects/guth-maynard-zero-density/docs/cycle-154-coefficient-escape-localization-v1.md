# Cycle 154: finite labelled coefficient-escape localization

## Claim boundary

`PROVED`: under the exact Cycle-153 labelled escape alternative, if its
escape component is grouped into a fixed finite additive partition of `J`
reason-labelled classes and

```text
-Re <F,w_h>/W_h >= kappa > 0,       ||w_h||_2^2 <= A W_h,             (1)
```

then one labelled class `F_j` obeys

```text
-Re <F_j,w_h>/W_h >= kappa/J,
||F_j||_2^2 >= (kappa/J)^2 W_h/A.                                      (2)
```

The class retains the escape reason and its coefficient/rational-tail/payload
labels.  This is a finite-pigeonhole plus Cauchy localization theorem.

It does **not** prove that the actual Guth--Maynard escape has the required
finite additive decomposition, establish a fixed `A` for the relevant comb,
bound the selected class, prove positive coefficient transport, activate the
Cycle-152 divisor fan, or prove a moment, density, or prime-interval result.

## Exact derivation

Write `F=sum_(j=1)^J F_j`, with a frozen reason label on each summand.  Set

```text
a_j=(-Re <F_j,w_h>/W_h)_+.
```

Since `-Re sum_j <F_j,w_h>/W_h <= sum_j a_j`, (1) gives
`sum_j a_j>=kappa`.  Hence some `a_j>=kappa/J`, proving the first part of
(2).  Cauchy and the second condition in (1) give

```text
||F_j||_2^2 >= |<F_j,w_h>|^2/||w_h||_2^2
             >= (kappa/J)^2 W_h/A.
```

Nothing in this argument identifies a real escape partition or suppresses
cancellation within its individual classes.  Those are precisely the next
coefficient-transport obligations.

## Decision and liveness record

The persistent session companion `/root/guth_maynard_session_mentor` was
observed completed, reactivated under the same stable identity, and replied
on 2026-08-02 UTC.  It recommended the labelled coefficient-escape route:
conditional on a frozen finite partition, isolate a class carrying a
quantitative projection and one-ray `L2` obstruction, rather than treating
fixed-accuracy tensor error as negligible.  The primary adopts this narrowly
scoped failure-branch compiler.  The companion identifies the next critical
checkpoint as the Cycle-154/155 finite classes, `c_kappa`, and actual comb
norm/positive-transport criterion.

## Gate effect

This makes every **already supplied** finite reason-labelled escape
alternative actionable one class at a time.  It does not close the Cycle-154
transport-or-escape preregistration, because the actual coefficient partition
and comb-norm majorant remain to be derived or rejected.
