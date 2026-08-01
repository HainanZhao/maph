# Cycle-2 source manifest v2

**Claim boundary — OBSERVED.** This artifact is a deterministic inventory of
the bytes presently frozen under `artifacts/sources/` and of selected extracted
TeX/README inputs. It does not certify any mathematical assertion, source
authority, completeness of an upstream record, or licence beyond the stated
access metadata.

Run:

```sh
python3 proof/build_source_manifest_v2.py --check
```

The manifest lists every regular file immediately under `artifacts/sources/`,
including local rendered-text derivatives, and these canonical extracted inputs:

- Guth--Maynard `LargevaluesDirichlet17.tex` and extraction README;
- Chourasiya--Simonic `InghamPostArXiv.tex` and extraction README; and
- Maynard--Pratt `HalfIsolatedv2.tex`.

Each row records relative path, byte count, SHA-256, role, provenance/access
metadata where available, and proof-script textual consumers. Duplicate byte
objects remain in place and are reported as explicit alias groups.

Kedlaya's two notes record the MIT OCW DSpace provenance handle and the
CC BY-NC-SA 4.0 licence URL. The restricted Iwaniec AMS PDF is intentionally
absent: the manifest records the policy absence only, with no copied PDF, OCR,
page image, or extracted text.

Version 1 (`proof/verify_source_manifest.py`) remains the independent,
narrow Cycle-1 three-object verifier and is not superseded for that purpose.
