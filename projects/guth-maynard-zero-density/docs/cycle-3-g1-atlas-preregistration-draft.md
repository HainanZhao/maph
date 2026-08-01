# Draft: Cycle 3 G1 atlas preregistration

**Claim boundary.** This is a proposed finite discovery protocol, written before
any G1 evaluation.  It is not itself a frozen preregistration, does not authorize
a search, and proves no new large-values, density, or short-interval statement.
Every numerical row produced under a successor protocol remains discovery-only.

`PROVED` (source scope): the pinned Guth--Maynard source has (i) its
large-values range `7/10 <= log(V)/log(N) <= 4/5`, (ii) its energy proposition
in the local range `T^(3/4) <= N <= T`, and (iii) the zero-density critical
pattern
`s=7/10`, `N_0=T^(5/13)`, `L=N_0^2=T^(10/13)`,
`U=T^(12/13)`, `L=U^(5/6)`, `V=L^(7/10)`, and
`|W|=U^(2/3)`.  At that pattern all three displayed energy terms have exponent
`5/3` in `U`; the source expressly identifies `S_3` as the remaining possible
source of improvement and describes the random-energy and rational-affine
near-obstruction.  These are source statements and exact substitutions already
checked in Cycle 1, not extremizer theorems.

Source locators: `LargevaluesDirichlet17.tex`, Theorem 1.1, lines 64--79;
Proposition 11.1, lines 1785--1804; the refined `S_3` estimate, lines
1675--1763; and the final Section 13.1 Remark, line 2398.  The pinned TeX hash
is `36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428`.

`CONJECTURED`: a finite atlas which deliberately includes random-like,
additively structured, and rational-affine families can distinguish a useful
local target from an apparent extremizer family.  Failure of this finite atlas
is not evidence of a universal no-go result.

## 1. Coordinates: two charts, never silently identified

The protocol must carry both charts in every row.

| Chart | Exact coordinates | Purpose |
|---|---|---|
| Local large-values | `n=log(L)/log(U)`, `v=log(V)/log(L)`, `w=log(|W|)/log(U)` | Theorem 1.1 / Proposition 11.1 / `S_3` architecture. |
| Zero-detection transfer | `s`, `n_0=log(N_0)/log(T)`, `q=log(N_0^k)/log(T)` | Maps a possible local gain through the checked Section 13.1 branches. |

`PROVED` (conditional on the frozen source formulas): the local bottleneck is
`(n,v,w)=(5/6,7/10,2/3)`.  The transfer chart has
`s=7/10`, `n_0=5/13`, `q=10/13`; the local length is `L=N_0^2`, and `U` is a
subinterval.  Thus `n`, `n_0`, and `q` are different coordinates.  A row that
does not state its chart is invalid.

Freeze the following closed rational domain before any run:

```text
s in {70/100, 71/100, ..., 80/100}
n in {45/60, 46/60, ..., 60/60}
v in {70/100, 71/100, ..., 80/100}
w in {1/2, 7/12, 2/3, 3/4}
n_0 in {1/100, 2/100, ..., 1/2}
q in {j/600 : 0 <= j <= 600}, retained only when l(s) <= q <= u(s)
```

Here `l(s)=10/(6+10s)`, `u(s)=15/(6+10s)`, and
`alpha(s)=15(1-s)/((3+5s)(18/5-4s))`, all evaluated with exact rational
arithmetic.  The local-chart grid has `11*16*11*4` rows before family choices.
The transfer chart records every admissible `q` together with the exact labels
`q<=alpha(s)` and `q>alpha(s)`; it does not sample an unregistered real
parameter.

The frozen **primary probe spine** is the subset

```text
s in {7/10, 3/4, 4/5},
n in {4/5, 5/6},
v in {s-1/100, s, s+1/100} intersect [7/10,4/5],
w in {1/2, 2/3, 3/4}.
```

The full grid is an exact activity atlas; numerical coefficient/set trials begin
only on the spine.  It therefore has exactly 42 coordinate rows before the 14
predeclared coefficient/set pairs, or 588 screening rows.  This makes the
published `s=7/10` bottleneck and the historical `s=3/4` / `n=4/5` comparison
visible without pretending that a finite simulation covers all real parameters.

## 2. Exact activity map and adaptive rule

For each local row, calculate using `fractions.Fraction`:

```text
A_1 = 2n - 2nv
A_2 = (18/5)n - 4nv
A_3 = 1 + (12/5)n - 4nv
E_1 = w + n(4-4v)
E_2 = (21/8)w + 1/4 + n(1-2v)
E_3 = 3w + n(1-2v).
```

These are only the exponent forms of the three displayed large-values and
energy terms.  A successor must record the maximum, its complete tie set, and
every signed pairwise residual, not merely a chosen active term.  It must also
record the exact transfer-cell labels from the preceding section.

After the primary spine, adaptive refinement is permitted only as follows:

1. A retained discovery row creates the `3 x 3 x 3` cube with increments
   `(1/300, 1/180, 1/300)` in `(s,n,v)`, intersected with the frozen domain;
   `w` and family parameters do not change.
2. At most 3 retained rows per `(energy-regime, coefficient-family)` create a
   cube, ranked by the frozen score below and then lexicographically by row ID.
3. Duplicates are retained once, and every omitted row is written with the
   reason `quota`, `outside-domain`, or `not-retained`.

No adaptive step may introduce a new family, scale, coordinate range, score, or
random stream.  The exact activity map is recomputed at every refined cell.

## 3. Finite coefficient families

All polynomials have support on the integer interval `(L,2L]` and must satisfy
`|b_m|<=1` entrywise before any value calculation.  Coefficient definitions are
part of the artifact, rather than inferred from a display.

| ID | Finite family and frozen parameters | Reason for inclusion |
|---|---|---|
| `C0-flat` | `b_m=1`. | Baseline coherent polynomial. |
| `C1-block` | One smooth discrete block of width `H=floor(L^v)`, centred at `L+floor(L/2)`, with a pinned compactly supported tent weight. | Discrete version of the published lower-example geometry. |
| `C2-multiblock` | Two disjoint translates of a tent block of width `floor(H/4)`, with fixed phases `1,-1`. | Tests packed coherent components without relaxing the `ell_infinity` hypothesis. |
| `C3-root-chirp` | `b_m=exp(2*pi*i*m^2/509)`. | Finite oscillatory, algebraically specified coefficients. |
| `C4-rademacher` | `b_m in {-1,1}` from SplitMix64. | Random-like control family. |
| `C5-point-aligned` | For the lexicographically first `t_0` of the companion set, `b_m=exp(-i*t_0*log(m))`. | Tests the deliberately coherent one-point extreme; it is not evidence of many large values. |

The tent in `C1` and all rounding rules must be placed in a conventions module
before execution.  The phase values in `C3` are exact roots of unity as
coefficient specifications; evaluations of `m^(it)` are not exact.

## 4. Finite large-value-set and affine probes

Every `W` is an increasing integer subset of `[0,U]`, has no duplicate, and is
checked to be 1-separated.  Set size is
`M=floor(U^w)` (with the lower endpoint included only if this preserves the
declared cardinality).  Its exact additive energy is

```text
E_1(W)=#{(a,b,c,d) in W^4 : |a+b-c-d|<=1}.
```

| ID | Construction | Regime tested |
|---|---|---|
| `W0-sidon` | Greedy integer Sidon construction: scan `0,1,...,U`, retain the first point whose new unordered pair sums differ by more than one from all old sums.  It is run only at `w=1/2`; at larger `w` it is a predeclared `infeasible-cardinality` row. | Low energy / near-diagonal. |
| `W1-prng-uniform` | Sort the first `M` distinct SplitMix64 residues modulo `U+1`; restart by the pinned rejection rule if a duplicate occurs. | Random-like intermediate energy. |
| `W2-jitter-grid` | `floor(j*U/M)+e_j`, with `e_j` the prescribed bounded SplitMix64 jitter, then deterministic collision repair to the least unused integer. | Random-like intermediate energy with controlled spacing. |
| `W3-AP` | `a+jh`, `0<=j<M`, where `h=floor((U-2a)/(M-1))` and `a=floor(U/7)`. | High energy / additive structure. |
| `W4-block-AP` | Four equal arithmetic blocks.  Put `r=ceil(M/4)`, origins at `floor((2b+1)U/8)` for `0<=b<4`, and within-block step `max(1,floor(U/(32r)))`; take the first `M` entries in block order. | Tunable intermediate-to-high energy. |
| `W5-rational-resonant` | Let `Q` be the least integer with `Q^3>=U`; take `r=(Q+8)/Q`, `h=round(2*pi/abs(log(r)))`, and the maximal translated AP of size `M` with step `h` in `[0,U]`; if it cannot fit, record `infeasible`. | The source’s rational/affine obstruction shape. |
| `W6-two-scale` | Split `M` as `M_1=floor(M/2)`, `M_2=M-M_1`; put the two APs at origins `floor(U/8)` and `floor(5U/8)`, with `h_1=2*floor(U/(16*max(1,M_1)))+1` and `h_2` the least integer greater than `h_1` coprime to `h_1`. | Mixed structured/intermediate regime. |

`W0-sidon` is deliberately a finite greedy model, not a claim of asymptotic
Sidon optimality.  `W5-rational-resonant` gives a controlled peak of
`R(r)=sum_{t in W} r^(it)`; it is **not** claimed to realize the simultaneous
affine near-obstruction described by Guth--Maynard.  This distinction must
remain in every report.

The frozen pair list, instead of an uncontrolled Cartesian product, is

```text
(C0,W0) (C0,W1) (C0,W3) (C1,W1) (C1,W3)
(C2,W2) (C2,W4) (C3,W0) (C3,W5) (C4,W0)
(C4,W1) (C4,W2) (C5,W3) (C5,W5).
```

This gives low (`W0`), intermediate/random (`W1,W2,W4,W6`), high (`W3`), and
rational-affine (`W5`) coverage while keeping the first pass finite.  `W6` is
included in the frozen family registry but omitted from the primary pair list;
it is exercised only by the already-specified refinement quota if its matching
regime has no retained row.  That exception is deterministic and must be logged.

## 5. Scales, seed, resources, and failure rows

Use the reference 64-bit SplitMix64 recurrence implemented in the project, with
unsigned seed `0x47554d41594e4731`.  Separate streams are obtained by XOR with
the fixed tags `0x434f454646000001` (coefficients) and
`0x57414c5545000001` (sets), then by the lexicographic row number.  No system
RNG, wall-clock seed, or library-default generator is permitted.

Screen every one of the 588 primary-pair/spine rows at `U=2^12`.  Per energy
regime and coefficient family retain at most three rows which meet the retention
rule, hence at most 54 rows in total; replay those rows at `U=2^15` and `U=2^18`.
The exact activity map has no scale and is always complete.  The maximum
discovery budget is 128 CPU-hours, 2 GiB resident memory, and 180 seconds per
row; a performance artifact records wall time and peak RSS separately from
mathematical observations.  Any timeout, memory breach, underflow/overflow,
infeasible construction, spacing failure, coefficient-bound failure, or precision
disagreement creates a retained failed row.  It may not be rerun with altered
parameters within this version.

## 6. Observables and retention rule

For a valid row, record:

1. exact `M`, spacing minimum, and `E_1(W)`; `e=log(E_1(W))/log(U)` only as a
   display value;
2. `min_{t in W}|D(t)|`, `max_{t in W}|D(t)|`, and the threshold ratio
   `min|D(t)|/L^v`;
3. the exact three local large-values and three energy exponents, their tie
   labels, and their slacks;
4. `||R||_2^2`, `||R||_4^4` on the pinned 4096-point quadrature, plus the
   rational-resonance/affine-incidence proxy on the finite rational list
   `{(a+1)/a: 2<=a<=floor(U^(1/3))}`; and
5. hashes of canonical coefficients, `W`, configuration, source inputs, and
   executing code.

The **retention score** is the minimum of the following two exponent margins:

```text
rho_value  = log(min_{t in W}|D(t)|/L^v)/log(U),
rho_energy = -abs(log(E_1(W)/E_target)/log(U)),
```

where `E_target` is respectively `M^2`, `M^4/U`, or `M^3` for the declared
low, intermediate, or high regime.  A row is retained iff

```text
rho_value >= -1/400 and rho_energy >= -1/400,
```

at both 256-bit and 384-bit complex evaluations, with the two displayed margins
within `1/1600`.  Ties are resolved by the canonical row ID.  This is a selection
threshold, not a proof margin and not a statement that the target energy is
sharp.  The rational-affine proxy is diagnostic only and cannot independently
retain a row.

## 7. Artifact schema and epistemic firewall

The immutable configuration artifact should be
`artifacts/cycle-3-g1-atlas-preregistration-v1.json`, generated from this frozen
document.  It includes the full formula strings, every rational list, families,
pair list, rounding convention, seed, source hashes, expected row counts,
resource caps, retention rule, and a SHA-256 of the generating script.

The discovery run writes the timing-independent
`artifacts/cycle-3-g1-atlas-observations-v1.json`, with sorted rows:

```json
{
  "row_id": "...", "chart": {"local": {...}, "transfer": {...}},
  "family": {"coefficient": "C...", "set": "W...", "parameters": {...}},
  "scale": "2^12", "seed_stream": "0x...", "input_hashes": {...},
  "validity": {"coefficient_linf": true, "one_separated": true},
  "exact_observables": {...}, "recognized_observables": {...},
  "activity_labels": {...}, "status": "...", "retention": {...},
  "failure": null
}
```

`PROVED` may label only an exact symbolic source-formula comparison whose cited
hypotheses are recorded and checked.  A finite integer energy count must instead
be labelled `CERTIFIED_NUMERICAL` only if an independently checked exact
enumeration supplies radius `0` and an explicit stated comparison margin.
Complex large-value, quadrature, affine-proxy, and phase-aligned observations
are at most `RECOGNIZED`; cross-row patterns are at most `OBSERVED`.  No retained
row is a theorem, a sharpness result, or a density improvement.  Discovery code
lives under `discovery/`; no `proof/` module may import its output.

## 8. Predeclared falsifiers and G1 decision rule

The following outcomes are more informative than a favorable-looking score.

1. `CONJECTURED` low-energy route: an admissible low-energy row that is retained
   at all three scales, has a stable rational-affine proxy, and lies in an
   envelope-sensitive transfer cell refutes the working assumption that only
   high energy is relevant.  Preserve it as a P2A/P2B candidate; it is not a
   theorem.
2. `CONJECTURED` saturation candidate: an admissible intermediate or high-energy
   row that remains within `1/400` of every designated local term and the
   published random-energy scale at all three scales refutes any claim that the
   corresponding proposed local improvement is automatically available.  It
   opens P4 as an obstruction candidate, not a no-go theorem.
3. `PROVED` later containment rule: only after a candidate inequality has a
   frozen exact parameter polytope may the P3 transfer optimizer show that it
   leaves the `30/13` envelope unchanged.  That result sends the candidate to
   `CONTAINED`; G1 itself must not assert such a conclusion from its samples.
4. A missing retained row, a nonconvergent row, or a resource breach is not a
   no-go result.  It is a failed discovery row and blocks only that row/family
   at this version.

G1 selects P2A only if retained low/intermediate-energy rows point to a trace
feature not represented by the cubic terms; P2B only if energy profiles are the
common active obstruction; and P2C only if neither kind of candidate survives
but the frozen transfer chart identifies a specifically audited decomposition
loss.  A combination requires finite, labeled evidence for each constituent.
Every rejected route and every not-yet-transferable candidate is written to the
G1 decision artifact.  A proof-grade route still needs a separate theorem,
independent verification, and a full density propagation audit.
