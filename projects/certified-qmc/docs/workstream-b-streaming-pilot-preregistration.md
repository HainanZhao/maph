# Workstream B streaming pilot preregistration

Frozen: 2026-07-29T06:47:00Z, before timing.

## Measured object

The pilot is the compiled plain-remainder `__int128` evaluator at
\(N=1024,d=256,\gamma_j=j^{-2}\), using the frozen `29102` vector
prefix.  It is prime-major and incremental within each column:

1. initialize \(p(k)=1\) once for a prime;
2. visit dimensions in order;
3. update every \(p(k)\) once at the next dimension;
4. emit the prefix residue;
5. never recompute an earlier prefix from dimension one.

The full-grid count of 54,901,459,582,976 is confirmed to use this
running-product reuse.  It is a lower bound on modular updates, not a
per-cell-from-scratch estimate.

The pilot uses 151 work primes and two universal overflow-check primes.
After one warmup it records five runs and uses the median aggregate wall
nanoseconds per work-prime update.  Montgomery reduction is disabled;
this measures the banked correctness representation.

## Frozen production threshold

The exact full fidelity grid is authorized if and only if:

- all selected residues match the independent Python modular oracle;
- the checkpoint write/read digest replays exactly;
- both overflow primes are evaluated for every emitted prefix;
- projected work is at most **7 node-days**; and
- replay overhead is at most **15%** of work-prime time.

The projection is
\[
 \frac{
 t_{\rm update}\;54{,}901{,}459{,}582{,}976
 }{10^9\cdot86400}
 \quad\text{node-days}.
\]
Thus the maximum passing measured throughput is
**11.016100566250485 ns/update**.

Replay overhead is
\[
 \frac{T_{\rm two\ overflow\ primes}
       +T_{\rm checkpoint\ write/read/verify}}
      {T_{\rm work\ primes}}.
\]

These thresholds are frozen before the measurement.

## Mechanical no-go fallback

If correctness and replay pass but the projection exceeds seven
node-days, the data product becomes two-tier:

- dimensions \(d\le d_{\rm cut}\): `VERIFIED` exact values;
- dimensions \(d>d_{\rm cut}\): `ENCLOSED` Arb balls.

The cutoff is not chosen by looking at merits or production discomfort.
It is the largest global \(d_{\rm cut}\in[16,3600]\) for which the
measured throughput projects the complete two-family fidelity workload
through that dimension, plus the frozen usability workload, under seven
node-days.

Arb begins at 160 bits and doubles precision until
\[
 \operatorname{rad}(x)
 \le 2^{-100}\max(1,|\operatorname{mid}(x)|).
\]

If correctness fails or replay overhead exceeds 15%, neither full exact
nor two-tier production is authorized; the streaming implementation
must be redesigned and preregistered again.

## Artifact geometry

The worst entry has 3,738 work residues, or 29,904 bytes before
metadata and overflow residues.  Charging that worst count to all
79,200 fidelity entries gives a conservative 2.368 GB decimal residue
upper bound.  The consumer-facing release is therefore expected to be
roughly 2–3 GB before compression, with chunk-selective downloads and
verification.

The two overflow primes are universal, never sampled.

## Versioned redesign after the first run

The first execution correctly returned `REDESIGN_REQUIRED`: all
checkpoint and overflow checks passed, but none of the 25 selected
residues matched the Python oracle.  The failed transcript is preserved
as `certificates/workstream-b-streaming-pilot-failed-v1.json`.

Inspection isolated one deterministic error.  The native evaluator
multiplied the subtracted constant by
\(F_j(0)=6j^2N^2+N^2\), whereas the scaled numerator requires the common
denominator factor \(C_j=6j^2N^2\).  A v2 preregistration was frozen at
2026-07-29T06:55:14Z before measuring the corrected implementation.  It
permits only that replacement and changes no threshold, workload,
statistic, or correctness check.

## Paper perimeter

The paper retains this sentence:

> Across the frozen distribution sites and the named, hash-frozen
> six-paper primary-literature perimeter, we found no numerical merit
> attached to the frozen vectors; this is not a universal claim about
> the QMC literature.
