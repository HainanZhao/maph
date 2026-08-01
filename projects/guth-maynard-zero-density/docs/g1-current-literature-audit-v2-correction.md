# G1/P2 current literature audit v2 correction

## Claim boundary

`OBSERVED`: This is a byte-level presentation correction to the sealed
[v1 literature-audit report](g1-current-literature-audit-v1.md). No
mathematical, provenance, overlap, route-selection, or novelty claim changes.
The v1 report and its JSON artifact remain preserved, byte-pinned authorities.

## Correction record

The v1 Markdown report contains exactly one embedded `0x0d` carriage-return
byte at zero-based byte offset 1421, in the **Cubic and higher tensors** table
row. It replaces the intended two-byte `\r` sequence of the tensor identifier
and can cause a renderer to display an apparent line break before `m Dir`.

Corrected rendering: `S_{M_{\rm Dir},3}`.

`OBSERVED`: The immediate byte-level substitution is certified by the v2
replay. The upstream authoring mechanism is not determined. The v1 JSON anchor
already records `S_{M_Dir,3}`, and the pinned Guth source TeX is unchanged;
therefore the defect affects presentation only. No mathematical, provenance,
overlap, route-selection, or novelty claim changes.

## Preservation and scope

- v1 report SHA-256: `3fe0fc50a9ea2ff56c1f5b9ec3422a1675a34b4ab6641453bd9aff1058407a2c`.
- v1 JSON SHA-256: `49da2e838ce60699ba870e0c532aab5ec8ba564c560811d9683ac92f0afbe6be`.
- The correction adds no source audit, theorem, novelty determination, G1
  route selection, or P2 authorization.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/audit_g1_current_literature_v2_correction.py --check
python3 -m unittest tests/test_g1_current_literature_audit_v2_correction.py -v
```
