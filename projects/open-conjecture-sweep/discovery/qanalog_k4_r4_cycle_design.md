# Topic 2 proof-engine selection

Decision question: can the four-section dominance lemma in
`qanalog_k4_r4_reduction.md` be proved uniformly, thereby resolving the
`k=r=4` sufficient-condition case of Connelly--Ito--Martinez--Shevchenko--Yang
Conjecture 5.4?

## Question the question

The inherited induction asks for a comparison of two residue-mismatched
sampled windows in a three-interval coefficient sequence. Ordinary symmetry
and unimodality do not by themselves compare such windows, so treating the
missing step as a routine tail-monotonicity lemma risks proving a false
generalization. The actual structure to exploit is that the sequence is a
three-fold interval convolution and that the modulus is exactly four.

Questioning that critique: an explicit modulus-four decomposition may create
81 residue cases and obscure a simple injection. Conversely, insisting on a
case-free injection may hide the small periodic correction that is the only
obstruction. The first discriminator should therefore test structural claims
about the four residue sections, not merely extend the existing parameter
census.

## Exclusion map and candidates

- Former question: direct bounded verification of the full product and the
  stronger four-section lemma. Outcome: `OBSERVED` through `a_i <= 64`, with
  zero margins. Delta here: seek a symbolic invariant for every parameter,
  rather than another finite census.
- Former question: induction under `a -> a+4`. Outcome: `PROVED` reduction to
  the sampled-window inequality (5)/(6), but no comparison across residues.
  Delta here: resolve the residue mismatch using the exact interval-convolution
  structure.

Serious mechanisms:

1. **Residue-section decomposition.** Expand
   `[4c+s]_q=[s]_q+q^s[4]_q[c]_{q^4}` and express `A/[4]_q` as a finite
   residue correction plus nonnegative convolutions on the `q^4` lattice.
   Falsifier: a section summand whose required centerward dominance fails for
   an unbounded parameter family.
2. **Box-spline difference formula.** Apply inclusion--exclusion to the
   three-interval coefficients in (5), sum the resulting quadratic positive
   parts on arithmetic progressions, and prove the piecewise expression.
   Falsifier: a chamber whose polynomial has negative values inside the
   admissible cone.
3. **Weight-preserving injection.** Inject triples counted on the shifted
   sampled window into triples counted on the closer window. Falsifier: exact
   small rows where every coordinatewise reflection changes the residue in
   the wrong direction, requiring nonlocal cancellation.

Selected engine: residue-section decomposition first, with the box-spline
formula as the main rejected alternative. It exposes the exact periodic
correction and admits a small direct verifier before symbolic promotion.

- Input state: four lengths `a_i=4c_i+s_i`, `s_i in {1,2,3}`, and the formal
  quotient `Q=product_i[a_i]_q/[4]_q`.
- Proposed invariant: each modulus-four section has the centerward dominance
  and prefix positivity required by the two clauses of the lemma, after the
  finite residual correction is isolated.
- Smallest direct verifier: enumerate all 81 ordered residue patterns and
  small `c_i`, reporting the first failed section/difference and the exact
  decomposition terms.
- Resource stop: at most two minutes and 1 GiB for the discriminator; a failed
  invariant returns immediately to the box-spline engine rather than raising
  the parameter limit.
- Advance condition: a symbolic section formula with inequalities reducible
  to nonnegative interval-convolution coefficients, or a proved finite chamber
  list.
- Falsifier: any negative required section difference under the stated
  diagonal bound, or any mismatch between the decomposition and direct exact
  multiplication.
