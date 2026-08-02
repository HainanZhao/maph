# Cycle 119: the simple-root zeroth mode is too large

Put `g=exp(2 pi/D)`.  On one fixed same-sign or opposite-sign block, the
Cycle-118 simple-root count is majorized by a periodic Selberg polynomial for

```text
dist(B g^a+C g^b,Z) <= c/K,
```

where `B,C~Q` and both mode intervals have length `asymp D`.  A majorant of
degree `H~K` has constant coefficient `asymp 1/K`.  Its zeroth Fourier mode
therefore contributes

```text
Q^2 D^2/K = X^(28/15-xi).                         (1)
```

Cycle 112's corrected coefficient kernel is `Q^(-3/2)=X^(-1/2)`, so (1)
has weighted exponent

```text
41/30-xi.                                         (2)
```

This equals `109/150` at `xi=16/25` and tends to `89/150` at the upper edge
`xi=58/75`.  Both exceed the Cycle-114 benchmark `13/30=65/150`.  The exact
missing power is

```text
X^(14/15-xi),
```

ranging from `X^(22/75)` to `X^(4/25)` across the lower band.

The nonzero modes should not be hidden in an undifferentiated discrepancy
term.  If `I_sigma,I_tau` are the frozen sign intervals and

```text
T_sigma(h)=sum_{B~Q, a in I_sigma} e(h B g^a),
```

then the Fourier expansion factorizes exactly as

```text
hat(S)(h) T_sigma(h) T_tau(h).                    (3)
```

The second factor in (3) is not automatically a conjugate, so replacing the
product by `|T(h)|^2` would erase the sign-sector geometry.

Consequently, a Selberg-majorant argument that takes absolute values of the
nonzero modes cannot close the simple branch: its upper bound already
contains the positive term (1).  This is the precise no-go.  It does not
exclude a discrepancy theorem that proves cancellation against the mean,
and it is not a theorem about every unsigned method.  The next analytic
object must preserve the signs in (3), or restore the original stationary
phase and prove the stated saving there.
