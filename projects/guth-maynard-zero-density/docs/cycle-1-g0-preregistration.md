# Cycle 1: G0 reconstruction preregistration

Date frozen: 2026-08-01 UTC, before reading either independent route's output.

## Claim boundary

This cycle reconstructs published exponents and their exact arithmetic.  It
does not claim a new zero-density estimate, a new short-interval result, or an
independent proof of the analytic theorems used as inputs.

## Frozen inputs

- `PROVED`: Guth--Maynard Theorem 1.2 supplies the coefficient
  `G(sigma) = 15/(3+5 sigma)` in
  `N(sigma,T) <= T^(G(sigma)(1-sigma)+o(1))`.
- `PROVED`: the Ingham estimate used by Guth--Maynard supplies
  `I(sigma) = 3/(2-sigma)` on the lower-sigma side of the crossover.
- `PROVED`: Guth--Maynard Corollaries 1.3 and 1.4 state the uniform and
  almost-all endpoints `17/30` and `2/15`, respectively, subject to the
  hypotheses in the source ledger.
- The project zero count includes multiplicity and zeros with
  `|Im(rho)| <= T`. Any one-sided source convention must be explicitly
  converted before exponent comparison.

## Route independence

Route A must use direct exact rational substitution and solve the equality
`I(sigma)=G(sigma)`. It may then replay the two arithmetic conversions from a
constant density coefficient `b`:

```text
theta_uniform = 1 - 1/b
theta_almost_all = 1 - 2/b.
```

Route B must instead clear denominators, analyze the sign of the resulting
polynomial on the full frozen sigma interval, and certify the piecewise
Ingham/Guth--Maynard/Huxley envelope. Route B may use the source proof's `T`-range
inequalities to derive the two theta endpoints, but must state explicitly if
it merely replays one of the displayed conversion formulae.

The two routes must not import one another or a shared implementation of the
formulas. Both may compare their final labeled outputs with
`conventions/baseline.py`.

## Expected values and pass rule

The preregistered exact outputs are:

| Label | Expected value |
|---|---:|
| crossover sigma | `7/10` |
| global density coefficient | `30/13` |
| uniform PNT theta | `17/30` |
| almost-all PNT theta | `2/15` |

### Frozen zero-density bottleneck cell amendment

This amendment was frozen on 2026-08-01 UTC after the first crossover replay
but before reading either route's bottleneck-cell output. It extends P0; it is
not a post-result parameter search.

The final Remark of Guth--Maynard Section 13.1 freezes

```text
sigma = 7/10
original zero-detecting length N = T^(5/13)
squared polynomial length L = T^(10/13)
local interval length U = T^(12/13)
L = U^(5/6)
V = L^sigma = U^(7/12)
|W| = U^(2/3)
E(W) = |W|^(5/2) = |W|^4/U = U^(5/3).
```

Both independent routes must evaluate every term, without floating point.
The preregistered outputs are:

| Object | Expected local `U` exponents |
|---|---|
| Theorem 1.1 terms | `1/2`, `2/3`, `2/3` |
| Proposition 11.1 energy terms | `5/3`, `5/3`, `5/3` |
| displayed energy models | `5/3`, `5/3` |
| number of local intervals `T/U` | global `T` exponent `1/13` |
| total large-value count | global `T` exponent `9/13` |
| `(30/13)(1-7/10)` | `9/13` |

PASS requires labeled agreement on all terms, not just the maxima. A tie is a
saturation fingerprint of the published bound, not a proof that any term or
method is universally sharp.

### Frozen Theorem 1.2 case-split amendment

This amendment was frozen on 2026-08-01 UTC after direct inspection of the
published proof in Section 13.1, but before either independent implementation
of the complete case split. It closes a coverage gap in the first baseline
replay: agreement at the crossover and bottleneck cell alone does not exercise
every branch used to obtain Theorem 1.2.

Freeze

```text
s = sigma in [7/10, 4/5]
n = log(N)/log(T)
q = log(N^k)/log(T)
l(s) = 10/(6+10s)
u(s) = 15/(6+10s)
B(s) = 15(1-s)/(3+5s)
d(s) = 18/5-4s
alpha(s) = B(s)/d(s).
```

The zero-detecting construction supplies `N` in
`[T^(1/100), T^(1/2)(log T)^2]`; powers of `log T` are retained as `o(1)`
and are not silently treated as exact finite-`T` inequalities. The exact
power-scale audit must establish the following labels:

| Branch or boundary | Expected exact relation |
|---|---|
| Type II zeros | `2(1-s) <= B(s)` for `s <= 9/10` |
| small-`n` integer choice | if `n <= 5/(6+10s)`, `k=ceil(l/n)` gives `l <= q <= u` |
| large-`n` integer choice | if `n > 5/(6+10s)`, `k=2` gives `q > l` and the source's `q <= u+o(1)` because `u>1` on the frozen range |
| Theorem 1.1, first term | `2q(1-s) <= B(s)` from `q <= u` |
| Theorem 1.1, second term | `d(s)q <= B(s)` from `q <= alpha(s)` |
| Theorem 1.1, third term | `1+(12/5-4s)q <= B(s)` from `q >= l` |
| Mean-value, first term | `2q(1-s) <= B(s)` from `q <= u` |
| Mean-value, second term | `1+(1-2s)q < B(s)` from `q>alpha(s)` |
| strict mean-value margin | `B-[1+(1-2s)alpha] = [250(s-3/4)^2+3/8]/[2(3+5s)(9-10s)] > 0` |

Route A must verify these relations by direct rational-function substitution,
monotonicity signs, and endpoint inequalities. Route B must independently
clear denominators, factor or expand every residual polynomial, and certify
the signs on the entire frozen interval. Both routes must retain the strict
margin and distinguish exact power exponents from `o(1)` endpoint slack.

This amendment audits the exponent logic conditional on the cited
zero-detection lemma, Theorem 1.1, and the mean-value theorem. It is not an
independent proof of those analytic inputs. A missing integer-choice branch,
an incorrect sign caused by multiplying through a nonpositive denominator, or
replacement of `u+o(1)` by an unqualified finite-`T` `u` is a failed G0 audit.

G0 arithmetic PASS requires:

1. both routes return all four exact rational labels;
2. both routes agree with the frozen expected values;
3. the labels and conventions agree, not merely the unordered values;
4. Route B certifies which branch is active on each side of the crossover;
5. all tests pass with only pinned standard-library arithmetic;
6. the source/hypothesis ledger supplies the analytic hypotheses that the
   arithmetic replay does not prove.

Any disagreement is a failed audit. The affected result is contained until a
versioned correction explains and resolves the discrepancy.

## Resource and failure rules

- Arithmetic: Python `fractions.Fraction`; no binary floating point.
- Dependencies: Python standard library only.
- Runtime cap: 60 seconds per independent replay on the reference host.
- Memory cap: 256 MiB per independent replay.
- Failed rows, failed assertions, and uncovered theorem branches are retained
  in the cycle report; they are never silently dropped.
- Re-running one route is replay, not independent verification.

## What would falsify the frozen reconstruction

- exact route disagreement on any labeled value;
- a source hypothesis incompatible with the frozen counting convention;
- a denominator or parameter range that changes sign inside an asserted
  interval;
- a source-level derivation of either theta that is not licensed by the
  recorded density estimate and explicit-formula ranges.
