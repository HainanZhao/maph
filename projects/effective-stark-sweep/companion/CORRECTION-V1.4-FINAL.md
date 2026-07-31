# Results companion v1.4 DOI-bearing release layer

## Release identity

- reserved DOI: `10.5281/zenodo.21712478`;
- predecessor DOI: `10.5281/zenodo.21708121` (v1.3);
- state while this layer was built: Zenodo draft, unsubmitted.

This deterministic layer nests the complete pre-DOI companion v16
byte-for-byte. It adds the DOI-bearing main paper, supplement, and
RQ-000013 addendum; the final Zenodo metadata; the sanitized DOI
reservation record; and versioned Engine-C, full-referee, and exact
release-delta audits.

## Claim boundary

`PROVED`: the Engine-C packet polynomials, magnitude certificates,
sigma-positive Artin convention, and theorem tags are unchanged.

`CONTAINED_CORRECTION`: the fully oriented five-control numerical
replay remains withdrawn because direct/inverse character orientation
was selected after opening the analytic target. The retained numerical
statement is the two-orientation match only.

`PROVED`: in the five independently certified quartic Stark cases,
Roblot uniqueness gives
\(L'(0,\chi)/c_\chi(\eta)=\chi(h)^{-1}\in\mu_4\).

`PROVED`: RQ-000013 realizes the nonzero imprimitive branch
\(E_\chi=I_\chi=2\) with
\(X_{[0]}=u^2,\ X_{[1]}=u^{-2}\).

The exact release-delta audit proves that, relative to published v1.3,
the main source changes only the Tangedal--Young page range and archive
DOI; the old supplement changes only its archive DOI; and the new
addendum supplies the RQ-000013 row.

## Replay

From the extracted archive root:

```bash
python3 projects/effective-stark-sweep/scripts/verify_results_companion_v17.py .
```
