# P7 detector local occupancy v2 — regression-test correction

`PROVED`: this is a versioned correction to
`p7-detector-local-occupancy-v1`.  No mathematical claim changes.

The v1 artifact is intact and replays byte-for-byte. Its two regression-test
failures came solely from case-sensitive prose-substring expectations:
the artifact says One common at the start of a sentence and uses the exact
phrase exact finite conductor. Its rendered Markdown also lost several
literal TeX backslashes, including \mathfrak commands and two \beta commands
that became control characters. The v2 tests check the actual strings, and
the corrected companion p7-detector-local-occupancy-v2.md restates the full
result with literal TeX escaping. The v2 builder first verifies the entire
sealed v1 replay.

Unchanged result:

- `PROVED`: individual local zero counts and primitive-family cardinality do
  not remove the cross-character (P) factor in
  (mathcal D_Delta); the (P)-colour block model sharply realizes
  (mathcal D_Delta=mP).
- `PROVED` conditional: a common detector polynomial with uniform threshold
  can yield the exact local occupancy condition needed by the joint Hecke
  large sieve.
- `OBSERVED`: no such P7 detector is currently source-checked, and P7-3
  remains open; the separate averaged-block cubic input remains open too.

No PLAN or RESEARCH_LOG entry is changed by this correction.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/build_p7_detector_local_occupancy_v1.py --check
python3 proof/build_p7_detector_local_occupancy_v2.py --check
python3 -m unittest tests/test_p7_detector_local_occupancy_v2.py -v
```
