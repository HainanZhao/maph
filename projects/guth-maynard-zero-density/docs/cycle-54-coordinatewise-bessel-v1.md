# Cycle 54: the coordinatewise engine must expose every ordinary prime

## Claim boundary

`PROVED` conditional design theorem: under the registered coordinatewise
Bessel contract, failure of `AMPR_s` crosses the off-diagonal trigger only
after all `s` ordinary prime coordinates have been exposed. This remains true
after assigning the full Cycle 48 saving `7/50` to the powered `q^m`
coordinate. With only `s-1` ordinary contractions the missing exponent is
`3/50`; with all `s` the strict margin is `47/50`.

`CONJECTURED`: there exists a source-valid coordinatewise Bessel inequality
realizing one full power per ordinary coordinate and retaining the `7/50`
powered-coordinate saving. The present cycle does not prove that inequality,
`AMPR_s`, a density gain, or a short-interval improvement.

## Exact design ledger

After harmonic selection, an `AMPR_s` failure supplies

```text
r+2v >= s+14/5.
```

The one-shot trigger is `2s+2`. Under the candidate contract, exposing `j`
ordinary coordinates and then using the `q^m` saving gives trigger

```text
D_s(j) = 2s+2-j-7/50.
```

Thus the signed gap between the trigger and the selected level is

```text
D_s(j)-(s+14/5) = s-j-47/50.
```

The conclusion is independent of whether `s=3` or `s=4`:

| ordinary coordinates exposed | signed gap | consequence |
|---:|---:|---|
| `s-1` | `3/50` | still misses the strict trigger |
| `s` | `-47/50` | triggers with margin `47/50` |

Without the powered-coordinate saving the corresponding gaps are `1/5` and
`-4/5`. The Cycle 48 input narrows the penultimate miss but cannot replace
the last ordinary contraction.

## New engine specification

The analytic target is no longer the vague instruction “try coordinatewise
Bessel.” It is the following all-coordinate contraction:

1. keep `q^m` separate and apply the joint wrap estimate only to that powered
   phase;
2. expose each `p_i` through a separate Bessel/duality step without collapsing
   the coefficient tensor to the full distinct support;
3. preserve the common row phases through all `s` contractions;
4. after the last contraction, route the resulting popular difference into
   the Cycle 52 two-scale inverse theorem.

Any proof that loses a full ordinary-coordinate contraction is insufficient
at the current exponents, even if it retains all `7/50` from Cycle 48. This is
a sharp go/no-go test for proposed inequalities inside this design.

## Creative alternatives licensed by the miss

The small residual `3/50` at `j=s-1` suggests two hybrid engines worth
developing alongside the full contraction:

- `CONJECTURED` **three-coordinate plus curvature:** expose only `s-1`
  ordinary coordinates and seek the missing `3/50` by averaging the
  Huxley--Sargos wrap census over the popular-difference variable before
  maximizing in the phase parameter;
- `CONJECTURED` **centered cube trace:** replace the last Bessel contraction
  by a centered fourth Gram/cube trace in which Cycle 51 collision partitions
  are subtracted exactly and only genuine four-row parallelograms remain.

The first hybrid has a precisely sized target. The second must be evaluated
against the same `3/50` threshold, not against an unspecified “nontrivial
saving.”

## Gate effect

The gate remains `MULTILINEAR_TRIGGER_THEN_TWO_SCALE_INVERSE_OPEN`, now with
a quantitative fork: prove the full all-coordinate contraction, or recover
at least `3/50` after `s-1` contractions by curvature or centered trace.
