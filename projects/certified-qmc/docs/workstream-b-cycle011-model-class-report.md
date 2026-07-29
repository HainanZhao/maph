# Workstream B Cycle 011 — schema survey and model-class boundary

## Outcome

The frozen Workstream B target is a vector table, not a merit table.
The official UNSW collection specifies exactly two fields—dimension
and generating-vector component—and publishes no merit value.  The
current audit therefore has nothing to subtract from an exact result
and needs no producer-algorithm bound.  Its deliverable is a newly
certified reference merit for each frozen vector and normalization.

That deliverable is banked for the current scope:
`workstream-b-unsw-prefix-reference-table.json` contains independently
replayable exact certificates at every dimension \(1,\ldots,16\).
The artifact explicitly does not claim the unvendored 3,600-component
source is certified.

The inventory also sampled the Magic Point Shop and the vector bundled
with the frozen QMCPy snapshot.  Both sampled artifacts are likewise
vector-only.  They remain candidate targets rather than additions to
the frozen audit set.

No published merit value was acquired or compared in this cycle.

## Corrected classification object

For a future unseen table that does publish a lexical merit \(y\) for a
published vector \(z\), the comparison target is the exact or enclosed
value \(q=e^2(z,N)\).  Producer CBC selection error is irrelevant:
optimality of the producer's search does not alter the merit of the
vector it published.

The prospective classification bound is therefore
\[
 B_{\rm alg}(\mathcal M)
 =T_{\rm eval}(\mathcal M)+T_{\rm format}.
\]
Selection certification remains part of A3/C, not Workstream B.

The v2 gate remains closed for future merit-bearing targets until the
kernel, weights, normalization, observed lexical precision, complete
evaluation envelope, and sensitivity verdict are frozen before the
merit value is read.

## Exact formatting component

`src/format_bound.py` converts a finite decimal lexeme to an exact
rational and derives its lexical grid spacing, including scientific
notation and displayed trailing zeroes.  Under the declared
round-to-nearest formatting model,
\[
 T_{\rm format}=\frac12\,\text{grid spacing}.
\]
An explicit table-wide significant-digit count resolves integer
trailing-zero ambiguity.  The executable preflight uses synthetic
lexemes only and contains no external merit data.

## Reference transform component

`src/radix2_model.py` implements the declared binary64 radix-two
operation graph and a rational forward-error factor.  Under
round-to-nearest, no overflow or harmful underflow, stored-twiddle
error at most \(8u\), and \(L\) radix-two-equivalent levels, the proved
bound is
\[
 \|\widehat{Fx}-Fx\|_\infty
 \le ((1+\eta)^L-1)\|x\|_1.
\]

Arb replay contains the reference transform and stored twiddles for
both forward and normalized-inverse transforms at lengths
\(2,4,\ldots,64\).  The certificate records doubled-twiddle and
doubled-depth sensitivity factors at \(2^{10}\) and \(2^{20}\).

This closes only the transform component.  A complete
\(T_{\rm eval}(\mathcal M)\) must still compose kernel construction,
state updates, convolution products, normalization, and accumulation.
No claim in this cycle promotes that unfinished composition.

## Trusted-base disposition

The pinned FFTW plans, compiled LatNet midpoint replays, and synthetic
fast-CBC transcripts remain useful evidence that the model class is
realistic.  They are tagged `NUMERICAL_MODEL_VALIDATION` and are not
part of the Workstream B proof chain.

The design rule is now explicit: certify the implementation we control,
envelope plausible implementations we do not control, and do not make
an unrecoverable historical binary a proof obligation.

## Artifacts

- `data/workstream-b-table-inventory.json`
- `data/workstream-b-classification-v2.json`
- `certificates/workstream-b-format-bound-preflight.json`
- `certificates/workstream-b-radix2-model.json`
- `certificates/workstream-b-unsw-prefix-reference-table.json`
- `docs/workstream-b-radix2-model-bound.md`

Cycle 009 is independent of this disposition and remains governed by
its Arb-106-first preregistration and exact-CRT escalation gate.
