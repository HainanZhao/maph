# Cycle 174: capacity-saturated bounded-slack transport

## Claim boundary

`PROVED`: the exact forward transport error has a row-local multiplier. On
the frozen capacity-saturated branch `qK>=H/2`, it is bounded by `4Y`, so a
fixed enlarged strip constant transports the beta seed with no Cycle-67 depth
exponent loss. Every remaining admissible edge belongs to a retained dyadic
capacity-deficit class with an explicit lower bound for that multiplier.

No population of either class, target-local packet, recurrence in the actual
census, skeleton, density, or interval gain is proved.

## Exact error, not the unit budget

For the reduced forward map `h_plus=qh/a`, `j_plus=j+h-h_plus`, C167 gives

```text
R_plus = R - (h/a)(1+alpha_ell)(qE-a).               (1)
```

If `|qE-a|<=C_1/(KX)`, define

```text
rho = h(1+alpha_ell)/(aK)
    = h_plus(1+alpha_ell)/(qK).                      (2)
```

Then the target row has strip constant `C_0+rho C_1`. The equality in (2)
retains the row, edge, and curve labels; it is not a global worst-case
replacement.

## Fixed saturated branch

Freeze `eta=1/2`. If `qK>=H/2`, `h_plus<=2H`, and
`1+alpha_ell<=Y`, then

```text
rho <= 2HY/(qK) <= 4Y.                               (3)
```

The constant `4Y` is fixed independently of `X` on the registered label
range. Thus the Cycle-67 identity may be used with packet/seed constants
`C_0` and `4Y C_1`; its proof is algebraic and its realized progression depth
still has exponent `log_X K`. This deliberately escapes Cycle 173's unit
conservative budget, but does not make arbitrary slack free.

## Labelled deficit bank

Every other admissible edge has one unique retained index `r>=1`:

```text
2^(-(r+1))H < qK <= 2^(-r)H.                         (4)
```

Because `h_plus>=H`, it obeys the quantitative lower bound

```text
rho >= 2^r(1+alpha_ell).                             (5)
```

The bank records the complete source/cross-edge/target labels and `r`; it is
not yet a structural inverse or a mass estimate.

## Consequence

Cycle 170 can reuse a capacity-saturated edge with edge error constant
`4Y C_1` in its projective-lift ledger. The next missing theorem is a lower
bound for that saturated complete-pair population, or a quantitative theorem
for the labelled dyadic deficit banks.
