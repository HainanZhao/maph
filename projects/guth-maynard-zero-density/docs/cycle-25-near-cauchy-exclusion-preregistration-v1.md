# Cycle 25 near-Cauchy prime recurrence exclusion preregistration v1

## Claim boundary

This cycle may combine Cycle 24's near-Cauchy packet with an explicit
two-logarithm lower bound to exclude that packet for the full dyadic prime
row system at the frozen polynomial height. It may not exclude residual
singularity or stretched-exponential residual ill-conditioning, prove the
skeleton target, or promote density/interval consequences.

## Frozen source input

Use Theorem 5.4 in J.-H. Evertse's Chapter 5 notes, a stated explicit rational
case of Matveev (2000), pinned at

```text
artifacts/sources/evertse-linear-forms-logarithms-ch5.pdf
SHA-256 1f7f41e3b3292e380651baf4b30ed8717c3411909202dc0409a0d41ed4f149f0
```

For two nonzero rationals `a_1,a_2` and integers `b_1,b_2` with
`a_1^b_1 a_2^b_2!=1`, it gives

```text
|a_1^b_1 a_2^b_2-1| > (eB)^(-C_0),
```

where `B=max(|b_1|,|b_2|)` and `C_0` is a fixed explicit constant times
`max(1,log H(a_1))max(1,log H(a_2))`.

For rational ratios of primes at height at most `2X` and
`B<=X^(12/5+o(1))`, register the consequence

```text
|b_1 log a_1+b_2 log a_2| >= exp(-O((log X)^3))
```

whenever the form is nonzero. The elementary passage from the multiplicative
form to the real logarithmic form must be shown explicitly.

## Frozen phase-concentration lemma

Let `z_p=p^(-ih)` over all `M` primes in `[X,2X]`. If

```text
|M^(-1) sum_p z_p| >= 1-2delta,
```

and `omega` is the phase of the mean, then

```text
sum_p |z_p-omega|^2 <= 4M delta.
```

Consequently every pair satisfies

```text
|exp(-ih log(p/q))-1| <= 4 sqrt(M delta).
```

## Frozen three-prime contradiction

By the checked prime number theorem, choose distinct primes `q,p,r` in three
fixed proportional subintervals of `[X,2X]`, so

```text
alpha=log(p/q), beta=log(r/q)
```

are bounded above and below by positive constants. Phase concentration gives
integers `m,n`, each `asymp |h|`, such that

```text
|h alpha-2pi m|, |h beta-2pi n| << sqrt(M delta).
```

Therefore

```text
|n alpha-m beta| << sqrt(M delta).
```

The form is nonzero by unique factorization. Freeze

```text
X^(3/5)<=|h|<=X^(12/5),
delta=exp(-k rho/8),
k rho=X^(6/25-o(1)).
```

Its upper bound is

```text
exp(-X^(6/25-o(1))/16),
```

which contradicts the Matveev lower bound `exp(-O((log X)^3))` for all
sufficiently large `X`.

## Compute and review rules

- CPython `3.12.3`, optimization level zero, exact `Fraction` arithmetic for
  exponent and constant-flow checks.
- No RNG or network during replay.
- Builder cap: 30 seconds and 256 MiB RSS.
- Hostile audit remains deferred to paper stage.
