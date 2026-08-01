# Cycle 10 E1/E2 engine preregistration v1

## Claim boundary

`OBSERVED`: this document freezes the first exact research block for E1
polyphonic zero detection and E2 centred nonbacktracking trace. It proves no
new large-value estimate, zero-density exponent, short-interval result,
Base/CRR incompatibility, or L-function extension.

`PROVED` by source inspection in this run: the pinned Guth--Maynard zero
detector first produces `O(log T)` dyadic lengths and then selects one length;
its singular-value argument already subtracts the scalar cubic mean
`tr(G)^3/|W|^2`. Therefore mere dyadic colouring and mere scalar centring are
baseline operations, not new engines.

The source is
`artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex`, SHA-256
`36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428`.
The relevant source regions are TeX lines 497--590 and 2280--2408.

## Frozen E1 object

Let `M` be an `m x n` complex matrix. Let `b^(1),...,b^(K)` be detector
columns and let positive rational weights `omega_j` sum to one. Freeze

```text
B = sum_j omega_j b^(j) b^(j)*,
K_B = M B M*,
q_t = (K_B)_(t,t) = sum_j omega_j |(M b^(j))_t|^2.
```

The E1 toy theorem to prove is

```text
#{t:q_t>=V^2} V^(2r) <= tr(K_B^r),       r in Z_(>=1).
```

The exact source bridge to be exposed is the colour-cover consequence: if
each retained row has `|(M b^(j(t)))_t|>=V`, then uniform weights give
`q_t>=V^2/K`. The theorem must record the complete factor `K^r`; it may not
hide it in constants. A pure partition/pigeonhole bound is the registered
countermodel: it changes no power exponent when `K=T^o(1)` and supplies no
gain over applying a scalar estimate to the largest colour.

`CONJECTURED`: E1 can improve an exponent only if the source construction
provides additional frame structure that yields a mixed-trace saving larger
than the explicit colour loss. No such source construction is assumed here.

## Frozen E2 objects

Let `G` be an `m x m` Hermitian matrix with constant diagonal `d`, and put

```text
A = G-dI,
r_i = sum_(j != i) |A_(i,j)|^2,
R = diag(r_1,...,r_m),
C_2 = A^2-R.
```

The E2 toy theorem to prove is the exact two-step-return decomposition

```text
||C_2||_F^2 = tr(A^4)-sum_i r_i^2
```

and the spectral consequence

```text
lambda_max(G) <= d + sqrt(max_i r_i + ||C_2||_op)
              <= d + sqrt(max_i r_i + ||C_2||_F).
```

Also freeze the closed nonbacktracking length-four polynomial

```text
NB4(A) = tr(A^4)-2 sum_i r_i^2+sum_(i != j)|A_(i,j)|^4.
```

The registered sign test searches real symmetric zero-diagonal matrices of
orders `3<=m<=6`, entries in `{-2,-1,0,1,2}`, lexicographic order, stopping at
the first `NB4<0`. The search cap is `250000` matrices per order, no RNG. A
surviving negative example contains only the claim that raw `NB4` is not a
general one-sided PSD surrogate; it does not terminate E2. If no example is
found, the result is `OBSERVED` bounded-search survival only.

The registered phase-lattice benchmark uses only the already sealed exact
alias and Base artifacts:

- CRR v2 SHA-256
  `e26be797539eabe53ee765b7067d1c99fe4d440035e27785cf38aa64bc2fc84e`;
- phase-lattice Base SHA-256
  `3207a7764470d5512d20778e739e0e0bdc31535c0b2ac68b8366707304678534`;
- signed extremizer SHA-256
  `9616ef55eec03f2f11ba2b625fd9e8cbd3c4ad581900a8a441ce9ed130d05796`.

No floating actual-log matrix is authorized in v1. The exponent translation
must be symbolic: at the frozen scales, Base requires sampled eigenvalue
`lambda>=v^(12-o(1))`; E2 must state the corresponding necessary alternative
for `max r_i` or `||C_2||` without claiming either side is small.

## Exact-arithmetic and resource rules

- Universal identities are proved algebraically in the theorem note and
  replayed using integers/Fractions; finite checks are corroboration, not the
  universal proof.
- The proof builder and focused tests use CPython `3.12.3`, optimization level
  zero, no third-party numerical library, no RNG, and no network.
- Builder wall-time cap: 30 seconds. Peak-RSS cap: 256 MiB.
- The first sealed artifact is immutable. Any defect requires a versioned
  correction artifact.
- Research-stage checks are source, algebra, replay, and constructive
  counterexample checks only. Hostile audit is deferred to paper stage.

## Outcomes and continuation

- `E1_FRAME_IDENTITY`: the exact trace inequality and colour cost are proved.
- `E2_TWO_STEP_IDENTITY`: the exact return-deleted identity and spectral
  inequality are proved.
- `NB4_SIGN_COUNTERMODEL`: an exact negative raw-`NB4` example is found.
- `NO_COUNTERMODEL_WITHIN_CAP`: the bounded sign search survives; no
  universal positivity claim follows.
- `CONTAINED_FAIL`: an algebra/source/replay check fails; contain that row,
  record it, and continue safe work on the other engine.

The next research object after closure is an E1+E2 hybrid inequality for
`K_B`: determine whether detector-frame structure controls its row-return
term and two-step excess with a net fixed-power margin after the colour cost.
