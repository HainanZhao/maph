# Cycle 173: positive forward conservative balance obstruction

## Claim boundary

`PROVED`: on the actual positive exponential source branch, the frozen
**forward conservative** Cycle-167 direct-map gate has no eligible row. Its
simultaneous dyadic ranges conflict exactly with its balance and admissibility
conditions.

This does not prohibit reverse orientation, a larger strip-constant budget,
a different transport map, or a global exponential/fibre coupling theorem.
It proves no recurrence, skeleton, density, or interval result.

## Endpoint squeeze

Let `y=1+alpha_ell>1`, let `Y>=y`, and retain the forward map

```text
h_plus=q h/a,
h,h_plus in [H,2H],
qK<=H,
2HYC_*<=aK,       C_*>=1.                           (1)
```

The two row ranges and the map give exactly

```text
a/q=h/h_plus<=2.                                    (2)
```

On the other hand, divide the balance inequality by the admissibility bound:

```text
a/q=(aK)/(qK)>=2Y C_*.                              (3)
```

Since `Y>1` and `C_*>=1`, the right side of (3) is strictly larger than two,
contradicting (2).

The only formal endpoint of the non-strict inequalities is
`Y=C_*=1`, `a/q=2`, `h=2H`, `h_plus=H`. It is excluded on the positive source
branch because `Y>=1+alpha_ell>1` (the `ell=0`/zero-numerator boundary is not
part of this result).

## Consequence

The direct forward route cannot be used to force the Cycle-171 divisor moment
on actual positive source labels while retaining the frozen Cycle-167
conservative strip budget. Any progress must explicitly leave this gate: use
reverse orientation, quantify a justified slack change, or invent a new
transport/coupling mechanism. No broader impossibility is claimed.
