# Cycle 13 source obstruction and weighted fractional tensor preregistration v1

## Claim boundary

`OBSERVED`: Cycle 12 left open an exact balanced factorization of the full
critical Type-I detector. This cycle first tests that source claim, then
replaces it by a cellwise theorem. A negative source result does not weaken
the conditional Cycle-12 theorem.

This cycle may prove an exact coefficient-support obstruction and an abstract
weighted fractional-tensor theorem. It may not promote a zeta density or
prime-interval improvement. A generalized Vaughan/Heath--Brown identity is a
candidate for redesigning the detector; it is not silently substituted into
the published Guth--Maynard argument.

## Frozen sources and scales

- Guth--Maynard TeX SHA-256:
  `36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428`.
- Freeze TeX lines 2309--2315:
  `b_n=(sum_(d|n,d<=2T^(1/100)) mu(d)) exp(-n/T^(1/2))`.
- Freeze the Cycle-12 critical scale `T=v^13`, detector length exponent `5`,
  local time exponent `12`, threshold exponent `7/2`, and baseline local-row
  exponent `8`.
- Heath--Brown 1982 PDF SHA-256:
  `b32e586d26dac73cb36a4f6dc7c6a7bf08ea5fa88e8ef8b18a8df2d5e849a807`.
  It is registered only as a primary-source candidate for a later
  prime-weighted detector decomposition. No theorem from it is imported in
  this cycle.

## Frozen source-obstruction theorem

For a prime `p>2T^(1/100)`, the only divisor of `p` not exceeding the cutoff
is `1`; hence `b_p=exp(-p/T^(1/2))` is nonzero. The same is true after the
nonzero Guth--Maynard normalization.

Any Dirichlet convolution of five sequences supported on integers at least
`2` vanishes at every prime. Consequently no sum, finite or otherwise, of
such balanced fivefold products equals the full detector coefficient vector
on a dyadic interval containing a prime above the cutoff.

The conclusion is support-theoretic only. It does not assert that the prime
remainder is large on zero ordinates or defeats every approximate,
prime-inclusive, or redesigned factorization.

## Frozen weighted fractional-tensor theorem

Let `A=product_(i=1)^m A_i`, with positive rational factor-length exponents
`y_i` satisfying `sum y_i=5`. An increment pattern is

```text
k=(k_1,...,k_m) in Z_{>=0}^m,       sum_i y_i k_i <= 2.
```

It defines the integer moment

```text
B_k=product_i A_i^(2+k_i),
```

whose length exponent is at most `12`. An exact fractional design consists
of finitely many admissible patterns and rational probabilities `pi_k` such
that

```text
sum_k pi_k=1,       sum_k pi_k k_i=tau  for every i.
```

Freeze the conclusions:

1. the weighted geometric mean of `|B_k|` is exactly `|A|^(2+tau)`;
2. one supported pattern satisfies `|B_k|>=|A|^(2+tau)`;
3. under the same coefficient-square mean-value hypothesis as Cycle 12, the
   local row exponent is `10-7tau`, with slack loss `2(2+tau)delta`;
4. there is a strict improvement over `8` exactly when `tau>2/7`;
5. every design has `tau<=2/5`, because
   `5tau=sum_i y_i E(k_i)<=2`.

These statements are conditional on the transformed coefficient-square
norms. They do not prove that a given source cell has those norms.

## Frozen constructive design and grid

If every `y_i<=2`, put `q_i=floor(2/y_i)`. The singleton patterns `q_i e_i`
are admissible. Assign probability

```text
pi_i=(1/q_i)/sum_j(1/q_j).
```

Then every expected increment equals

```text
tau_single=1/sum_i(1/q_i).
```

This supplies a theorem, not an optimality claim. The exact grid is all
sorted positive fifths `y_i=a_i/5`, `a_i>=1`, summing to `5`, for
`m in {3,4,5,6,7,8,9,10}`. Record the number of cells, the cells with
`max y_i<=2`, the cells with `tau_single>2/7`, and the best/worst positive
gain. No cell is discarded when the singleton design fails.

Registered examples:

- balanced `(1,1,1,1,1)` has `q_i=2`, `tau_single=2/5`, and exponent `36/5`;
- `(1/2,1/2,1,3/2,3/2)` has `q=(4,4,2,1,1)`,
  `tau_single=1/3`, and exponent `23/3`;
- any cell with one `y_i>2` has no positive uniform increment under the
  admissible-pattern definition and is recorded as a rough/unbalanced
  failure for this engine.

## Compute and review rules

- CPython `3.12.3`, optimization level zero, exact integers/Fractions, no
  RNG, no third-party numerical libraries, and no network.
- Grid cap: 250,000 cells total.
- Builder cap: 30 seconds and 256 MiB peak RSS.
- Research-stage checks are exact source text, algebra, enumeration, replay,
  and constructive counterexamples. Hostile audit remains at paper stage.
