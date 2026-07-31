# Results companion v1.4 Track-A2 successor layer

## Claim boundary

This deterministic successor does not rewrite either the published
v1.3 archive or the locally frozen v1.4 correction layer. It nests the
v1.4 layer byte-for-byte and adds the corrected top-level manuscript,
its deterministic PDF, and an exact editorial audit.

Relative to the immutable published v1.3 source, the manuscript changes
exactly one line: the Tangedal--Young bibliography range is corrected
from the erroneous 1022--1045 to the publisher's 1045--1061. No
mathematical display, theorem, case row, polynomial, exponent, margin,
or Artin label changes.

The same audit confirms that the requested historical-scope
back-reference, companion-paper anchor citations, and the
Tate IV.5.4 / Arakawa / Roblot scope paragraph are present.

## Replay

From the extracted archive root:

```bash
python3 projects/effective-stark-sweep/scripts/verify_results_companion_v15.py .
```
