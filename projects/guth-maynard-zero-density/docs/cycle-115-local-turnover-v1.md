# Cycle 115: a local atlas removes the artificial weak gap

Let `f(t)=A-Be^(at)-Ce^(bt)`, `x>0`, `M=max(|a|,|b|)`, and
`S2=Ba^2+Cb^2`. On `I=[x/2,3x/2]`,

```text
ell_x=S2 e^(-3Mx/2)<=|f''(t)|<=S2 e^(3Mx/2)=L_x. (1)
```

`PROVED`. Put `delta=|f(x)|`, `eta=|f'(x)|`. If

```text
eta>=max(4delta/x,2sqrt(L_x delta)),               (2)
```

the Newton displacement `z=-2f(x)/f'(x)` stays in `I`; Taylor's theorem
changes the sign and produces a real root within `2delta/eta`.

If instead `eta<=ell_x x/2`, same-sign modes are excluded by their direct
derivative lower bound. Strict concavity then places the unique critical
point in `I` within distance `eta/ell_x`.

The only remaining transition has `ell_x x/2<eta` but fails (2). Hence one
of `eta<4delta/x` or `eta<2sqrt(L_x delta)` holds, and in either case

```text
delta>ell_x^2 x^2/(16L_x).                        (3)
```

Thus below (3) the old weak branch disappears completely: every row is
either a quantitative simple root or a locally strong critical point.

For `x=2pi/D`, `M<=D`, equation (3) is bounded below by

```text
(pi^2 e^(-9pi)/4) S2/D^2.                         (4)
```

Unlike Cycle 97's global `e^(-M)` ledger, this loses only an absolute
constant because `Mx<=2pi`. The registered stationary tolerance still has
to be compared with (4); simple-root averaging and the complete moment remain
open.
