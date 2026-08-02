# Cycle 26 detector reconstruction preregistration v1

## Claim boundary

This cycle may reinterpret Cycle 23's inverse leverage and Cycle 24's
singular residual as explicit reconstruction/annihilation statements for the
common coefficient vector. It may not prove that the reconstructed detector
is source-valid after surgery, exclude exact row dependence, prove the
skeleton target, or promote density/interval consequences.

## Frozen matrix convention

Let `X` be the normalized `k by M` row matrix, let `b` be the normalized
common coefficient column, and set

```text
q=Xb,  R=X(I-bb*),  Z=RR*,
D=diag(sqrt(1-|q_t|^2)),  W=D^(-1)R,
B=WW*,  s=D^(-1)q.
```

Then the scaled row matrix has the exact decomposition

```text
D^(-1)X = s b* + W.
```

## Frozen positive-definite reconstruction

If `B` is positive definite, set

```text
c=B^(-1)s,  L=s*B^(-1)s.
```

The builder must verify algebraically

```text
c*s=L,
||c*W||^2=L,
||(c*/L)D^(-1)X-b*||=L^(-1/2).
```

Thus inverse leverage at least `exp(k rho/4)/2` reconstructs `b` from the
scaled phase rows with error at most

```text
sqrt(2) exp(-k rho/8).
```

At `k rho=X^(6/25-o(1))`, this is stretched-exponentially accurate.

## Frozen singular split

If `B` is singular, then `ker(B)=ker(W*)`. For any nonzero `c` in that
kernel,

```text
c*D^(-1)X=(c*s)b*.
```

Register exactly two alternatives:

1. some null vector has `c*s!=0`, giving exact reconstruction of `b`;
2. every null vector has `c*s=0`, and every residual null relation is also an
   exact linear dependence among the scaled prime rows.

Do not claim the second alternative is impossible.

## Compute and review rules

- CPython `3.12.3`, optimization level zero, exact `Fraction` arithmetic for
  exponent and finite rational-matrix checks.
- No RNG or network during replay.
- Builder cap: 30 seconds and 256 MiB RSS.
- Pin Cycle 23, Cycle 24, and Cycle 25 artifacts.
- Hostile audit remains deferred to paper stage.
