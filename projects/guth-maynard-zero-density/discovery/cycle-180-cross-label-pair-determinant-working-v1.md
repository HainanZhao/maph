# Cycle 180 working ledger: nonzero cross-label pair determinant

## Frozen engine

The Cycle-179 triangle used one pair at `ell` and one row at `m`. This cycle
keeps a pair at `m` too. It is a four-row refinement, not a replacement that
forgets the prior state.

## Candidate identities — `CONJECTURED` pending exact replay

For pair errors `delta=a-d alpha_ell`, `epsilon=b-e alpha_m`,

```text
D=e*a-d*b=d*e*(alpha_ell-alpha_m)+e*delta-d*epsilon,
|D-Psi|<=4CH/X.
```

If `D=0`, both pairs reduce to the same rational slope because
`a/d=b/e`. Their individual errors then give

```text
|alpha_ell-alpha_m|<=2C/X*(1/d+1/e)<=4C/X,
```

contradicting the frozen exponential spacing `alpha_(ell+1)-alpha_ell>=z-1`.

For light fibres put `p_ell=binom(N_ell,2)`. Expected population route:

```text
P=sum p_ell >= (T-L)/2,
max p_ell < 2R^2,
W_cross=P^2-sum p_ell^2 >= P(P-2R^2).
```

At the frozen direct threshold and `X>=2^38`, this should give
`W_cross>=T^2/32`. The next analytic object is the complete labelled
nonzero-determinant rectangle census, not merely `||de(alpha_ell-alpha_m)||`.

## Product split — `CONJECTURED` pending exact replay

For `r=|ell-m|`, division of the pair determinant error gives

```text
|D/(de)-(alpha_ell-alpha_m)|<=4CH/(de X).
```

Since `|alpha_ell-alpha_m|>=2 pi r/Delta`, the error is at most half this
spacing once `rde>=K0=(4C/pi)H Delta/X`. In that stable range the nonzero
integer `D` should satisfy `|D|asymp rde/Delta`. Below it, a fixed `(ell,m,d,e)`
has at most `4R^2` physical rectangles; summing ordered label pairs with
`rde<K0` should give at most `8R^2 Delta K0(1+log K0)^2=X^(28/25+o(1))`.
This is below the
critical `X^(32/25)` rectangle mass and should force a stable survivor.
