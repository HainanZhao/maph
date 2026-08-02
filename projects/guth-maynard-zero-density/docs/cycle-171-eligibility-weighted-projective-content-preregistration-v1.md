# Cycle 171 preregistration: eligibility-weighted projective-content web

## Question and boundary

Cycle 170 reduces a compatible source-packet/cross-edge pair to a seeded deep
target packet exactly when its transported seed is integral and in range and
its projective content clears both its error and capacity thresholds. This
cycle asks whether the resulting **eligible** labelled pair measure admits a
divisor-content population transfer, or instead has a quantitative retained
low-content obstruction web. It proves no lower bound for an actual census,
recurrence, E7/E9 skeleton, density, or interval result.

## Frozen pair data and deep threshold

For every complete labelled pair `gamma` consisting of a Cycle-170 source
packet and compatible reduced-rational cross edge, retain its nonnegative
weight `w_gamma`, every source/cross-edge/target label, and the Boolean
`S_gamma` that its transported beta seed is integral and in the frozen target
range. Write

```text
D=q d,             N=a(d+b)-q d,
g=gcd(|D|,|N|),    Q=|D|/g,
Lambda=a C_S/K_S+(|d+b|+1) C_E/K_E.
```

Freeze an integer critical depth `L>=1` and target height cap `H`. On the
preeligible set `Gamma_sr={gamma:S_gamma=true}`, define the exact integer
content requirement

```text
G_req(gamma)=ceil(max(L Lambda, L |D|/H)).           (1)
```

Cycle 170 implies that `gamma` is a seeded depth-`L` target packet if and
only if `g>=G_req(gamma)`. The convention includes `Lambda=0`; its first
term in (1) is then zero. No raw gcd or total marginal statistic may replace
this eligibility-weighted criterion.

## New factorization engine

For signed nonzero `d`, put

```text
c=gcd(|d|,|b|),   d0=d/c,       b0=b/c,
u=gcd(|d0|,a),    v=gcd(q,|d0+b0|).                 (2)
```

The proposed exact engine is

```text
g = c u v.                                             (3)
```

Here `u` and `v` are coprime. The source-core factor `c` may share primes with
either of them; it is kept as a separate labelled factor rather than falsely
absorbed into a primitive decomposition. Thus every pair records a labelled
source-core divisor `c`, numerator-absorption divisor `u`, and
denominator-absorption divisor `v`; their congruence web is retained rather
than collapsed to the scalar `g`.

Freeze the divisor-content functional

```text
M = sum_(gamma in Gamma_sr) w_gamma g_gamma/G_req(gamma)
  = sum_(gamma in Gamma_sr) w_gamma/G_req(gamma)
       sum_(r | c_gamma u_gamma v_gamma) phi(r).     (4)
```

and the eligible mass `W=sum_(Gamma_sr) w_gamma`. All divisor rows retain
`gamma` and its factor triple; (4) is not a deduplicated divisor count.

## Gates

1. **Exact factorization.** Prove (3), the exact coprimality statement
   `gcd(u,v)=1`, and its signed/zero-`b` conventions from
   `g=gcd(qd,a(d+b))`.
2. **Exact eligibility equivalence.** Prove `g>=G_req` iff the Cycle-170
   error and denominator depth conditions both reach `L`, including
   `Lambda=0`.
3. **Sharp weighted transfer.** With a frozen finite cap
   `R_max>=max(g/G_req)` on a specified retained bank, prove the best
   pointwise-moment implication from `M` to mass of `g>=G_req`, and exhibit
   its extremal two-level model. A claim using `M` without the cap is not
   permitted.
4. **Obstruction web.** Retain the Cycle-170 first failure (error-supported
   depth before denominator capacity) on every below-threshold eligible row.
   Independently refine its low content by the first frozen divisor coordinate:
   low source core, low numerator absorption, or low denominator absorption,
   relative to a preregistered factor allocation of `G_req`. The allocation
   must be exact and exhaustive, not chosen after seeing a row. The complement
   of `Gamma_sr` remains the separate seed/range obstruction bank.

## Falsifier and advance condition

The registered falsifier is an eligible signed pair for which (3) fails; a
pair satisfying `g>=G_req` but failing either Cycle-170 depth condition; or a
weighted-moment population claim defeated by a bounded two-level extremizer.

Advance only by an exact factorized divisor-content theorem with a sharp
mass-transfer ledger or by a retained, quantitative labelled obstruction web.
A scalar gcd average, an ineligible-pair count, a raw high-content example,
or a divisor count without pair labels is non-progress.
