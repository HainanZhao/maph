# Cycle 97 preregistration: algebraic-root inverse atlas

## Claim boundary

This cycle may prove an exact algebraic encoding of real residual roots and
a local simple-root/near-double-root dichotomy. It may not claim an effective
lower bound for `|D log(alpha)-2pi|`, exhaustion of the Poisson support, a
complete alias estimate, a moment theorem, or a density/interval gain.

## Frozen notation

- `A,B,C` are positive integers; `a,b` are integers, not both zero.
- `f(t)=A-B exp(at)-C exp(bt)`.
- `M=max(|a|,|b|)` and `s=max(0,-a,-b)`.
- After collecting equal powers,
  `P(Y)=A Y^s-B Y^(s+a)-C Y^(s+b)`.
- `W=A+B+C`, `S2=Ba^2+Cb^2`.
- At a test point `x>0`, set `delta=|f(x)|`,
  `eta=|f'(x)|`,
  `L=S2 exp(M(x+1))`, and
  `ell=S2 exp(-M(x+1))`.

## Preregistered algebraic contract

1. Prove `P` is a nonzero integer polynomial with degree at most `2M` and
   coefficient `l1` norm at most `W`.
2. Prove `f(t)=exp(-st)P(exp(t))`; hence a real root `r` gives a positive
   algebraic number `alpha=exp(r)` satisfying `P(alpha)=0`.
3. Record the safe root-height input
   `deg(alpha)<=2M` and
   `h(alpha)<=log(W)+log(2M+1)/2`, using the defining polynomial's Euclidean
   coefficient norm and Mahler measure. This bound is not yet asserted to be
   useful.
4. Prove `f''<0`, so there is at most one critical point and at most two real
   roots. A critical point exists only if `ab<0`, and then
   `exp((a-b)t*)=-Cb/(Ba)`.

## Preregistered local inverse

Assume `delta>0` and define

```text
tau=max(2delta,2sqrt(L delta)).
```

5. If `eta>=tau`, prove that `f` has a real root `r` with
   `|r-x|<=2delta/eta`. Record the actual entropy consequence
   `|D log(alpha)-2pi|<=2D delta/eta` when `x=2pi/D`.
6. If `eta<tau`, output the simultaneous certificate
   `|f(x)|=delta`, `|f'(x)|<tau`; do not call this a simple-root estimate.
7. In the second case, if additionally `eta<=ell/2`, prove that `ab<0`, the
   unique critical point `t*` exists, and
   `|t*-x|<=2eta/ell`. Bound
   `|f(t*)|<=delta+2eta^2/ell+2L eta^2/ell^2`.

## Falsifiers

- An identically zero cleared polynomial in a noncentral mode halts the
  algebraic contract.
- A row meeting `eta>=tau` with no root inside the registered Newton radius
  halts the simple-root branch.
- A row meeting `eta<=ell/2` without opposite-sign nonzero modes or without
  the registered critical point halts the critical branch.
- Floating root agreement is a test only and never proves the theorem.
