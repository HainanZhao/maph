# Cycle 165 working decision summary v1

`EXPLORATORY`; not a sealed claim or a density/interval result. This compact
ledger records one substantive block. Frozen formulas and the next proof
attempt are in `docs/cycle-165-seed-factorization-preregistration-v1.md`; do
not append derivational scratch here.

## Frozen question and retained failed paths

- Original question: does a typed map
  `TransportRow63 -> UpperAtom87 -> WebLeaf164` preserve the Cycle-67 seed
  predicate, especially the absolute shift `beta`?
- `OBSERVED`: sealed builders give no constructor from Cycle 63 to Cycle 87.
  This is a finite typed-interface cut, not a field-wide no-ancestry theorem.
  `TransportRow63` retains `(alpha,beta,h,j,L_pkt,q,a,...)`; upper/web atoms
  do not retain these fields.
- `SUPERSEDED`: the initial source-condenser draft assumed an actual Cycle-63
  Fourier atom `z_r`. Cycle 63 is only a positive fixed-beta census; it has
  no inherited source Fourier moment. Do not revive this as a Cycle-87
  pullback.
- `PROVED` finite-model warning: a scalar fourth moment can be created by
  cross-payload coherence of many small beta fibres. Fibre extraction needs a
  beta-averaged/diagonal payload moment or a new inverse.
- `CONJECTURED`, retained alternative: payload lift, seed-detector completion,
  and the two-jet lift may still work, but none is a source representation.

## Primary new engine: compact beta detector

`EXPLORATORY`; the source state is `(h,ell,w)` with `0<=w<=1`,
`H<=h<=2H`, `alpha_ell=exp(2pi ell/Delta)-1`, and
`x_(h,ell)=h alpha_ell (mod 1)`. `beta` is a single external circular anchor;
an integer `j` is recovered only when a source point is in its Cycle-63 strip.
For the graph inverse, use a fixed nonnegative smooth bump `psi`, equal to one
on the strip core and supported on a larger fixed interval, then set
`psi_X(t)=sum_(k in Z)psi(X(t+k))`. Set

```text
D_X(beta)=sum_(h,ell) w_(h,ell) psi_X(beta-x_(h,ell)),
hat(psi_X)(n)=X^(-1)hat(psi)(n/X),
S_n=sum_(h,ell)w_(h,ell)e(-n h alpha_ell).
```

`OBSERVED`: this is a genuinely direct construction whose correlation is
supported at beta distance `O(X^-1)`. Cycle 66's phase may later guide
estimates but is beta-free and cannot provide ancestry.

## Cross-fibre invariant and proved scale calculation

Define `D_(X,ell)=sum_h w_(h,ell)psi_X(beta-h alpha_ell)` and

```text
E_cross^psi=int D_X^2-sum_ell int D_(X,ell)^2
           =2 sum_(ell<ell') int D_(X,ell)D_(X,ell') >=0.         (1)
```

The physical-space equality is exact and strictly local; frequency-by-
frequency cross brackets need not be positive. `OBSERVED` post-v3 elementary
calculation: if `psi=1` on `[-2C,2C]`, every Cycle-63 strip hit at `beta0`
equals one throughout the beta arc `|beta-beta0|<=C/X`. Hence, for fibre
masses `t_ell` and `T=sum t_ell`,

```text
E_cross^psi >= (2C/X) (T^2-sum_ell t_ell^2).                      (2)
```

`PROVED` elementary exponent consequence: `t_ell<=H+O(1)` implies that at the
dangerous `T=X^(16/25+o(1))`,
`sum t_ell^2<=HT=X^(27/25+o(1))=o(T^2)` and hence
`E_cross^psi>>X^(7/25+o(1))`. A fixed-share single-ell branch is impossible at
this threshold. This is one-way only; no census bound follows from it yet.

`PROVED` auxiliary Fejer check: the prior normalized-Fejer calculation has
the same forward implication, but its correlation tail is nonlocal. It is not
the graph-inverse localization kernel.

## Decisive obstruction and new inverse targets

`OBSERVED` finite-model obstruction to local positivity/Parseval alone: mass
`N=H Delta=X^(26/25)` arranged into `M=X^(20/25)` beta cells of mass
`B=X^(6/25)` has cross-energy scale `MB^2/R=X^(7/25)` while every cell is
well below `X^(16/25)`. It respects fibre capacity at exponent level but is
not claimed to be realized by the exponential curve. Thus an `L2` estimate
must use geometry or expose a labelled diffuse structure.

The frozen advance condition is exactly one of:

1. `CONJECTURED`: prove a diffuse-energy-versus-beta-localized-web inverse;
   or
2. `CONJECTURED`: construct a legal exponential-curve diffuse saturator,
   with all labels, proving this detector cannot close the census alone.

The smallest falsifier is critical `E_cross`, subcritical every beta cell,
and no localized rational/low-rank web. It refutes only the intended inverse,
not the detector identity.

## Three retained mechanisms for the inverse

1. `CONJECTURED` **shift-eliminating parallelograms.** For four rows in one
   beta cell and `ell1+ell2=ell3+ell4`, exact exponential multiplicativity
   gives a rational quadratic `P(beta)=O(1/(HX))=O(X^(-36/25))`. A theorem
   should turn many such quadratics into a common factor/rational-beta web or
   record a high-complexity obstruction. This is a *single-anchor* engine;
   it does not follow from a graph four-cycle. A diffuse cell can have a
   Sidon label set because `X^(6/25)<Delta^(1/2)`, so no local additive-energy
   claim is available. Clearing four `h` denominators enlarges its error to
   `X^(8/25)`; one relation cannot be rounded to an exact polynomial.
2. `CONJECTURED` **anchor-cell transport graph.** A finite preregistered
   family of shifted/coarsened half-open grids routes each compact-kernel pair
   to one common cell while assigning every row a unique home cell per grid.
   Vertices are beta cells and curve labels; it is initially a multigraph,
   with edge label `(h,j)`. The
   critical diffuse ledger is `E=X^(26/25)`, beta degree `X^(6/25)`, ell
   degree at most `X^(11/25)`. First split heavy multiplicities on one
   `(I,ell)` from a pruned simple/weighted graph. A repeated anchor-fibre is
   only `seed-rich` until packet depth is separately checked. In a simple
   near-biregular graph, beta-side wedges have scale `X^(32/25)` over
   `X^(30/25)` ell pairs, forcing average codegree `X^(2/25)` and C4 scale
   `X^(34/25)`. A C4 between cells `I,I'` and labels `ell,ell'` exports the
   *two-anchor* relations
   `d_ell alpha_ell=delta_(I,I')+a_ell+O(X^-1)` and
   `d_ell' alpha_ell'=delta_(I,I')+a_ell'+O(X^-1)`.
   The compiler must retain this common `delta_(I,I')`, proving a
   common-shift web or banking a labelled high-girth/weighted obstruction.
   The matching `6/25` with Cycle 19/67 is only an analogy; no
   transport-to-prime constructor is claimed.
3. `CONJECTURED` **divisor-fibre dual.** Exact regrouping gives
   `S_n=sum_(m:n|m, m/n~H) sum_ell w_(m/n,ell)e(-m alpha_ell)` with
   `m<=RH=X^(36/25+o(1))`. A two-variable dual estimate must retain the
   divisor fibre, saving `6/25` or producing a labelled divisor-fibre web.
   Generic folded large sieve is already insufficient.

## Weighted-graph lemma to prove next

`EXPLORATORY` corrected dyadic transfer, adopted after the mentor checkpoint.
For one routed grid write `nu_(I,ell)=sum w_r` over rows in the home-cell
pair, `B_I=sum_ell nu_(I,ell)`, and
`Q_I=B_I^2-sum_ell nu_(I,ell)^2`. Compact-kernel energy at
`X^(7/25-o(1))` forces supported weighted cross-pair mass
`Q=sum_I Q_I>=X^(32/25-o(1))`, because the kernel is at most `C_psi/X`.
After dyadic `B_I~X^b`, a retained level has `M X^(2b)>=X^(32/25-o(1))` and
`M X^b<=X^(26/25+o(1))`; hence `b>=6/25-o(1)`. A level
`b>=16/25` is a fixed-enlarged-constant dangerous beta cell after the frozen
finite refinement.

Freeze `U=X^(1/50)` and a cross-pair-energy share `rho>0`. Split all selected
pairs into light-light and heavy-involved terms, where heavy means
`mu_(I,ell)>U`. If heavy-involved terms carry at least `rho Q`, retain a
massed repeated-anchor-fibre cross-pair bank. Otherwise light-light mass is
a fixed share of `Q`. Since every light pair has weight at most `U^2`, its
simple support graph satisfies

```text
Q_light <= 2 U^2 W_support,
W_support=sum_I binom(d_I,2)
          =sum_(ell<ell') codeg(ell,ell')
          >= X^(32/25-2u-o(1)).                    (3)
```

After deterministic target-independent representative selection ordered by
`(h,j,source-row-id)` on every occupied home-cell pair, its four-cycle count
satisfies

```text
C4=sum_(ell<ell')binom(codeg(ell,ell'),2)
 >= (W_support^2/binom(V_curve,2)-W_support)/2
 >= X^(34/25-4u-o(1)).                              (4)
```

Here `V_curve<=Delta=X^(15/25+o(1))`; `u=1/50` makes the C4 scale
`X^(32/25-o(1))`. The same capacity check says an all-light cell has
`B_I<=U Delta`, so `b>31/50` already routes to the heavy branch. Every C4
retains its four `(I,I',ell,h,j)` labels and exports the two relations with
the same ordered anchor difference `delta_(I,I')`. The proof task is to make
the compact-grid routing and the heavy/light energy retention proof-grade;
heavy-light terms must never be dropped.

## New engine: difference-fibre web from the C4 bank

`EXPLORATORY`. A C4 has an oriented cell difference
`delta=(I-I')w` drawn from only `O(X)` grid differences, not from all cell
pairs. Group its two-anchor exports by delta. A relation witness is

```text
d alpha_ell=delta+a+O(X^-1),   |d|<=H.               (5)
```

This defines a labelled bipartite difference-fibre graph between delta values
and curve labels; the cell-pair witness `I`, `d`, and `a` are retained. If one
curve label supports two distinct delta relations, then eliminating
`alpha_ell` gives

```text
d_2 delta_1-d_1 delta_2=integer+O(H/X)=integer+O(X^(-14/25)).    (6)
```

This is a secondary diagnostic, not the primary compiler: compression to the
raw `(delta,ell)` graph can lose the four-anchor moment. It may distinguish
repeated witnesses and sparse obstructions, but does not alone force a web.

## New engine: exact two-label determinant compiler

`EXPLORATORY`, independently checkpointed and now the primary compiler. In the light C4 bank, let two
curve labels share four distinct home cells `I_1,...,I_4`; take `I_1` as base.
For `i=2,3,4`, retain the selected rows and set

```text
d_i=h_(I_i,ell)-h_(I_1,ell),
d'_i=h_(I_i,ell')-h_(I_1,ell'),
k_i=(j_(I_i,ell)-j_(I_1,ell))-(j_(I_i,ell')-j_(I_1,ell')).
```

Circle lifts are absorbed in the integer `k_i`. The common anchored-cell
differences formally give

```text
d_i alpha_ell-d'_i alpha_ell'-k_i=O(X^-1).          (7)
```

Let `c=d cross d'`. Then `c` is integral with size `O(H^2)` and dotting (7)
gives the integer relation `c dot k=O(H^2/X)=O(X^(-3/25))`; for large `X` it
must vanish exactly:

```text
det [ d | -d' | k ]=0.                              (8)
```

`PROVED` combinatorial target: `W_support>=X^(31/25-o(1))` over at most
`Delta^2=X^(30/25)` label pairs forces a `K_(4,2)` bank of scale
`X^(34/25-o(1))` by convexity in the pair codegrees. The compiler's rank
split is explicit: dependent `d,d'` is a labelled rank-one anchor pattern;
independent `d,d'` gives an exact rational-plane relation for `k`. In the
rank-two branch, a nonzero minor `D` gives `|D alpha-N|<<H/X`; after reducing
by `g=gcd(N,D)`, it has packet depth `K=g/H` and `qK=D/H<=H`. Therefore
`g>=X^(17/25-o(1))` yields a genuine seeded `X^(6/25-o(1))` Cycle-67 packet.
The remaining rank-two low-content planes and rank-one resonances are labelled
structural banks, not density results.

## Correction and replacement: preserve the actual beta seed

`PROVED` scope correction: the compact detector's *global* cross-energy is
integrated over beta. Its selected grid/C4 witness can therefore sit at a beta
unrelated to the original Cycle-63 critical census. It cannot provide the
fixed-beta strip seed required by Cycle 67. Retain that graph only as an
unseeded diagnostic; do not promote its high-content Cramer branch to a
transport packet.

`PROVED` elementary anchored count: fix a critical `(beta,C)` census, put
`H_ell={h: |j+beta-h alpha_ell|<=C/X}` with its unique `j` label, and write
`t_ell=|H_ell|`, `T=sum t_ell`. For `T=X^(16/25-o(1))`,
`sum t_ell^2<=HT=o(T^2)`, hence

```text
S=sum_(ell<ell') t_ell t_ell' >> X^(32/25-o(1)).
```

Each of the `P_(ell,ell')=t_ell t_ell'` ordered fibre-product anchors carries
the original beta. Convexity across at most `Delta^2` curve-label pairs gives

```text
sum_(ell<ell') binom(P_(ell,ell'),4)
 >> S^4/Delta^6 >> X^(38/25-o(1)).
```

`CONJECTURED`/proof task: for each four-anchor witness, the determinant
calculation is exact as in (7)--(8), but now its base row is a genuine
Cycle-63 seed. Use both Cramer contents `g=gcd(N,D)` and
`g'=gcd(N',D)`, freeze packet safety constants, and partition labelled
witnesses—retaining multiplicity—into rank one; rank two/high `g`; rank
two/low `g`, high `g'`; and rank two/low both. At least one bank carries a
quarter of the `X^(38/25-o(1))` witness mass. Only either high-content bank
may invoke Cycle 67; rank-one resonances and low-content rational planes are
structural output, not packets.

## Guardrails and mentor record

- Same-ell many-hit families are not Cycle-67 deep packets without the
  separately checked `1/(L_pkt X)` rational approximation and error.
- Fejer is auxiliary only. The compact bump, Fourier-tail norm, shifted grids,
  and weighted graph split are frozen in the canonical preregistration.
- `OBSERVED`: session mentor `guth_maynard_session_mentor` recommended the
  direct detector; adopted after confirming the Cycle-63 source-phase cut.
  It required the diffuse-saturator test and the global physical-space
  positivity formulation. Its later checkpoint replaced Fejer by the compact
  bump for inverse localization. Its second checkpoint adopted the dependency
  stack `detector -> diffuse dyadic cells -> weighted anchor graph ->
  two-anchor compiler`, with the divisor-fibre dual estimating that same
  graph state. It also corrected the multigraph, Sidon, one-anchor-vs-C4,
  denominator-spacing, and signed-frequency seams above.
- `OBSERVED`: at the seal checkpoint it recommended `REFINE, then seal`.
  The adopted refinement normalizes `C_*=max(1,C)`, pins the signed reduced
  numerator, and proves/tests rank-one proportionality; its stated falsifier
  was any exact fixed-beta row violating determinant, reduction, packet, or
  base-seed retention. The focused tests passed.

## Current gate and next action

`SEALED_BETA_ANCHORED_FOUR_ANCHOR_PACKET_OR_RESONANCE_PLANE_CLASSIFICATION`.
The proof artifact freezes the anchored convexity, determinant, signed
two-coordinate Cramer calculation, conservative packet constants, and
exhaustive labelled terminal split. The global compact-grid route remains an
unseeded diagnostic only. `OBSERVED`: no census, density, or interval margin
has been obtained. Next research block: distinguish/bound the actual-curve
rank-one and low-content terminal banks, or carry a retained high-content
seeded packet into the E7/E9 skeleton with a strict margin.
