# Cycle 165 working decision summary v1

`EXPLORATORY`; not a sealed claim or a density/interval result. This compact
ledger records one substantive block. Frozen formulas and the next proof
attempt are in `docs/cycle-165-direct-detector-preregistration-v2.md`; do not
append derivational scratch here.

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

## Primary new engine: direct beta detector

`EXPLORATORY`; the source state is `(h,ell,w)` with `0<=w<=1`,
`H<=h<=2H`, `alpha_ell=exp(2pi ell/Delta)-1`, and
`x_(h,ell)=h alpha_ell (mod 1)`. `beta` is a single external circular anchor;
an integer `j` is recovered only when a source point is in its Cycle-63 strip.
Set `R=cX`, with `c` frozen small relative to the strip constant, and
`phi_R=F_R/R`. Then

```text
D_R(beta)=sum_(h,ell) w_(h,ell) phi_R(beta-x_(h,ell)),
D_R(beta)=R^(-1) sum_(|n|<R)(1-|n|/R)e(n beta) S_n,
S_n=sum_(h,ell)w_(h,ell)e(-n h alpha_ell).
```

`OBSERVED`: this is a genuinely direct construction. Cycle 66's phase may
later guide estimates but is beta-free and cannot provide ancestry.

## Cross-fibre invariant and proved scale calculation

Define `D_(R,ell)=sum_h w_(h,ell)phi_R(beta-h alpha_ell)` and

```text
E_cross=int D_R^2-sum_ell int D_(R,ell)^2
       =2 sum_(ell<ell') int D_(R,ell)D_(R,ell') >=0.             (1)
```

The physical-space equality is exact; frequency-by-frequency cross brackets
need not be positive. Freeze `R=floor(X/(8C))`. Since
`phi_R(t)=R^(-2)(sin(pi R t)/sin(pi t))^2`, it is at least `4/pi^2` for
`|t|<=2C/X`. If a Cycle-63 strip at `beta0` contains fibre masses `t_ell`
and `T=sum t_ell`, then

```text
E_cross >= (32C/(pi^4 X)) (T^2-sum_ell t_ell^2).                  (2)
```

`PROVED` elementary exponent consequence: `t_ell<=H+O(1)`, so at the
dangerous `T=X^(16/25+o(1))`,
`sum t_ell^2<=HT=X^(27/25+o(1))=o(T^2)` and hence
`E_cross>>X^(7/25+o(1))`. A fixed-share single-ell branch is impossible at
this threshold. This is one-way only; no census bound follows from it yet.

## Decisive obstruction and new inverse targets

`OBSERVED` finite-model obstruction to positivity/Parseval alone: mass
`N=H Delta=X^(26/25)` arranged into `M=X^(20/25)` beta cells of mass
`B=X^(6/25)` has cross-energy scale `MB^2/R=X^(7/25)` while every cell is
well below `X^(16/25)`. It respects fibre capacity at exponent level but is
not claimed to be realized by the exponential curve. Thus an `L2` estimate
must use geometry or expose a labelled diffuse structure.

The frozen v2 advance condition is exactly one of:

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
2. `CONJECTURED` **anchor-cell transport graph.** Vertices are beta cells and
   curve labels; it is initially a multigraph, with edge label `(h,j)`. The
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

`CONJECTURED` exact combinatorial target. Let `mu_(I,ell)` be the number of
labelled `(h,j)` edges on an anchor-cell/curve-label pair, and fix a
preregistered multiplicity cutoff `U=X^u`. Either some pair has `mu>U`
(a labelled seed-rich repeated anchor-fibre, not a packet conclusion), or
the simple support graph has at least `e>=E/U` edges. After a deterministic
label-blind representative choice on every occupied pair, set
`V_beta=#I` and `V_curve=#ell`. Its wedge count and four-cycle count satisfy

```text
W >= (e^2/V_beta-e)/2,
C4 >= (W^2/binom(V_curve,2)-W)/2.                   (3)
```

At the diffuse exponents `E=X^(26/25)`, `V_beta=X^(20/25)`,
`V_curve=X^(15/25)`, and `u=o(1)`, (3) predicts
`W=X^(32/25-o(1))` and `C4=X^(34/25-o(1))`. Every
selected C4 retains its four original `(h,j)` labels and exports the two
relations with the same ordered anchor difference `delta_(I,I')`. The proof
task is to pin the dyadic level/weight transfer that supplies `E,B,L`; the
displayed graph inequalities themselves are elementary. A weighted model
that puts the requisite cross energy entirely in the `mu>U` arm is the
first explicit alternative, to be preserved rather than folded into C4.

## Guardrails and mentor record

- Same-ell many-hit families are not Cycle-67 deep packets without the
  separately checked `1/(L_pkt X)` rational approximation and error.
- All detector ideas before v2 are `EXPLORATORY`; only v2 constants/formulas
  are preregistered for the next proof attempt.
- `OBSERVED`: session mentor `guth_maynard_session_mentor` recommended the
  direct detector; adopted after confirming the Cycle-63 source-phase cut.
  It required the diffuse-saturator test and the global physical-space
  positivity formulation. Its second checkpoint adopted the dependency
  stack `detector -> diffuse dyadic cells -> weighted anchor graph ->
  two-anchor compiler`, with the divisor-fibre dual estimating that same
  graph state. It also corrected the multigraph, Sidon, one-anchor-vs-C4,
  denominator-spacing, and signed-frequency seams above.

## Current gate and next action

`BETA_ANCHORED_CROSS_FIBRE_DETECTOR_DIFFUSE_WEB_OR_OBSTRUCTION_OPEN`.
Next: complete a proof-grade version of (1)--(2), then prove the weighted
multigraph pruning and forced-C4/codegree ledger with retained
`(I,I',ell,h,j)` labels. Only then test its two-anchor compiler against a
legal diffuse model. Do not seal, rebuild status, update `PLAN.md`, or claim
a transport/density gain until that bound-or-obstruction decision is resolved.
