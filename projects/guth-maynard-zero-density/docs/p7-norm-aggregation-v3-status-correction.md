# P7-1 norm aggregation v3 status correction

`OBSERVED`: the immutable v2 reconciliation document used the noncanonical
tag `PROVED_CONDITIONAL_ON_LENGTH_HEIGHT_RELATION`. Repository policy permits
`PROVED` with the hypothesis stated explicitly, but not that compound tag.
No calculation, source, gate outcome, or scope changes.

The corrected statement is:

- `PROVED`: if (N\leq T^C) for a fixed (C), then the recorded divisor
  normalization is exponent-harmless for the cited single-polynomial
  Guth--Maynard Theorem 1.1; this includes the pinned proof's (N<T) regime;
- `OBSERVED`: no such absorption was established for unrestricted independent
  (N,T), and no Hecke-family density theorem was promoted.

The v2 document and artifact remain unchanged. Paper-stage hostile audit is
still deferred.

Replay:

```sh
python3 proof/p7_norm_aggregation_v3_status_correction.py --check
python3 -m unittest tests.test_p7_norm_aggregation_v3_status_correction -v
```
