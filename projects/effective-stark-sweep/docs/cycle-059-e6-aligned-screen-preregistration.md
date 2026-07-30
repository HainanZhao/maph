# Cycle 059 — aligned-candidate \(e=6\) screen preregistration

**Frozen at:** `2026-07-30T05:45:42Z`  
**State:** frozen before any new route computation on the one unresolved
packet-field model.

## Scope

The ten `ALIGNED_NOT_DUAL_PROVED` candidates are fixed by
`artifacts/remaining-dual-alignments-v1.json`, SHA-256
`871667c5e2a6ec033afa85ea523c7abce40d3de5f0dbcb1000a87f83b2843318`.
Six candidates' exact packet polynomials already occur in the
pre-existing Engine-C \(e\)-inventory; their banked values are reused
without recomputation:

- RQ-004130, RQ-004147, RQ-004161, RQ-004178: `(4,4)`;
- RQ-004842: `(4,8)`;
- RQ-006800: `(4,8)`.

The remaining four occurrences, RQ-007674, RQ-007682, RQ-007721, and
RQ-007752, share the single unresolved exact packet polynomial

```text
x^8 - 4*x^7 - 32*x^6 - 4*x^5 + 298*x^4 + 584*x^3
    - 672*x^2 - 2736*x - 1674.
```

Its two already identified CM bases are `x^2-x+5` and `x^2+10`.

## Frozen route order and decision

Canonical route order is increasing
`(abs(poldisc(polredbest(k))), textual polredbest(k))`.  Thus the
primary route is `x^2-x+5` and the second route is `x^2+10`.  The exact
roots-of-unity count \(e=|\mu(E)|\) is obtained from a certified
`bnfinit(...,1)` character field with `bnfcertify=1`; no numerical
estimate participates.

Both \(e\)-values may be computed under this preregistration.  This is
only an inventory computation, not a second W3 proof.  If either value
is six, choose the cheapest such occurrence by the already-frozen
ordering in `remaining-dual-alignments-v1.json`, then:

1. freeze a separate second-route W3 selection/orientation artifact;
2. execute the complete route without reading any first-route W3
   intermediate;
3. seal its transcript and certificate hash before comparing its
   predicted Artin-labeled packet with the already banked alignment
   target;
4. mismatch is `HALT`, never reconciliation;
5. equality plus the complete first-route W3 bundle is required for
   `DUAL_PROVED`.

If neither route has \(e=6\), report that no validation candidate
exists among the ten and skip Task 8.  Exact alignment alone remains
insufficient for promotion.

## Frozen inputs

- `engine-c-e-inventory-v1.json`:
  `a53be7591753b11fecdad2d96dca4479b99bbfaf732982fc1cf17dcf0ac5ef9b`
- `engine-c-geometry-full-v1.transcript`:
  `0ab3c647d9de69d2cc347a6846298eca30ea3f46adc60270de4f6b67d6f66278`
- `screen_engine_c_e_values.gp`:
  `d8e037ac3f34aadb6155742b82a99132658fac47f314189f679cdf256c9af9f4`

