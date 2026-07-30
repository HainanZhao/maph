# Cycle 067 — Engine-D anchor gate and census containment

**Date:** 2026-07-30  
**Outcome:** proposed Engine D rejected; 64 B rows quarantined  
**Promotions:** one uniform no-go theorem, three negative anchors  
**Retractions:** no banked W3 theorem; two census interpretations

## Gate outcome

The requested census split
\[
 \texttt{FRONTIER}:1818\to1542,\qquad
 \text{substantive}:2483\to2759
\]
was not applied. Before bulk or analytic work, the first anchor
RQ-000018 produced exact signature \((8,4)\). This is incompatible
with an abelian extension of \(\mathbb Q\), which must be Galois and
therefore totally real or totally imaginary.

The cause is exact. The W1 index computation treated conjugation as an
endomorphism of one ray group without first checking
\(\bar{\mathfrak f}=\mathfrak f\). For a split prime ideal it instead
maps to a different ray problem. The recorded quotient is then not
\([H:H\cap\mathbb Q^{\rm ab}]\).

## Corrected Engine-D census

The former 3,521-row proxy has:

| component | occurrences |
|---|---:|
| empty support | 2,552 |
| substantive Engine A | 693 |
| proposed new D, unstable modulus | 276 |

There are 1,042 conjugation-stable rows in the proxy, but none is a
new substantive case. Thus corrected Engine-D yield is zero.

The uniform theorem explains the empty result. An absolute Dirichlet
character restricts to parity \((0,0)\) or \((1,1)\) at the two real
places of a quadratic field. The one-place difference is supported on
\((0,1)\) or \((1,0)\). The proposed “odd-on-\(R\) characters become
Dirichlet characters” mechanism is therefore impossible.

## Three anchor bundles

All proposed anchors fail the missing predicate:

| case | field | norm | ray degree | signature |
|---|---|---:|---:|---:|
| RQ-000018 | \(\mathbb Q(\sqrt2)\) | 41 | 16 | \((8,4)\) |
| RQ-000032 | \(\mathbb Q(\sqrt2)\) | 79 | 12 | \((6,3)\) |
| RQ-000274 | \(\mathbb Q(\sqrt{10})\) | 36 | 8 | \((4,2)\) |

Each bundle contains the exact conjugate ideal, relative and absolute
ray polynomials, discriminant, signature, and transcript hash. No
Arb/Sturm work was started after the algebraic predicate failed.

## Containment beyond Engine D

The same missing predicate affects the B battery's use of the phrase
“normal closure.” Of 195 nominal B rows:

- 131 have conjugation-stable finite modulus and remain eligible;
- 64 have unstable modulus and are quarantined;
- RQ-000458, RQ-000129, and RQ-002057 are stable, so the banked
  headline results are not exposed.

Engine A is relative and unaffected. The complete Engine-C gate builds
the actual packet splitting closure and checks its normal group and CM
bases directly; its 728 eligible rows are unaffected.

The next B repair is mathematically prescribed: form the compositum of
the ray field for \(\mathfrak f\) and the conjugate ray field for
\bar{\mathfrak f}\), then recompute the maximal absolutely abelian
subfield and index in that actual normal closure.

## Odd-index correction

All 88 rows behind the former odd-index correlation have unstable
finite moduli. Therefore

- 85/88 proxy-index = proxy-commutator, and
- 86/88 proxy-index shares an odd prime with support

remain byte-replayable coordinate statistics but are retracted as
field-theoretic laws. The three \(3\)-versus-\(6\) records and two
support-prime records are stored individually under
`artifacts/frontier-odd-index-exceptions/`.

## Artifact hashes

- stability audit:
  `494de62e78896c8aac93b172b5341c38be2a2d10721b1ec108c64f6412499f4a`
- negative anchors:
  `e62fdddcb4450a74c3314e08d5485fe74133370519efdbef4a10615347c1d56b`
- full containment audit:
  `98735d7d772e68203b157dbdd2ff003e26363cb3a4a9b184aa1e78968d33b113`
- odd-index correction:
  `9f9753eaa6b8a114fb5caf993504ba709264a6572d24a0e7e645b963acd5584b`
- theorem file:
  `61ee1a960cf68f0c7c42af8ef2896e1cf9c3a67c71dfce92c00e7cae8fe2a929`

The failed proposed split remains preserved in
`artifacts/census-split-v3-engine-d-proposal-rejected-v1.json`.

