# Cycle-2 source manifest v3 correction

Claim boundary: `OBSERVED` byte inventory and stated access metadata only. This
does not establish mathematical source authority or G0 PASS. V1 and V2 are
preserved.

`PROVED`: V2 is stale as a current direct-source inventory: it predates four
now-frozen files—the DSpace item metadata, official SWORD archive, and two
official extracted PDFs. V3 inventories all 36 current direct files and the
five declared canonical extracted inputs. Every row has a byte count and
SHA-256; aliases remain as explicit groups.

`PROVED`: the legacy V2 regression now tests this exact four-file delta and
requires V2's current-inventory checker to fail closed. It no longer asks the
historical V2 artifact to equal the post-V2 inventory; V2's script and artifact
remain unchanged.

`PROVED`: V2’s CC BY-NC-SA 4.0 statement for the separately hosted Kedlaya
author copies was wrong in scope. V3 records those copies solely as direct
author-primary access and makes no inherited-CC assertion. The DSpace metadata,
official SWORD archive, and official extracted PDF rows instead record the
course item’s CC BY-NC-SA 3.0 rights. This is a provenance correction, not a
claim about the mathematical authority of any source.

`OBSERVED`: no proof-script consumer list is included. The frozen G0 consumer
scope is `OMITTED_BY_DESIGN`; consequently, adding or editing a proof script
does not alter this source-byte manifest. A change to the immediate
`artifacts/sources` inventory, or to one of the five extracted canonical
inputs, intentionally causes the checker to fail until a versioned correction
is issued.

`OBSERVED`: the restricted Iwaniec AMS PDF remains absent by policy. No PDF,
OCR, page image, text extraction, or copied excerpt is included.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/build_source_manifest_v3.py --check
```
