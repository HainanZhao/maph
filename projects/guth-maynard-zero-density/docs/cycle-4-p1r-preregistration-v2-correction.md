# Cycle 4 P1R preregistration v2 correction

## Correction boundary

`OBSERVED`: P1R preregistration v1 is preserved byte-for-byte but is not the
continuing replay authority. Its hostile audit records four defects: an invalid
documented replay command, a mutable `PLAN.md` hash input, a wrong source
attribution for the four-term (S_3) scale calculation, and a completed-proof
tag on an unexecuted P1R-FS gate. V2 corrects those records only; it proves no
new large-values, density, short-interval, compatibility, extremizer, or
saturation theorem and authorizes no CRR search.

V2 pins `cycle-4-p1r-authorization-snapshot-v1.json`, which records the
authorization clauses and the historical Plan hash. The current `PLAN.md` is
checked semantically, without being a hash-pinned input. Thus a harmless Plan
prose update does not destroy replay, while deletion of the live P1R branch,
its pre-search CRR prohibition, or its no-P2-selection boundary fails the
current-plan compatibility check.

## Correct replay command

From the project root, the documented and parser command are identical:

```sh
python3 proof/build_cycle_4_p1r_preregistration_v2.py --check
python3 -m unittest tests/test_cycle_4_p1r_preregistration_v2.py -v
```

There is deliberately no positional artifact argument. The v2 builder checks
its fixed versioned output path and refuses `--write` if that artifact exists.

## Source-ledger correction

`PROVED` as source-statement inspection: GM Proposition `prpstnS3` is the
two-term refined (S_3) estimate and assumes (T^\epsilon)-separation.
`PROVED` as source-statement inspection: the four-term expression used by the
critical monomial bookkeeping is the later Proposition `prpstn:S3`, whose
additional hypothesis is (N\ge T^{3/4}). Under the frozen relabelling
(T=H=v^{12}), (N=L=v^{10}=H^{5/6}), that range condition holds exactly.

`OBSERVED`: the source’s critical rational/random discussion remains a
heuristic remark, not a simultaneous construction or a saturation theorem.

## FS status correction

`PROVED`: the pinned fixed-splice identity algebra is already exact:

\[
\frac{30}{13}-\frac3{2-\sigma}
=\frac{30(7/10-\sigma)}{13(2-\sigma)}.
\]

`OBSERVED`: P1R-FS remains `PREREGISTERED_UNEXECUTED`. The required two
independent routes, reconciliation, and hostile audit have not completed, so
v2 does not record a scoped obstruction theorem.

## Status convention

V2 separates the unambiguous fields
`status = SEALED_PREREGISTRATION` and
`discovery_authorization = PROHIBITED_PENDING_CRR_FORMALIZATION`. The latter
is not a double-negative claim that a search is authorized.
