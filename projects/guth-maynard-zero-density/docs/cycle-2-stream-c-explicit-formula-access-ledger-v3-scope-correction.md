# Cycle 2 — Stream C explicit-formula access ledger v3 scope correction

Claim boundary: `PROVED` for the preregistered mathematical source-authority
requirement. `OBSERVED` remains the separate distribution caveat. V1 and v2
are preserved.

`PROVED`: the preregistration requires one reachable primary source, not
evidence that an author-hosted byte is identical to an OCW or DSpace byte.
The frozen PDFs are directly hosted by K. S. Kedlaya's own 18.785 course site
and identify the author/course in their text. Independent official DSpace API
metadata names the same course, handle, and author, labels it a non-withdrawn
publication, and records course-specific CC BY-NC-SA 3.0 rights. This closes
the mathematical source-authority requirement.

`PROVED`: Theorem 1 supplies the all-\(T\), half-weighted formula and the
proof unit supplies multiplicity. The source checker now pins `mutool`
version 1.23.10 as well as all source bytes and source anchors.

`OBSERVED`: direct DSpace bitstreams remained inaccessible, and no byte
identity with the author-hosted copies was established. V3 therefore withdraws
v2's stronger claim that the frozen author bytes are OCW-licensed. This is a
distribution/provenance caveat, not a blocker under the actual Cycle-2
reachable-primary-source clause.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/check_cycle_2_stream_c_explicit_formula_sources_v3.py
```
