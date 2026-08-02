# Cycle 180: nonzero pair determinants and stable cross-label rectangles

## Claim boundary

`PROVED`: in the Cycle-178 light branch, direct-target failure forces at least
`X^(32/25)/32` ordered distinct-label four-row rectangles.  Each retains two
actual rows at each label and has a nonzero integer determinant

```text
D=e*a-d*b,
|D-d*e*(alpha_ell-alpha_m)|<=4CH/X.                         (1)
```

`PROVED`: rectangles with `|ell-m|*d*e < (4C/pi)H Delta/X` total only
`X^(28/25+o(1))`. Thus a fixed-power critical population survives in the
stable range, where `|D|` is comparable to
`|ell-m|*d*e/Delta` with explicit constants.

This is a full rectangle reduction. It proves no upper bound for the stable
determinant-shell census, no aggregate recurrence, density improvement, or
prime-interval result.

## Pair state and nonzero determinant

At `ell`, take two actual rows in increasing height order and write

```text
d=h2-h1>0,       a=j2-j1,
|a-d alpha_ell|<=2C/X.                                    (2)
```

At a different label `m`, write `(e,b)` similarly. The integer determinant

```text
D=e*a-d*b                                                   (3)
```

satisfies, after substituting (2),

```text
|D-d e(alpha_ell-alpha_m)|
 <= 2C(d+e)/X
 <= 4CH/X.                                                   (4)
```

It is essential that `D` cannot vanish. If it did, `a/d=b/e` would be one
common rational slope. Dividing the two pair errors in (2) gives

```text
|alpha_ell-alpha_m|
 <= 2C/X(1/d+1/e)
 <= 4C/X.                                                    (5)
```

For the actual exponential, with `z=exp(2 pi/Delta)>1`, distinct labels have

```text
|alpha_ell-alpha_m|>=z-1.
```

The frozen large-scale condition `z-1>4C/X` contradicts (5). This uses the
common rational slope, not merely the weaker product approximation (4).

## Critical rectangle population

Let `p_ell=binom(N_ell,2)`, `P=sum p_ell`, and

```text
W_cross=sum_(ell!=m)p_ell p_m=P^2-sum p_ell^2.              (6)
```

In the light branch `N_ell<=2R`, where `R=ceil(X^(6/25))`,

```text
P >= (T-L)/2,
max p_ell < 2R^2,
W_cross >= P(P-2R^2).                                       (7)
```

Indeed `binom(n,2)>=(n-1)/2` for every nonnegative integer `n`, while a
fixed positive gap supports at most `N_ell` source pairs. At
`T>=X^(16/25)`, `L<=Delta=X^(15/25)`, and `X>=2^38`, (7) gives

`P>=T/4`, `P>=4R^2`, and therefore

```text
W_cross>=P^2/2>=T^2/32>=X^(32/25)/32.                       (8)
```

The normalization in (6) is ordered in the two label fields and uses an
unordered increasing-height pair at each individual label.

## Low product is too sparse

Put `r=|ell-m|` and

```text
K0=(4C/pi) H Delta/X = (4C/pi)X^(1/25).                     (9)
```

For fixed `ell,m,d,e`, there are at most
`N_ell N_m<=4R^2` physical rectangles with those two gaps. If
`K=ceil(K0)`, then the low-product count obeys

```text
W_low
 <=8R^2 L #{(r,d,e) in Z_{>0}^3: rde<=K}
 <=8R^2 Delta K(1+log K)^2.                                 (10)
```

The last inequality follows by summing
`floor(K/(r d))` and two harmonic sums. Thus

```text
W_low=O_{C,c}(X^(28/25) log^2 X)=o(X^(32/25)).               (11)
```

This calculation preserves the original pair gaps and row-pair
multiplicities; it is not an unweighted scalar product count.

## Stable determinant shells

For `ell<m`, the exponential difference satisfies

```text
2 pi r/Delta
 <= alpha_m-alpha_ell
 <= 2 pi exp(2 pi c) r/Delta.                               (12)
```

Divide (4) by `de`. In the stable range `rde>=K0`, its error is at most
`pi r/Delta`, half the lower spacing in (12). Since `D!=0`,

```text
pi r d e/Delta
 <= |D|
 <= (2 pi exp(2 pi c)+pi) r d e/Delta.                      (13)
```

By (8)--(11), a direct-target failure has `>>X^(32/25)` retained stable
rectangles satisfying (13). The next analytic census must keep the complete
rectangle state together with the determinant shell `|D|~Q` and product
shell `rde~Q Delta`; an upper bound for that labelled shell census, or a
nonrational actual saturator for it, is the remaining task.

## Gate effect

Exact-rational towers and low product rectangles are now subcritical. The
active E13 bottleneck is the stable nonzero-determinant shell census. No
unweighted `||de(alpha_ell-alpha_m)||` estimate, density ledger, or interval
ledger is authorized as a substitute.
