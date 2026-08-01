# Cycle 4 P6 CGL-v2 preregistration hostile audit v1

## Outcome and claim boundary

`OBSERVED`: the sealed 46-row P6 Chen--Gupta--Li v2 reconstruction
preregistration passes this read-only hostile audit. The result is only an
integrity and scope result for the preregistration package. It neither proves
nor repairs a statement in arXiv:2507.08296v2, validates its claimed `7/3`
exponent, selects P7, nor gives a zero-density or short-interval theorem.

The expected P6 outcome remains `OPEN_ANALYTIC_INPUT`. In particular,
`S06_EXTERNAL_INPUTS`, `Z03_TAIL_X_RANGE`,
`Z05_PRIMITIVE_EULER_FACTORS`, `Z06_CONDUCTOR_SUM_Q1`, and
`F08_T_SMOOTH_UNDEFINED` remain expected open analytic obligations, not
defects repaired by this audit.

## Independent checks

The audit pins and checks the authorization snapshot, preregistration
document, sealer, target artifact, target regression test, bounded literature
audit/correction, and CGL-v2 TeX/tar/PDF bytes. It verifies that the named
regular tar member is byte-identical to the canonical TeX; it also checks the
pre-existing rendered-PDF page-anchor text files associated with the pinned
PDF.

It independently verifies every numeric TeX locator is in the 2,468-line
source, then checks source content for the author block, Partial-LVE
hypotheses, both L12 character-subdivision cases, the zero-detector domain,
the `X`/`T`/`T=1` tail issue, primitive-to-all source wording, smoothness
uses/divisor chain, and the `q_1`/`beta` conclusion anchors. `L12` retains
the mandatory `odd_prime` and `two_power` subchecks; `L13` is absent as an
executable row and preserved only as the retired alias.

The crossing check is independent exact rational/radical bookkeeping: it
checks the four frozen coefficient functions, the cleared-denominator C3
quadratic and discriminant at `beta=1`, the four `q_1=q` reductions, and the
strict rational margins `1/12` and `1/39`. This is an audit of displayed
algebra, not a new large-values or zero-density proof.

The replay is checked while reads of the mutable project `PLAN.md` are made
fatal. The audit also checks `-O` and `-OO` rejection, one-shot overwrite
rejection, the resource gate before the exclusive artifact write, live
source-tamper rejection, self-tamper binding, and the target's regression
suite.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/audit_cycle_4_p6_cgl_v2_preregistration_v1_hostile.py \
  --check artifacts/cycle-4-p6-cgl-v2-reconstruction-preregistration-v1-hostile-audit-v1.json
python3 -m unittest \
  tests/test_cycle_4_p6_cgl_v2_reconstruction_preregistration_v1_hostile_audit.py -v
```

The hostile artifact's `OBSERVED` PASS is version-pinned. Its package hashes
and all individual check labels are in
`artifacts/cycle-4-p6-cgl-v2-reconstruction-preregistration-v1-hostile-audit-v1.json`.
