# Cycle 4 P1R-CRR finite-analogue probe preregistration v1

## Claim boundary

`CONJECTURED`: this is a finite surrogate for the critical CRR balances, not
the continuous CRR witness problem.  This document freezes a discovery search
only.  It proves no CRR compatibility or incompatibility statement, no
extremizer, no saturation theorem, no new zero-density estimate, and no
short-interval consequence.

Any finite retained hit is at most `OBSERVED` (with its complex numerical
subcalculations `RECOGNIZED`).  A completed table with no retained hit does
not support a universal negative, including CRR-U.  The continuous
formalization v2 remains the analytic authority and is pinned by the sealed
artifact.  This finite protocol is deliberately a separate branch.

No search is executed by the preregistration builder.  No hostile audit is
initiated here; paper-stage promotion remains the first point at which a
hostile audit is appropriate.

## Frozen finite surrogate

For each base size `N`, set, using exact floor rational powers,

```text
H=floor(N^(6/5)), R=floor(N^(4/5)), Q=floor(N^(2/5)).
```

The ambient group is `G_H=Z/HZ`, represented by `0,...,H-1`.  A candidate is
one common pair `(b,W)`, with `b=(b_0,...,b_(N-1))`, `|b_n|<=1`, and
`W subset G_H`, `|W|=R`.  The finite diagnostics are

```text
D_b(t) = sum_(n=0)^(N-1) b_n exp(2*pi*i*n*t/H),
E_H(W) = #{(a,b,c,d) in W^4 : a+b=c+d mod H},
R_W(x) = sum_(t in W) exp(2*pi*i*t*x), x in [0,1],
B_M(x,y) = 1_(x!=y) 2 sum_(m=1)^M (1-m/(M+1)) cos(2*pi*m*(x-y)/H),
C_M(W) = N^3 tr(B_M^3).
```

`C_M` is a signed proxy, not the source `S3`; deleting the diagonal is a
deliberate finite-model choice that prevents a diagonal-only positive trace
from being scored as a cubic mechanism.  The group energy is an exact integer
count, but its use as a CRR surrogate is still only `OBSERVED`.

The exact frozen scale rows are:

| N | H | R | Q | floor(N^(7/10)) | floor(N^(3/5)) |
|---:|---:|---:|---:|---:|---:|
| 256 | 776 | 84 | 9 | 48 | 27 |
| 512 | 1782 | 147 | 12 | 78 | 42 |
| 1024 | 4096 | 256 | 16 | 128 | 64 |
| 2048 | 9410 | 445 | 21 | 207 | 97 |

## Schedule, candidates, and RNG

There are exactly `4*5*4*2=160` rows, in this sole order: increasing `N`,
then the family order below, then variant order, then replicate `0,1`.  The
master unsigned 64-bit seed is `0x43525255424F4C44`.  Row seeds are the next
160 outputs of the reference unsigned-wraparound SplitMix64 stream in that
order.  Each row initializes a fresh SplitMix64 stream at its assigned row
seed.  No system RNG, wall-clock seed, random-device call, or library-default
generator is permitted.

| Family | V1 | V2 | V3 | V4 |
|---|---:|---:|---:|---:|
| `F1-phase-rounded-frame` | 8 phase bins | 12 | 16 | 24 |
| `F2-macrocell-resonant-layers` | 2 cells | 3 | 4 | 6 |
| `F3-near-product-rational-packet` | denominator 2 | 3 | 5 | 7 |
| `F4-quadratic-modular-chirp` | modulus 257 | 263 | 269 | 271 |
| `F5-symmetric-positive-trace-spectral` | rank 2 | 3 | 4 | 5 |

The prospective runner must implement the following fixed construction
contract.  This contract resolves conventions only; it authorizes no run in
this artifact.

1. Construct an initial distinct `R`-set in `G_H` from the listed family and
   row stream.  `F1` uses a jittered `R`-frame; `F2` distributes successive
   frame points through the stated number of equal macrocells; `F3` uses the
   stated rational packet denominator before its bounded jitter; `F4` uses a
   uniform distinct stream set; and `F5` inserts each nonzero residue with its
   additive inverse before a possible final `0`.  A collision is repaired by
   the first unused residue found by forward cyclic scan.  An exhausted scan
   is `INIT_INVALID`, not a changed construction.
2. For `F1`, `F2`, `F3`, and `F5`, derive coefficients from the current common
   `W` by phase-rounding
   `sum_(t in W) exp(-2*pi*i*n*t/H)` to the stated number of equally spaced
   unit phases.  A zero vector is phase `1`; ties choose the least phase index.
   `F4` instead uses `b_n=exp(2*pi*i*(n^2+n)/p)` for its listed prime `p`.
   The candidate fails `COEFFICIENT_BOUND` if any evaluated coefficient has
   magnitude above `1` plus its recognition radius.
3. Make exactly 128 proposals.  Each proposal removes the stream-selected
   indexed member of sorted `W`, inserts the next stream-selected residue
   after the same forward collision repair, recomputes the family coefficient
   rule, and evaluates the 16-node/mode-8 proxy below.  Accept iff the proxy
   score rises by at least `2^-40`; ties and smaller rises are rejected.
   Coefficients are never separately optimized from `W`.

Thus a row does not inspect another row, a final 32-node score, or a
post-result-selected family while it is being constructed.

## Farey quadrature and cubic rules

Let `F_Q` be the increasing reduced Farey list in `[0,1]` with denominator at
most `Q`.  Give each member the closed-open midpoint cell bounded by the
midpoints to its adjacent Farey neighbors, with the endpoints `0,1` at the
two extremes.  The cells form a fixed partition of `[0,1]`; this is what
“full Farey” means here.  On every cell, map the standard Gauss--Legendre
nodes and weights of order 16 or 32 affinely to that cell.  At order `k`, set

```text
mu_k = sum(all mapped weights at nodes x with
           |R_W(x)| >= (1+0.05)*(3/4)*N^(3/5)).
```

The 16-node value is the mutation proxy; the 32-node value is the final
score.  A retained hit requires

```text
mu_32 >= (1+0.05)*(1/5)*N^(-2/5),
|mu_16-mu_32| <= 0.01*max(mu_32,(1/5)*N^(-2/5)).
```

Compute `C_8` and `C_12` from the displayed `B_M`, with the explicit
positive-sign requirements

```text
C_8>0, C_12>0,
C_12 >= (1+0.05)*(1/20)*N^(18/5),
|C_8-C_12| <= 0.05*max(|C_12|,(1/20)*N^(18/5)).
```

The 16-node/mode-8 proxy score used for a mutation is the minimum of the
four ratios for large value, lower/upper energy band, rational measure, and
positive cubic threshold; an invalid sign has score `-infinity`.  It is used
only for the frozen in-row acceptance rule and never reported as a final hit.

## Final retention, precision, and failures

A final retained hit must satisfy all of:

```text
min_(t in W)|D_b(t)| >= (1+0.05)*(3/4)*N^(7/10),
(1+0.05)*(1/4)*N^2 <= E_H(W) <= 4*N^2/(1+0.05),
the Farey and cubic final rules above.
```

The integer energy is recorded exactly.  Every complex quantity is evaluated
at 256 and 384 bits with CPython 3.12.3 and mpmath 1.2.1.  Its
*recognition ball* is centred at the 384-bit value and has empirical radius
twice the larger of the inter-precision difference and
`2^-256*(1+|centre|)`.  Every value used by a retained final inequality must
have radius strictly below `10^-30*N^(7/10)`.  This is a stability screen,
not interval certification; complex results remain `RECOGNIZED`.

The complete run has a hard aggregate wall cap of 55 minutes and a hard
process RSS cap of 1 GiB.  If either cap fires, the active row is retained as
`RESOURCE_CAP` and every unstarted scheduled row is retained once as
`GLOBAL_CAP_UNREACHED`; there is no resume or parameter-changing retry.
Otherwise every scheduled row is retained exactly once as `RETAINED_HIT`,
`NO_RETAINED_HIT`, or a specific failure code.  Other required codes are
`INIT_INVALID`, `COEFFICIENT_BOUND`, `SET_CARDINALITY`, `SET_DUPLICATE`,
`SET_DOMAIN`, `NONFINITE`, `RECOGNITION_RADIUS`,
`QUADRATURE_DISAGREEMENT`, `CUBIC_PROXY_DISAGREEMENT`, and `REPLAY_MISMATCH`.
No code may be dropped, merged away, or retried with changed parameters.

`RETAINED_HIT` is an `OBSERVED` finite configuration only.  An all-miss table,
a resource-limited table, or a precision/failure table is not evidence for a
universal incompatibility statement.  Any analytic use requires a separate
proof route from the finite discovery artifact.

## Replay boundary

The builder creates only the sealed preregistration artifact and checks it
byte-for-byte.  It does not import a future search runner, evaluate a Farey
node, mutate a candidate, or create discovery results.  A future execution
must first use this exact schedule and write a new `discovery/` artifact; it
may not rewrite this preregistration.
