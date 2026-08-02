# Cycle 85 discovery candidate: logarithmic crossing occupancy

## Status

`CONJECTURED`: discovery-only candidate.

## Candidate

For a fixed Fejer frequency `j=X^(nu+o(1))`, a real crossing of

```text
j c0 exp(2pi d/D)
```

with the integer `r~j` is occupied only if

```text
||(D/(2pi))log(r/(j c0))|| << D/(jK).              (1)
```

Apply the checked order-three Huxley--Sargos theorem to the inverse-log curve
in `r`.  With `K=X^xi`, its registered exponents are

```text
derivative: 1/10+nu/2,
tube:       1/5+2nu/3-xi/3,
ratio:      (2nu-xi)/3,
constant:   0.                                     (2)
```

For `xi>=43/75`, the derivative term dominates.  Taking the minimum with the
trivial `X^nu` crossing count gives

```text
C_j <= X^(min(nu,1/10+nu/2)+o(1)).                 (3)
```

After summing `j` dyadically, the final Fourier-`L1` exponent is at most

```text
xi+max_(0<=nu<=1/3)[nu+min(nu,1/10+nu/2)]
=xi+3/5.                                           (4)
```

Thus the full unsigned volume range should close strictly for
`xi<31/25-3/5=16/25`, adding width `1/15` beyond Cycle 84.

## Falsifiers

1. The crossing error in (1) has the wrong factor of `D`, `j`, or `K`.
2. The Cycle-47 theorem does not apply uniformly to the moving `(j,c0)`
   family.
3. A tube or ratio term exceeds the derivative term on the active rectangle.
4. A smaller-`j` dyadic block exceeds the endpoint `nu=1/3` ledger.
5. Annular Fejer weights reintroduce the removed crossing loss.

