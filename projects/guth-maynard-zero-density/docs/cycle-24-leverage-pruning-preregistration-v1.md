# Cycle 24 leverage-pruning preregistration v1

## Claim boundary

This cycle may refine Cycle 23's inverse-leverage branch into an exact
trichotomy: near-Cauchy prime recurrence, negative residual spectral shift,
or exponentially small residual eigenvalue. It may not exclude any of those
branches for actual primes, prove the skeleton target, or promote density or
interval consequences.

## Frozen normalized system

Use Cycle 23's notation for `k` normalized rows `x_t`, normalized common
vector `b`, projection masses

```text
rho_t=|<b,x_t>|^2 >= rho,
```

and residual correlation matrix `B` on any retained subsystem.
Assume `k rho/4>=log 2` and freeze

```text
delta=exp(-k rho/8).
```

Call a row near-Cauchy when `rho_t>=1-delta`.

## Frozen near-Cauchy branch

After phase alignment, write

```text
x_t=sqrt(rho_t)b+sqrt(1-rho_t)e_t,    e_t perpendicular to b.
```

For two near-Cauchy rows,

```text
|<x_t,x_s>|
 >= sqrt(rho_t rho_s)-sqrt((1-rho_t)(1-rho_s))
 >= 1-2delta.
```

Thus if at least `k/2` rows are near-Cauchy, they form a complete
near-maximal recurrence graph. For prime rows this means

```text
|sum_p p^(-i(t-s))|/M >= 1-2delta
```

on every pair in that subsystem.

## Frozen regular branch

Otherwise retain at least `n>=k/2` rows with `1-rho_t>delta`. Their Cycle-23
vector satisfies

```text
||s||^2=sum_t rho_t/(1-rho_t) <= k/delta.
```

If the residual is singular, register `RESIDUAL_SINGULAR`. If it is positive
definite, either its renormalized shift is at most

```text
-n rho/2,
```

or Cycle 23 forces

```text
L=s*B^(-1)s > exp(n rho/2)-1 >= (1/2)exp(k rho/4).
```

Since `L<=||s||^2/lambda_min(B)`, the latter gives

```text
lambda_min(B) <= 2k exp(-k rho/8).
```

## Frozen critical translation

At `k=X^(21/25)` and `rho=X^(-3/5)`, every non-shift branch is therefore
stretched-exponentially structured at scale `X^(6/25)`:

1. a complete prime recurrence packet with kernel deficit
   `2exp(-X^(6/25)/8)`;
2. a singular residual; or
3. residual minimum eigenvalue at most
   `2k exp(-X^(6/25)/8)`.

These are alternatives, not claims that any branch occurs for actual prime
rows.

## Compute and review rules

- CPython `3.12.3`, optimization level zero, exact `Fraction` arithmetic for
  constants, inequalities, and exponent translation.
- No RNG, third-party library, or network.
- Builder cap: 30 seconds and 256 MiB RSS.
- Hostile audit remains deferred to paper stage.
