# Cycle 079 — results v1.4 correction staging

Recorded: 31 July 2026 UTC.

## Outcome

`CONTAINED_CORRECTION`: the completion audit rejected the initial
assessment that Track A1 was already complete.  Public Zenodo v1.3
contains the exact Engine-C Fourier correction to the
\(\sigma^{+r}\) convention, but it predates the phase project's
`CONTAINED_ORIENTATION_CIRCULARITY` record.  It therefore cannot
contain the required withdrawal of the fully oriented five-control
replay.

No proved Engine-C packet, packet polynomial, magnitude validation, or
gauge-independent two-orientation numerical statement is withdrawn.
The affected claim is only that the archived choice between
\(\chi\) and \(\chi^{-1}\) was data-independent.

## Local successor

A deterministic v1.4 correction layer was built at
`dist/effective-stark-results-companion-v14.tar.gz`, SHA-256
`6225d7660b2b6455480fd73e412b3937438d4dbb9f2f1c68cb4d7e3ac1052648`.
It contains the immutable v1.3 companion byte-for-byte and adds:

- the Engine-C Fourier/\(\sigma^{+r}\) correction;
- the circularity and withdrawn-replay correction;
- the five-case Roblot hypothesis screen and certified-case
  \(\mu_4\) clarification lemma;
- the exact RQ-000013 \(E_\chi=2\) certificate and addendum.

Two builds were byte-identical.  The extracted outer archive passed
its manifest and replay verifier; the nested v1.3 archive passed its
own manifest.  The builder used 0.18 seconds wall time and 29,516 KiB
peak resident memory.

## Five-case email premise

`PROVED`: the exact screen verifies Roblot's (A1)--(A3) for all five
rows RQ-000129, RQ-001280, RQ-001569, RQ-001894, and RQ-007519, while
the results theorem proves their Stark packets.  Roblot's uniqueness
therefore implies that each weak/Stark character-coefficient ratio is
in \(\mu_4\).

The exact raw quarter-turn labels are not yet available: exact Artin
transport remains missing.  Any correspondence must state the
gauge-invariant \(\mu_4\) corollary and must not present the withdrawn
oriented replay as independent evidence.

## Publication gate

The proposed files, metadata, and checksums are frozen in
`artifacts/results-paper-v1.4-publication-candidate-v1.json`.
No Zenodo token is present, no v1.4 DOI has been reserved, and no
external mutation or publication action was taken.

The required sequence is:

1. obtain a Zenodo token and explicit authority to create the new
   version;
2. reserve the DOI;
3. insert it into the addendum and metadata;
4. rebuild twice and re-show final hashes;
5. obtain explicit immediate pre-publication approval;
6. upload, verify remote checksums, and publish.

Track A4 remains blocked on this corrected A1 release and on an
available mail channel.
