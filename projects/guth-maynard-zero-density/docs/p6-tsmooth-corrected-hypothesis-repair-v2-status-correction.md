# P6 F08 corrected-hypothesis repair v2 status correction

`OBSERVED`: the immutable v1 artifact and document used the noncanonical tag
`PROVED_CONDITIONAL`. Repository policy instead uses `PROVED` with every
hypothesis stated explicitly. No calculation, corrected hypothesis, source
boundary, gate effect, or dependency changes.

The corrected statements are:

- `PROVED`: the divisor-chain and fixed-(v) subdivision deductions follow
  under the amended (T)-smooth hypothesis and the displayed primitive
  large-value subdivision inequality;
- `PROVED`: the smooth (30/13) envelope follows conditional on the primitive
  large-value input, the (qT)-uniform detector and its named external and
  multiplicity inputs, the cited comparison envelopes in their exact ranges,
  and the primitive-to-all transfer;
- `OBSERVED`: CGL-v2 does not define its (T)-smooth term, so source F08 and
  unrelated conductor-sensitive rows remain open.

The v1 files remain unchanged. No density theorem is promoted as an
unconditional result, and paper-stage hostile audit remains deferred.

Replay:

```sh
python3 proof/p6_tsmooth_corrected_hypothesis_repair_v2_status_correction.py --check
python3 -m unittest tests.test_p6_tsmooth_corrected_hypothesis_repair_v2_status_correction -v
```
