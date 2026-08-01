# Cycle 3 G1 exact structural atlas v1

## Outcome and claim boundary

`PROVED` conditional on the frozen published formulas: the artifact evaluates
all 7,744 local rational rows and all 560 preregistered zero-detection transfer
rows with `fractions.Fraction`. It records every signed formula residual and
tie label, retains the exact source-term exponents and `B(s)` residuals for
each transfer row, and verifies both mandatory anchors.

This is not a new large-values, density, short-interval, extremizer, or
saturation theorem. It evaluates zero finite complex Dirichlet polynomials and
zero of the 588 screening rows; those remain for the separately authorized
finite experiment.

## Frozen inputs and conventions

The source of truth is the preregistration artifact
`cycle-3-g1-atlas-preregistration-v1.json`, SHA-256
`227ec1c66b2e109653354b6c3245b4e809fe52692c01514ac10064c23db2b6f8`.
The replay rejects a changed preregistration artifact and compares every
frozen transfer coordinate, not merely its count or its required anchor.

`PROVED`: local residuals are serialized as `left-minus-right`; transfer
residuals are serialized as `B-minus-source-term`; all rational strings are
reduced numerator/denominator pairs. Energy labels occur only on `v=s` rows.
The source's `n0=1/2` rows remain labelled
`ASYMPTOTIC_ENDPOINT_ONLY`, while their exact arithmetic feasibility is kept
distinct from that source-endpoint qualification.

## Replay

Run from the repository root:

```sh
python3 projects/guth-maynard-zero-density/discovery/run_g1_exact_structural_atlas_v1.py --check
python3 -m unittest projects/guth-maynard-zero-density/tests/test_cycle_3_g1_exact_structural_atlas_v1.py -v
```

The first command is timing-independent. Its `--write-performance` mode writes
a separate `OBSERVED` host measurement only after the immutable atlas has
already passed its byte-for-byte check.

## Falsification policy

`PROVED`: the branch halts if a local formula, residual, tie label, mandatory
anchor, frozen transfer row, or diagonal-only energy firewall disagrees with
the exact replay. A nonzero complex-probe count is also a scope violation.
No row is discarded on such a failure.
