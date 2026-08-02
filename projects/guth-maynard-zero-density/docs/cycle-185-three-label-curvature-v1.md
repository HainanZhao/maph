# Cycle 185: three-label curvature exactification and its mass-only limit

## Claim boundary

`PROVED`: an arithmetic-progression triple of common-intercept primitive rays
has a cleared integer curvature. Above the explicit depth threshold it
vanishes exactly, giving a rational geometric triple of slopes.

`PROVED`: critical cross-rectangle mass, complete-fibre capacity, and stable
shell membership alone do not force such a label triple: an explicit shifted
ternary-digit AP-free occupancy has those scales and no nontrivial label AP.

This proves no actual-positive-exponential distribution estimate, populated
box bound, seeded recurrence, density gain, or prime-interval result.

## Exact curvature

For labels `ell-r,ell,ell+r`, write `U_i=v*u_i` and
`A_i=U_i*alpha_i+epsilon_i`. Since `alpha_-*alpha_+=alpha_0^2`,

```text
K=U_0^2*A_-*A_+ - U_-*U_+*A_0^2 = v^2*K',
K'=u_0^2*A_-*A_+ - u_-*u_+*A_0^2.                         (1)
```

The exact expansion after division by `U_-*U_+*U_0^2` is the five-term
error expression in the replay. It also retains the pair determinants:

```text
K'=u_0*A_+*(u_0*A_- - u_-*A_0)
   -u_-*A_0*(u_+*A_0-u_0*A_+).                              (2)
```

If every `N_i-1>=S`, the full-fibre capacity bound gives the sufficient
integer-exactification condition

```text
8*A_c*C*H^3/(v^2*S^4*X) + 8*C^2*H^2/(v^2*S^4*X^2) < 1.     (3)
```

Thus the primitive curvature vanishes. At `v=1` its scale is a constant
multiple of `X^(2/25)`; the common-intercept denominator improves it by
`v^(-1/2)`.

## Why mass alone cannot activate it

Take `X=3^(50k)`, `H=3^(22k)`, `Delta=3^(30k)`, depth
`S+1=3^(4k)+1`, denominator `U=3^(18k)`, and
`M=3^(13k)` labels. Select them from the shifted ternary-digit set with
digits only `0,1`; it is three-AP-free. Each full fibre has
`binom(S+1,2)` pairs, so the ordered cross mass is at least a fixed fraction
of `M^2*S^4=X^(21/25)`. Its smallest product shell is already stable.

This construction is deliberately not an actual exponential configuration.
It rules out only a combinatorial inference from mass/capacity/shell data to
the label AP required by (1).

## Gate effect

The raw three-label curvature engine is banked as a conditional exactifier,
but cannot be promoted from packet mass alone. The next engine must constrain
the actual exponential distribution of high-depth approximants or use a
cross-box coefficient relation that defeats the AP-free occupancy model.

## Replay

```sh
python3 proof/build_cycle_185_three_label_curvature_v1.py --check
python3 -m unittest tests/test_cycle_185_three_label_curvature_v1.py
```
