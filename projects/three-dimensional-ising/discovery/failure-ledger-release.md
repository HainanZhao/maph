# Lane B release failure ledger

## Missing frozen report input

- False step: release-archive v0 included artifacts, discovery, proof, source,
  tests, and paper trees, but omitted `docs/`.
- Detection: the first extracted Cycle 7 `--check` completed its computation
  and then failed because `docs/cycle7-lane-b-arbitrary-width-closure.md` was
  absent.
- Containment: the unpublished v0 archive was discarded.  The deterministic
  builder now includes `docs/`, and all byte-comparison, manifest, source
  compilation, and extracted-replay gates are rerun from the beginning.
- Affected mathematical claims: none.
