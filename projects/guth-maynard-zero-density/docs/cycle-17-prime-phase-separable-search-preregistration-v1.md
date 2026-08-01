# Cycle 17 prime-phase separable search preregistration v1

## Claim boundary

`OBSERVED`: this is a discovery search for finite rank-one prime-phase
countermodels or structural separation. No finite miss, fitted exponent, or
optimizer output is proof of an asymptotic estimate.

The search may identify coefficient/row families for exact follow-up or
falsify a proposed numerical formulation. It may not promote a density gain,
a prime restriction theorem, or a universal negative.

## Frozen model

For each `m in {16,24,32,48,64}`:

1. set `x_0=ceil(4m log(4m))`;
2. deterministically sieve primes in `[x_0,2x_0]` and take the first `m`;
3. set `H=floor(m^(12/5))`, `V=m^(7/10)`, and integer rows
   `t in {0,...,H}`;
4. evaluate `P_a(t)=sum_j a_j p_j^(it)` with `|a_j|=1`.

The use of `m` rather than the dyadic endpoint removes finite logarithmic
prime-count distortion. It is a model of the exponent geometry, not a source
substitution.

## Frozen optimizer

Use NumPy `1.26.4`, complex128, RNG `PCG64`, seeds `0,...,7`. For each `m`
and seed run two initializations:

- independent uniform phases;
- coherent phases aligned at `t=floor(H/2)`.

Run 25 alternating iterations:

1. evaluate all integer rows;
2. retain the `R_select=min(H+1,ceil(m^(8/5)))` largest magnitudes;
3. form the fourth-moment phase gradient
   `g_j=sum_(t in W) conjugate(p_j^(it)) |P_a(t)|^2 P_a(t)`;
4. replace `a_j` by `g_j/|g_j|`, retaining the old phase if `g_j=0`;
5. accept the update only if the selected fourth-moment objective does not
   decrease.

After the final iteration record:

- number of all rows with `|P_a(t)|>=V`;
- normalized exponents `log(max(count,1))/log(m)`;
- selected fourth moment divided by `m^2` (the separable Rayleigh quotient);
- full-grid `24/5` moment divided by `H m^(12/5)`;
- top ten row locations and magnitudes;
- coefficient hash.

## Frozen benchmarks and outcomes

- `BASELINE_APPROACHED`: some run has count exponent at least `3/2`.
- `TARGET_CROSSED`: some run has count exponent at least `36/25`.
- `NO_TARGET_CROSSING`: neither occurs.

These labels describe the finite search only. A crossing is a candidate
countermodel requiring exact/asymptotic reconstruction; a miss leaves the
conjecture open.

Also run deterministic coefficient families: all ones, alternating signs,
quadratic phase in prime index, and alignments at rows `0,H/4,H/2,3H/4`.

## Resource and review rules

- No network. Matrix evaluation is chunked at 8,192 rows; do not allocate a
  full `H by m` matrix.
- Wall cap: 120 seconds. RSS cap: 512 MiB.
- Persist every registered run, including failures; no post-result seed or
  threshold changes.
- Hostile audit remains deferred to paper stage.
