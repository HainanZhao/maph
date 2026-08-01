# Flat-monoid partial-zeta obstruction to ordinary character descent

**Status:** `PROVED` (local model; not an AFK-stratum TCC statement)
**Date:** 2026-08-01 UTC
**Claim boundary:** This proves that there is no *universal* theorem
factoring imprimitive differenced partial zeta functions through ordinary
monoid characters. It uses the elementary local model
\((\mathbb Z/9\mathbb Z,\cdot)\); it does not assert that the AFK D12
packet has this particular local factor or that its derivative at zero is
nonzero on every radical direction.

## Exact countermodel

Let \(M=(\mathbb Z/9\mathbb Z,\cdot)\), the local flat monoid in the
Kopp--Lagarias squared-prime example with \(p=3\). Let \([a]\) denote the
standard basis of \(\mathbb C[M]\). The element
\[
 y=[3]-[0]
\]
is nonzero and square-zero, because \(3^2\equiv0\pmod9\) and zero is
absorbing. Every ordinary monoid character extends linearly to an algebra
map \(\mathbb C[M]\to\mathbb C\), and therefore annihilates \(y\).

For real \(s>1\), define the standard one-place sign-differenced residue
partial zeta functional by
\[
 \mathcal Z_s([a])=
 \sum_{\substack{n\ge1\\ n\equiv a\,(9)}}n^{-s}
 -\sum_{\substack{n\ge1\\ n\equiv-a\,(9)}}n^{-s}.
\]
Then \(\mathcal Z_s([0])=0\), while
\[
 \mathcal Z_s([3])
 =\sum_{k\ge0}\big((9k+3)^{-s}-(9k+6)^{-s}\big)>0.
\]
Hence \(\mathcal Z_s(y)\ne0\). It follows that \(\mathcal Z_s\) is not
a linear combination of ordinary monoid characters, since every such
linear combination vanishes on \(y\).

## Consequence for the proposed Engine-A repair

**PROVED:** A theorem of the form

```text
all flat-monoid differenced zeta packets factor through the ordinary
character Fourier transform of the monoid
```

is false. The failure occurs before analytic continuation or a Stark-unit
identification. Thus an all-order extension of Engine A must include
additional radical/generalized-eigenvector data, or prove a new
AFK-specific cancellation theorem; ordinary quadratic-character support
cannot be its complete input.

This complements—not replaces—the source-level obstruction in
`tcc-sweep-flat-monoid-fourier-obstruction-v1.md`. The latter shows the
radical exists; this note shows the relevant kind of differenced partial
zeta functional can genuinely see it.

Kopp--Lagarias source pin: December-2022 PDF SHA-256
`3fdf11b0a581a6499c653e45c4e5f6c5665f84b942c8d341e29313756537e1d0`,
Appendix A, Example A.9 identifies this residue monoid construction.
