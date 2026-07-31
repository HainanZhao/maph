# Dedekind-sum phase formula project — final report

Completed: 2026-07-31 UTC

## Final status

`FINISHED_WITH_VERIFIED_NO_GO_FOR_FROZEN_MECHANISM`

The project began with a plausible conjecture: a quartic weak Stark
phase defect might be an exact low-complexity
Dedekind--Rademacher congruence. It ends with one positive discovery and
two structural obstructions.

## Positive result

Five independently constructed Roblot weak solutions satisfy
quarter-turn phase quantization within certified \(L'\)-balls. In every
case, after choosing the correct character orientation, a unique
element of \(\mu_4\) carries the certified ball to the independently
computed coefficient. The coefficient embeddings are high-precision
numerical evaluations of exact unit-lattice data, so this observation
retains its `NUMERICAL_PHASE_MATCH_WITH_CERTIFIED_LPRIME_BALLS` tag.

This is real evidence for a phase theorem. It is not explained by the
formula family tested here.

## First obstruction: gauge and missing ray data

The raw quarter-turn label changes under the allowed
\(\mathbf Z[i]^\times\)-orbit of a weak solution. A
dominant-embedding gauge repairs the response variable, but the
simplest field-only Dedekind family then fails exactly on a two-case
collision.

The SIC papers contain richer multiplier data, but only after a form,
ray class, characteristic, lift, and stabilizer are supplied. A ray
character alone does not canonically select one such tuple.

## Second obstruction: parity mismatch

The supplied-tuple multiplier nevertheless descends perfectly on the
dimension-five anchor. That success exposes the decisive failure:

- the descended squared multiplier is invariant under the sign class
  \(R\);
- the differenced Stark packet is supported exactly on characters odd
  under \(R\);
- hence every relevant Fourier coefficient of the multiplier is zero.

Choosing signed square roots would move the multiplier into the odd
subspace. Selecting them from the known Stark answer would be circular;
constructing them intrinsically from the full metaplectic law would be a
new theorem outside this project's frozen mechanism.

## Stop condition

The preregistered character-resolvent gate fails by an exact pairing
argument. Continuing would require a new noncanonical square-root
choice or a new theorem not determined by the archived transformation
laws. The project's stop condition is therefore met.

## Reusable outputs

1. exact Dedekind and SIC-Rademacher arithmetic;
2. an exact supplied-tuple Kopp multiplier evaluator;
3. five independent phase-quantization controls;
4. the dominant-embedding gauge lemma;
5. the exact field-only feature collision;
6. the class-descent/Fourier-cancellation proposition.

## Research recommendation

Do not continue this as an empirical fitting project. The remaining
mathematical question is narrower and harder:

> Can the \(R\)-odd square-root orientation of the AFK/Kopp cocycle be
> constructed intrinsically from metaplectic or spin data?

That is a new project in the metaplectic transformation law, not an
extension of the present Dedekind-sum regression. It should compete
against the program's other priorities rather than inherit momentum
automatically.
