# Ray-cocycle data availability audit

Recorded: 2026-07-31 UTC

## Question

After the field-only Dedekind family failed exactly, can the missing
modulus-dependent feature be extracted from code already present in the
program, without opening a new theoretical workstream?

## Files inspected

- `projects/sic-stark/paper/sic-stark-dimensions-four-five.tex`
- `projects/sic-stark/paper/sic-stark-dimensions-seven-eight.tex`
- `projects/sic-stark/src/sic_stark.py`
- the dimension-six, dimension-seven, and dimension-eight tuple-audit
  scripts named by those papers.

## Finding

The existing exact multiplier ledgers are attached to special SIC data:
a quadratic form, its positive stabilizer, a chosen characteristic,
positive lifts, and an AFK/Kopp ray-label bridge. They correctly compute
Dedekind sums, Rademacher invariants, theta-character multipliers, and
finite phase comparisons for those frozen tuples.

The five present census controls supply only a real quadratic field,
one-place modulus, quartic character, and independently constructed weak
Stark solution. The repository contains no generic, convention-preserving
map

\[
  (K,\mathfrak m,\chi)
  \longmapsto
  (Q,A,\boldsymbol r,\text{positive lifts},\text{ray-labelled cocycle})
\]

whose output could be inserted into the existing SIC multiplier code.
The special-purpose tuple scripts therefore cannot be reused as a
generic feature extractor for the five controls.

## Consequence

Obtaining the missing feature is not another empirical fitting cycle. It
requires a theorem-level bridge from oriented ray characters to
geodesic/form data and its cocycle multiplier, together with a proof that
the construction is invariant under the canonical gauge. That is a new
research project.

The current project consequently stops its fitting track. It banks:

1. five independent phase-quantization controls;
2. the gauge-ambiguity lemma and a canonical dominant-embedding repair;
3. an exact no-go for the simplest field-only Dedekind family; and
4. a precise specification of the missing ray-cocycle bridge.

No 50-row holdout is authorized until that bridge and a new feature family
are pre-registered.
