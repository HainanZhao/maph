# Cycle 2 — Stream C explicit-formula adversarial audit v2

Claim boundary: `PROVED` only for the scope correction. The author/DSpace byte
identity and author-byte licensing questions remain `OBSERVED`. This does not
declare G0 PASS.

`PROVED`: the Cycle-2 preregistration asks for a reachable primary source. It
does not ask for byte identity between an author-hosted primary source and an
institutional mirror, nor proof that the author-hosted bytes inherit an OCW
license. Kedlaya directly hosts the 18.785 formula and proof course notes;
the notes identify their author/course, and frozen official DSpace metadata
independently identifies the same course and author as a non-withdrawn
publication. The explicit-formula mathematical source-authority blocker in
audit v1 is withdrawn.

`PROVED`: the v3 source check pins the PDF bytes, source theorem/proof
anchors, course-specific DSpace CC BY-NC-SA 3.0 metadata, and `mutool`
1.23.10. The theorem/range/half-weight/remainder/multiplicity node therefore
meets the actual preregistered source clause.

`OBSERVED`: byte identity with inaccessible DSpace bitstreams remains
unverified. V3 expressly does not claim that its frozen author-hosted bytes
are OCW-licensed bytes. This is a distribution caveat outside the mathematical
source-authority gate.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/check_cycle_2_stream_c_explicit_formula_sources_v3.py
python3 projects/guth-maynard-zero-density/proof/audit_cycle2_stream_c_explicit_formula_v2_v2.py --check projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-explicit-formula-v2-adversarial-audit-v2.json
```
