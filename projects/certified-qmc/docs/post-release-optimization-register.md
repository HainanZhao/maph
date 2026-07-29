# Post-release optimization register

Status: closed until release v1.0 has a published DOI

The production release uses the frozen plain-`__int128` kernel,
compiler, flags, and scalar layout.  The following work opens only after
the DOI-backed release is published:

1. Montgomery multiplication and lazy reduction.  Promotion requires
   bit-identical residues, reconstructed values, and final outputs
   against a banked plain-reduction transcript.
2. SIMD/vectorized inner loops.  Promotion requires the same
   bit-identical replay and a new dependency/build manifest.
3. Double-double decision shadow.  This is considered only if the
   Arb-106 profile shows a material bottleneck.  It must use published
   rigorous double-word constants and pass a dual-shadow replay with a
   bit-identical complete branch trace—not merely an identical final
   vector.

No item changes a v1.0 certificate or retroactively replaces its
kernel.  Optimized results require a separately versioned transcript.
