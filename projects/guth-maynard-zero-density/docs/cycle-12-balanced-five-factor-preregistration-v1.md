# Cycle 12 balanced five-factor fractional-tensor preregistration v1

## Claim boundary

`OBSERVED`: this document freezes the first affirmative E3/E4 engine. The
result sought is conditional on a balanced five-factor decomposition of the
critical zero detector. No such decomposition of the source detector is
assumed or claimed here.

The cycle may prove an abstract large-value theorem and its exact critical
exponent translation. It may not promote a new zeta zero-density estimate,
uniform density coefficient, shorter prime interval, or L-function theorem
until the source factorization and a full neighborhood/envelope propagation
are closed.

## Frozen source bridge

The pinned Guth--Maynard TeX source has SHA-256
`36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428`.
Freeze the following source statements:

- TeX lines 2309--2330 define the Type-I detector and its normalized
  length-`N` polynomial;
- TeX lines 2332--2351 apply the large-values theorem to an integer power;
- TeX line 2398 identifies the critical point `sigma=7/10`, original detector
  length `N=T^(5/13)`, squared length `N^2=T^(10/13)`, local interval
  `T_1=T^(12/13)`, and local row scale `T_1^(2/3)`.

Under `T=v^13`, freeze

```text
X=v^5          (original detector length),
H=v^12         (local time length),
V_A=v^(7/2)    (original detector threshold),
R_baseline=v^8.
```

The identity `X^(12/5)=H` selects the fractional tensor exponent `12/5`.

## Frozen balanced-factor theorem

Let

```text
A(t)=product_(j=1)^5 A_j(t),
A_j(t)=sum_n a_(j,n)n^(it),
```

where each `A_j` has nominal length `v` and coefficients bounded by
`v^o(1)`. For every two-element subset `S` of `{1,...,5}`, define

```text
B_S(t)=product_(j in S) A_j(t)^3
       product_(j not in S) A_j(t)^2.
```

Freeze these obligations:

1. `B_S` has nominal length `v^12=H` and coefficient square norm
   `<=v^(12+o(1))`.
2. For every `t`,
   `max_(|S|=2)|B_S(t)|>=|A(t)|^(12/5)`.
3. For a one-separated `W` in an interval of length `H` with
   `|A(t)|>=v^(7/2-delta)` on `W`, colouring by a maximizing `S` and applying
   the discrete mean-value theorem gives

   ```text
   |W|<=v^(36/5+(24/5)delta+o(1)).
   ```

The exact main exponent is `36/5`; the local gain over `8` is `4/5`.

## Frozen combinatorial and unbalanced checks

- Exact combinatorial check: across all ten two-subsets, each factor is cubed
  four times and squared six times, so the geometric mean of `|B_S|` is
  `|A|^(12/5)`.
- Exact length check: if factor-length exponents are `x_1,...,x_5` with
  `sum x_j=5`, then `B_S` has length exponent `10+sum_(j in S)x_j`.
- Registered balance lemma: every pair length is `<=12` iff every pair sum is
  `<=2`; together with `sum x_j=5`, this forces `x_1=...=x_5=1`.
  The proof is algebraic. Finite rational corroboration enumerates sorted
  fifths `x_j in {0,1/5,...,3}` summing to five; no RNG.

The balance lemma contains only this uniform ten-moment design. It does not
rule out weighted, adaptive, or unequal-factor variants.

## Source-decomposition gate

`CONJECTURED`: it is sufficient to express the critical detector, after
subpower normalization, as a sum of `v^o(1)` balanced fivefold products. A
large value of the sum then selects one component with only subpower loss,
and the abstract theorem applies.

The registered adverse outcomes are:

- the detector has a component with no balanced fivefold factorization and a
  power-size contribution at the critical rows;
- the number of balanced product components is `v^kappa` for fixed
  `kappa>0`;
- coefficient convolution makes `||B_S||_2^2` exceed `v^(12+o(1))` by a
  fixed power;
- one must use an unbalanced pair moment of length `v^(12+kappa)`.

Any adverse outcome contains only the corresponding factorization design and
is retained as input for weighted/adaptive E4.

## Conditional downstream map

If the local bound `v^(36/5+o(1))` applies to every critical local interval,
there are `v` such intervals in the global height `v^13`. Freeze only the
anchor calculation

```text
global exponent at sigma=7/10 = 41/5,
anchor density coefficient = (41/5)/(13*3/10)=82/39,
anchor coefficient gain = 30/13-82/39=8/39.
```

This is not a uniform density theorem: the left-neighborhood and complete
zero-detection envelope remain open. The formal interval endpoint
`1-1/(82/39)=43/82` is recorded only as a conditional target, not a result.

## Compute and review rules

- CPython `3.12.3`, optimization level zero, integers/Fractions, no RNG, no
  third-party numerical libraries, no network.
- Exact enumeration cap: 60,000 rational exponent tuples; expected actual
  count is below this cap.
- Builder cap: 30 seconds and 256 MiB peak RSS.
- Research-stage checks are source, algebra, replay, and constructive
  counterexample checks. Hostile audit remains deferred to paper stage.
