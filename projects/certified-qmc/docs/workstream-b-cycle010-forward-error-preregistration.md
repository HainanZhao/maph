# Workstream B Cycle 010 — producer-error bound

Preregistered at: **2026-07-29T04:38:59Z**

## Protocol incident and quarantine

While tracing the producer path, the repository example field
`# Merit:` in `examples/examples-IO/test_lat/output.txt` was exposed
before \(B_{\rm alg}\) was frozen. No subtraction from an exact or
enclosed target was performed.

This is a gate violation. The file is quarantined as
`EXPLORATORY_PROTOCOL_CONTAMINATED` and cannot support the first
confirmatory Workstream B finding. Its frozen SHA-256 is
`c677aa656e82578401c5327ba31a91ec5fdf0cc3a4ae0af6d202fc1d09ea0f11`.
A new, unseen external target must be preregistered after the bound
passes.

## Version-pinned producer model

The forward-error analysis targets LatNet Builder commit
`39dd60fceb0c86a6124b701072d91f8e3aed73df`, ordinary rank-1 lattices,
product weights, `CU:P2`, norm type 2, symmetric base-2 storage, and
`fast-CBC`.

The source path fixes:

- binary64 `Real`;
- \(P_2(x)=2\pi^2B_2(x)\);
- pointwise product-state updates;
- FFTW real FFT, Fourier-space complex multiplication, normalized
  inverse FFT, and lower-level accumulation;
- ordinary floating-point minimum selection; and
- default C++ stream formatting at six significant digits unless
  `--merit-digits-displayed` is explicitly supplied.

The analysis is version-pinned to a specific FFTW build and plan.
Historical example output lacking its FFTW/compiler/libstdc++ producer
metadata remains `UNCLASSIFIED_EXTERNAL`, even if the source commit is
known.

## Required bound

\(B_{\rm alg}\) is the sum of outward bounds for:

1. binary64 input and \(P_2\) kernel construction;
2. product-state updates;
3. each FFT and inverse FFT;
4. Fourier-space complex multiplication and compression scaling;
5. lower-level accumulation and candidate comparison;
6. final merit accumulation; and
7. decimal formatting.

The FFT component uses a Higham-style \(\gamma_k=ku/(1-ku)\) bound,
with operation counts obtained from the frozen FFTW plan rather than an
unrecorded asymptotic constant. Every assumption and plan count is
stored in the certificate.

## Gate

No external merit value is read or compared during this cycle. Cycle
010 passes only when:

- the producer binary, compiler, FFTW, libstdc++, rounding mode, plan
  flags, and operation counts are frozen;
- the compositional bound is executable with outward rounding;
- adversarial small transforms are contained by the bound; and
- an independently computed Arb transform enclosure is contained.

Only then may a new unseen external target be selected and fetched.
