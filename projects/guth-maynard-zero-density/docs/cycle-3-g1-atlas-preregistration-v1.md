# Cycle 3 G1 critical-cell and extremizer atlas preregistration v1

Date frozen: 2026-08-01 UTC, before any G1 atlas row was evaluated.

## Claim boundary and source pins

This document freezes a finite discovery protocol. It proves no new
large-values estimate, density estimate, short-interval theorem, extremizer,
or saturation result. Exact source-formula substitutions may be `PROVED`;
finite complex experiments are at most `RECOGNIZED`; cross-row patterns are
at most `OBSERVED`.

Pinned source: Guth--Maynard arXiv `2405.20552v2`, source-tar SHA-256
`9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc`,
TeX SHA-256
`36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428`.
Locators: Theorem 1.1 and comparator, TeX lines 68--94; Proposition 11.1 and
energy discussion, lines 1785--1820; Section 13.1 transfer, lines 2307--2364;
critical final remark, line 2398.

`PROVED`: the source's displayed comparison is strictly favorable in the
epsilon-separated window `7/10 < log(V)/log(N) < 4/5` when
`log(N)/log(T) < 5/6` in the stated regime. Theorem 1.1 itself is not assigned
that restricted range. Boundary rows are comparison-only.

`PROVED`: the local bottleneck in the final remark is
`(s,n,v,w)=(7/10,5/6,7/10,2/3)` after writing
`n=log L/log U`, `v=log V/log L`, and `w=log|W|/log U`. Its original
zero-detection coordinates are `(s,n0,k,q)=(7/10,5/13,2,10/13)`.
The charts must never be identified silently.

## Exact charts and frozen domains

Local chart:

```text
s = 7/10 + i/100,                  0 <= i <= 10
n = 3/4 + j/60,                    0 <= j <= 15
v = 7/10 + h/100,                  0 <= h <= 10
w in {1/2, 7/12, 2/3, 3/4}
```

All fractions are reduced before IDs or hashes are formed. The resulting
base atlas has exactly `11*16*11*4 = 7744` rows. The range `3/4<=n<=1` is
the Proposition 11.1 length range; the `v` interval is the comparison window,
not a hypothesis of Theorem 1.1.

Zero-detection transfer chart, separately for every frozen `s`:

```text
n0 in {j/100: 2 <= j <= 50} union {5/13, ell(s)/2}
ell(s)=10/(6+10s),  u(s)=15/(6+10s)
if n0 <= ell(s)/2: k=ceil(ell(s)/n0)
otherwise:          k=2
q=k*n0
alpha(s)=15(1-s)/((3+5s)(18/5-4s))
B(s)=15(1-s)/(3+5s)
```

Duplicates are reduced and removed. The source-active detector range is
strictly `n0>1/100`; no `n0=1/100` row is present. The `n0=1/2` row is
labelled `ASYMPTOTIC_ENDPOINT_ONLY`, because the source has
`n0<=1/2+o(1)` rather than an exact finite-`T` endpoint. Other feasible rows
are `EXACT_POWER_SCALE`. Every row records `1<=k<=77`, `q=k*n0`,
`ell(s)<=q`, and either `q<=u(s)` exactly or the quarantined
`q<=u(s)+o(1)` endpoint statement. The mandatory
`(7/10,5/13,2,10/13)` anchor must exist.

## Exact activity and envelope-sensitivity map

For every local row compute with `fractions.Fraction`:

```text
A1 = 2n(1-v)
A2 = n(18/5-4v)
A3 = 1+n(12/5-4v)
G  = max(A1,A2,A3)

C1 = 2n(1-v)
C2 = 1+n(1-2v)
C3 = 1+n(4-6v)
C  = max(C1,min(C2,C3))
Delta_LV = C-G
```

Record all pairwise signed residuals and complete tie sets. `Delta_LV>0`
compares the two published displayed bounds only; it is no new inequality.

Energy labels are permitted only on the exact diagonal `v=s`. There compute

```text
E1 = w+n(4-4s)
E2 = (21/8)w+1/4+n(1-2s)
E3 = 3w+n(1-2s).
```

Off-diagonal rows have `energy_eligible=false` and no E labels. At the
mandatory local bottleneck all three E terms must equal `5/3`. Each transfer
row records `B(s)`, its `q<=alpha(s)` or `q>alpha(s)` branch, every source
term exponent, and the exact residual against `B(s)`. This is required for
mechanical P2C/envelope sensitivity; active-term labels alone are inadequate.

## Frozen empirical spine

Finite experiments occur only on:

```text
s in {7/10,3/4,4/5}
n in {4/5,5/6}
v in ({s-1/100,s,s+1/100} intersect [7/10,4/5])
w in {1/2,2/3,3/4}
```

This is exactly 42 coordinate rows. The 14 registered coefficient/set pairs
below create exactly 588 screening rows at `U=2^12`. Infeasible registered
combinations remain rows; they are never dropped.

## Coefficient conventions

Let `L=floor(U^n)`, support `m in {L+1,...,2L}`, and
`H=max(1,floor(L^v))`.

- `C0-flat`: `b_m=1`.
- `C1-tent`: centre `c=L+floor(L/2)` and
  `b_m=max(0,1-|m-c|/H)` exactly as a rational real number.
- `C2-two-tent`: centres `c1=L+floor(L/3)`,
  `c2=L+floor(2L/3)`, half-width `h=max(1,floor(H/8))`; use the same tent
  formula with phases `+1,-1`. If supports overlap, add and reject the row if
  `|b_m|>1`; no renormalization is allowed.
- `C3-root-chirp`: `b_m=exp(2*pi*i*(m mod 509)^2/509)` as an algebraic root
  specification; numerical evaluation is `RECOGNIZED`.
- `C4-rademacher`: signs from the pinned SplitMix64 coefficient stream.
- `C5-point-aligned`: for the least point `t0` of the companion W,
  `b_m=exp(-i*t0*log m)`; this probes one-point coherence only.

Every row checks `|b_m|<=1`. Exact rational coefficients are serialized as
reduced pairs; phase coefficients are serialized by their defining integers,
not platform complex bytes.

## Set conventions

Set `M=floor(U^w)`. Every W must be an increasing subset of
`{0,...,U}`, have exactly M distinct points, and be 1-separated.

- `W0-sidon`: only for `w=1/2`; greedily scan `0,...,U`, accepting a point
  iff every new unordered pair sum differs by more than 1 from every retained
  pair sum. At other w record `INFEASIBLE_CARDINALITY`.
- `W1-uniform`: consume SplitMix64 set-stream values modulo `U+1`, rejecting
  duplicates until M values occur; fail after `100(U+1)` draws; then sort.
- `W2-jitter`: start with `floor(j(U+1)/M)`, add stream jitter in `{-1,0,1}`
  and clamp to `[0,U]`; on collision choose the least unused integer at or
  above the candidate, wrapping once to 0; fail if none exists; then sort.
- `W3-AP`: `a=floor(U/7)`,
  `h=max(1,floor((U-2a)/max(1,M-1)))`, points `a+jh`; reject if the last
  point exceeds U.
- `W4-four-block`: `r=ceil(M/4)`, origins
  `floor((2b+1)U/8)`, `0<=b<4`, within-block step
  `max(1,floor(U/(32r)))`; traverse blocks then indices, take the first M
  distinct in-range values, and sort; otherwise fail.
- `W5-rational`: `Q` is least with `Q^3>=U`, `r=(Q+8)/Q`, and
  `h=floor(2*pi/abs(log r)+1/2)` using the positive half-up convention.
  Centre the size-M AP by `a=floor((U-(M-1)h)/2)`; if `a<0`, record
  `INFEASIBLE_CARDINALITY`.

The exact additive energy diagnostic is
`#{(a,b,c,d) in W^4: |a+b-c-d|<=1}`, computed from exact pair-sum
multiplicities. W5 probes one rational resonance only; it is not the source's
simultaneous affine near-obstruction.

Registered pairs, in this exact order:

```text
(C0,W0) (C0,W1) (C0,W3) (C1,W1) (C1,W3)
(C2,W2) (C2,W4) (C3,W0) (C3,W5) (C4,W0)
(C4,W1) (C4,W2) (C5,W3) (C5,W5)
```

No conditional family insertion is allowed.

## RNG, precision, retention, refinement, and resources

SplitMix64 uses unsigned 64-bit wraparound with seed
`0x47554d41594e4731`; coefficient and set streams XOR respectively
`0x434f454646000001` and `0x57414c5545000001`, then the lexicographic
screen-row number. No library or system RNG is permitted.

Complex values are evaluated independently at 256 and 384 bit precision.
For declared low/intermediate/high regimes use energy targets respectively
`M^2`, `max(M^2,M^4/U)`, and `M^3`. Define

```text
rho_value  = log(min_W |D(t)| / L^v)/log U
rho_energy = -abs(log(E(W)/E_target)/log U).
```

A screen row is retained iff both precisions give
`rho_value>=-1/400`, `rho_energy>=-1/400`, and corresponding margins differ
by at most `1/1600`. This is a `RECOGNIZED` selection rule, not a certified
proof margin. Rank by `min(rho_value,rho_energy)`, then row ID.

Retain at most two rows per `(declared energy regime, coefficient family)`,
at most 36 total. Replay each retained row, unchanged, at `U=2^15` and
`U=2^18`, at most 72 validation rows. Around each retained coordinate add an
exact-only `3^3` `(s,n,v)` cube with increments
`(1/300,1/180,1/300)`, fixed w, intersected with the base domain; no new
finite experiment is authorized there. Deduplicate exact triples.

Caps: 180 seconds and 2 GiB RSS per finite row; 128 aggregate CPU-hours.
The scheduled maximum is 660 finite rows and hence at most 33 CPU-hours at
the per-row ceiling. A timeout, memory breach, nonfinite value, precision
disagreement, invalid coefficient, invalid spacing, infeasible construction,
or replay mismatch is retained with its distinct failure code and receives no
parameter-changing retry.

## Artifacts, tags, and G1 decision

The deterministic preregistration artifact freezes this document hash,
runtime/library versions, grids, formulas, conventions, row counts, families,
pairs, seed, precision, caps, and failure policy. Discovery writes a
timing-independent sorted observation artifact plus a separate `OBSERVED`
performance record. Every one of the 7744 structural rows and 588 screen rows
must occur exactly once.

An exact integer energy enumeration has radius zero and may be
`CERTIFIED_NUMERICAL` only for that finite count with its explicit comparison
margin. Complex values and scores are `RECOGNIZED`; cross-scale patterns are
`OBSERVED`. No discovery output enters `proof/` or becomes a theorem.

G1 route selection:

- choose P2A only if retained rows isolate a trace feature absent from the
  cubic terms;
- choose P2B only if the active obstruction is consistently energy/affine
  structure;
- choose P2C only if the exact transfer map identifies a named decomposition
  or branch loss after local candidates are propagated;
- choose a combination only with separate labeled evidence for each route;
- otherwise record `NO_SELECTION` and every rejected route. This is not a
  saturation theorem.

Falsifiers: the mandatory bottleneck/tie identities fail; any scheduled row is
missing; a supposedly feasible W or coefficient violates its invariant; the
two precisions exceed the tolerance; a candidate loses its score at a larger
scale; or exact propagation shows it cannot affect the `30/13` envelope. Each
surviving falsifier is preserved as the headline outcome of its scope.
