# Cycle 96 preregistration: integer-jet separation

## Claim boundary

This cycle may prove a quantitative lower bound for the Cycle-95 Laurent
residual in an explicitly defined small-mode sector. It may not claim that
the sector exhausts the Poisson support, closes the stationary-alias branch,
proves a moment theorem, or changes a density or interval exponent.

## Frozen notation

- `A,B,C` are positive integers and `a,b` are integers, not both zero.
- `x>0`, `M=max(|a|,|b|)`, `S1=B|a|+C|b|`, and
  `S2=Ba^2+Cb^2`.
- `f(x)=A-B exp(ax)-C exp(bx)`.
- `J0=A-B-C` and `J1=Ba+Cb` are the constant and signed linear integer jets.
- The actual entropy substitution is
  `(A,B,C,a,b,x)=(p0n,p0n',q0m,u,u+v,2pi/D)`.

## Preregistered cases and gates

1. If `J0!=0`, assume `x exp(xM) S1<=1/2` and prove `|f(x)|>=1/2`.
2. If `J0=0` and `J1>0`, prove `|f(x)|>=x` without an extra size condition.
3. If `J0=0` and `J1<0`, assume
   `x exp(xM) S2<=1/2` and prove `|f(x)|>=x/2`.
4. If `J0=J1=0`, prove
   `|f(x)|>=exp(-xM)x^2S2/2`.
5. Verify that the four cases are exhaustive and that the last case has
   `S2>=1` because `(a,b)!=(0,0)` and `B,C>0`.

The cycle advances only if every sign case follows from the exact derivative
identities

```text
f'(t)=-Ba exp(at)-Cb exp(bt),
f''(t)=-Ba^2 exp(at)-Cb^2 exp(bt)<0.
```

## Falsifiers

- A valid row satisfying its registered sector condition but violating its
  lower bound halts the theorem.
- A proof that treats `J1<0` as monotone without controlling derivative
  turnover halts the theorem.
- A numerical scan is a test only and cannot prove the inequalities.
