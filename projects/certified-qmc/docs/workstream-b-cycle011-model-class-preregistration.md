# Workstream B Cycle 011 — model-class amendment

Frozen at: **2026-07-29T06:08:09Z**

## Structural correction

For Workstream B, the audited object is a published pair \((z,y)\):
the published generating vector and its published lexical merit.  The
comparison recomputes the mathematical merit \(q=e^2(z,N)\).

Whether the historical CBC search selected \(z\) optimally is
irrelevant.  Search selection is an A3/C question and is deleted from
the Workstream B error composition.

For every future unseen merit-bearing target,
\[
 B_{\rm alg}(\mathcal M)
 =T_{\rm eval}(\mathcal M)+T_{\rm format}.
\]

Here \(\mathcal M\) is an explicit class of plausible binary64
evaluation pipelines, not a reconstructed historical executable.
Classification outside the bound means outside the certified envelope
for every pipeline in \(\mathcal M\).

## Formatting first

The lexical decimal is interpreted exactly.  Its displayed grid spacing
is obtained from the place value of its final displayed digit, including
any decimal exponent.  Under round-to-nearest formatting,
\(T_{\rm format}\) is exactly half that grid spacing.

The observed lexical representation—not a guessed nominal precision—is
the source of the bound.  Fixed and scientific notation therefore use
one rule, and trailing zeroes remain significant evidence.

## Producer model class

The initial model class freezes:

- binary64 round-to-nearest arithmetic;
- radix-2 or radix-4 backward-stable FFT structure with an explicit
  transform-depth bound;
- a stated absolute/relative twiddle-accuracy assumption;
- stated accumulation-order variants;
- normal finite intermediates, with overflow and harmful underflow
  excluded;
- an independently implemented reference radix-2 transform with a
  Higham-style outward error envelope; and
- sensitivity variants for doubled twiddle error and alternative
  accumulation order.

The historical producing binary is not part of the trusted base and
need not be recoverable.  The banked FFTW/LatNet artifacts are retained
as `NUMERICAL_MODEL_VALIDATION`: they test whether the envelope is
realistic but cannot certify it.

## Scoping result before arithmetic

The current frozen audit set contains one UNSW target.  The collection
states that every file has exactly two columns: dimension and
generating-vector component.  It publishes no merit column.

The Magic Point Shop sample and the frozen QMCPy packaged vector are
also integer-vector-only artifacts.  Therefore:

- frozen merit-bearing tables: **0**;
- frozen vector-only tables: **1**;
- current Workstream B disposition:
  `CERTIFIED_REFERENCE_MERIT_ONLY`; and
- \(B_{\rm alg}\) required for the current frozen set: **no**.

No exact-minus-published merit subtraction occurred during this
metadata survey.

## Admission rule for future targets

A future target enters the discrepancy-classification track only if it
publishes a merit column.  Before subtraction, its lexical precision,
\(T_{\rm format}\), normalization, \(\mathcal M\),
\(T_{\rm eval}(\mathcal M)\), and sensitivity variants are timestamped.
The frozen three-way rule remains:

- \(|y-q|>B_{\rm alg}(\mathcal M)\): discrepancy under \(\mathcal M\);
- \(|y-q|\le B_{\rm alg}(\mathcal M)\): expected rounding under
  \(\mathcal M\);
- missing assumptions: `UNCLASSIFIED_EXTERNAL`.

Artifacts:

- `data/workstream-b-table-inventory.json`
- `data/workstream-b-classification-v2.json`
